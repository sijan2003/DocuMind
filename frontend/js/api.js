const API_BASE = 'http://localhost:8000';

function getToken() {
    return localStorage.getItem('token');
}

function getHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
    };
}

// Check authentication
function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// API Calls
const api = {
    // Documents
    async getDocuments() {
        const response = await fetch(`${API_BASE}/documents/`, {
            headers: getHeaders()
        });
        if (!response.ok) throw new Error('Failed to fetch documents');
        return response.json();
    },

    async createDocument(data) {
        const response = await fetch(`${API_BASE}/documents/`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to create document');
        return response.json();
    },

    async updateDocument(id, data) {
        const response = await fetch(`${API_BASE}/documents/${id}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to update document');
        return response.json();
    },

    async deleteDocument(id) {
        const response = await fetch(`${API_BASE}/documents/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        if (!response.ok) throw new Error('Failed to delete document');
    },

    async uploadFile(file, title, category) {
        const formData = new FormData();
        formData.append('file', file);
        if (title) formData.append('title', title);
        if (category) formData.append('category', category);

        const response = await fetch(`${API_BASE}/documents/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            },
            body: formData
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to upload file');
        }
        return response.json();
    },

    // AI Features
    async summarize(id) {
        const response = await fetch(`${API_BASE}/ai/summarize/${id}`, {
            method: 'POST',
            headers: getHeaders()
        });
        if (!response.ok) throw new Error('Failed to generate summary');
        return response.json();
    },

    async getKeyPoints(id) {
        const response = await fetch(`${API_BASE}/ai/keypoints/${id}`, {
            method: 'POST',
            headers: getHeaders()
        });
        if (!response.ok) throw new Error('Failed to extract key points');
        return response.json();
    },

    async paraphrase(id) {
        const response = await fetch(`${API_BASE}/ai/paraphrase/${id}`, {
            method: 'POST',
            headers: getHeaders()
        });
        if (!response.ok) throw new Error('Failed to paraphrase');
        return response.json();
    },

    async askQuestion(id, question) {
        const response = await fetch(`${API_BASE}/ai/ask/${id}?question=${encodeURIComponent(question)}`, {
            method: 'POST',
            headers: getHeaders()
        });
        if (!response.ok) throw new Error('Failed to answer question');
        return response.json();
    }
};
