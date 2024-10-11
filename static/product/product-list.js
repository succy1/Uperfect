document.querySelectorAll('.view-details').forEach(button => {
    button.addEventListener('click', function() {
        const detailsDiv = this.closest('.card').querySelector('.product-details');
        detailsDiv.style.display = detailsDiv.style.display === 'none' ? 'block' : 'none';
        this.textContent = detailsDiv.style.display === 'none' ? 'View Details' : 'Hide Details';
    });
});