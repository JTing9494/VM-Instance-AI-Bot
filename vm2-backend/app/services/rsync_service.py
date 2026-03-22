import subprocess
import logging
from typing import List, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class RsyncService:
    def __init__(self):
        self.rsync_host = settings.RSYNC_HOST
        self.rsync_port = settings.RSYNC_PORT
        self.rsync_user = settings.RSYNC_USER
        self.rsync_password = settings.RSYNC_PASSWORD
        self.rsync_module = settings.RSYNC_MODULE
        self.local_cache_dir = "./rsync_cache"
        
        # Ensure cache directory exists
        import os
        os.makedirs(self.local_cache_dir, exist_ok=True)
    
    def _build_rsync_command(self, source: str, destination: str, 
                           delete: bool = False, archive: bool = True) -> List[str]:
        """Build rsync command with authentication"""
        cmd = ["rsync"]
        
        if archive:
            cmd.append("-a")  # archive mode
        if delete:
            cmd.append("--delete")  # delete extraneous files
        
        # Add verbose and progress for logging
        cmd.extend(["-v", "--progress"])
        
        # Build the source/destination with SSH or direct rsync daemon
        if self.rsync_password:
            # Using password file for authentication
            import tempfile
            import os
            
            # Create temporary password file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(self.rsync_password)
                password_file = f.name
            
            try:
                cmd.extend([
                    "--password-file", password_file,
                    f"{self.rsync_user}@{self.rsync_host}::{self.rsync_module}/{source}",
                    destination
                ])
            finally:
                # Clean up password file
                os.unlink(password_file)
        else:
            # No password - direct rsync daemon access
            cmd.extend([
                f"{self.rsync_user}@{self.rsync_host}::{self.rsync_module}/{source}",
                destination
            ])
        
        return cmd
    
    def sync_from_storage(self) -> bool:
        """Sync company data from VM-3 storage to local cache"""
        try:
            logger.info("Starting rsync sync from storage...")
            
            # Sync from VM-3 rsync daemon to local cache
            source = ""  # Root of the module
            destination = self.local_cache_dir
            
            cmd = self._build_rsync_command(source, destination)
            logger.debug(f"Running rsync command: {' '.join(cmd)}")
            
            # Execute rsync
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                logger.info("Rsync sync completed successfully")
                logger.debug(f"Rsync output: {result.stdout}")
                return True
            else:
                logger.error(f"Rsync failed with return code {result.returncode}")
                logger.error(f"Rsync stderr: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Rsync operation timed out")
            return False
        except Exception as e:
            logger.error(f"Error during rsync sync: {str(e)}")
            return False
    
    def sync_to_storage(self, local_path: str) -> bool:
        """Sync local changes to VM-3 storage (read-only in our case)"""
        # In our architecture, VM-3 storage is read-only, so this would typically not be used
        # But implementing for completeness
        try:
            logger.info("Starting rsync sync to storage...")
            
            destination = ""  # Root of the module
            cmd = self._build_rsync_command(local_path, destination, archive=True)
            logger.debug(f"Running rsync command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info("Rsync sync to storage completed successfully")
                return True
            else:
                logger.error(f"Rsync to storage failed with return code {result.returncode}")
                logger.error(f"Rsync stderr: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error during rsync sync to storage: {str(e)}")
            return False
    
    def list_available_files(self) -> List[str]:
        """List files available in the rsync module"""
        try:
            logger.info("Listing available files in rsync module...")
            
            # Using rsync to list files
            cmd = ["rsync"]
            
            if self.rsync_password:
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                    f.write(self.rsync_password)
                    password_file = f.name
                
                try:
                    cmd.extend(["--password-file", password_file])
                    cmd.append(f"{self.rsync_user}@{self.rsync_host}::{self.rsync_module}/")
                finally:
                    os.unlink(password_file)
            else:
                cmd.append(f"{self.rsync_user}@{self.rsync_host}::{self.rsync_module}/")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Parse the output to get file list
                files = []
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('@') and not line.endswith('/'):
                        files.append(line)
                logger.debug(f"Found {len(files)} files in rsync module")
                return files
            else:
                logger.error(f"Failed to list files: {result.stderr}")
                return []
                
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return []