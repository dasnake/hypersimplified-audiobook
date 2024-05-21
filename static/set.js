document.getElementById('seekForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const percentage = parseFloat(document.getElementById('percentage').value);
    if (isNaN(percentage) || percentage < 0 || percentage > 100) {
        document.getElementById('status').textContent = 'Please enter a valid percentage between 0 and 100.';
        return;
    }

    fetchFileSize().then(totalBytes => {
        const newPosition = Math.round((percentage / 100) * totalBytes);
        updateCookie('last_position', newPosition);
        document.getElementById('status').textContent = `Cookie updated to position: ${newPosition} bytes.`;
    }).catch(error => {
        console.error('Error fetching file size:', error);
        document.getElementById('status').textContent = 'Failed to fetch file size.';
    });
});

