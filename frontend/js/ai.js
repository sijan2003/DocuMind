// AI Tools Event Listeners
let currentAiResult = null;
let currentAiAction = null;

document.querySelectorAll('.ai-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const action = btn.dataset.action;
        const resultDiv = document.getElementById('aiResult');
        const saveBtn = document.getElementById('saveAiResult');

        resultDiv.classList.remove('hidden');
        resultDiv.textContent = 'Processing...';
        resultDiv.style.color = '#f1f5f9';
        saveBtn.classList.add('hidden');

        try {
            let result;

            switch (action) {
                case 'summarize':
                    result = await api.summarize(currentDocId);
                    resultDiv.textContent = result.summary;
                    currentAiResult = result.summary;
                    currentAiAction = 'Summary';
                    saveBtn.classList.remove('hidden');
                    break;

                case 'keypoints':
                    result = await api.getKeyPoints(currentDocId);
                    resultDiv.textContent = result.key_points;
                    currentAiResult = result.key_points;
                    currentAiAction = 'Key Points';
                    saveBtn.classList.remove('hidden');
                    break;

                case 'paraphrase':
                    result = await api.paraphrase(currentDocId);
                    resultDiv.textContent = result.paraphrased;
                    currentAiResult = result.paraphrased;
                    currentAiAction = 'Paraphrased';
                    saveBtn.classList.remove('hidden');
                    break;

                case 'ask':
                    const question = prompt('What would you like to know about this document?');
                    if (!question) {
                        resultDiv.classList.add('hidden');
                        return;
                    }
                    result = await api.askQuestion(currentDocId, question);
                    resultDiv.textContent = `Q: ${question}\n\nA: ${result.answer}`;
                    currentAiResult = `Q: ${question}\n\nA: ${result.answer}`;
                    currentAiAction = 'Q&A';
                    saveBtn.classList.remove('hidden');
                    break;
            }
        } catch (error) {
            resultDiv.textContent = 'Error: ' + error.message;
            resultDiv.style.color = '#ef4444';
            saveBtn.classList.add('hidden');
        }
    });
});

// Save AI Result as New Document
document.getElementById('saveAiBtn').addEventListener('click', async () => {
    if (!currentAiResult) return;

    const originalDoc = documents.find(d => d.id === currentDocId);
    const newTitle = `${originalDoc.title} - ${currentAiAction}`;

    try {
        await api.createDocument({
            title: newTitle,
            content: currentAiResult,
            category: originalDoc.category,
            is_public: false
        });

        alert('AI result saved as new document!');
        document.getElementById('viewModal').classList.add('hidden');
        loadDocuments();
    } catch (error) {
        alert('Error saving document: ' + error.message);
    }
});
