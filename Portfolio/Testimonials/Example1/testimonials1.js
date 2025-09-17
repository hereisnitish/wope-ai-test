// Testimonial interactions and animations

// Intersection Observer for scroll animations
const testimonialsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
      
      // Add typing effect to blockquotes
      const blockquotes = entry.target.querySelectorAll('blockquote');
      blockquotes.forEach((quote, index) => {
        setTimeout(() => {
          addTypingEffect(quote);
        }, index * 200 + 800);
      });
      
      testimonialsObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
});

// Add typing effect to testimonial text
function addTypingEffect(element) {
  const originalText = element.textContent;
  const words = originalText.split(' ');
  let currentWordIndex = 0;
  
  element.textContent = '';
  
  const typeWord = () => {
    if (currentWordIndex < words.length) {
      element.textContent += (currentWordIndex > 0 ? ' ' : '') + words[currentWordIndex];
      currentWordIndex++;
      setTimeout(typeWord, 100); // Adjust speed here
    }
  };
  
  // Start typing with a delay
  setTimeout(typeWord, 500);
}

// Enhanced hover effects for testimonial cards
document.addEventListener('DOMContentLoaded', () => {
  const testimonialCards = document.querySelectorAll('.testimonial-card');
  
  testimonialCards.forEach((card, index) => {
    // Add stagger delay for initial animations
    card.style.animationDelay = `${index * 0.1}s`;
    
    // Enhanced hover interactions
    card.addEventListener('mouseenter', () => {
      // Subtle scale effect on client image
      const clientImg = card.querySelector('.client-info img');
      if (clientImg) {
        clientImg.style.transform = 'scale(1.1) rotate(5deg)';
      }
      
      // Enhance quote icon animation
      const quoteIcon = card.querySelector('.quote-icon');
      if (quoteIcon) {
        quoteIcon.style.transform = 'scale(1.2) rotate(10deg)';
        quoteIcon.style.boxShadow = '0 8px 25px rgba(52, 152, 219, 0.4)';
      }
      
      // Highlight stars
      const stars = card.querySelectorAll('.rating i');
      stars.forEach((star, starIndex) => {
        setTimeout(() => {
          star.style.transform = 'scale(1.2)';
          star.style.color = '#f1c40f';
        }, starIndex * 50);
      });
    });
    
    card.addEventListener('mouseleave', () => {
      // Reset client image
      const clientImg = card.querySelector('.client-info img');
      if (clientImg) {
        clientImg.style.transform = 'scale(1) rotate(0deg)';
      }
      
      // Reset quote icon
      const quoteIcon = card.querySelector('.quote-icon');
      if (quoteIcon) {
        quoteIcon.style.transform = 'scale(1) rotate(0deg)';
        quoteIcon.style.boxShadow = '0 5px 15px rgba(52, 152, 219, 0.3)';
      }
      
      // Reset stars
      const stars = card.querySelectorAll('.rating i');
      stars.forEach(star => {
        star.style.transform = 'scale(1)';
        star.style.color = '#f39c12';
      });
    });
    
    // Click to expand functionality
    card.addEventListener('click', () => {
      expandTestimonial(card, index);
    });
    
    // Keyboard accessibility
    card.setAttribute('tabindex', '0');
    card.setAttribute('role', 'button');
    card.setAttribute('aria-label', `Read testimonial from ${card.querySelector('.client-details h4').textContent}`);
    
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        expandTestimonial(card, index);
      }
    });
  });
});

// Expand testimonial functionality
function expandTestimonial(card, index) {
  const testimonialData = [
    {
      client: "John Smith",
      company: "TechStart Inc.",
      fullTestimonial: "Alex delivered an exceptional website that exceeded our expectations. The attention to detail and professional approach made the entire process seamless. From the initial consultation to the final deployment, Alex demonstrated expertise in both design and development. The website not only looks stunning but also performs flawlessly across all devices. Our conversion rates have increased by 40% since the launch!",
      projectDetails: "Complete website redesign with e-commerce integration, mobile optimization, and SEO enhancement.",
      timeline: "6 weeks",
      rating: 5
    },
    {
      client: "Sarah Miller",
      company: "AppVenture",
      fullTestimonial: "Working with Alex was a game-changer for our mobile app. The user interface is intuitive and the performance is outstanding. The app has received countless positive reviews from our users, and the retention rate has improved significantly. Alex's ability to understand our vision and translate it into a functional, beautiful app is remarkable.",
      projectDetails: "Cross-platform mobile app development with real-time features and cloud integration.",
      timeline: "10 weeks",
      rating: 5
    },
    {
      client: "Michael Johnson",
      company: "GreenTech",
      fullTestimonial: "Professional, responsive, and creative. Alex transformed our brand identity and created a stunning digital presence. The results speak for themselves - our brand recognition has improved dramatically, and we've seen a 60% increase in qualified leads. The comprehensive approach to branding and web development was exactly what we needed.",
      projectDetails: "Complete brand identity overhaul including logo design, website development, and marketing materials.",
      timeline: "8 weeks",
      rating: 5
    },
    {
      client: "Lisa Davis",
      company: "StyleShop",
      fullTestimonial: "The e-commerce platform Alex built for us increased our online sales by 300%. The attention to user experience and conversion optimization was remarkable. Every aspect of the shopping experience has been carefully crafted to encourage purchases while maintaining a premium brand feel. The backend management system is equally impressive.",
      projectDetails: "Full-featured e-commerce platform with inventory management, payment processing, and analytics dashboard.",
      timeline: "12 weeks",
      rating: 5
    },
    {
      client: "Robert Wilson",
      company: "DataInsights",
      fullTestimonial: "Alex's expertise in both design and development is rare. The dashboard interface created for our analytics platform is both beautiful and functional. Our clients love the intuitive design, and the performance improvements have been substantial. The project was delivered on time and within budget.",
      projectDetails: "Advanced analytics dashboard with real-time data visualization and custom reporting features.",
      timeline: "14 weeks",
      rating: 5
    },
    {
      client: "Emma Thompson",
      company: "ArtStudio",
      fullTestimonial: "From concept to deployment, Alex provided exceptional service. The website is fast, responsive, and perfectly captures our brand essence. The portfolio showcase functionality has helped us attract higher-quality clients, and the integrated booking system has streamlined our operations significantly.",
      projectDetails: "Creative portfolio website with booking system, gallery management, and client portal.",
      timeline: "7 weeks",
      rating: 5
    }
  ];
  
  const data = testimonialData[index];
  if (!data) return;
  
  // Create expanded modal
  const modal = document.createElement('div');
  modal.className = 'testimonial-modal';
  modal.innerHTML = `
    <div class="testimonial-modal-content">
      <button class="modal-close" onclick="closeTestimonialModal()">&times;</button>
      <div class="expanded-testimonial">
        <div class="client-header">
          <img src="${card.querySelector('.client-info img').src}" alt="${data.client}">
          <div class="client-info-expanded">
            <h3>${data.client}</h3>
            <p>${data.company}</p>
            <div class="rating-expanded">
              ${Array(data.rating).fill('<i class="fas fa-star"></i>').join('')}
            </div>
          </div>
        </div>
        <div class="testimonial-content-expanded">
          <blockquote>"${data.fullTestimonial}"</blockquote>
          <div class="project-summary">
            <h4>Project Details:</h4>
            <p>${data.projectDetails}</p>
            <div class="project-meta">
              <span><strong>Timeline:</strong> ${data.timeline}</span>
              <span><strong>Rating:</strong> ${data.rating}/5 stars</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  document.body.style.overflow = 'hidden';
  
  // Add modal styles
  if (!document.getElementById('testimonialModalStyles')) {
    const modalStyles = document.createElement('style');
    modalStyles.id = 'testimonialModalStyles';
    modalStyles.textContent = `
      .testimonial-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(5px);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.3s ease;
      }
      
      .testimonial-modal-content {
        background: white;
        border-radius: 20px;
        max-width: 700px;
        max-height: 80vh;
        overflow-y: auto;
        margin: 20px;
        position: relative;
        animation: slideInUp 0.3s ease;
      }
      
      .modal-close {
        position: absolute;
        top: 20px;
        right: 25px;
        background: none;
        border: none;
        font-size: 2rem;
        cursor: pointer;
        color: #666;
        z-index: 1001;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
      }
      
      .modal-close:hover {
        background: #f5f5f5;
        color: #333;
      }
      
      .expanded-testimonial {
        padding: 40px;
      }
      
      .client-header {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 2px solid #ecf0f1;
      }
      
      .client-header img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid #3498db;
      }
      
      .client-info-expanded h3 {
        color: #2c3e50;
        margin: 0 0 5px 0;
        font-size: 1.4rem;
      }
      
      .client-info-expanded p {
        color: #666;
        margin: 0 0 10px 0;
      }
      
      .rating-expanded {
        display: flex;
        gap: 3px;
      }
      
      .rating-expanded i {
        color: #f39c12;
        font-size: 1rem;
      }
      
      .testimonial-content-expanded blockquote {
        font-size: 1.2rem;
        line-height: 1.8;
        color: #555;
        margin: 0 0 30px 0;
        font-style: italic;
        padding: 20px;
        background: #f8f9fa;
        border-left: 4px solid #3498db;
        border-radius: 0 10px 10px 0;
      }
      
      .project-summary h4 {
        color: #2c3e50;
        margin-bottom: 15px;
        font-size: 1.2rem;
      }
      
      .project-summary p {
        color: #666;
        line-height: 1.6;
        margin-bottom: 20px;
      }
      
      .project-meta {
        display: flex;
        gap: 30px;
        flex-wrap: wrap;
      }
      
      .project-meta span {
        color: #555;
        font-size: 0.95rem;
      }
      
      @media (max-width: 768px) {
        .testimonial-modal-content {
          margin: 10px;
          max-height: 90vh;
        }
        
        .expanded-testimonial {
          padding: 30px 25px;
        }
        
        .client-header {
          flex-direction: column;
          text-align: center;
          gap: 15px;
        }
        
        .testimonial-content-expanded blockquote {
          font-size: 1.1rem;
          padding: 15px;
        }
        
        .project-meta {
          flex-direction: column;
          gap: 10px;
        }
      }
    `;
    document.head.appendChild(modalStyles);
  }
}

// Close testimonial modal
function closeTestimonialModal() {
  const modal = document.querySelector('.testimonial-modal');
  if (modal) {
    modal.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => {
      modal.remove();
      document.body.style.overflow = '';
    }, 300);
  }
}

// Keyboard navigation for modal
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeTestimonialModal();
  }
});

// Initialize observer
document.addEventListener('DOMContentLoaded', () => {
  const testimonialsSection = document.querySelector('#testimonials1');
  if (testimonialsSection) {
    testimonialsObserver.observe(testimonialsSection);
  }
});

// Add fade animations to CSS
const fadeAnimations = document.createElement('style');
fadeAnimations.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
  }
`;
document.head.appendChild(fadeAnimations);
