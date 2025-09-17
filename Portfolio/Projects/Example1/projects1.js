// Project filtering functionality
let currentFilter = 'all';

function filterProjects(category) {
  const projectCards = document.querySelectorAll('.project-card');
  const filterBtns = document.querySelectorAll('.filter-btn');
  
  // Update active filter button
  filterBtns.forEach(btn => {
    btn.classList.remove('active');
    if (btn.getAttribute('data-filter') === category) {
      btn.classList.add('active');
    }
  });
  
  // Filter project cards with animation
  projectCards.forEach((card, index) => {
    const cardCategory = card.getAttribute('data-category');
    const shouldShow = category === 'all' || cardCategory === category;
    
    if (shouldShow) {
      setTimeout(() => {
        card.classList.remove('hidden', 'filtering-out');
        card.classList.add('filtering-in');
        card.style.display = 'block';
      }, index * 50);
    } else {
      card.classList.add('filtering-out');
      card.classList.remove('filtering-in');
      setTimeout(() => {
        card.classList.add('hidden');
        card.style.display = 'none';
      }, 300);
    }
  });
  
  currentFilter = category;
}

// Initialize filter functionality
document.addEventListener('DOMContentLoaded', () => {
  const filterBtns = document.querySelectorAll('.filter-btn');
  
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const category = btn.getAttribute('data-filter');
      filterProjects(category);
    });
  });
});

// Project preview functionality
const projectDetails = {
  ecommerce: {
    title: "E-commerce Platform",
    description: "A full-featured e-commerce platform built with React and Django, featuring user authentication, product catalog, shopping cart, payment processing, and admin dashboard.",
    features: [
      "User authentication and profiles",
      "Product catalog with search and filters",
      "Shopping cart and wishlist",
      "Secure payment integration (Stripe)",
      "Order management system",
      "Admin dashboard with analytics"
    ],
    tech: ["React", "Django", "PostgreSQL", "Redis", "Stripe API", "AWS"],
    images: [
      "https://via.placeholder.com/600x400/3498db/ffffff?text=Homepage",
      "https://via.placeholder.com/600x400/2980b9/ffffff?text=Product+Page",
      "https://via.placeholder.com/600x400/1abc9c/ffffff?text=Cart"
    ]
  },
  taskmanager: {
    title: "Task Manager App",
    description: "Cross-platform mobile application for task management and team collaboration, built with React Native and Firebase.",
    features: [
      "Task creation and organization",
      "Team collaboration tools",
      "Real-time synchronization",
      "Offline functionality",
      "Push notifications",
      "Progress tracking and analytics"
    ],
    tech: ["React Native", "Firebase", "Redux", "Push Notifications", "Async Storage"],
    images: [
      "https://via.placeholder.com/300x600/e74c3c/ffffff?text=Task+List",
      "https://via.placeholder.com/300x600/c0392b/ffffff?text=Task+Details",
      "https://via.placeholder.com/300x600/e67e22/ffffff?text=Analytics"
    ]
  },
  portfolio: {
    title: "Creative Portfolio",
    description: "A responsive portfolio website featuring smooth animations, dark mode toggle, and performance optimizations.",
    features: [
      "Responsive design across all devices",
      "Dark/Light mode toggle",
      "Smooth scroll animations",
      "Performance optimizations",
      "Contact form integration",
      "SEO optimization"
    ],
    tech: ["Vue.js", "SCSS", "GSAP", "Webpack", "Netlify", "Formspree"],
    images: [
      "https://via.placeholder.com/600x400/2ecc71/ffffff?text=Hero+Section",
      "https://via.placeholder.com/600x400/27ae60/ffffff?text=Projects",
      "https://via.placeholder.com/600x400/16a085/ffffff?text=Contact"
    ]
  },
  designsystem: {
    title: "UI Design System",
    description: "Comprehensive design system with reusable components, style guides, and interaction patterns for modern applications.",
    features: [
      "Component library with 50+ components",
      "Design tokens and style guidelines",
      "Interactive documentation",
      "Figma design files",
      "Code snippets and examples",
      "Accessibility standards compliance"
    ],
    tech: ["Figma", "Storybook", "CSS Custom Properties", "JavaScript", "Documentation"],
    images: [
      "https://via.placeholder.com/600x400/9b59b6/ffffff?text=Components",
      "https://via.placeholder.com/600x400/8e44ad/ffffff?text=Style+Guide",
      "https://via.placeholder.com/600x400/663399/ffffff?text=Documentation"
    ]
  },
  dashboard: {
    title: "Analytics Dashboard",
    description: "Interactive data visualization dashboard with real-time updates, charts, and customizable widgets.",
    features: [
      "Real-time data visualization",
      "Interactive charts and graphs",
      "Customizable dashboard layout",
      "Data export functionality",
      "User role management",
      "Mobile-responsive design"
    ],
    tech: ["D3.js", "Node.js", "Socket.io", "MongoDB", "Express", "Chart.js"],
    images: [
      "https://via.placeholder.com/600x400/f39c12/ffffff?text=Main+Dashboard",
      "https://via.placeholder.com/600x400/e67e22/ffffff?text=Charts",
      "https://via.placeholder.com/600x400/d35400/ffffff?text=Analytics"
    ]
  },
  weather: {
    title: "Weather Forecast App",
    description: "Beautiful weather application with location-based forecasts, interactive maps, and offline capabilities.",
    features: [
      "Location-based weather data",
      "7-day weather forecast",
      "Interactive weather maps",
      "Offline data caching",
      "Weather alerts and notifications",
      "Multiple location support"
    ],
    tech: ["Flutter", "OpenWeather API", "SQLite", "Provider", "Geolocator"],
    images: [
      "https://via.placeholder.com/300x600/1abc9c/ffffff?text=Current+Weather",
      "https://via.placeholder.com/300x600/16a085/ffffff?text=Forecast",
      "https://via.placeholder.com/300x600/0f6b5c/ffffff?text=Maps"
    ]
  }
};

function openProjectPreview(projectKey) {
  const project = projectDetails[projectKey];
  if (!project) return;
  
  // Create modal HTML
  const modalHTML = `
    <div class="project-modal" id="projectModal">
      <div class="modal-backdrop" onclick="closeProjectPreview()"></div>
      <div class="modal-content">
        <button class="modal-close" onclick="closeProjectPreview()">&times;</button>
        <div class="modal-header">
          <h2>${project.title}</h2>
          <p>${project.description}</p>
        </div>
        <div class="modal-body">
          <div class="project-images">
            ${project.images.map((img, index) => 
              `<img src="${img}" alt="${project.title} Screenshot ${index + 1}" 
                   class="${index === 0 ? 'active' : ''}" 
                   onclick="changeProjectImage(${index})">`
            ).join('')}
          </div>
          <div class="project-info">
            <div class="project-features">
              <h3>Key Features</h3>
              <ul>
                ${project.features.map(feature => `<li>${feature}</li>`).join('')}
              </ul>
            </div>
            <div class="project-technologies">
              <h3>Technologies Used</h3>
              <div class="tech-tags">
                ${project.tech.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // Add modal to DOM
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  // Add modal styles
  if (!document.getElementById('modalStyles')) {
    const modalStyles = document.createElement('style');
    modalStyles.id = 'modalStyles';
    modalStyles.textContent = `
      .project-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.3s ease;
      }
      
      .modal-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(5px);
      }
      
      .modal-content {
        position: relative;
        background: white;
        border-radius: 20px;
        max-width: 900px;
        max-height: 80vh;
        overflow-y: auto;
        margin: 20px;
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
      
      .modal-header {
        padding: 30px 30px 20px;
        border-bottom: 1px solid #eee;
      }
      
      .modal-header h2 {
        color: #2c3e50;
        margin-bottom: 10px;
      }
      
      .modal-body {
        padding: 30px;
      }
      
      .project-images {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-bottom: 30px;
      }
      
      .project-images img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        opacity: 0.7;
      }
      
      .project-images img.active,
      .project-images img:hover {
        opacity: 1;
        transform: scale(1.02);
      }
      
      .project-info {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
      }
      
      .project-features h3,
      .project-technologies h3 {
        color: #2c3e50;
        margin-bottom: 15px;
      }
      
      .project-features ul {
        list-style: none;
        padding: 0;
      }
      
      .project-features li {
        padding: 8px 0;
        position: relative;
        padding-left: 20px;
      }
      
      .project-features li::before {
        content: '✓';
        position: absolute;
        left: 0;
        color: #27ae60;
        font-weight: bold;
      }
      
      .tech-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }
      
      @media (max-width: 768px) {
        .modal-content {
          margin: 10px;
          max-height: 90vh;
        }
        
        .modal-header,
        .modal-body {
          padding: 20px;
        }
        
        .project-info {
          grid-template-columns: 1fr;
          gap: 20px;
        }
        
        .project-images {
          grid-template-columns: 1fr;
        }
      }
    `;
    document.head.appendChild(modalStyles);
  }
  
  // Prevent body scroll
  document.body.style.overflow = 'hidden';
}

function closeProjectPreview() {
  const modal = document.getElementById('projectModal');
  if (modal) {
    modal.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => {
      modal.remove();
      document.body.style.overflow = '';
    }, 300);
  }
}

function changeProjectImage(index) {
  const images = document.querySelectorAll('.project-images img');
  images.forEach((img, i) => {
    img.classList.toggle('active', i === index);
  });
}

// Initialize project preview functionality
document.addEventListener('DOMContentLoaded', () => {
  const previewBtns = document.querySelectorAll('.btn-preview');
  
  previewBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const projectKey = btn.getAttribute('data-project');
      openProjectPreview(projectKey);
    });
  });
});

// Intersection Observer for animations
const projectsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
      projectsObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
});

// Initialize observer
document.addEventListener('DOMContentLoaded', () => {
  const projectsSection = document.querySelector('#projects1');
  if (projectsSection) {
    projectsObserver.observe(projectsSection);
  }
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeProjectPreview();
  }
});

// Add fade in animation for CSS
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
  }
  
  @keyframes slideInUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;
document.head.appendChild(style);
