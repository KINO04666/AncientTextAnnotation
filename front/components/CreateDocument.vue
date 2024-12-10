<template>
  <div class="create-document-container">
    <div class="create-document">
      <h2>创建新文档</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="documentName">文档名称</label>
          <input
            v-model="documentName"
            type="text"
            id="documentName"
            placeholder="请输入文档名称"
            required
          />
        </div>

        <div class="form-group">
          <label for="documentDescription">文档描述</label>
          <textarea
            v-model="documentDescription"
            id="documentDescription"
            placeholder="请输入文档描述（可选）"
          ></textarea>
        </div>

        <div class="buttons">
          <button type="button" @click="goBack" class="back-button">返回</button>
          <button type="submit" class="submit-button">新建文档</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      documentName: '',
      documentDescription: '',
      projectId: this.$route.query.projectId || '',
    }
  },
  methods: {
    // 返回按钮
    goBack() {
      this.$router.push(`/documents/${this.projectId}`) // 返回文档管理页面
    },

    // 提交表单
    async handleSubmit() {
      if (this.documentName.trim() === '') {
        alert('文档名称是必填项')
        return
      }

      // 发送数据到后端
      try {
        const response = await axios.post('/api/documents', {
          name: this.documentName,
          description: this.documentDescription,
        })

        // 如果创建成功，跳转回文档管理页面
        if (response.status === 201) {
          alert('文档创建成功')
          this.$router.push(`/documents/${this.projectId}`) // 跳转到文档管理页面
        }
      } catch (error) {
        console.error('创建文档失败', error)
        alert('创建文档失败，请稍后再试')
      }
    },
  },
}
</script>

<style scoped>
/* 整个页面容器 */
.create-document-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 100%; /* 使用整个视口高度 */
  width: 100%;
  background-color: #f9f9f9;
}

/* 表单容器 */
.create-document {
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
