import httpx
import json
import asyncio
import subprocess
import os
from typing import List, Dict, Any, Optional
from app.config import settings

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        # Using gemini-3-flash-preview as requested
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
        self.vm3_host = "vm3-storage"  # Docker service name
        self.rsync_user = "app_user"
        self.rsync_password = os.getenv("RSYNC_PASSWORD", "rsyncpassword123")
    
    async def generate_content(self, prompt: str, context_data: Optional[List[Dict]] = None) -> str:
        """
        Generate content using Gemini 3 Flash Preview with optional context
        Includes retry logic for rate limiting (429 errors)
        """
        if not self.api_key:
            return "Gemini API key not configured"
            
        # Prepare the prompt with context if provided
        full_prompt = prompt
        if context_data:
            context_str = "\n".join([f"{item.get('key', '')}: {item.get('value', '')}" for item in context_data])
            full_prompt = f"Context:\n{context_str}\n\nQuestion: {prompt}"
        
        # Prepare request payload
        payload = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
            }
        }
        
        # Make request to Gemini API with retry logic
        max_retries = 3
        base_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}?key={self.api_key}",
                        json=payload,
                        timeout=30.0
                    )
                    
                    # Handle rate limiting
                    if response.status_code == 429:
                        if attempt < max_retries - 1:  # Not the last attempt
                            # Extract retry delay from headers if available, otherwise use exponential backoff
                            retry_after = response.headers.get("retry-after")
                            if retry_after:
                                try:
                                    delay = int(retry_after)
                                except ValueError:
                                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                            else:
                                delay = base_delay * (2 ** attempt)  # Exponential backoff
                            
                            # Wait before retrying
                            await asyncio.sleep(delay)
                            continue
                        else:
                            # Max retries exceeded
                            return "I'm experiencing high demand right now. Please try again in a few moments."
                    
                    # Handle other HTTP errors
                    response.raise_for_status()
                    
                    result = response.json()
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            return candidate["content"]["parts"][0]["text"]
                    return "No response generated"
                    
            except httpx.TimeoutException:
                if attempt < max_retries - 1:
                    await asyncio.sleep(base_delay * (2 ** attempt))
                    continue
                return "Request timed out. Please try again."
            except httpx.RequestError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(base_delay * (2 ** attempt))
                    continue
                return f"Network error: {str(e)}"
            except Exception as e:
                # For any other exception, don't retry
                return f"Error calling Gemini API: {str(e)}"
        
        # If we exhausted all retries
        return "Service temporarily unavailable due to high demand. Please try again later."
    
    def _run_rsync_command(self, source: str, dest: str) -> bool:
        """
        Run rsync command to fetch files from VM-3
        """
        try:
            # Set up RSYNC_PASSWORD environment variable for authentication
            env = os.environ.copy()
            env["RSYNC_PASSWORD"] = self.rsync_password
            
            # Run rsync command
            result = subprocess.run([
                "rsync", "-avz", 
                f"{self.rsync_user}@{self.vm3_host}::{source}/",
                dest
            ], env=env, capture_output=True, text=True, timeout=30)
            
            return result.returncode == 0
        except Exception as e:
            print(f"RSYNC error: {e}")
            return False
    
    async def search_files(self, query: str, company_id: int) -> List[Dict[str, Any]]:
        """
        Search for files using rsync to access the AI Books collection on VM-3
        Company-based file access control:
        - Company 1: AI Engineering, Applied-Machine-Learning, Artificial Intelligence
        - Company 2: Deep Learning, Gans-in-action, Generative-Deep-Learning
        - Company 3: Generative-Deep-Learning, Hands-On Generative AI, Hands-On_LLM
        - Company 4: Hands-On_LLM, LLM Engineers Handbook, ML Math
        - Company 5: ML Math, NLP with Transformer
        """
        company_file_mapping = {
            1: ["AI Engineering.pdf", "Applied-Machine-Learning-and-AI-for-Engineers.pdf", "Artificial Intelligence. A modern approach (Stuart Russell  Peter Norvig) (Z-Library).pdf"],
            2: ["Deep Learning by Ian Goodfellow, Yoshua Bengio, Aaron Courville.pdf", "Gans-in-action-deep-learning-with-generative-adversarial-networks.pdf", "Generative-Deep-Learning.pdf"],
            3: ["Generative-Deep-Learning.pdf", "Hands-On Generative AI with Transformers and Diffusion.pdf", "Hands-On_Large_Language_Models.pdf"],
            4: ["Hands-On_Large_Language_Models.pdf", "LLM Engineers Handbook.pdf", "ML Math.pdf"],
            5: ["ML Math.pdf", "NLP with Transformer models.pdf"]
        }
        
        allowed_files = company_file_mapping.get(company_id, [])
        
        # Create a temporary directory for downloaded files
        temp_dir = "/tmp/ai_books_search"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Sync the ai_books module from VM-3
        success = self._run_rsync_command("ai_books", temp_dir)
        
        if not success:
            # Fallback to mock data if rsync fails
            return [
                {
                    "filename": f,
                    "snippet": f"Document available for company {company_id}",
                    "relevance_score": 1.0
                }
                for f in allowed_files
            ]
        
        # Search through the downloaded files
        results = []
        query_lower = query.lower()
        
        try:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith('.pdf') and file in allowed_files:
                        filename_lower = file.lower()
                        score = 0.5
                        
                        if query_lower in filename_lower:
                            score += 0.4
                        
                        query_words = query_lower.split()
                        for word in query_words:
                            if word in filename_lower:
                                score += 0.2
                        
                        score = min(score, 1.0)
                        
                        results.append({
                            "filename": file,
                            "snippet": f"Content from {file} relevant to '{query}'",
                            "relevance_score": score
                        })
            
            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            return results
            
        except Exception as e:
            print(f"Error processing files: {e}")
            return []
