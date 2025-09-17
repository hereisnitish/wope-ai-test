// Comprehensive Footer Controller
class ComprehensiveFooter {
  constructor() {
    this.init();
    this.setupEventListeners();
  }

  init() {
    this.setupNewsletter();
    this.setupScrollToTop();
    this.setupSmoothScrolling();
    this.setupSocialCards();
    this.setupAnimations();
    this.setupStatCounters();
    this.setupParallaxElements();
  }

  setupEventListeners() {
    // Handle window resize for responsive adjustments
    window.addEventListener('resize', this.debounce(this.handleResize.bind(this), 250));
    
    // Handle scroll events
    window.addEventListener('scroll', this.throttle(this.handleScroll.bind(this), 16));
    
    // Handle visibility change
    document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
  }

  setupNewsletter() {
    const form = document.getElementById('newsletterForm');
    const status = document.getElementById('newsletterStatus');
    
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleNewsletterSubmission(form, status);
      });

      // Real-time email validation
      const emailInput = form.querySelector('input[type="email"]');
      if (emailInput) {
        emailInput.addEventListener('input', () => {
          this.validateEmail(emailInput);
        });
      }
    }
  }

  async handleNewsletterSubmission(form, status) {
    const formData = new FormData(form);
    const email = formData.get('email');
    
    if (!this.isValidEmail(email)) {
      this.showFormStatus(status, 'Please enter a valid email address', 'error');
      return;
    }

    // Show loading state
    const button = form.querySelector('button');
    const originalText = button.innerHTML;
    button.innerHTML = '<span>Subscribing...</span>';
    button.disabled = true;

    try {
      // Simulate API call
      await this.simulateNewsletterSubscription(email);
      
      this.showFormStatus(status, 'Successfully subscribed! Welcome to the newsletter.', 'success');
      form.reset();
      
      // Show celebration animation
      this.triggerCelebrationAnimation();
      
    } catch (error) {
      this.showFormStatus(status, 'Subscription failed. Please try again later.', 'error');
    } finally {
      button.innerHTML = originalText;
      button.disabled = false;
    }
  }

  simulateNewsletterSubscription(email) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // 95% success rate simulation
        if (Math.random() > 0.05) {
          console.log(`Newsletter subscription for: ${email}`);
          resolve();
        } else {
          reject(new Error('Network error'));
        }
      }, 2000);
    });
  }

  validateEmail(input) {
    const email = input.value;
    const isValid = this.isValidEmail(email);
    
    if (email && !isValid) {
      input.style.borderColor = 'rgba(255, 107, 107, 0.5)';
    } else {
      input.style.borderColor = 'rgba(255, 255, 255, 0.1)';
    }
  }

  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  showFormStatus(statusElement, message, type) {
    statusElement.textContent = message;
    statusElement.className = `form-status ${type}`;
    
    setTimeout(() => {
      statusElement.classList.remove(type);
      statusElement.style.opacity = '0';
    }, 5000);
  }

  triggerCelebrationAnimation() {
    // Create confetti effect
    for (let i = 0; i < 30; i++) {
      this.createConfetti();
    }
  }

  createConfetti() {
    const confetti = document.createElement('div');
    confetti.style.cssText = `
      position: fixed;
      top: -10px;
      left: ${Math.random() * 100}%;
      width: 8px;
      height: 8px;
      background: linear-gradient(45deg, #667eea, #764ba2);
      border-radius: 50%;
      pointer-events: none;
      z-index: 10000;
      animation: confettiFall ${2 + Math.random() * 3}s linear forwards;
    `;
    
    document.body.appendChild(confetti);
    
    setTimeout(() => {
      confetti.remove();
    }, 5000);
  }

  setupScrollToTop() {
    const scrollButton = document.getElementById('scrollToTop');
    
    if (scrollButton) {
      scrollButton.addEventListener('click', () => {
        this.smoothScrollToTop();
      });
    }
  }

  smoothScrollToTop() {
    const duration = 1000;
    const start = window.pageYOffset;
    const startTime = performance.now();

    const easeOutQuart = (t) => 1 - Math.pow(1 - t, 4);

    const animateScroll = (currentTime) => {
      const timeElapsed = currentTime - startTime;
      const progress = Math.min(timeElapsed / duration, 1);
      const easedProgress = easeOutQuart(progress);
      
      window.scrollTo(0, start * (1 - easedProgress));
      
      if (progress < 1) {
        requestAnimationFrame(animateScroll);
      }
    };

    requestAnimationFrame(animateScroll);
  }

  setupSmoothScrolling() {
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
          console.log(`Navigation to: ${targetId}`);
        }
      });
    });
  }

  setupSocialCards() {
    const socialCards = document.querySelectorAll('.social-card');
    
    socialCards.forEach((card, index) => {
      // Stagger animation delays
      card.style.animationDelay = `${0.5 + index * 0.1}s`;
      
      // Handle clicks for demo social links
      if (card.getAttribute('href') === '#') {
        card.addEventListener('click', (e) => {
          e.preventDefault();
          this.handleSocialCardClick(card);
        });
      }
      
      // Add enhanced hover effects
      card.addEventListener('mouseenter', () => {
        this.animateSocialCard(card, true);
      });
      
      card.addEventListener('mouseleave', () => {
        this.animateSocialCard(card, false);
      });
    });
  }

  handleSocialCardClick(card) {
    const platform = this.getSocialPlatform(card);
    this.showNotification(`Opening ${platform} profile...`, 'info');
    
    // Add click animation
    card.style.transform = 'scale(0.95)';
    setTimeout(() => {
      card.style.transform = '';
    }, 150);
  }

  animateSocialCard(card, isHover) {
    const icon = card.querySelector('.social-icon');
    const info = card.querySelector('.social-info');
    
    if (isHover) {
      icon.style.transform = 'rotateY(180deg) scale(1.1)';
      info.style.transform = 'translateX(10px)';
    } else {
      icon.style.transform = 'rotateY(0deg) scale(1)';
      info.style.transform = 'translateX(0)';
    }
  }

  getSocialPlatform(cardElement) {
    if (cardElement.classList.contains('github')) return 'GitHub';
    if (cardElement.classList.contains('linkedin')) return 'LinkedIn';
    if (cardElement.classList.contains('twitter')) return 'Twitter';
    if (cardElement.classList.contains('instagram')) return 'Instagram';
    return 'Social Media';
  }

  setupAnimations() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -100px 0px'
    };

    const footerObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.triggerSectionAnimations(entry.target);
          footerObserver.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe different sections
    const sections = document.querySelectorAll('.newsletter-section, .footer-main, .footer-social-section');
    sections.forEach(section => {
      footerObserver.observe(section);
    });
  }

  triggerSectionAnimations(section) {
    section.classList.add('animate');
    
    // Special animations for different sections
    if (section.classList.contains('footer-main')) {
      this.animateStatCounters();
    }
    
    if (section.classList.contains('footer-social-section')) {
      this.animateSocialCards();
    }
  }

  setupStatCounters() {
    this.statCounters = document.querySelectorAll('.stat-number');
    this.hasAnimatedStats = false;
  }

  animateStatCounters() {
    if (this.hasAnimatedStats) return;
    
    this.statCounters.forEach((counter, index) => {
      const target = parseInt(counter.textContent.replace('+', ''));
      
      setTimeout(() => {
        this.animateCounter(counter, target, 2000);
      }, index * 200);
    });
    
    this.hasAnimatedStats = true;
  }

  animateCounter(element, target, duration) {
    let start = 0;
    const increment = target / (duration / 16);
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

  animateSocialCards() {
    const cards = document.querySelectorAll('.social-card');
    cards.forEach((card, index) => {
      setTimeout(() => {
        card.style.transform = 'translateY(0)';
        card.style.opacity = '1';
      }, index * 100);
    });
  }

  setupParallaxElements() {
    this.floatingElements = document.querySelectorAll('.floating-element');
  }

  handleScroll() {
    const scrolled = window.pageYOffset;
    
    // Animate floating elements
    this.floatingElements.forEach((element, index) => {
      const speed = 0.5 + index * 0.1;
      const yPos = scrolled * speed;
      element.style.transform = `translateY(${yPos}px)`;
    });
    
    // Show/hide scroll to top button
    const scrollButton = document.getElementById('scrollToTop');
    if (scrollButton) {
      if (scrolled > 300) {
        scrollButton.style.opacity = '1';
        scrollButton.style.visibility = 'visible';
      } else {
        scrollButton.style.opacity = '0';
        scrollButton.style.visibility = 'hidden';
      }
    }
  }

  handleResize() {
    // Recalculate animations and layouts on resize
    this.setupParallaxElements();
  }

  handleVisibilityChange() {
    if (document.visibilityState === 'visible') {
      // Resume animations when page becomes visible
      const floatingElements = document.querySelectorAll('.floating-element');
      floatingElements.forEach(element => {
        element.style.animationPlayState = 'running';
      });
    }
  }

  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `footer-notification-${type}`;
    notification.textContent = message;
    
    Object.assign(notification.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      padding: '15px 25px',
      borderRadius: '12px',
      color: 'white',
      fontWeight: '600',
      fontSize: '0.95rem',
      zIndex: '10000',
      transform: 'translateX(400px)',
      transition: 'all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
      maxWidth: '350px',
      boxShadow: '0 10px 30px rgba(0, 0, 0, 0.3)',
      backdropFilter: 'blur(10px)'
    });
    
    const backgrounds = {
      success: 'linear-gradient(135deg, #2ed573, #19d96e)',
      error: 'linear-gradient(135deg, #ff6b6b, #ee5a24)',
      info: 'linear-gradient(135deg, #667eea, #764ba2)'
    };
    
    notification.style.background = backgrounds[type] || backgrounds.info;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
      notification.style.transform = 'translateX(400px)';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 400);
    }, 4000);
  }

  // Utility functions
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }
}

// Add CSS animations for confetti
if (!document.getElementById('confetti-styles')) {
  const style = document.createElement('style');
  style.id = 'confetti-styles';
  style.textContent = `
    @keyframes confettiFall {
      to {
        transform: translateY(100vh) rotate(360deg);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);
}

// Initialize footer functionality
document.addEventListener('DOMContentLoaded', () => {
  new ComprehensiveFooter();
});

// Global utility functions
window.scrollToFooter = function() {
  const footer = document.getElementById('footer2');
  if (footer) {
    footer.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  }
};

// Handle page load performance
window.addEventListener('load', () => {
  // Optimize animations after page load
  const floatingElements = document.querySelectorAll('.floating-element');
  floatingElements.forEach((element, index) => {
    element.style.animationDelay = `${index * 0.5}s`;
    element.style.animationPlayState = 'running';
  });
});
