// static/js/enhancements.js
// 增强页面交互效果

// 增强页面加载效果
function enhancePageLoad() {
    // 添加页面加载动画
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.6s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
        
        // 添加卡片入场动画
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(40px) scale(0.95)';
            card.style.transition = `all 0.8s ease ${index * 0.1}s`;
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0) scale(1)';
            }, 100);
        });
        
        // 添加导航栏动画
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.style.transform = 'translateY(-100%)';
            navbar.style.transition = 'transform 0.6s ease';
            
            setTimeout(() => {
                navbar.style.transform = 'translateY(0)';
            }, 300);
        }
    }, 100);
}

// 增强滚动效果
function enhanceScrollEffects() {
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // 导航栏隐藏/显示效果
        if (navbar) {
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                navbar.classList.add('navbar-scrolled');
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.classList.add('navbar-scrolled');
                navbar.style.transform = 'translateY(0)';
            }
            
            if (scrollTop === 0) {
                navbar.classList.remove('navbar-scrolled');
            }
        }
        
        lastScrollTop = scrollTop;
    });
}

// 增强鼠标交互
function enhanceMouseInteractions() {
    // 点击涟漪效果
    document.addEventListener('click', function(e) {
        const target = e.target;
        if (target.classList.contains('btn') || target.closest('.btn')) {
            const btn = target.classList.contains('btn') ? target : target.closest('.btn');
            createRippleEffect(btn, e);
        }
    });
}

function createRippleEffect(btn, e) {
    const ripple = document.createElement('span');
    const rect = btn.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s linear;
    `;
    
    btn.style.position = 'relative';
    btn.style.overflow = 'hidden';
    btn.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// 滚动到顶部按钮
function createScrollToTopButton() {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.className = 'scroll-to-top-btn';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border: none;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        z-index: 1000;
    `;
    
    document.body.appendChild(scrollBtn);
    
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.transform = 'translateY(0)';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.transform = 'translateY(20px)';
        }
    });
}
// 平滑滚动到锚点
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || !document.querySelector(targetId)) return;
            
            e.preventDefault();
            document.querySelector(targetId).scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    });
}


// 初始化所有增强效果
document.addEventListener('DOMContentLoaded', function() {
    enhancePageLoad();
    enhanceScrollEffects();
    enhanceMouseInteractions();
    createScrollToTopButton();
    setupSmoothScroll();
});

