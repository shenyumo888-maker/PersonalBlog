// 等待页面加载完成
document.addEventListener('DOMContentLoaded', function() {
  // 获取所有点赞表单
  const likeForms = document.querySelectorAll('.like-form');
  
  likeForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault(); // 阻止表单默认提交行为
      
      const slug = this.querySelector('input[name="slug"]').value;
      const csrfToken = this.querySelector('input[name="csrfmiddlewaretoken"]').value;
      const likeBtn = this.querySelector('.like-btn');
      const likeCountEl = this.parentElement.querySelector('.like-count');
      
      // 发送AJAX请求
      fetch(this.action, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken
        },
        body: new URLSearchParams({
          'slug': slug
        })
      })
      .then(response => response.json())
      .then(data => {
        // 更新点赞按钮文本和样式
        if (data.liked) {
          likeBtn.textContent = '取消点赞';
          likeBtn.style.background = '#dc3545';
        } else {
          likeBtn.textContent = '点赞';
          likeBtn.style.background = '#0d6efd';
        }
        
        // 更新点赞数量显示
        likeCountEl.textContent = `点赞数：${data.count}`;
      })
      .catch(error => {
        console.error('点赞失败:', error);
        // 失败时可以刷新页面使用传统方式更新
        window.location.reload();
      });
    });
  });
});