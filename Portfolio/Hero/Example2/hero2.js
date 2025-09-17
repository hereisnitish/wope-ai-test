// Smooth scroll functionality for CTA button
document.addEventListener('DOMContentLoaded', function() {
  const ctaButton = document.querySelector('.cta-button');
  
  if (ctaButton) {
    ctaButton.addEventListener('click', function(e) {
      e.preventDefault();
      const target = this.getAttribute('href');
      const targetElement = document.querySelector(target);
      
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  }
});

// Parallax effect for hero background
window.addEventListener('scroll', function() {
  const hero = document.querySelector('.hero-image');
  const scrolled = window.pageYOffset;
  const parallaxSpeed = 0.5;
  
  if (hero) {
    hero.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
  }
});

// Dynamic background images (optional)
const backgroundImages = [
  'https://via.placeholder.com/1200x600/2c3e50/ffffff?text=Background+1',
  'https://via.placeholder.com/1200x600/34495e/ffffff?text=Background+2',
  'https://via.placeholder.com/1200x600/2980b9/ffffff?text=Background+3'
];

let currentBgIndex = 0;

function changeBackground() {
  const hero = document.querySelector('.hero-image');
  if (hero) {
    currentBgIndex = (currentBgIndex + 1) % backgroundImages.length;
    hero.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                                 url('${backgroundImages[currentBgIndex]}')`;
  }
}

// Change background every 10 seconds
setInterval(changeBackground, 10000);
