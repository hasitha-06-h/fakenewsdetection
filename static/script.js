document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const newsInput = document.getElementById('news-input');
    const predictBtn = document.getElementById('predict-btn');
    const clearBtn = document.getElementById('clear-btn');
    
    // UI Elements
    const spinner = document.querySelector('.spinner');
    const iconRight = document.querySelector('.icon-right');
    const btnText = document.querySelector('.btn-text');
    
    // Result Elements
    const emptyState = document.getElementById('empty-state');
    const resultContainer = document.getElementById('result-container');
    const resultBadge = document.getElementById('result-badge');
    const resultIcon = document.getElementById('result-icon');
    const predictionResult = document.getElementById('prediction-result');
    const confidenceValue = document.getElementById('confidence-value');
    const progressFill = document.getElementById('progress-fill');
    
    const errorMessage = document.getElementById('error-message');
    const historyList = document.getElementById('history-list');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const text = newsInput.value.trim();
        
        if (!text) {
            showError("Please enter some text to analyze.");
            return;
        }

        hideError();
        setLoadingState(true);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Analysis failed. Please try again.');
            }

            // Simulate slight delay for "Processing" feel (Optional, makes it feel more complex)
            setTimeout(() => {
                displayResult(data.result, data.confidence);
                updateHistory(data.history);
                setLoadingState(false);
            }, 600);

        } catch (error) {
            showError(error.message);
            setLoadingState(false);
        }
    });

    clearBtn.addEventListener('click', () => {
        newsInput.value = '';
        resultContainer.classList.add('hidden');
        emptyState.classList.remove('hidden');
        hideError();
        
        // Reset progress bar
        progressFill.style.width = '0%';
        newsInput.focus();
    });

    function setLoadingState(isLoading) {
        if (isLoading) {
            btnText.textContent = 'Analyzing...';
            spinner.classList.remove('hidden');
            iconRight.classList.add('hidden');
            predictBtn.disabled = true;
            predictBtn.style.opacity = '0.7';
            predictBtn.style.cursor = 'not-allowed';
            
            // Hide previous results while loading
            resultContainer.classList.add('hidden');
            emptyState.classList.remove('hidden');
        } else {
            btnText.textContent = 'Run Analysis';
            spinner.classList.add('hidden');
            iconRight.classList.remove('hidden');
            predictBtn.disabled = false;
            predictBtn.style.opacity = '1';
            predictBtn.style.cursor = 'pointer';
        }
    }

    function displayResult(result, confidenceStr) {
        // Switch views
        emptyState.classList.add('hidden');
        resultContainer.classList.remove('hidden');
        
        // Reset Classes
        resultBadge.className = 'result-badge';
        resultIcon.className = 'fa-solid';
        progressFill.className = 'progress-fill';
        
        // Extract numeric value from "XX.XX%"
        const confNum = parseFloat(confidenceStr);
        
        // Ensure dynamic rendering based on result
        if (result === 'Real News') {
            resultBadge.classList.add('is-real');
            resultIcon.classList.add('fa-check-circle');
            progressFill.classList.add('fill-real');
            confidenceValue.style.color = 'var(--success)';
        } else {
            resultBadge.classList.add('is-fake');
            resultIcon.classList.add('fa-triangle-exclamation');
            progressFill.classList.add('fill-fake');
            confidenceValue.style.color = 'var(--danger)';
        }

        predictionResult.textContent = result;
        
        // Animate the confidence counter and progress bar
        animateValue(confidenceValue, 0, confNum, 1000, "%");
        
        // Small delay before filling progress bar for cool effect
        setTimeout(() => {
            progressFill.style.width = confNum + '%';
        }, 100);
    }

    function updateHistory(historyItems) {
        if (!historyItems || historyItems.length === 0) return;

        historyList.innerHTML = '';

        historyItems.forEach(item => {
            const isReal = item.result === 'Real News';
            const tr = document.createElement('tr');
            
            tr.innerHTML = `
                <td class="excerpt-cell" title="${item.text}">${item.text}</td>
                <td>
                    <span class="tag ${isReal ? 'tag-real' : 'tag-fake'}">
                        ${isReal ? '<i class="fa-solid fa-check"></i>' : '<i class="fa-solid fa-xmark"></i>'} 
                        ${item.result}
                    </span>
                </td>
                <td class="conf-cell" style="color: ${isReal ? 'var(--success)' : 'var(--danger)'}">
                    ${item.confidence}
                </td>
            `;
            
            historyList.appendChild(tr);
        });
    }

    function showError(message) {
        errorMessage.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> ${message}`;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.classList.add('hidden');
        errorMessage.textContent = '';
    }

    // Utility for animating numbers
    function animateValue(obj, start, end, duration, suffix = "") {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            // Ease out quad
            const easeProgress = progress * (2 - progress);
            const currentVal = (easeProgress * (end - start) + start).toFixed(2);
            obj.innerHTML = currentVal + suffix;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});
