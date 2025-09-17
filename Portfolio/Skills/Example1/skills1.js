// Skill descriptions for tooltips
const skillDescriptions = {
  html: {
    title: "HTML5",
    description: "Semantic markup language for structuring web content with modern standards and accessibility features."
  },
  css: {
    title: "CSS3",
    description: "Advanced styling with animations, flexbox, grid, and responsive design techniques."
  },
  javascript: {
    title: "JavaScript",
    description: "Modern ES6+ JavaScript for dynamic web applications and interactive user experiences."
  },
  react: {
    title: "React",
    description: "Component-based JavaScript library for building user interfaces with hooks and state management."
  },
  vue: {
    title: "Vue.js",
    description: "Progressive JavaScript framework for building interactive web applications."
  },
  python: {
    title: "Python",
    description: "Versatile programming language for web development, automation, and data processing."
  },
  django: {
    title: "Django",
    description: "High-level Python web framework for rapid development with built-in admin and ORM."
  },
  nodejs: {
    title: "Node.js",
    description: "JavaScript runtime for server-side development and building scalable network applications."
  },
  database: {
    title: "MongoDB",
    description: "NoSQL database for flexible, document-based data storage and retrieval."
  },
  api: {
    title: "REST API",
    description: "RESTful web services for communication between frontend and backend systems."
  },
  git: {
    title: "Git",
    description: "Distributed version control system for tracking changes and collaboration."
  },
  docker: {
    title: "Docker",
    description: "Containerization platform for consistent deployment across different environments."
  },
  figma: {
    title: "Figma",
    description: "Collaborative design tool for UI/UX design, prototyping, and design systems."
  },
  aws: {
    title: "AWS",
    description: "Amazon Web Services cloud platform for hosting, storage, and scalable applications."
  },
  webpack: {
    title: "Webpack",
    description: "Module bundler for JavaScript applications with code splitting and optimization."
  }
};

// Tooltip functionality
let tooltip = null;

function showTooltip(element, skillKey) {
  tooltip = document.getElementById('skillTooltip');
  const skill = skillDescriptions[skillKey];
  
  if (!skill || !tooltip) return;
  
  // Update tooltip content
  document.getElementById('tooltipTitle').textContent = skill.title;
  document.getElementById('tooltipDescription').textContent = skill.description;
  
  // Position tooltip
  const rect = element.getBoundingClientRect();
  const tooltipRect = tooltip.getBoundingClientRect();
  
  tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltipRect.width / 2)}px`;
  tooltip.style.top = `${rect.top - tooltipRect.height - 15}px`;
  
  // Show tooltip
  tooltip.classList.add('show');
}

function hideTooltip() {
  if (tooltip) {
    tooltip.classList.remove('show');
  }
}

// Skill hover effects
document.addEventListener('DOMContentLoaded', () => {
  const skillItems = document.querySelectorAll('.skill-list li');
  
  skillItems.forEach(item => {
    const skillKey = item.getAttribute('data-skill');
    
    item.addEventListener('mouseenter', (e) => {
      showTooltip(e.currentTarget, skillKey);
    });
    
    item.addEventListener('mouseleave', () => {
      hideTooltip();
    });
    
    // Add click effect for mobile
    item.addEventListener('click', () => {
      item.style.transform = 'scale(0.95)';
      setTimeout(() => {
        item.style.transform = '';
      }, 150);
    });
  });
});

// Hide tooltip when scrolling
window.addEventListener('scroll', hideTooltip);

// Intersection Observer for animations
const skillsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
      
      // Animate individual skills with stagger
      const skillItems = entry.target.querySelectorAll('.skill-list li');
      skillItems.forEach((item, index) => {
        setTimeout(() => {
          item.style.opacity = '0';
          item.style.transform = 'translateX(-20px)';
          item.style.transition = 'all 0.5s ease';
          
          setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
          }, 50);
        }, index * 100);
      });
      
      skillsObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.2,
  rootMargin: '0px 0px -50px 0px'
});

// Initialize observer
document.addEventListener('DOMContentLoaded', () => {
  const skillsSection = document.querySelector('#skills1');
  if (skillsSection) {
    skillsObserver.observe(skillsSection);
  }
});

// Skill category hover effects
document.addEventListener('DOMContentLoaded', () => {
  const categories = document.querySelectorAll('.skill-category');
  
  categories.forEach(category => {
    category.addEventListener('mouseenter', () => {
      category.style.borderTopColor = '#2980b9';
    });
    
    category.addEventListener('mouseleave', () => {
      category.style.borderTopColor = '#3498db';
    });
  });
});

// Keyboard navigation for accessibility
document.addEventListener('DOMContentLoaded', () => {
  const skillItems = document.querySelectorAll('.skill-list li');
  
  skillItems.forEach(item => {
    item.setAttribute('tabindex', '0');
    item.setAttribute('role', 'button');
    
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const skillKey = item.getAttribute('data-skill');
        showTooltip(item, skillKey);
        
        setTimeout(() => {
          hideTooltip();
        }, 3000); // Auto-hide after 3 seconds
      }
    });
  });
});
