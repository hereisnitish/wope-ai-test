// Project data for modal content
const projectData = {
  'Project 1': {
    title: 'Advanced Web Application',
    description: 'A comprehensive web application built with modern technologies, featuring user authentication, real-time data synchronization, and responsive design.',
    details: `
      <div class="project-details">
        <h3>Project Overview</h3>
        <p>This full-stack web application demonstrates advanced development skills with a focus on user experience and performance optimization.</p>
        
        <h4>Key Features:</h4>
        <ul>
          <li>User authentication and authorization system</li>
          <li>Real-time data synchronization with WebSocket</li>
          <li>Responsive design for all devices</li>
          <li>Advanced search and filtering capabilities</li>
          <li>Performance optimization with lazy loading</li>
          <li>Comprehensive testing coverage</li>
        </ul>
        
        <h4>Technologies Used:</h4>
        <div class="tech-stack">
          <span class="tech-badge">React</span>
          <span class="tech-badge">Node.js</span>
          <span class="tech-badge">MongoDB</span>
          <span class="tech-badge">Socket.io</span>
          <span class="tech-badge">JWT</span>
          <span class="tech-badge">Jest</span>
        </div>
        
        <div class="project-image-gallery">
          <img src="https://via.placeholder.com/600x300/3498db/ffffff?text=Dashboard+View" alt="Dashboard">
          <img src="https://via.placeholder.com/600x300/2980b9/ffffff?text=User+Interface" alt="UI">
        </div>
      </div>
    `,
    liveUrl: 'https://example.com/project1',
    codeUrl: 'https://github.com/username/project1'
  },
  'Project 2': {
    title: 'Mobile Application',
    description: 'Cross-platform mobile application with native performance and beautiful user interface.',
    details: `
      <div class="project-details">
        <h3>Mobile App Development</h3>
        <p>A feature-rich mobile application designed for both iOS and Android platforms with focus on performance and user engagement.</p>
        
        <h4>Features:</h4>
        <ul>
          <li>Cross-platform compatibility</li>
          <li>Push notifications system</li>
          <li>Offline data synchronization</li>
          <li>Biometric authentication</li>
          <li>In-app purchases integration</li>
          <li>Social media sharing</li>
        </ul>
        
        <h4>Tech Stack:</h4>
        <div class="tech-stack">
          <span class="tech-badge">React Native</span>
          <span class="tech-badge">Redux</span>
          <span class="tech-badge">Firebase</span>
          <span class="tech-badge">AsyncStorage</span>
          <span class="tech-badge">Push Notifications</span>
        </div>
        
        <div class="project-image-gallery">
          <img src="https://via.placeholder.com/300x600/e74c3c/ffffff?text=Home+Screen" alt="Home Screen">
          <img src="https://via.placeholder.com/300x600/c0392b/ffffff?text=Profile+View" alt="Profile">
        </div>
      </div>
    `,
    liveUrl: 'https://play.google.com/store/apps/project2',
    codeUrl: 'https://github.com/username/project2'
  },
  'Project 3': {
    title: 'Dashboard Interface',
    description: 'Comprehensive dashboard with data visualization, analytics, and real-time monitoring capabilities.',
    details: `
      <div class="project-details">
        <h3>Analytics Dashboard</h3>
        <p>An intuitive dashboard interface providing comprehensive data visualization and business intelligence tools.</p>
        
        <h4>Dashboard Features:</h4>
        <ul>
          <li>Interactive charts and graphs</li>
          <li>Real-time data monitoring</li>
          <li>Customizable widget layouts</li>
          <li>Export functionality (PDF, CSV)</li>
          <li>User role-based access control</li>
          <li>Mobile-responsive design</li>
        </ul>
        
        <h4>Technologies:</h4>
        <div class="tech-stack">
          <span class="tech-badge">D3.js</span>
          <span class="tech-badge">Chart.js</span>
          <span class="tech-badge">Express.js</span>
          <span class="tech-badge">PostgreSQL</span>
          <span class="tech-badge">WebSocket</span>
        </div>
        
        <div class="project-image-gallery">
          <img src="https://via.placeholder.com/600x300/2ecc71/ffffff?text=Analytics+View" alt="Analytics">
          <img src="https://via.placeholder.com/600x300/27ae60/ffffff?text=Reports+Section" alt="Reports">
        </div>
      </div>
    `,
    liveUrl: 'https://example.com/dashboard',
    codeUrl: 'https://github.com/username/dashboard'
  },
  'Project 4': {
    title: 'E-commerce Platform',
    description: 'Modern e-commerce solution with advanced features for online retail businesses.',
    details: `
      <div class="project-details">
        <h3>E-commerce Solution</h3>
        <p>A comprehensive e-commerce platform designed to provide seamless shopping experience with modern payment integration.</p>
        
        <h4>E-commerce Features:</h4>
        <ul>
          <li>Product catalog with advanced search</li>
          <li>Shopping cart and wishlist functionality</li>
          <li>Secure payment processing</li>
          <li>Order tracking system</li>
          <li>Inventory management</li>
          <li>Customer review system</li>
        </ul>
        
        <h4>Built With:</h4>
        <div class="tech-stack">
          <span class="tech-badge">Next.js</span>
          <span class="tech-badge">Stripe</span>
          <span class="tech-badge">Prisma</span>
          <span class="tech-badge">PostgreSQL</span>
          <span class="tech-badge">Tailwind CSS</span>
        </div>
        
        <div class="project-image-gallery">
          <img src="https://via.placeholder.com/600x300/f39c12/ffffff?text=Product+Catalog" alt="Catalog">
          <img src="https://via.placeholder.com/600x300/e67e22/ffffff?text=Checkout+Process" alt="Checkout">
        </div>
      </div>
    `,
    liveUrl: 'https://example.com/ecommerce',
    codeUrl: 'https://github.com/username/ecommerce'
  },
  'Project 5': {
    title: 'Brand Identity Design',
    description: 'Complete brand identity package including logo design, color palette, and brand guidelines.',
    details: `
      <div class="project-details">
        <h3>Brand Identity Project</h3>
        <p>A comprehensive branding project that establishes a strong visual identity and brand presence across all touchpoints.</p>
        
        <h4>Branding Elements:</h4>
        <ul>
          <li>Logo design and variations</li>
          <li>Color palette and typography</li>
          <li>Business card and stationery design</li>
          <li>Brand guidelines document</li>
          <li>Social media template designs</li>
          <li>Website mockups and layouts</li>
        </ul>
        
        <h4>Design Tools:</h4>
        <div class="tech-stack">
          <span class="tech-badge">Adobe Illustrator</span>
          <span class="tech-badge">Adobe Photoshop</span>
          <span class="tech-badge">Figma</span>
          <span class="tech-badge">Adobe InDesign</span>
          <span class="tech-badge">Color Theory</span>
        </div>
        
        <div class="project-image-gallery">
          <img src="https://via.placeholder.com/600x300/9b59b6/ffffff?text=Logo+Design" alt="Logo">
          <img src="https://via.placeholder.com/600x300/8e44ad/ffffff?text=Brand+Guidelines" alt="Guidelines">
        </div>
      </div>
    `,
    liveUrl: 'https://behance.net/project5',
    codeUrl: 'https://dribbble.com/shots/project5'
  },
  'Project 6': {
    title: 'Landing Page Design',
    description: 'High-converting landing page with optimized user experience and conversion rate optimization.',
    details: `
      <div class="project-details">
        <h3>Landing Page Optimization</h3>
        <p>A conversion-focused landing page designed to maximize user engagement and achieve business objectives.</p>
        
        <h4>Optimization Features:</h4>
        <ul>
          <li>A/B tested design elements</li>
          <li>Conversion rate optimization</li>
          <li>Mobile-first responsive design</li>
          <li>Fast loading performance</li>
          <li>SEO optimized content</li>
          <li>Analytics integration</li>
        </ul>
        
        <h4>Technologies Used:</h4>
        <div class="tech-stack">
          <span class="tech-badge">HTML5</span>
          <span class="tech-badge">CSS3</span>
          <span class="tech-badge">JavaScript</span>
          <span class="tech-badge">GSAP</span>
          <span class="tech-badge">Google Analytics</span>
        </div>
        
        <div class="project-image-gallery">
          <img src="https://via.placeholder.com/600x300/1abc9c/ffffff?text=Hero+Section" alt="Hero">
          <img src="https://via.placeholder.com/600x300/16a085/ffffff?text=CTA+Section" alt="CTA">
        </div>
      </div>
    `,
    liveUrl: 'https://example.com/landing',
    codeUrl: 'https://github.com/username/landing'
  }
};

let currentProjectIndex = 0;
const projectKeys = Object.keys(projectData);

function openModal(projectName) {
  const modal = document.getElementById('modal');
  const modalTitle = document.getElementById('modal-title');
  const modalContent = document.getElementById('modal-content');
  const liveBtn = document.querySelector('.btn-primary');
  const codeBtn = document.querySelector('.btn-secondary');
  
  currentProjectIndex = projectKeys.indexOf(projectName);
  const project = projectData[projectName];
  
  if (project) {
    modalTitle.textContent = project.title;
    modalContent.innerHTML = project.details;
    liveBtn.href = project.liveUrl;
    codeBtn.href = project.codeUrl;
    
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal() {
  const modal = document.getElementById('modal');
  modal.classList.remove('show');
  document.body.style.overflow = '';
}

function prevProject() {
  currentProjectIndex = (currentProjectIndex - 1 + projectKeys.length) % projectKeys.length;
  const projectName = projectKeys[currentProjectIndex];
  updateModalContent(projectName);
}

function nextProject() {
  currentProjectIndex = (currentProjectIndex + 1) % projectKeys.length;
  const projectName = projectKeys[currentProjectIndex];
  updateModalContent(projectName);
}

function updateModalContent(projectName) {
  const modalTitle = document.getElementById('modal-title');
  const modalContent = document.getElementById('modal-content');
  const liveBtn = document.querySelector('.btn-primary');
  const codeBtn = document.querySelector('.btn-secondary');
  
  const project = projectData[projectName];
  
  if (project) {
    // Add fade animation
    modalContent.style.opacity = '0';
    modalTitle.style.opacity = '0';
    
    setTimeout(() => {
      modalTitle.textContent = project.title;
      modalContent.innerHTML = project.details;
      liveBtn.href = project.liveUrl;
      codeBtn.href = project.codeUrl;
      
      modalContent.style.opacity = '1';
      modalTitle.style.opacity = '1';
    }, 150);
  }
}

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('modal');
  
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
  const modal = document.getElementById('modal');
  if (modal.classList.contains('show')) {
    switch(e.key) {
      case 'Escape':
        closeModal();
        break;
      case 'ArrowLeft':
        prevProject();
        break;
      case 'ArrowRight':
        nextProject();
        break;
    }
  }
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
  const projectsSection = document.querySelector('#projects2');
  if (projectsSection) {
    projectsObserver.observe(projectsSection);
  }
});

// Add hover sound effects (optional)
document.addEventListener('DOMContentLoaded', () => {
  const projectItems = document.querySelectorAll('.project-item');
  
  projectItems.forEach(item => {
    item.addEventListener('mouseenter', () => {
      // Add subtle visual feedback
      item.style.filter = 'brightness(1.1)';
    });
    
    item.addEventListener('mouseleave', () => {
      item.style.filter = 'brightness(1)';
    });
  });
});

// Add CSS styles for modal content
const modalContentStyles = document.createElement('style');
modalContentStyles.textContent = `
  .project-details h3 {
    color: #2c3e50;
    font-size: 1.5rem;
    margin-bottom: 15px;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
  }
  
  .project-details h4 {
    color: #34495e;
    font-size: 1.2rem;
    margin: 25px 0 15px 0;
  }
  
  .project-details p {
    line-height: 1.7;
    color: #555;
    margin-bottom: 20px;
  }
  
  .project-details ul {
    margin: 15px 0;
    padding-left: 25px;
  }
  
  .project-details li {
    margin-bottom: 8px;
    color: #666;
    position: relative;
  }
  
  .project-details li::marker {
    color: #3498db;
  }
  
  .tech-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 15px 0 25px 0;
  }
  
  .tech-badge {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
  }
  
  .project-image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin-top: 25px;
  }
  
  .project-image-gallery img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
  }
  
  .project-image-gallery img:hover {
    transform: scale(1.05);
  }
  
  @media (max-width: 768px) {
    .project-image-gallery {
      grid-template-columns: 1fr;
    }
    
    .tech-stack {
      justify-content: center;
    }
  }
`;
document.head.appendChild(modalContentStyles);
