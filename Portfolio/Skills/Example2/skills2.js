// Progress bar animation functionality
function animateProgressBars() {
  const progressBars = document.querySelectorAll('.progress-fill');
  
  progressBars.forEach((bar, index) => {
    const targetWidth = bar.getAttribute('data-width');
    
    setTimeout(() => {
      bar.style.width = targetWidth + '%';
      
      // Add glow effect during animation
      bar.style.boxShadow = `0 2px 20px rgba(243, 156, 18, 0.6)`;
      
      setTimeout(() => {
        bar.style.boxShadow = `0 2px 10px rgba(243, 156, 18, 0.3)`;
      }, 2000);
    }, index * 200); // Stagger the animations
  });
}

// Counter animation for percentages
function animatePercentages() {
  const percentageElements = document.querySelectorAll('.skill-percentage');
  
  percentageElements.forEach((element, index) => {
    const targetValue = parseInt(element.textContent);
    let currentValue = 0;
    const increment = targetValue / 60; // Animation duration ~1 second at 60fps
    
    setTimeout(() => {
      const counter = setInterval(() => {
        currentValue += increment;
        if (currentValue >= targetValue) {
          element.textContent = targetValue + '%';
          clearInterval(counter);
        } else {
          element.textContent = Math.floor(currentValue) + '%';
        }
      }, 16); // ~60fps
    }, index * 200 + 500); // Start after progress bar animation begins
  });
}

// Intersection Observer for scroll animations
const skillsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
      
      // Start progress bar animations
      setTimeout(() => {
        animateProgressBars();
        animatePercentages();
      }, 300);
      
      // Trigger summary card animations
      const summaryCards = entry.target.querySelectorAll('.summary-card');
      summaryCards.forEach((card, index) => {
        setTimeout(() => {
          card.style.opacity = '0';
          card.style.transform = 'translateX(30px)';
          card.style.transition = 'all 0.6s ease';
          
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateX(0)';
          }, 100);
        }, index * 200 + 800);
      });
      
      skillsObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.2,
  rootMargin: '0px 0px -100px 0px'
});

// Skill bar hover effects
document.addEventListener('DOMContentLoaded', () => {
  const skillBars = document.querySelectorAll('.skill-bar');
  
  skillBars.forEach(bar => {
    bar.addEventListener('mouseenter', () => {
      const progressFill = bar.querySelector('.progress-fill');
      const percentage = bar.querySelector('.skill-percentage');
      
      // Enhanced glow on hover
      progressFill.style.boxShadow = '0 2px 20px rgba(243, 156, 18, 0.8)';
      percentage.style.color = '#fff';
      percentage.style.textShadow = '0 0 10px rgba(243, 156, 18, 0.8)';
    });
    
    bar.addEventListener('mouseleave', () => {
      const progressFill = bar.querySelector('.progress-fill');
      const percentage = bar.querySelector('.skill-percentage');
      
      // Return to normal glow
      progressFill.style.boxShadow = '0 2px 10px rgba(243, 156, 18, 0.3)';
      percentage.style.color = '#f39c12';
      percentage.style.textShadow = 'none';
    });
  });
});

// Summary card interactive effects
document.addEventListener('DOMContentLoaded', () => {
  const summaryCards = document.querySelectorAll('.summary-card');
  
  summaryCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateX(15px) scale(1.02)';
      card.style.background = 'rgba(255, 255, 255, 0.2)';
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateX(0) scale(1)';
      card.style.background = 'rgba(255, 255, 255, 0.1)';
    });
  });
});

// Initialize observer
document.addEventListener('DOMContentLoaded', () => {
  const skillsSection = document.querySelector('#skills2');
  if (skillsSection) {
    skillsObserver.observe(skillsSection);
  }
});

// Reset animations function (useful for testing)
function resetSkillsAnimation() {
  const progressBars = document.querySelectorAll('.progress-fill');
  const percentages = document.querySelectorAll('.skill-percentage');
  const summaryCards = document.querySelectorAll('.summary-card');
  
  progressBars.forEach(bar => {
    bar.style.width = '0%';
  });
  
  percentages.forEach((element, index) => {
    const targetValue = parseInt(element.getAttribute('data-original') || element.textContent);
    element.textContent = '0%';
    element.setAttribute('data-original', targetValue);
  });
  
  summaryCards.forEach(card => {
    card.style.opacity = '1';
    card.style.transform = 'translateX(0)';
  });
  
  document.querySelector('#skills2').classList.remove('animate');
}

// Keyboard accessibility
document.addEventListener('DOMContentLoaded', () => {
  const skillBars = document.querySelectorAll('.skill-bar');
  
  skillBars.forEach(bar => {
    bar.setAttribute('tabindex', '0');
    bar.setAttribute('role', 'progressbar');
    
    const skillLevel = bar.getAttribute('data-skill');
    bar.setAttribute('aria-valuenow', skillLevel);
    bar.setAttribute('aria-valuemin', '0');
    bar.setAttribute('aria-valuemax', '100');
    
    const skillName = bar.querySelector('.skill-name').textContent.trim();
    bar.setAttribute('aria-label', `${skillName}: ${skillLevel}% proficiency`);
  });
});

// Performance optimization: Use requestAnimationFrame for smoother animations
function smoothProgressAnimation(element, targetWidth, duration = 2000) {
  const startTime = performance.now();
  const startWidth = 0;
  
  function animate(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Easing function for smoother animation
    const easeProgress = 1 - Math.pow(1 - progress, 3);
    const currentWidth = startWidth + (targetWidth - startWidth) * easeProgress;
    
    element.style.width = currentWidth + '%';
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }
  
  requestAnimationFrame(animate);
}

// Export functions for external use (if needed)
window.skillsAnimations = {
  reset: resetSkillsAnimation,
  animate: animateProgressBars,
  smoothAnimate: smoothProgressAnimation
};
