<template>
  <div class="register-container">
    <div class="background">
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
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    }
  },
  methods: {
    async handleSubmit() {
      if (this.password !== this.confirmPassword) {
        alert('密码和确认密码不一致')
        return
      }

      const userData = {
        username: this.username,
        email: this.email,
        password: this.password,
      }

      try {
        const response = await register(userData)
        console.log('注册成功:', response.data)

        alert('注册成功！')
        this.$router.push('/login') // 跳转到登录页面
      } catch (error) {
        console.error('注册失败:', error)
        alert('注册失败，请检查信息并重试')
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

.register-box {
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
</style>
