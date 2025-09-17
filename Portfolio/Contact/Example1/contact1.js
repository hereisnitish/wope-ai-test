// Form validation and submission
class ContactForm {
  constructor(formId) {
    this.form = document.getElementById(formId);
    this.submitBtn = this.form.querySelector('.submit-btn');
    this.formStatus = document.getElementById('formStatus');
    this.init();
  }

  init() {
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    
    // Real-time validation
    const inputs = this.form.querySelectorAll('input, textarea');
    inputs.forEach(input => {
      input.addEventListener('blur', () => this.validateField(input));
      input.addEventListener('input', () => this.clearError(input));
    });
  }

  validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';

    // Clear previous errors
    this.clearError(field);

    switch (fieldName) {
      case 'name':
        if (value.length < 2) {
          errorMessage = 'Name must be at least 2 characters long';
          isValid = false;
        }
        break;
      
      case 'email':
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
          errorMessage = 'Please enter a valid email address';
          isValid = false;
        }
        break;
      
      case 'subject':
        if (value.length < 3) {
          errorMessage = 'Subject must be at least 3 characters long';
          isValid = false;
        }
        break;
      
      case 'message':
        if (value.length < 10) {
          errorMessage = 'Message must be at least 10 characters long';
          isValid = false;
        }
        break;
    }

    if (!isValid) {
      this.showError(field, errorMessage);
    }

    return isValid;
  }

  showError(field, message) {
    const errorElement = document.getElementById(field.name + 'Error');
    if (errorElement) {
      errorElement.textContent = message;
      errorElement.classList.add('show');
    }
    field.style.borderColor = '#ff6b6b';
  }

  clearError(field) {
    const errorElement = document.getElementById(field.name + 'Error');
    if (errorElement) {
      errorElement.classList.remove('show');
      setTimeout(() => {
        errorElement.textContent = '';
      }, 300);
    }
    field.style.borderColor = 'rgba(255, 255, 255, 0.3)';
  }

  validateAllFields() {
    const inputs = this.form.querySelectorAll('input, textarea');
    let allValid = true;

    inputs.forEach(input => {
      if (!this.validateField(input)) {
        allValid = false;
      }
    });

    return allValid;
  }

  async handleSubmit(e) {
    e.preventDefault();

    if (!this.validateAllFields()) {
      this.showStatus('Please fix the errors above', 'error');
      return;
    }

    // Show loading state
    this.submitBtn.classList.add('loading');
    this.submitBtn.disabled = true;

    try {
      // Simulate form submission (replace with actual API call)
      await this.simulateFormSubmission();
      
      this.showStatus('Message sent successfully! I\'ll get back to you soon.', 'success');
      this.form.reset();
      
    } catch (error) {
      this.showStatus('Failed to send message. Please try again.', 'error');
    } finally {
      // Remove loading state
      this.submitBtn.classList.remove('loading');
      this.submitBtn.disabled = false;
    }
  }

  simulateFormSubmission() {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // Simulate 90% success rate
        if (Math.random() > 0.1) {
          resolve();
        } else {
          reject(new Error('Network error'));
        }
      }, 2000);
    });
  }

  showStatus(message, type) {
    this.formStatus.textContent = message;
    this.formStatus.className = `form-status ${type}`;
    
    if (type === 'success') {
      setTimeout(() => {
        this.formStatus.classList.remove('success');
        this.formStatus.style.opacity = '0';
      }, 5000);
    }
  }
}

// Intersection Observer for scroll animations
const observerOptions = {
  threshold: 0.2,
  rootMargin: '0px 0px -50px 0px'
};

const contactObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
      contactObserver.unobserve(entry.target);
    }
  });
}, observerOptions);

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize contact form
  if (document.getElementById('contactForm')) {
    new ContactForm('contactForm');
  }
  
  // Initialize scroll animations
  const contactSection = document.querySelector('#contact1');
  if (contactSection) {
    contactObserver.observe(contactSection);
  }
  
  // Add staggered animation to info items
  const infoItems = document.querySelectorAll('.info-item');
  infoItems.forEach((item, index) => {
    item.style.animationDelay = `${index * 0.2}s`;
  });
});

// Smooth scroll function for navigation
function scrollToContact() {
  const contactElement = document.getElementById('contact1');
  if (contactElement) {
    contactElement.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  }
}
