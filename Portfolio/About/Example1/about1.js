// Counter animation for statistics
function animateCounter(element, target, duration = 2000) {
  let start = 0;
  const increment = target / (duration / 16); // 60 FPS
  
  const timer = setInterval(() => {
    start += increment;
    if (start >= target) {
      element.textContent = target + '+';
      clearInterval(timer);
    } else {
      element.textContent = Math.floor(start) + '+';
    }
  }, 16);
}

// Intersection Observer for scroll animations
const observerOptions = {
  threshold: 0.3,
  rootMargin: '0px 0px -50px 0px'
};

const aboutObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
      
      // Start counter animations
      const stats = entry.target.querySelectorAll('.stat h3');
      const targets = [50, 5, 20]; // Values corresponding to projects, years, clients
      
      stats.forEach((stat, index) => {
        setTimeout(() => {
          animateCounter(stat, targets[index]);
        }, index * 200); // Stagger the animations
      });
      
      // Stop observing once animated
      aboutObserver.unobserve(entry.target);
    }
  });
}, observerOptions);

// Initialize observer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const aboutSection = document.querySelector('#about1');
  if (aboutSection) {
    aboutObserver.observe(aboutSection);
  }
});

// Add hover effects for stats
document.addEventListener('DOMContentLoaded', () => {
  const statElements = document.querySelectorAll('.stat');
  
  statElements.forEach(stat => {
    stat.addEventListener('mouseenter', () => {
      stat.style.transform = 'translateY(-15px) scale(1.05)';
    });
    
    stat.addEventListener('mouseleave', () => {
      stat.style.transform = 'translateY(0) scale(1)';
    });
  });
});
