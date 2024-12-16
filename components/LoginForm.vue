<template>
  <div class="login-container">
    <div class="login-box">
      <h2>登录</h2>
      <!-- 添加浙江工商大学古籍标注的文本 -->
      <p class="footer-text">浙江工商大学古籍标注</p>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="email">邮箱</label>
          <input type="email" id="email" v-model="email" placeholder="请输入邮箱" />
        </div>
        <div class="input-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" placeholder="请输入密码" />
        </div>
        <button type="submit" :disabled="isLoading">{{ isLoading ? '登录中...' : '登录' }}</button>
      </form>

      <!-- 注册页面链接 -->
      <p class="register-link">还没有账号？<router-link to="/register">点击这里注册</router-link></p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';  // 导入 useRouter
import axios from 'axios';

export default {
  name: 'LoginForm',
  setup() {
    // 定义表单数据
    const email = ref('');
    const password = ref('');
    const isLoading = ref(false);  // 用于处理加载状态
    const errorMessage = ref('');  // 用于显示错误消息

    // 获取 router 实例
    const router = useRouter();

    // 处理登录请求
    const handleLogin = async () => {
      isLoading.value = true;
      errorMessage.value = ''; // 清空之前的错误信息

      try {
        // 发送登录请求到后端
        const response = await axios.post('/api/login', {
          user_email: email.value,  // 将邮箱作为 user_email 发送
          user_password: password.value,  // 密码作为 user_password 发送
        });

        // 处理成功的响应
        if (response.data.message === 'Login successful!') {
          // 登录成功，跳转到主页
          alert('登录成功！');
          router.push('/home');  // 路由跳转到主页（可以根据实际情况调整路由）
        } else {
          // 如果后端返回了错误信息
          errorMessage.value = response.data.error || '登录失败，请稍后重试';
        }
      } catch (error) {
        console.error('请求失败:', error);
        errorMessage.value = '请求失败，请稍后重试';
      } finally {
        isLoading.value = false;
      }
    };

    return {
      email,
      password,
      isLoading,
      errorMessage,
      handleLogin,
    };
  },
};
</script>

<style scoped>
/* 背景样式 */
.login-container {
  width: 100%;
  height: 100vh;
  background: url('@/assets/background.png') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 登录框样式 */
.login-box {
  width: 400px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.9); /* 半透明背景 */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 标题样式 */
h2 {
  margin-bottom: -10px;
  text-align: center;
  font-size: 32px;  /* 和注册页面一致的字体大小 */
  font-weight: bold;  /* 加粗 */
  color: #575555;
}

/* 输入框样式 */
.input-group {
  margin-bottom: 5px; /* 增加输入框之间的间距 */
}

input {
  width: 80%;
  padding: 10px;
  margin-top: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  margin-bottom: 20px;
}

/* 按钮样式 */
button {
  width: 100%;
  padding: 12px;
  background-color: #3f4040;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 18px;
  cursor: pointer;
  margin-top: 20px;
}

button:hover {
  background-color: #5e6663;
}

button:disabled {
  background-color: #ccc;
}

/* 注册链接样式 */
.register-link {
  text-align: center;
  font-size: 14px;
  margin-top: 20px;
}

/* 添加的 footer-text 样式 */
.footer-text {
  font-size: 12px;
  color: #aaa;
  text-align: center;
  margin-top: 20px;
}

label {
  margin-right: 15px;
}
</style>
