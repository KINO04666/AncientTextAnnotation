<template>
  <div class="main-page">
    <!-- 主体内容 -->
    <main class="content">
      <!-- 正中央的按钮 -->
      <div class="center-button">
        <button @click="handleProjectManagement" class="project-button">项目管理</button>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    handleProjectManagement() {
      this.$router.push('/project-management') // 跳转到项目管理页面
    },
    handleLogout() {
      alert('您已退出')
      // 清除 Token 或跳转到登录页面
      this.$router.push('/login')
    },
  },
}
</script>

<style scoped>
/* 页面整体样式 */
.main-page {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column; /* 垂直排列 */
}
.project-button {
  margin-top: 10px;
  padding: 8px 20px;
  font-size: 16px;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.project-button:hover {
  background-color: #0056b3;
}

/* 主体内容样式 */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center; /* 水平居中 */
  position: relative; /* 为绝对定位按钮提供父容器 */
}
</style>
