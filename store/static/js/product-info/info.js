
document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            
            stars.forEach(s => s.classList.remove('active'));
            
            stars.forEach(s => {
                if (s.dataset.rating <= rating) {
                    s.classList.add('active');
                    s.textContent = '★';
                } else {
                    s.textContent = '☆';
                }
            });
        });
    });
});