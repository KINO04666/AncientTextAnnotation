<template>
  <div class="create-project-container">
    <div class="create-project">
      <h2>创建新项目</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="projectName">项目名称</label>
          <input
            v-model="projectName"
            type="text"
            id="projectName"
            placeholder="请输入项目名称"
            required
          />
        </div>

        <div class="form-group">
          <label for="projectDescription">项目描述</label>
          <textarea
            v-model="projectDescription"
            id="projectDescription"
            placeholder="请输入项目描述（可选）"
          ></textarea>
        </div>

        <div class="buttons">
          <button type="button" @click="goBack" class="back-button">返回</button>
          <button type="submit" class="submit-button">新建项目</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'
import api from '@/axios/axios'
export default {
  data() {
    return {
      projectName: '',
      projectDescription: '',
      //userId: localStorage.getItem('userId'), // 假设你已经从登录状态中获取了用户 ID
    }
  },
  methods: {
    // 返回按钮
    goBack() {
      this.$router.push('/project-management') // 返回项目管理页面
    },

    // 提交表单
    // 发送数据到后端创建项目
    async handleSubmit() {
      //console.log(Cookies.get('userId'))
      try {
        const response = await api.post(`/api/createProject`, {
          user_id: Cookies.get('userId'),
          project_name: this.projectName,
          project_describe: this.projectDescription,
        })
        // 如果创建成功，获取返回的 project_id，并跳转到项目管理页面
        if (response.status === 201) {
          //const projectId = response.data.project_id // 获取新创建的 project_id
          alert('项目创建成功')
          this.$router.push(`/project-management`) // 跳转到项目管理页面
        }
      } catch (error) {
        console.error('创建项目失败', error)
        alert('创建项目失败，请稍后再试')
      }
    },
  },
}
</script>

<style scoped>
/* 整个页面容器 */
.create-project-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 100%; /* 使用整个视口高度 */
  width: 100%;
  background-color: #f9f9f9;
}

/* 表单容器 */
.create-project {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px; /* 限制最大宽度 */
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-size: 16px;
  margin-bottom: 5px;
  display: block;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-top: 5px;
}

textarea {
  height: 100px;
}

.buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.back-button,
.submit-button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.back-button {
  background-color: #6c757d;
  color: white;
}

.submit-button {
  background-color: #28a745;
  color: white;
}

.back-button:hover {
  background-color: #5a6268;
}

.submit-button:hover {
  background-color: #218838;
}
</style>
