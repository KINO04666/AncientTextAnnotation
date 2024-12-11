<template>
  <div class="login-container">
    <h2>登录</h2>
    <form @submit.prevent="handleSubmit">
      <div class="input-group">
        <label for="username">账号</label>
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="请输入账号"
        />
      </div>
      <div class="input-group">
        <label for="password">密码</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="请输入密码"
        />
      </div>
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? '登录中...' : '登录' }}
      </button>
    </form>

    <!-- 忘记密码链接 -->
    <div class="forgot-password-container">
      <a href="#" @click="showForgotPassword = true">忘记密码？</a>
    </div>

    <!-- 忘记密码弹窗 -->
    <div v-if="showForgotPassword" class="modal" @click.self="showForgotPassword = false">
      <div class="modal-content">
        <span class="close" @click="showForgotPassword = false">&times;</span>
        <h3>重置密码</h3>
        <form @submit.prevent="handleResetPassword">
          <div class="input-group">
            <label for="reset-email">请输入您的电子邮件地址：</label>
            <input
              type="email"
              id="reset-email"
              v-model="resetEmail"
              placeholder="请输入邮箱地址"
              required
            />
          </div>
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? '发送中...' : '发送重置链接' }}
          </button>
        </form>
      </div>
    </div>

    <!-- 显示错误信息 -->
    <p v-if="errorMessage" style="color: red; text-align: center;">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from '../utils/axios' // 引入 Axios 配置文件

export default {
  data() {
    return {
      username: '',
      password: '',
      isLoading: false,
      errorMessage: '',
      showForgotPassword: false, // 控制是否显示忘记密码弹窗
      resetEmail: '', // 存储重置密码的邮箱地址
    };
  },
  methods: {
    // 登录提交
    async handleSubmit() {
      this.isLoading = true
      this.errorMessage = ''  // 清空之前的错误信息

      try {
        const response = await axios.post('/login', {
          username: this.username,
          password: this.password
        })

        // 假设后端返回的成功响应包含一个 token
        if (response.data.success) {
          console.log('登录成功:', response.data)
          localStorage.setItem('token', response.data.token)  // 存储 token
          // 跳转到其他页面（例如：dashboard）
          this.$router.push('/dashboard')
        } else {
          this.errorMessage = response.data.message || '登录失败，请检查账号和密码'
        }
      } catch (error) {
        console.error('请求失败:', error)
        this.errorMessage = '请求失败，请稍后重试'
      } finally {
        this.isLoading = false
      }
    },

    // 忘记密码提交
    async handleResetPassword() {
      this.isLoading = true
      this.errorMessage = ''  // 清空之前的错误信息

      try {
        const response = await axios.post('/api/auth/reset-password', {
          email: this.resetEmail
        })

        // 假设后端返回成功时提示用户重置链接已发送
        if (response.data.success) {
          alert('重置链接已发送到您的邮箱')
          this.showForgotPassword = false  // 关闭弹窗
        } else {
          this.errorMessage = response.data.message || '发送失败，请稍后重试'
        }
      } catch (error) {
        console.error('请求失败:', error)
        this.errorMessage = '请求失败，请稍后重试'
      } finally {
        this.isLoading = false
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  width: 300px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
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
}

button:hover {
  background-color: #36a375;
}

button:disabled {
  background-color: #ccc;
}

.forgot-password-container {
  text-align: center;
  margin-top: 10px;
}

.forgot-password-container a {
  color: #007bff;
  text-decoration: none;
}

.forgot-password-container a:hover {
  text-decoration: underline;
}

/* 模态框样式 */
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #fff;
  margin: 15% auto;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 400px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

p {
  font-size: 14px;
  text-align: center;
  margin-top: 20px;
}
</style>
