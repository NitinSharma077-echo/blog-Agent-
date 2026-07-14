document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'https://blog-agent-pw8u.onrender.com';
    const form = document.getElementById('generator-form');
    const topicInput = document.getElementById('topic-input');
    const generateBtn = document.getElementById('generate-btn');
    const btnText = document.querySelector('.btn-text');
    const btnSpinner = document.getElementById('btn-spinner');
    
    const resultsContainer = document.getElementById('results-container');
    const blogCard = document.getElementById('blog-card');
    const critiqueCard = document.getElementById('critique-card');
    
    const blogContent = document.getElementById('blog-content');
    const critiqueContent = document.getElementById('critique-content');
    
    const statusItems = [
        document.getElementById('status-search'),
        document.getElementById('status-scrape'),
        document.getElementById('status-write'),
        document.getElementById('status-critic')
    ];

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const topic = topicInput.value.trim();
        if (!topic) return;

        // Reset UI
        resultsContainer.style.display = 'block';
        blogCard.style.display = 'none';
        critiqueCard.style.display = 'none';
        blogContent.innerHTML = '';
        critiqueContent.innerHTML = '';
        
        statusItems.forEach(item => {
            item.classList.remove('active', 'completed');
        });
        statusItems[0].classList.add('active'); // Start search
        
        // Button state
        generateBtn.disabled = true;
        btnText.style.display = 'none';
        btnSpinner.style.display = 'block';

        // Fake status progression for UX (since the backend is one big call right now)
        // In a real app, we'd use Server-Sent Events (SSE) or WebSockets
        let currentStatus = 0;
        const fakeProgress = setInterval(() => {
            if (currentStatus < 3) {
                statusItems[currentStatus].classList.remove('active');
                statusItems[currentStatus].classList.add('completed');
                currentStatus++;
                statusItems[currentStatus].classList.add('active');
            }
        }, 5000); // Progress every 5 seconds artificially

        try {
            const response = await fetch(`${API_BASE_URL}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic })
            });

            const data = await response.json();
            
            clearInterval(fakeProgress);
            
            // Mark all complete
            statusItems.forEach(item => {
                item.classList.remove('active');
                item.classList.add('completed');
            });

            if (data.status === 'success') {
                blogCard.style.display = 'block';
                critiqueCard.style.display = 'block';
                
                // Parse markdown to HTML
                blogContent.innerHTML = marked.parse(data.blog_post);
                critiqueContent.innerHTML = marked.parse(data.critique);
                
                // Scroll to results
                blogCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                alert('Generation failed. Check console.');
                console.error(data);
            }
            
        } catch (error) {
            clearInterval(fakeProgress);
            console.error('Error generating content:', error);
            alert('An error occurred during generation.');
            statusItems.forEach(item => {
                item.classList.remove('active', 'completed');
            });
        } finally {
            // Restore button
            generateBtn.disabled = false;
            btnText.style.display = 'block';
            btnSpinner.style.display = 'none';
        }
    });
});
