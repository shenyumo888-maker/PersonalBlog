// 评论功能AJAX实现 - 增强交互版本
document.addEventListener('DOMContentLoaded', function() {
    initializeCommentSystem();
    
    // 监听页面变化（如Turbolinks等）
    document.addEventListener('page:load', initializeCommentSystem);
    document.addEventListener('turbo:load', initializeCommentSystem);
});

function initializeCommentSystem() {
    initializeCommentForms();
    initializeReplyButtons();
    initializeCommentActions();
    addRealTimeValidation();
    setupAutoSave();
}

function initializeCommentForms() {
    const commentForms = document.querySelectorAll('.comment-form');
    
    commentForms.forEach(form => {
        const textarea = form.querySelector('textarea[name="content"]');
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (!textarea || !submitBtn) return;
        
        // 保存原始状态
        const originalBtnText = submitBtn.innerHTML;
        
        // 输入框聚焦效果
        textarea.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            form.classList.add('active');
            submitBtn.style.transform = 'translateY(-2px)';
            submitBtn.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        });
        
        textarea.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.parentElement.classList.remove('focused');
            }
            form.classList.remove('active');
            submitBtn.style.transform = 'translateY(0)';
            submitBtn.style.boxShadow = '';
        });
        
        // 输入时实时字符计数和验证
        setupCharacterCounter(textarea, submitBtn, form);
        
        // 表单提交
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleCommentSubmit(this, textarea, submitBtn, originalBtnText);
        });
        
        // Ctrl+Enter 快捷提交
        textarea.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                form.dispatchEvent(new Event('submit'));
            }
        });
    });
}

function setupCharacterCounter(textarea, submitBtn, form) {
    let counter = form.querySelector('.char-counter');
    if (!counter) {
        counter = document.createElement('div');
        counter.className = 'char-counter text-muted small mt-2';
        form.querySelector('.mb-3').appendChild(counter);
    }
    
    textarea.addEventListener('input', function() {
        const charCount = this.value.length;
        const maxLength = 1000;
        
        counter.textContent = `${charCount}/${maxLength}`;
        
        if (charCount > maxLength) {
            counter.style.color = '#dc3545';
            submitBtn.disabled = true;
            textarea.style.borderColor = '#dc3545';
        } else if (charCount > maxLength * 0.8) {
            counter.style.color = '#fd7e14';
            submitBtn.disabled = false;
            textarea.style.borderColor = '#fd7e14';
        } else {
            counter.style.color = '#6c757d';
            submitBtn.disabled = false;
            textarea.style.borderColor = '#20c997';
        }

        // 添加输入动画效果
        if (this.value.length > 0) {
            this.classList.add('has-content');
        } else {
            this.classList.remove('has-content');
        }
        
        // 接近最大长度时的视觉警告
        counter = form.querySelector('.char-counter');
        if (counter) {
            if (this.value.length > 800) {
                counter.style.color = '#e74c3c';
                counter.style.transform = 'scale(1.1)';
            } else {
                counter.style.color = '';
                counter.style.transform = 'scale(1)';
            }
        }
        // 动态调整高度
        autoResizeTextarea(textarea);
    });
}

function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}

function handleCommentSubmit(form, textarea, submitBtn, originalBtnText) {
    const content = textarea.value.trim();
    
    if (!content) {
        showToast('请输入评论内容', 'warning');
        textarea.focus();
        return;
    }
    
    if (content.length > 1000) {
        showToast('评论内容过长，请控制在1000字以内', 'warning');
        return;
    }
    
    // 显示加载状态
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> 提交中...';
    form.classList.add('submitting');
    
    const formData = new FormData(form);
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData,
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // 成功提交后清空文本框
            textarea.value = '';
            autoResizeTextarea(textarea);
            
            // 更新字符计数器
            const counter = form.querySelector('.char-counter');
            if (counter) counter.textContent = '0/1000';
            
            // 显示成功消息
            showToast('评论发表成功！', 'success');
            
            // 刷新评论列表
            setTimeout(() => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    // 尝试局部更新评论列表
                    updateCommentsList();
                }
            }, 1000);
            
        } else {
            throw new Error(data.error || '评论提交失败');
        }
    })
    .catch(error => {
        console.error('评论失败:', error);
        showToast('评论发表失败，请重试', 'error');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
        form.classList.remove('submitting');
        
        // 清除自动保存
        clearAutoSave(textarea);
    });
}

function initializeReplyButtons() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.reply-btn')) {
            const replyBtn = e.target.closest('.reply-btn');
            const commentId = replyBtn.dataset.commentId;
            const username = replyBtn.dataset.username;
            
            handleReply(commentId, username, replyBtn);
        }
    });
}

function handleReply(commentId, username, replyBtn) {
    const form = document.querySelector('.comment-form');
    const textarea = form.querySelector('textarea');
    const parentIdInput = form.querySelector('input[name="parent_id"]');
    
    if (!parentIdInput) {
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'parent_id';
        hiddenInput.value = commentId;
        form.appendChild(hiddenInput);
    } else {
        parentIdInput.value = commentId;
    }
    
    // 设置@用户名
    textarea.value = `@${username} `;
    textarea.focus();
    
    // 添加视觉反馈
    const originalComment = document.getElementById(`comment-${commentId}`);
    if (originalComment) {
        originalComment.style.background = 'rgba(32, 201, 151, 0.1)';
        originalComment.style.borderLeft = '4px solid #20c997';
        
        setTimeout(() => {
            originalComment.style.background = '';
            originalComment.style.borderLeft = '';
        }, 2000);
    }
    
    // 滚动到评论表单
    form.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    showToast(`回复 @${username}`, 'info');
}

function initializeCommentActions() {
    // 评论删除确认增强
    document.addEventListener('click', function(e) {
        if (e.target.closest('.comment-delete-btn')) {
            e.preventDefault();
            const deleteBtn = e.target.closest('.comment-delete-btn');
            showDeleteConfirmation(deleteBtn);
        }
    });
}

function showDeleteConfirmation(deleteBtn) {
    const commentCard = deleteBtn.closest('.comment-card');
    
    // 添加抖动动画
    commentCard.style.animation = 'shake 0.5s ease';
    
    setTimeout(() => {
        commentCard.style.animation = '';
    }, 500);
    
    if (confirm('确定要删除这条评论吗？此操作不可撤销。')) {
        // 添加删除动画
        commentCard.style.transition = 'all 0.3s ease';
        commentCard.style.opacity = '0';
        commentCard.style.transform = 'translateX(-100%)';
        
        setTimeout(() => {
            window.location.href = deleteBtn.href;
        }, 300);
    }
}

function addRealTimeValidation() {
    const textareas = document.querySelectorAll('.comment-form textarea');
    
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            // 简单的关键词高亮（示例）
            const content = this.value;
            if (content.includes('@')) {
                this.style.borderLeft = '3px solid #20c997';
            } else {
                this.style.borderLeft = '';
            }
        });
    });
}

function setupAutoSave() {
    const textareas = document.querySelectorAll('.comment-form textarea');
    
    textareas.forEach(textarea => {
        let autoSaveTimer;
        
        textarea.addEventListener('input', function() {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(() => {
                localStorage.setItem('comment_draft', this.value);
            }, 1000);
        });
        
        // 恢复草稿
        const draft = localStorage.getItem('comment_draft');
        if (draft && !textarea.value) {
            if (confirm('检测到未提交的评论草稿，是否恢复？')) {
                textarea.value = draft;
                autoResizeTextarea(textarea);
            }
        }
    });
}

function clearAutoSave(textarea) {
    localStorage.removeItem('comment_draft');
}

function updateCommentsList() {
    const commentsContainer = document.getElementById('comments-list');
    if (commentsContainer) {
        // 简单的重新加载策略
        location.reload();
    }
}

function showToast(message, type = 'info') {
    const existingToast = document.querySelector('.custom-toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = `custom-toast alert alert-${type} alert-dismissible fade show`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1050;
        min-width: 250px;
        animation: slideInRight 0.3s ease;
    `;
    
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: '💡'
    };
    
    toast.innerHTML = `
        ${icons[type] || ''} ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 3000);
}

// 添加必要的CSS动画
if (!document.querySelector('#comment-animations')) {
    const style = document.createElement('style');
    style.id = 'comment-animations';
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .comment-form.active {
            border-color: #20c997;
            box-shadow: 0 0 0 0.2rem rgba(32, 201, 151, 0.25);
        }
        
        .comment-form.submitting {
            opacity: 0.7;
            pointer-events: none;
        }
        
        .spinner {
            display: inline-block;
            width: 1rem;
            height: 1rem;
            border: 2px solid transparent;
            border-top: 2px solid currentColor;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .char-counter {
            font-size: 0.875rem;
            text-align: right;
        }
    `;
    document.head.appendChild(style);
}


// 增强页面加载动画
function enhancePageLoad() {
    // 添加页面加载动画
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
        
        // 添加卡片入场动画
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = `all 0.6s ease ${index * 0.1}s`;
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        });
    }, 100);
}

// 增强滚动效果
function enhanceScrollEffects() {
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // 导航栏隐藏/显示效果
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
        }
        
        lastScrollTop = scrollTop;
        
        // 视差滚动效果
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                const speed = card.dataset.speed || 0.1;
                const yPos = -(rect.top * speed);
                card.style.transform = `translateY(${yPos}px)`;
            }
        });
    });
}

// 增强鼠标交互
function enhanceMouseInteractions() {
    // 鼠标跟随效果
    document.addEventListener('mousemove', function(e) {
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
}

// 初始化所有增强效果
document.addEventListener('DOMContentLoaded', function() {
    enhancePageLoad();
    enhanceScrollEffects();
    enhanceMouseInteractions();
});

// 增强评论表单交互
function enhanceCommentForms() {
    const commentForms = document.querySelectorAll('.comment-form');
    
    commentForms.forEach(form => {
        const textarea = form.querySelector('textarea');
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (textarea && submitBtn) {
            // 添加输入动画效果
            textarea.addEventListener('focus', function() {
                this.parentElement.style.transform = 'translateY(-2px)';
                this.parentElement.style.transition = 'all 0.3s ease';
            });
            
            textarea.addEventListener('blur', function() {
                this.parentElement.style.transform = 'translateY(0)';
            });
        }
    });
}

// 初始化增强效果
document.addEventListener('DOMContentLoaded', function() {
    enhanceCommentForms();
});