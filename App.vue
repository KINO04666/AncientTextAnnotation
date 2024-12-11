<template>
  <div id="app">
    <router-view> </router-view>
    <!-- 这里将根据路由动态渲染页面组件 -->
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
.background {
  width: 100%;
  height: 100vh;
  background: url('@/assets/background.png') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
