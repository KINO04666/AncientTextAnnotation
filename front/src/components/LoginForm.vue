<template>
  <div class="login-container">
    <div class="background">
      <div class="login-box">
        <h2>登录</h2>
        <form @submit.prevent="handleSubmit">
          <div class="input-group">
            <label for="username">账号</label>
            <input type="text" id="username" v-model="username" placeholder="请输入账号" />
          </div>
          <div class="input-group">
            <label for="password">密码</label>
            <input type="password" id="password" v-model="password" placeholder="请输入密码" />
          </div>
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
        </form>
        <p v-if="errorMessage" style="color: red; text-align: center">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      username: '',
      password: '',
      isLoading: false,
      errorMessage: '',
    }
  },
  methods: {
    async handleSubmit() {
      this.isLoading = true
      this.errorMessage = '' // 清空之前的错误信息

      try {
        const response = await axios.post('/login', {
          username: this.username,
          password: this.password,
        })

        if (response.data.success) {
          console.log('登录成功:', response.data)
          localStorage.setItem('token', response.data.token) // 存储 token
          this.$router.push('/page') // 跳转到其他页面
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
  },
}
</script>

<style scoped>
/* 背景样式 */
.background {
  width: 100%;
  height: 100vh;
  background: url('@/assets/background.png') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-box {
  width: 300px;
  padding: 20px;
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

button:disabled {
  background-color: #ccc;
}

p {
  font-size: 14px;
  text-align: center;
}
</style>
