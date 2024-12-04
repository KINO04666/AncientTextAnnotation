<template>
  <div class="project-management">
    <header>
      <span class="project-text" style="font-weight: bold">项目管理：</span>
      <button @click="handleCreateProject" class="create-project-button">创建项目</button>
    </header>

    <div class="project-list">
      <div v-for="project in projects" :key="project.id" class="project-item">
        <div class="project-info">
          <h3>{{ project.name }}</h3>
          <p>创建日期: {{ formatDate(project.createdAt) }}</p>
          <p>项目详情: {{ project.details }}</p>
        </div>
        <div class="project-actions">
          <button @click="openProject(project.id)" class="open-project-button">打开项目</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      projects: [],
    }
  },
  created() {
    this.fetchProjects()
  },
  methods: {
    // 模拟获取项目数据
    fetchProjects() {
      // 假设这是从后端获取到的项目数据
      this.projects = [
        {
          id: 1,
          name: '项目A',
          createdAt: '2024-01-01',
          details: '这是一个项目A的描述',
        },
        {
          id: 2,
          name: '项目B',
          createdAt: '2024-02-15',
          details: '这是一个项目B的描述',
        },
        {
          id: 3,
          name: '项目C',
          createdAt: '2024-03-20',
          details: '这是一个项目C的描述',
        },
      ]
    },
    // 格式化日期
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    // 打开项目
    openProject(projectId) {
      alert(`打开项目ID: ${projectId}`)
      // 这里可以通过路由跳转或其他方式打开项目
    },
    // 创建新项目
    handleCreateProject() {
      //alert('创建新项目')
      // 跳转到创建项目页面
      this.$router.push('/create-project')
    },
  },
}
</script>

<style scoped>
.project-management {
  padding: 20px;
  background-color: #f9f9f9;
  height: 100%;
  width: 100%;
}

.create-project-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  float: right;
}

.create-project-button:hover {
  background-color: #218838;
}

.project-list {
  margin-top: 20px;
}

.project-item {
  background-color: white;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.project-info h3 {
  font-size: 18px;
  font-weight: bold;
}

.project-actions .open-project-button {
  padding: 8px 16px;
  font-size: 14px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.project-actions .open-project-button:hover {
  background-color: #0056b3;
}
</style>
