// Check authentication
if (!checkAuth()) {
    throw new Error('Not authenticated');
}

// Display user email
document.getElementById('userEmail').textContent = localStorage.getItem('userEmail');

// Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    window.location.href = 'index.html';
});

// Load documents
let documents = [];
let currentDocId = null;

async function loadDocuments() {
    try {
        documents = await api.getDocuments();
        renderDocuments();
    } catch (error) {
        console.error('Error loading documents:', error);
        document.getElementById('documentsGrid').innerHTML =
            '<p style="color: #ef4444;">Failed to load documents</p>';
    }
}

function renderDocuments() {
    const grid = document.getElementById('documentsGrid');

    if (documents.length === 0) {
        grid.innerHTML = '<p style="color: #94a3b8;">No documents yet. Create your first one!</p>';
        return;
    }

    grid.innerHTML = documents.map(doc => `
        <div class="document-card" data-id="${doc.id}">
            <h3>${doc.title}</h3>
            <p>${doc.content.substring(0, 150)}${doc.content.length > 150 ? '...' : ''}</p>
            ${doc.category ? `<span class="category">${doc.category}</span>` : ''}
        </div>
    `).join('');

    // Add click listeners
    document.querySelectorAll('.document-card').forEach(card => {
        card.addEventListener('click', () => {
            const id = parseInt(card.dataset.id);
            viewDocument(id);
        });
    });
}

// New Document Modal
document.getElementById('newDocBtn').addEventListener('click', () => {
    currentDocId = null;
    document.getElementById('modalTitle').textContent = 'New Document';
    document.getElementById('documentForm').reset();
    document.getElementById('documentModal').classList.remove('hidden');
});

document.getElementById('closeModal').addEventListener('click', () => {
    document.getElementById('documentModal').classList.add('hidden');
});

// Save Document
document.getElementById('documentForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        title: document.getElementById('docTitle').value,
        content: document.getElementById('docContent').value,
        category: document.getElementById('docCategory').value || null,
        is_public: false
    };

    try {
        if (currentDocId) {
            await api.updateDocument(currentDocId, data);
        } else {
            await api.createDocument(data);
        }

        document.getElementById('documentModal').classList.add('hidden');
        loadDocuments();
    } catch (error) {
        alert('Error saving document: ' + error.message);
    }
});

// View Document
function viewDocument(id) {
    const doc = documents.find(d => d.id === id);
    if (!doc) return;

    currentDocId = id;
    document.getElementById('viewTitle').textContent = doc.title;
    document.getElementById('viewContent').textContent = doc.content;
    document.getElementById('aiResult').classList.add('hidden');
    document.getElementById('viewModal').classList.remove('hidden');
}

document.getElementById('closeViewModal').addEventListener('click', () => {
    document.getElementById('viewModal').classList.add('hidden');
});

// Edit Document
document.getElementById('editDocBtn').addEventListener('click', () => {
    const doc = documents.find(d => d.id === currentDocId);
    if (!doc) return;

    document.getElementById('modalTitle').textContent = 'Edit Document';
    document.getElementById('docTitle').value = doc.title;
    document.getElementById('docContent').value = doc.content;
    document.getElementById('docCategory').value = doc.category || '';

    document.getElementById('viewModal').classList.add('hidden');
    document.getElementById('documentModal').classList.remove('hidden');
});

// Delete Document
document.getElementById('deleteDocBtn').addEventListener('click', async () => {
    if (!confirm('Are you sure you want to delete this document?')) return;

    try {
        await api.deleteDocument(currentDocId);
        document.getElementById('viewModal').classList.add('hidden');
        loadDocuments();
    } catch (error) {
        alert('Error deleting document: ' + error.message);
    }
});

// Upload File Modal
document.getElementById('uploadFileBtn').addEventListener('click', () => {
    document.getElementById('uploadForm').reset();
    document.getElementById('uploadProgress').classList.add('hidden');
    document.getElementById('uploadModal').classList.remove('hidden');
});

document.getElementById('closeUploadModal').addEventListener('click', () => {
    document.getElementById('uploadModal').classList.add('hidden');
});

// Handle File Upload
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('uploadFile');
    const file = fileInput.files[0];
    const title = document.getElementById('uploadTitle').value;
    const category = document.getElementById('uploadCategory').value;

    if (!file) {
        alert('Please select a file');
        return;
    }

    // Show progress
    document.getElementById('uploadProgress').classList.remove('hidden');

    try {
        await api.uploadFile(file, title, category);
        document.getElementById('uploadModal').classList.add('hidden');
        loadDocuments();
    } catch (error) {
        alert('Error uploading file: ' + error.message);
    } finally {
        document.getElementById('uploadProgress').classList.add('hidden');
    }
});

// Initial load
loadDocuments();
