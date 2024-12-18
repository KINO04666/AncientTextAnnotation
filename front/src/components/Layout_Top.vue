<!-- src/components/Layout_Top.vue -->
<template>
  <div class="layout">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="logo">
        <img src="../pictures/logo.png" alt="Logo" class="logo-image" />
        <span class="logo-text">浙江工商大学古籍标注平台</span>
      </div>

      <!-- 右上角的用户信息和退出按钮 -->
      <div class="user-info">
        <button @click="handleLogout" class="logout-button">退出</button>
      </div>
    </header>

    <!-- 主体内容部分，通过 router-view 渲染不同页面 -->
    <main class="content">
      <router-view></router-view>
      <!-- 路由视图：这里显示不同页面的内容 -->
    </main>
  </div>
</template>

<script>
import Cookies from 'js-cookie' // 引入 js-cookie

export default {
  name: 'Layout_Top',
  created() {
    if (!Cookies.get('userId')) {
      alert('未检测到登录信息，请先登录。')
      this.$router.push({ name: 'login' })
    }
  },
  methods: {
    handleLogout() {
      alert('您已退出')
      Cookies.remove('userId') // 移除 userId Cookie
      this.$router.push({ name: 'login' })
    },
  },
}
</script>

<style scoped>
/* 布局的整体样式 */
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f9f9f9;
}

/* 顶部导航栏样式 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f5f5f5;
  padding: 0 20px;
  height: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 3px;
}

.logo {
  display: flex;
  align-items: center;
}

.logo-image {
  height: 40px;
  margin-right: 10px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  margin-right: 20px;
  font-size: 14px;
  color: #555;
}

.logout-button {
  padding: 8px 16px;
  font-size: 14px;
  color: white;
  background-color: #dc3545;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #a71d2a;
}

/* 主体内容样式 */
.content {
  flex: 1;
  display: flex;
  font-size: 24px;
  color: #333;
}
</style>
