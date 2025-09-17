// Footer functionality and interactions
class FooterController {
  constructor() {
    this.init();
  }

  init() {
    this.setupBackToTop();
    this.setupSmoothScrolling();
    this.setupSocialLinks();
    this.setupAnimations();
    this.setupLinkValidation();
  }

  setupBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    
    if (backToTopBtn) {
      // Show/hide back to top button based on scroll position
      window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
          backToTopBtn.style.opacity = '0.8';
          backToTopBtn.style.visibility = 'visible';
        } else {
          backToTopBtn.style.opacity = '0';
          backToTopBtn.style.visibility = 'hidden';
        }
      });

      // Smooth scroll to top
      backToTopBtn.addEventListener('click', () => {
        this.scrollToTop();
      });
    }
  }

  scrollToTop() {
    const duration = 800;
    const start = window.pageYOffset;
    const startTime = performance.now();

    const animateScroll = (currentTime) => {
      const timeElapsed = currentTime - startTime;
      const progress = Math.min(timeElapsed / duration, 1);
      
      // Easing function for smooth animation
      const easeOutCubic = 1 - Math.pow(1 - progress, 3);
      
      window.scrollTo(0, start * (1 - easeOutCubic));
      
      if (progress < 1) {
        requestAnimationFrame(animateScroll);
      }
    };

    requestAnimationFrame(animateScroll);
  }

  setupSmoothScrolling() {
    // Handle internal navigation links
    const footerLinks = document.querySelectorAll('.footer a[href^="#"]');
    
    footerLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        } else {
          // If target doesn't exist, simulate navigation
          console.log(`Navigating to section: ${targetId}`);
        }
      });
    });
  }

  setupSocialLinks() {
    const socialLinks = document.querySelectorAll('.social-link');
    
    socialLinks.forEach((link, index) => {
      // Add staggered animation delay
      link.style.animationDelay = `${0.6 + index * 0.1}s`;
      
      // Handle click events for demo social links
      link.addEventListener('click', (e) => {
        if (link.getAttribute('href') === '#') {
          e.preventDefault();
          this.handleSocialClick(link);
        }
      });

      // Add hover sound effect (optional)
      link.addEventListener('mouseenter', () => {
        this.playHoverSound();
      });
    });
  }

  handleSocialClick(socialLink) {
    const platform = this.getSocialPlatform(socialLink);
    
    // Show notification
    this.showNotification(`Opening ${platform} in new tab...`, 'info');
    
    // In a real application, these would open actual social media profiles
    setTimeout(() => {
      console.log(`Would open ${platform} profile`);
    }, 500);
  }

  getSocialPlatform(linkElement) {
    if (linkElement.classList.contains('github')) return 'GitHub';
    if (linkElement.classList.contains('linkedin')) return 'LinkedIn';
    if (linkElement.classList.contains('twitter')) return 'Twitter';
    if (linkElement.classList.contains('instagram')) return 'Instagram';
    if (linkElement.classList.contains('discord')) return 'Discord';
    return 'Social Media';
  }

  playHoverSound() {
    // Create a subtle hover sound effect using Web Audio API
    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
      gainNode.gain.setValueAtTime(0.05, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);
      
      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.1);
    } catch (error) {
      // Audio context not supported or blocked
      console.log('Audio hover effect not available');
    }
  }

  setupAnimations() {
    // Intersection Observer for footer animations
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const footerObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.triggerFooterAnimations(entry.target);
          footerObserver.unobserve(entry.target);
        }
      });
    }, observerOptions);

    const footer = document.querySelector('#footer1');
    if (footer) {
      footerObserver.observe(footer);
    }
  }

  triggerFooterAnimations(footer) {
    footer.classList.add('animate');
    
    // Animate social links with stagger
    const socialLinks = footer.querySelectorAll('.social-link');
    socialLinks.forEach((link, index) => {
      setTimeout(() => {
        link.style.animationPlayState = 'running';
      }, index * 100);
    });

    // Animate the logo dot
    const logoDot = footer.querySelector('.logo-dot');
    if (logoDot) {
      logoDot.style.animationPlayState = 'running';
    }
  }

  setupLinkValidation() {
    // Handle footer links that might not have destinations
    const policyLinks = document.querySelectorAll('.footer-links-bottom a');
    
    policyLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        
        if (href === '#privacy' || href === '#terms' || href === '#sitemap') {
          e.preventDefault();
          
          const linkType = href.substring(1);
          this.showNotification(`${this.capitalize(linkType)} page would open here`, 'info');
          
          // In a real application, you would navigate to actual pages
          console.log(`Would navigate to ${linkType} page`);
        }
      });
    });
  }

  capitalize(str) {
    if (str === 'sitemap') return 'Sitemap';
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `footer-notification footer-notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    Object.assign(notification.style, {
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      padding: '12px 20px',
      borderRadius: '8px',
      color: 'white',
      fontWeight: '500',
      fontSize: '0.9rem',
      zIndex: '10000',
      transform: 'translateY(100px)',
      transition: 'all 0.3s ease',
      maxWidth: '300px',
      boxShadow: '0 5px 15px rgba(0, 0, 0, 0.2)'
    });
    
    // Set background based on type
    const backgrounds = {
      success: 'linear-gradient(135deg, #27ae60, #2ecc71)',
      error: 'linear-gradient(135deg, #e74c3c, #c0392b)',
      info: 'linear-gradient(135deg, #3498db, #2980b9)'
    };
    
    notification.style.background = backgrounds[type] || backgrounds.info;
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
      notification.style.transform = 'translateY(0)';
    }, 100);
    
    // Auto remove
    setTimeout(() => {
      notification.style.transform = 'translateY(100px)';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }, 3000);
  }
}

// Parallax effect for footer background
function handleFooterParallax() {
  const footer = document.querySelector('#footer1');
  if (footer) {
    const scrolled = window.pageYOffset;
    const footerTop = footer.offsetTop;
    const windowHeight = window.innerHeight;
    
    if (scrolled + windowHeight > footerTop) {
      const rate = (scrolled + windowHeight - footerTop) * 0.3;
      footer.style.transform = `translateY(${rate}px)`;
    }
  }
}

// Initialize footer functionality
document.addEventListener('DOMContentLoaded', () => {
  // Initialize footer controller
  new FooterController();
  
  // Add parallax scrolling to footer
  let ticking = false;
  
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        handleFooterParallax();
        ticking = false;
      });
      ticking = true;
    }
  });
});

// Utility functions for external use
window.scrollToFooter = function() {
  const footer = document.getElementById('footer1');
  if (footer) {
    footer.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  }
};

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    // Re-initialize any time-sensitive features when page becomes visible
    const footer = document.querySelector('#footer1');
    if (footer) {
      const logoDot = footer.querySelector('.logo-dot');
      if (logoDot) {
        logoDot.style.animationPlayState = 'running';
      }
    }
  }
});
