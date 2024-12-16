<template>
  <div class="register-container">
    <div class="register-box">
      <h2>注册</h2>
      <!-- 添加浙江工商大学古籍标注的文本 -->
      <p class="footer-text">浙江工商大学古籍标注</p>
      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="username" placeholder="请输入用户名" />
        </div>
        <div class="input-group">
          <label1 for="email">邮箱</label1>
          <input type="email" id="email" v-model="email" placeholder="请输入邮箱" />
        </div>
        <div class="input-group">
          <label2 for="password">密码</label2>
          <input type="password" id="password" v-model="password" placeholder="请输入密码" />
        </div>
        <div class="input-group">
          <label3 for="confirmPassword">确认密码</label3>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="请确认密码"
          />
        </div>
        <button type="submit" :disabled="isLoading">{{ isLoading ? '注册中...' : '注册' }}</button>
      </form>

      <!-- 登录页面链接 -->
      <p class="login-link">已有账号？<router-link to="/">点击这里登录</router-link></p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';  // 导入 useRouter
import axios from 'axios';

export default {
  name: 'RegisterForm',
  setup() {
    // 定义表单数据
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const isLoading = ref(false);  // 用于处理加载状态
    const errorMessage = ref('');  // 用于显示错误消息

    // 获取 router 实例
    const router = useRouter();

    // 处理表单提交
    const handleSubmit = async () => {
      // 检查密码和确认密码是否一致
      if (password.value !== confirmPassword.value) {
        errorMessage.value = '密码和确认密码不一致';
        return;
      }

      isLoading.value = true;
      errorMessage.value = ''; // 清空之前的错误信息

      try {
        // 发送注册请求到后端
        const response = await axios.post('/api/add_user', {
          user_email: email.value,  // 将邮箱作为 user_email 发送
          user_password: password.value,  // 密码作为 user_password 发送
        });

        // 处理成功的响应
        if (response.data.message === 'User added!') {
          // 注册成功，跳转到登录页面
          alert('注册成功！');
          // 路由跳转到登录页面
          router.push('/');  // 使用 router.push 进行跳转
        } else {
          // 如果后端返回了错误信息
          errorMessage.value = response.data.error || '注册失败，请稍后重试';
        }
      } catch (error) {
        console.error('请求失败:', error);
        errorMessage.value = '请求失败，请稍后重试';
      } finally {
        isLoading.value = false;
      }
    };

    return {
      username,
      email,
      password,
      confirmPassword,
      isLoading,
      errorMessage,
      handleSubmit,
    };
  },
};
</script>

<style scoped>
/* 背景样式 */
.register-container {
  width: 100%;
  height: 100vh;
  background: url('@/assets/background.png') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 注册框样式 */
.register-box {
  width: 400px; /* 增加宽度，和登录框保持一致 */
  padding: 30px;
  background: rgba(255, 255, 255, 0.9); /* 半透明背景 */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 标题样式 */
h2 {
  margin-bottom: -10px;
  text-align: center;
  font-size: 32px;  /* 和登录页面一致的字体大小 */
  font-weight: bold;  /* 加粗 */
  color: #575555;
}

/* 输入框样式 */
.input-group {
  margin-bottom: 5px; /* 增加输入框之间的间距 */
}

input {
  width: 70%;
  padding: 10px; /* 增加内边距，增加输入框的高度 */
  margin-top: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px; /* 增大字体 */
  margin-bottom: 20px; /* 增加下边距 */
}

/* 按钮样式 */
button {
  width: 100%;
  padding: 12px; /* 增加按钮的高度 */
  background-color: #3f4040;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 18px; /* 增大按钮的字体 */
  cursor: pointer;
  margin-top: 20px;
}

button:hover {
  background-color: #5e6663; /* 悬停时的颜色 */
}

button:disabled {
  background-color: #ccc; /* 禁用状态 */
}

/* 登录链接样式 */
.login-link {
  text-align: center;
  font-size: 14px;
  margin-top: 20px;
}

/* 添加的 footer-text 样式 */
.footer-text {
  font-size: 12px;
  color: #aaa; /* 浅灰色字体 */
  text-align: center;
  margin-top: 20px;
}

label {
  margin-right: 29px; /* 增加标签的右边距 */
}

label1 {
  margin-right: 45px; /* 增加标签的右边距 */
}

label2 {
  margin-right: 45px; /* 增加标签的右边距 */
}

label3 {
  margin-right: 13px; /* 增加标签的右边距 */
}

</style>
