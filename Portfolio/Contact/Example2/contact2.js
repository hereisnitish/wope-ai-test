// Contact Card Interactions
class ContactCards {
  constructor() {
    this.init();
  }

  init() {
    this.setupCardAnimations();
    this.setupSocialLinks();
    this.setupLocationButton();
    this.setupCalendarButton();
    this.setupModal();
    this.setupQuickForm();
  }

  setupCardAnimations() {
    const cards = document.querySelectorAll('.contact-card');
    
    cards.forEach(card => {
      card.addEventListener('mouseenter', () => {
        this.animateCard(card, true);
      });
      
      card.addEventListener('mouseleave', () => {
        this.animateCard(card, false);
      });
    });
  }

  animateCard(card, isHover) {
    const icon = card.querySelector('.card-icon');
    const btn = card.querySelector('.contact-btn');
    
    if (isHover) {
      icon.style.transform = 'rotateY(360deg) scale(1.1)';
      btn.style.transform = 'scale(1.05)';
    } else {
      icon.style.transform = 'rotateY(0deg) scale(1)';
      btn.style.transform = 'scale(1)';
    }
  }

  setupSocialLinks() {
    const socialLinks = document.querySelectorAll('.social-link');
    
    socialLinks.forEach((link, index) => {
      link.style.animationDelay = `${0.6 + index * 0.1}s`;
      
      link.addEventListener('click', (e) => {
        if (link.getAttribute('href') === '#') {
          e.preventDefault();
          this.showNotification('Social link would open in new tab', 'info');
        }
      });
    });
  }

  setupLocationButton() {
    const locationBtn = document.querySelector('.location-btn');
    if (locationBtn) {
      locationBtn.addEventListener('click', () => {
        // Simulate opening map
        this.showNotification('Opening location in maps...', 'success');
        setTimeout(() => {
          // In real app, this would open Google Maps
          console.log('Opening Google Maps with coordinates for Mumbai, India');
        }, 1000);
      });
    }
  }

  setupCalendarButton() {
    const calendarBtn = document.querySelector('.calendar-btn');
    if (calendarBtn) {
      calendarBtn.addEventListener('click', () => {
        // Simulate booking system
        this.showNotification('Redirecting to booking system...', 'success');
        setTimeout(() => {
          // In real app, this would open Calendly or similar
          console.log('Opening calendar booking system');
        }, 1000);
      });
    }
  }

  setupModal() {
    const modal = document.getElementById('quickFormModal');
    const openBtn = document.getElementById('openQuickForm');
    const closeBtn = document.getElementById('closeModal');

    if (openBtn) {
      openBtn.addEventListener('click', () => {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        this.closeModal();
      });
    }

    // Close modal on overlay click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        this.closeModal();
      }
    });

    // Close modal on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        this.closeModal();
      }
    });
  }

  closeModal() {
    const modal = document.getElementById('quickFormModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  setupQuickForm() {
    const form = document.getElementById('quickContactForm');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleQuickFormSubmit(form);
      });
    }
  }

  async handleQuickFormSubmit(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    // Validate form
    if (!this.validateQuickForm(data)) {
      return;
    }

    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;

    try {
      // Simulate form submission
      await this.simulateQuickSubmission(data);
      
      this.showNotification('Message sent successfully!', 'success');
      form.reset();
      this.closeModal();
      
    } catch (error) {
      this.showNotification('Failed to send message. Please try again.', 'error');
    } finally {
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  }

  validateQuickForm(data) {
    const { name, email, message } = data;
    
    if (name.trim().length < 2) {
      this.showNotification('Name must be at least 2 characters', 'error');
      return false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      this.showNotification('Please enter a valid email address', 'error');
      return false;
    }
    
    if (message.trim().length < 5) {
      this.showNotification('Message must be at least 5 characters', 'error');
      return false;
    }
    
    return true;
  }

  simulateQuickSubmission(data) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // Simulate 95% success rate
        if (Math.random() > 0.05) {
          console.log('Quick form submitted:', data);
          resolve();
        } else {
          reject(new Error('Network error'));
        }
      }, 1500);
    });
  }

  showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    Object.assign(notification.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      padding: '15px 20px',
      borderRadius: '10px',
      color: 'white',
      fontWeight: '500',
      zIndex: '10000',
      transform: 'translateX(400px)',
      transition: 'all 0.3s ease',
      maxWidth: '300px'
    });
    
    // Set background based on type
    const backgrounds = {
      success: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
      error: 'linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)',
      info: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    };
    
    notification.style.background = backgrounds[type] || backgrounds.info;
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
      notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove
    setTimeout(() => {
      notification.style.transform = 'translateX(400px)';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }, 3000);
  }
}

// Intersection Observer for scroll animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const contactObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
      
      // Trigger staggered animations for cards
      const cards = entry.target.querySelectorAll('.contact-card');
      cards.forEach((card, index) => {
        setTimeout(() => {
          card.style.animationPlayState = 'running';
        }, index * 100);
      });
      
      contactObserver.unobserve(entry.target);
    }
  });
}, observerOptions);

// Parallax effect for background
function handleParallax() {
  const scrolled = window.pageYOffset;
  const contactSection = document.querySelector('#contact2');
  
  if (contactSection) {
    const rate = scrolled * -0.5;
    contactSection.style.backgroundPosition = `center ${rate}px`;
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize contact cards functionality
  new ContactCards();
  
  // Initialize scroll animations
  const contactSection = document.querySelector('#contact2');
  if (contactSection) {
    contactObserver.observe(contactSection);
  }
  
  // Add parallax scrolling
  window.addEventListener('scroll', handleParallax);
});

// Utility function for smooth scrolling to contact
function scrollToContact() {
  const contactElement = document.getElementById('contact2');
  if (contactElement) {
    contactElement.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  }
}
