const API_BASE = 'http://localhost:8000';

// Toggle between login and register forms
document.getElementById('showRegister').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
    document.getElementById('errorMessage').classList.add('hidden');
});

document.getElementById('showLogin').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('errorMessage').classList.add('hidden');
});

// Handle Login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Invalid credentials');
        }
        
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('userEmail', email);
        window.location.href = 'dashboard.html';
    } catch (error) {
        showError('Login failed. Please check your credentials.');
    }
});

// Handle Register
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Registration failed');
        }
        
        // Auto-login after registration
        document.getElementById('loginEmail').value = email;
        document.getElementById('loginPassword').value = password;
        document.getElementById('registerForm').classList.add('hidden');
        document.getElementById('loginForm').classList.remove('hidden');
        showError('Registration successful! Please login.', 'success');
    } catch (error) {
        showError(error.message);
    }
});

function showError(message, type = 'error') {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    if (type === 'success') {
        errorDiv.style.background = 'rgba(16, 185, 129, 0.1)';
        errorDiv.style.borderColor = '#10b981';
        errorDiv.style.color = '#10b981';
    } else {
        errorDiv.style.background = 'rgba(239, 68, 68, 0.1)';
        errorDiv.style.borderColor = '#ef4444';
        errorDiv.style.color = '#ef4444';
    }
}
