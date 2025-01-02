<template>
  <div class="register-container">
    <div class="register-box">
      <h2>注册</h2>
      <p class="footer-text">浙江工商大学古籍标注</p>
      <form @submit.prevent="handleSubmit">
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
        <div class="input-group">
          <label for="confirmPassword">确认密码</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="请确认密码"
            required
          />
        </div>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="login-link">已有账号？<router-link to="/">点击这里登录</router-link></p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
<<<<<<< HEAD

=======
import api from '@/axios/axios'
>>>>>>> dev
export default {
  name: 'RegisterForm',
  setup() {
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const isLoading = ref(false)
    const errorMessage = ref('')
    const router = useRouter()

    const handleSubmit = async () => {
      if (password.value !== confirmPassword.value) {
        errorMessage.value = '密码和确认密码不一致'
        return
      }

      isLoading.value = true
      errorMessage.value = ''

      try {
<<<<<<< HEAD
        const response = await axios.post('http://127.0.0.1:5000/api/add_user', {
=======
        const response = await api.post('/api/add_user', {
>>>>>>> dev
          user_email: email.value,
          user_password: password.value,
        })

        if (response.status === 201 && response.data.message === 'User added!') {
          alert('注册成功！')
          router.push('/')
        } else {
          errorMessage.value = response.data.error || '注册失败，请稍后重试'
        }
      } catch (error) {
        if (error.response && error.response.data) {
          errorMessage.value = error.response.data.error || '服务器错误，请稍后重试'
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
      confirmPassword,
      isLoading,
      errorMessage,
      handleSubmit,
    }
  },
}
</script>

<style scoped>
.register-container {
  width: 100%;
  height: 100vh;
  background: url('@/assets/background.png') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
<<<<<<< HEAD
=======
  position: fixed;
>>>>>>> dev
}

.register-box {
  width: 400px;
  padding: 40px 30px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.register-box:hover {
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

.login-link {
  text-align: center;
  font-size: 14px;
  margin-top: 25px;
  color: #555;
}

.login-link a {
  color: #3f4040;
  text-decoration: none;
  font-weight: bold;
}

.login-link a:hover {
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
  margin-bottom: 15px;
}
</style>
