document.addEventListener('DOMContentLoaded', function() {
  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.nav-dot');
  const prevButton = document.querySelector('.arrow-left');
  const nextButton = document.querySelector('.arrow-right');
  let currentSlide = 0;
  let isAnimating = false;
  let autoplayInterval;

  function goToSlide(index) {
    if (isAnimating) return;
    isAnimating = true;

    slides[currentSlide].classList.remove('active');
    dots[currentSlide].classList.remove('active');

    currentSlide = index;
    if (currentSlide >= slides.length) currentSlide = 0;
    if (currentSlide < 0) currentSlide = slides.length - 1;

    slides[currentSlide].classList.add('active');
    dots[currentSlide].classList.add('active');

    setTimeout(() => {
      isAnimating = false;
    }, 800);
  }

  function nextSlide() {
    goToSlide(currentSlide + 1);
  }

  function prevSlide() {
    goToSlide(currentSlide - 1);
  }

  prevButton.addEventListener('click', () => {
    prevSlide();
    resetAutoplay();
  });

  nextButton.addEventListener('click', () => {
    nextSlide();
    resetAutoplay();
  });

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      if (currentSlide !== index) {
        goToSlide(index);
        resetAutoplay();
      }
    });
  });

  function startAutoplay() {
    autoplayInterval = setInterval(nextSlide, 2000);
  }

  function resetAutoplay() {
    clearInterval(autoplayInterval);
    startAutoplay();
  }

  let touchStartX = 0;
  let touchEndX = 0;

  document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
  });

  document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  });

  function handleSwipe() {
    const swipeThreshold = 50;
    const difference = touchStartX - touchEndX;

    if (Math.abs(difference) > swipeThreshold) {
      if (difference > 0) {
        nextSlide();
      } else {
        prevSlide();
      }
      resetAutoplay();
    }
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') {
      prevSlide();
      resetAutoplay();
    } else if (e.key === 'ArrowRight') {
      nextSlide();
      resetAutoplay();
    }
  });

  startAutoplay();
});
  