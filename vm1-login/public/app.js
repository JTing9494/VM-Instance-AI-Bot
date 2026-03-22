document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    const dashboard = document.getElementById('dashboard');
    const usernameDisplay = document.getElementById('username');
    const companyNameDisplay = document.getElementById('companyName');
    const logoutBtn = document.getElementById('logoutBtn');
    const companyDataDiv = document.getElementById('companyData');
    const chatMessagesDiv = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    
    let token = null;
    
    // Handle login form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const userId = document.getElementById('userId').value.trim();
        const companyId = document.getElementById('companyId').value.trim();
        
        if (!userId || !companyId) {
            showLoginError('Please enter both User ID and Company ID');
            return;
        }
        
        try {
            loginError.style.display = 'none';
            
            // Call login API
            const response = await fetch('http://localhost:8000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: userId,
                    password: companyId
                })
            });
            
            if (!response.ok) {
                throw new Error('Login failed');
            }
            
            const data = await response.json();
            token = data.access_token;
            
            // Fetch user and company details from API
            await loadUserDetails();
            
            // Show dashboard
            dashboard.style.display = 'block';
            loginForm.reset();
            
            // Load company data
            await loadCompanyData();
            
        } catch (error) {
            console.error('Login error:', error);
            showLoginError('Invalid credentials. Please try again.');
        }
    });
    
    // Handle logout
    logoutBtn.addEventListener('click', function() {
        token = null;
        dashboard.style.display = 'none';
        loginForm.reset();
        companyDataDiv.innerHTML = '';
        chatMessagesDiv.innerHTML = '';
        usernameDisplay.textContent = '';
        companyNameDisplay.textContent = '';
    });
    
    // Handle send chat message
    sendBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });
    
    function showLoginError(message) {
        loginError.textContent = message;
        loginError.style.display = 'block';
    }
    
    async function loadUserDetails() {
        if (!token) return;
        
        try {
            const response = await fetch('http://localhost:8000/api/data/user', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to load user details');
            }
            
            const data = await response.json();
            usernameDisplay.textContent = data.username;
            companyNameDisplay.textContent = data.company_name;
        } catch (error) {
            console.error('Error loading user details:', error);
            usernameDisplay.textContent = 'User';
            companyNameDisplay.textContent = 'Company';
        }
    }
    
    async function loadCompanyData() {
        if (!token) return;
        
        try {
            const response = await fetch('http://localhost:8000/api/data', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to load company data');
            }
            
            const data = await response.json();
            displayCompanyData(data);
        } catch (error) {
            console.error('Error loading company data:', error);
            companyDataDiv.innerHTML = '<p class="loading">Error loading company data</p>';
        }
    }
    
    function displayCompanyData(data) {
        if (!data || data.length === 0) {
            companyDataDiv.innerHTML = '<p class="loading">No data available</p>';
            return;
        }
        
        companyDataDiv.innerHTML = data.map(item => `
            <div class="data-item">
                <span class="data-label">${item.data_key}</span>
                <span class="data-value">${item.data_value || 'N/A'}</span>
            </div>
        `).join('');
    }
    
    async function sendChatMessage() {
        const message = chatInput.value.trim();
        if (!message || !token) return;
        
        // Add user message to chat
        addChatMessage(message, 'user');
        chatInput.value = '';
        
        try {
            // Call chat API
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) {
                throw new Error('Failed to get response from AI');
            }
            
            const data = await response.json();
            addChatMessage(data.response, 'bot');
        } catch (error) {
            console.error('Chat error:', error);
            addChatMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    }
    
    function addChatMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = message;
        
        messageDiv.appendChild(contentDiv);
        chatMessagesDiv.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;
    }
});
