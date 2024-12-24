<template>
  <div class="login-container">
    <div class="login-box">
      <h2>登录</h2>
      <p class="footer-text">浙江工商大学古籍标注</p>

      <!-- 登录表单显示的条件 -->
      <form @submit.prevent="handleLogin" v-if="!isLoggedIn">
        <div class="input-group">
          <label for="email">邮箱</label>
          <input type="email" id="email" v-model="email" placeholder="请输入邮箱" required />
        </div>
        <div class="input-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="请输入密码"
            required
          />
        </div>
        <button type="submit" :disabled="isLoading || !email || !password">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>

      <!-- 自动登录提示和按钮 -->
      <p v-if="isLoggedIn" class="success-message">
        您已自动登录，正在跳转...
        <br />
        <button v-if="!redirecting" @click="redirectToProjectManagement">立即跳转</button>
      </p>

      <p class="register-link" v-if="!isLoggedIn">
        还没有账号？<router-link to="/register">点击这里注册</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Cookies from 'js-cookie'
import api from '@/axios/axios'
export default {
  name: 'LoginForm',
  setup() {
    const email = ref('')
    const password = ref('')
    const isLoading = ref(false)
    const errorMessage = ref('')
    const isLoggedIn = ref(false) // 是否已自动登录
    const redirecting = ref(false) // 用来控制是否显示自动跳转倒计时
    const router = useRouter()

    // 自动登录逻辑
    const handleAutoLogin = () => {
      const userId = Cookies.get('userId')
      if (userId) {
        isLoggedIn.value = true
        redirecting.value = false // 初始状态为不显示 "立即跳转"

        // 在 3 秒钟后自动跳转
        setTimeout(() => {
          if (redirecting.value != true) {
            redirecting.value = true // 3秒后开始跳转，显示倒计时和按钮
            router.push({ name: 'ProjectManagement' })
          }
        }, 3000)
      }
    }
    // 手动跳转
    const redirectToProjectManagement = () => {
      redirecting.value = true
      router.push({ name: 'ProjectManagement' })
    }

    // 检查自动登录
    onMounted(() => {
      handleAutoLogin()
    })

    const handleLogin = async () => {
      isLoading.value = true
      errorMessage.value = ''

      try {
        const response = await api.post('/api/userLogin', {
          user_email: email.value,
          user_password: password.value,
        })

        if (response.status === 200 && response.data.success) {
          const userId = response.data.user_id
          //userId已使用jwt验证
          // 使用 Cookies 设置 userId
          Cookies.set('userId', userId, { expires: 1, secure: true, sameSite: 'Lax' }) // 10分钟 = 1/144 天
          alert('登录成功！')
          router.push({ name: 'ProjectManagement' })
        } else {
          errorMessage.value = response.data.message || '登录失败，请稍后重试'
        }
      } catch (error) {
        if (error.response && error.response.data) {
          errorMessage.value = error.response.data.message || '服务器错误，请稍后重试'
        } else {
          errorMessage.value = '网络错误，请检查您的网络连接'
        }
      } finally {
        isLoading.value = false
      }
    }

    return {
      email,
      password,
      isLoading,
      errorMessage,
      isLoggedIn,
      redirecting,
      handleLogin,
      redirectToProjectManagement,
    }
  },
}
</script>

<style scoped>
/* 保持之前的样式 */
.login-container {
  width: 100%;
  height: 100vh;
  background: url('@/assets/background.png') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;

  position: fixed;
}

.login-box {
  width: 400px;
  padding: 40px 30px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.login-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
}

h2 {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 8px;
  font-size: 14px;
  color: #555;
}

input {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  transition:
    border-color 0.3s ease,
    box-shadow 0.3s ease;
}

input:focus {
  border-color: #3f4040;
  box-shadow: 0 0 5px rgba(63, 64, 64, 0.3);
  outline: none;
}

button {
  width: 100%;
  padding: 14px;
  background-color: #3f4040;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 18px;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
}

button:hover {
  background-color: #5e6663;
  transform: scale(1.02);
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  font-size: 14px;
  margin-top: 25px;
  color: #555;
}

.register-link a {
  color: #3f4040;
  text-decoration: none;
  font-weight: bold;
}

.register-link a:hover {
  text-decoration: underline;
}

.footer-text {
  font-size: 12px;
  color: #aaa;
  text-align: center;
  margin-top: 25px;
}

.error-message {
  color: #e74c3c;
  text-align: center;
  font-size: 14px;
  margin-top: 15px;
}

.success-message {
  text-align: center;
  color: #2ecc71;
  font-size: 16px;
  margin-top: 15px;
}

.success-message button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #3f4040;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.success-message button:hover {
  background-color: #5e6663;
}
</style>
