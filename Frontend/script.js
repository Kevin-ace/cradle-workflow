// Configuration
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000'  // Explicit localhost IP
    : 'http://localhost:5000';  // Fallback localhost URL

document.addEventListener('DOMContentLoaded', () => {
    // Get all required DOM elements
    const inputText = document.getElementById('inputText');
    const processBtn = document.getElementById('processBtn');
    const keywordsDiv = document.getElementById('keywords');
    const summaryDiv = document.getElementById('summary');
    const translationDiv = document.getElementById('translation');
    const languageSelect = document.getElementById('languageSelect');
    const errorDiv = document.getElementById('error') || createErrorDiv();
    const languageInfoDiv = document.getElementById('languageInfo') || createLanguageInfoDiv();

    // Create error div if it doesn't exist
    function createErrorDiv() {
        const div = document.createElement('div');
        div.id = 'error';
        div.style.color = 'red';
        div.style.marginTop = '10px';
        document.querySelector('.container').appendChild(div);
        return div;
    }

    // Create language info div if it doesn't exist
    function createLanguageInfoDiv() {
        const div = document.createElement('div');
        div.id = 'languageInfo';
        document.querySelector('.container').appendChild(div);
        return div;
    }

    // Detailed error display function
    function displayError(message) {
        console.error('Processing Error:', message);
        errorDiv.textContent = `Error: ${message}`;
        errorDiv.style.display = 'block';
        
        // Clear previous results
        keywordsDiv.innerHTML = '';
        summaryDiv.textContent = '';
        translationDiv.textContent = '';
        languageInfoDiv.textContent = '';
    }

    // Clear error and reset result divs
    function clearError() {
        errorDiv.textContent = '';
        errorDiv.style.display = 'none';
    }

    // Process text when button is clicked
    processBtn.addEventListener('click', async () => {
        // Reset previous state
        clearError();

        // Get input text and validate
        const text = inputText.value.trim();
        if (!text) {
            displayError('Please enter some text to process.');
            return;
        }

        try {
            // Detailed logging of request
            console.log('Sending request to:', `${API_BASE_URL}/process`);
            console.log('Request payload:', { 
                text: text,
                language: languageSelect.value 
            });

            // Send request to backend
            const response = await fetch(`${API_BASE_URL}/process`, {
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    text: text,
                    language: languageSelect.value 
                })
            });

            // Log response details
            console.log('Response status:', response.status);

            // Parse response
            const data = await response.json();
            console.log('Response data:', data);

            // Handle potential error in response
            if (!response.ok) {
                throw new Error(data.error || 'Processing failed');
            }

            // Update UI with results
            keywordsDiv.innerHTML = data.keywords && data.keywords.length > 0 
                ? data.keywords.map(k => `<span class="keyword">${k}</span>`).join(', ')
                : 'No keywords extracted';
            
            summaryDiv.textContent = data.summary || 'No summary generated';
            
            translationDiv.textContent = data.translation || 'No translation available';

            // Optional: Show source and target language information
            languageInfoDiv.textContent = `Source: ${data.source_language}, Target: ${data.target_language}`;
        } catch (error) {
            // Comprehensive error handling
            console.error('Full error:', error);
            displayError(error.message || 'Failed to process text');
        }
    });
});