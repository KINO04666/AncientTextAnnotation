<template>
  <div class="register-container">
      <div class="register-box">
        <h2>注册</h2>
        <form @submit.prevent="handleSubmit">
          <div class="input-group">
            <label for="username">用户名</label>
            <input type="text" id="username" v-model="username" placeholder="请输入用户名" />
          </div>
          <div class="input-group">
            <label for="email">邮箱</label>
            <input type="email" id="email" v-model="email" placeholder="请输入邮箱" />
          </div>
          <div class="input-group">
            <label for="password">密码</label>
            <input type="password" id="password" v-model="password" placeholder="请输入密码" />
          </div>
          <div class="input-group">
            <label for="confirmPassword">确认密码</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="请确认密码"
            />
          </div>
          <button type="submit">注册</button>
        </form>

        <!-- 登录页面链接 -->
        <p class="login-link">已有账号？<router-link to="/">点击这里登录</router-link></p>
      </div>
    </div>
</template>


<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'RegisterForm',
  setup() {
    // 定义表单数据
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');

    // 处理表单提交
    const handleSubmit = () => {
      if (password.value !== confirmPassword.value) {
        alert('密码和确认密码不一致');
        return;
      }
      // 进行其他注册逻辑
      console.log('注册信息', { username: username.value, email: email.value, password: password.value });
      // 比如可以发出请求到后端进行注册
    };

    return {
      username,
      email,
      password,
      confirmPassword,
      handleSubmit
    };
  }
});
</script>

<style scoped>
/* 注册框样式 */
.register-box {
  width: 300px;
  padding: 20px;
  margin-left: 400px;
  background: rgba(255, 255, 255, 0.9); /* 半透明背景 */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #36a375;
}
</style>
