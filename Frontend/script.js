document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const processBtn = document.getElementById('processBtn');
    const translateBtn = document.getElementById('translateBtn');
    const keywordsDiv = document.getElementById('keywords');
    const summaryDiv = document.getElementById('summary');
    const translationDiv = document.getElementById('translation');
    const languageSelect = document.getElementById('languageSelect');

    processBtn.addEventListener('click', async () => {
        const text = inputText.value;
        try {
            const response = await fetch('http://localhost:8000/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    text: text,
                    language: languageSelect.value 
                })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            
            // Update keywords
            keywordsDiv.innerHTML = data.keywords.map(keyword => 
                typeof keyword === 'string' ? keyword : keyword[0]
            ).join(', ');
            
            // Update summary
            summaryDiv.textContent = data.summary;
            
            // Update translation
            translationDiv.textContent = data.translation;
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to process text. Please try again.');
        }
    });
});