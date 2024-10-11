// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Change navbar background on scroll
window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
        document.querySelector('.navbar').style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
    } else {
        document.querySelector('.navbar').style.backgroundColor = 'white';
    }
});

// Login/Signup button click event
document.getElementById('loginBtn').addEventListener('click', function(e) {
    e.preventDefault();
    alert('Login/Signup functionality will be implemented here.');
});

// Add hover effect to feature cards
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseover', function() {
        this.style.backgroundColor = '#f8f9fa';
    });
    card.addEventListener('mouseout', function() {
        this.style.backgroundColor = 'white';
    });
});