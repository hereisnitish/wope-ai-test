function scrollToContact() {
  const contactElement = document.getElementById('contact');
  if (contactElement) {
    contactElement.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  } else {
    console.warn('Contact element not found');
  }
}

// Add typing effect to hero title
document.addEventListener('DOMContentLoaded', function() {
  const heroTitle = document.querySelector('#hero1 h1');
  if (heroTitle) {
    const originalText = heroTitle.textContent;
    heroTitle.textContent = '';
    
    let i = 0;
    const typeWriter = setInterval(() => {
      heroTitle.textContent += originalText[i];
      i++;
      if (i >= originalText.length) {
        clearInterval(typeWriter);
      }
    }, 100);
  }
});
