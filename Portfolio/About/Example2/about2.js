// CV Download functionality
function downloadCV() {
  // Create a temporary link element
  const link = document.createElement('a');
  
  // You can replace this with actual CV file path
  const cvUrl = 'assets/cv/Alex_Johnson_CV.pdf'; // Update with actual path
  
  link.href = cvUrl;
  link.download = 'Alex_Johnson_CV.pdf';
  
  // Temporarily add to DOM, trigger click, then remove
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  // Show user feedback
  showDownloadFeedback();
}

// Show download feedback
function showDownloadFeedback() {
  const button = document.querySelector('.download-cv');
  const originalText = button.innerHTML;
  
  button.innerHTML = '<i class="fas fa-check"></i> Downloaded!';
  button.style.background = 'linear-gradient(45deg, #27ae60, #2ecc71)';
  
  setTimeout(() => {
    button.innerHTML = originalText;
    button.style.background = 'linear-gradient(45deg, #3498db, #2980b9)';
  }, 2000);
}

// Parallax effect for profile image
document.addEventListener('scroll', () => {
  const aboutSection = document.querySelector('#about2');
  const profileImage = document.querySelector('.about-image img');
  
  if (aboutSection && profileImage) {
    const rect = aboutSection.getBoundingClientRect();
    const scrollPercent = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
    
    if (scrollPercent >= 0 && scrollPercent <= 1) {
      const rotation = scrollPercent * 5; // Subtle rotation
      profileImage.style.transform = `rotate(${rotation}deg)`;
    }
  }
});

// Intersection Observer for animations
const aboutObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // Animate skill items
      const skillItems = entry.target.querySelectorAll('.skill-item');
      skillItems.forEach((item, index) => {
        setTimeout(() => {
          item.style.animation = 'slideInRight 0.6s ease-out forwards';
          item.style.opacity = '0';
          item.style.transform = 'translateX(-30px)';
          setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
          }, 50);
        }, index * 150);
      });
      
      // Animate profile image
      const profileImage = entry.target.querySelector('.about-image img');
      if (profileImage) {
        profileImage.style.animation = 'zoomIn 1s ease-out';
      }
      
      aboutObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.2,
  rootMargin: '0px 0px -100px 0px'
});

// Initialize observers
document.addEventListener('DOMContentLoaded', () => {
  const aboutSection = document.querySelector('#about2');
  if (aboutSection) {
    aboutObserver.observe(aboutSection);
  }
  
  // Add hover effects to social links
  const socialLinks = document.querySelectorAll('.social-links a');
  socialLinks.forEach(link => {
    link.addEventListener('mouseenter', (e) => {
      e.target.style.transform = 'scale(1.2) rotate(5deg)';
    });
    
    link.addEventListener('mouseleave', (e) => {
      e.target.style.transform = 'scale(1) rotate(0deg)';
    });
  });
});

// Add CSS animations via JavaScript
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(-30px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
  
  @keyframes zoomIn {
    from {
      opacity: 0;
      transform: scale(0.8);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
`;
document.head.appendChild(style);
