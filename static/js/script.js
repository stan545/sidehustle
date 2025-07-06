document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const processBtn = document.getElementById('process-btn');
    const clearBtn = document.getElementById('clear-btn');
    const copyBtn = document.getElementById('copy-btn');
    const outputSection = document.querySelector('.output-section');
    const errorMessage = document.getElementById('error-message');
    const inputCharCount = document.getElementById('input-char-count');
    const outputCharCount = document.getElementById('output-char-count');
    const processingInfo = document.getElementById('processing-info');
    const btnText = document.querySelector('.btn-text');
    const loadingSpinner = document.querySelector('.loading-spinner');

    // Option checkboxes
    const paraphraseOption = document.getElementById('paraphrase');
    const removeAiPhrasesOption = document.getElementById('remove_ai_phrases');
    const humanizeOption = document.getElementById('humanize');

    // Update character count
    function updateCharCount() {
        const count = inputText.value.length;
        inputCharCount.textContent = `${count} characters`;
        
        // Enable/disable process button based on input
        processBtn.disabled = count === 0;
    }

    // Show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }

    // Show loading state
    function setLoading(isLoading) {
        processBtn.disabled = isLoading;
        if (isLoading) {
            btnText.style.display = 'none';
            loadingSpinner.style.display = 'inline-block';
        } else {
            btnText.style.display = 'inline-block';
            loadingSpinner.style.display = 'none';
        }
    }

    // Process text
    async function processText() {
        const text = inputText.value.trim();
        
        if (!text) {
            showError('Please enter some text to process.');
            return;
        }

        // Get selected options
        const options = {
            paraphrase: paraphraseOption.checked,
            remove_ai_phrases: removeAiPhrasesOption.checked,
            humanize: humanizeOption.checked
        };

        // Check if at least one option is selected
        if (!Object.values(options).some(option => option)) {
            showError('Please select at least one processing option.');
            return;
        }

        setLoading(true);
        
        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    options: options
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to process text');
            }

            // Display results
            outputText.textContent = data.processed_text;
            outputCharCount.textContent = `${data.processed_text.length} characters`;
            
            // Show applied options
            const appliedOptions = Object.entries(data.options_applied)
                .filter(([key, value]) => value)
                .map(([key, value]) => {
                    switch(key) {
                        case 'paraphrase': return 'Paraphrased';
                        case 'remove_ai_phrases': return 'AI phrases removed';
                        case 'humanize': return 'Humanized';
                        default: return key;
                    }
                });
            
            processingInfo.textContent = `Applied: ${appliedOptions.join(', ')}`;
            
            // Show output section and copy button
            outputSection.style.display = 'block';
            copyBtn.style.display = 'inline-flex';
            
            // Scroll to output
            outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (error) {
            console.error('Error processing text:', error);
            showError('Error processing text: ' + error.message);
        } finally {
            setLoading(false);
        }
    }

    // Clear all text
    function clearAll() {
        inputText.value = '';
        outputText.textContent = '';
        outputSection.style.display = 'none';
        copyBtn.style.display = 'none';
        updateCharCount();
        inputText.focus();
    }

    // Copy result to clipboard
    async function copyResult() {
        const text = outputText.textContent;
        
        try {
            await navigator.clipboard.writeText(text);
            
            // Show feedback
            const originalText = copyBtn.textContent;
            copyBtn.textContent = 'Copied!';
            copyBtn.style.background = '#48bb78';
            
            setTimeout(() => {
                copyBtn.textContent = originalText;
                copyBtn.style.background = '';
            }, 2000);
            
        } catch (error) {
            console.error('Failed to copy text:', error);
            showError('Failed to copy text to clipboard');
        }
    }

    // Event listeners
    inputText.addEventListener('input', updateCharCount);
    processBtn.addEventListener('click', processText);
    clearBtn.addEventListener('click', clearAll);
    copyBtn.addEventListener('click', copyResult);

    // Allow Enter + Ctrl/Cmd to process text
    inputText.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            processText();
        }
    });

    // Initialize
    updateCharCount();
    inputText.focus();

    // Add sample text for demonstration
    const sampleText = `However, as an AI language model, I must note that it's important to understand that artificial intelligence has significantly transformed the way we process information. Furthermore, it should be noted that these technologies facilitate enhanced communication and demonstrate remarkable capabilities. Additionally, I hope this information is helpful for your understanding of the subject matter.`;
    
    // Add a subtle hint about sample text
    const placeholder = inputText.getAttribute('placeholder');
    inputText.setAttribute('placeholder', placeholder + '\n\nTip: Try pasting some AI-generated text to see the transformation!');
    
    // Optional: Add sample text button for demo purposes
    const sampleBtn = document.createElement('button');
    sampleBtn.textContent = 'Try Sample Text';
    sampleBtn.className = 'btn btn-secondary';
    sampleBtn.style.fontSize = '14px';
    sampleBtn.style.padding = '8px 16px';
    sampleBtn.style.minWidth = 'auto';
    
    sampleBtn.addEventListener('click', function() {
        inputText.value = sampleText;
        updateCharCount();
    });
    
    // Add sample button to controls
    const controls = document.querySelector('.controls');
    controls.appendChild(sampleBtn);
});