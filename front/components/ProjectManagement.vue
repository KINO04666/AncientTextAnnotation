<template>
  <div class="project-management">
    <header>
      <span class="project-text" style="font-weight: bold">项目管理：</span>
      <button @click="handleCreateProject" class="create-project-button">创建项目</button>
    </header>

    <div class="project-list">
      <div v-for="project in projects" :key="project.project_id" class="project-item">
        <div class="project-info">
          <h3>{{ project.project_name }}</h3>
          <p>创建日期: {{ formatDate(project.project_create) }}</p>
          <p>项目详情: {{ project.project_descirbe }}</p>
        </div>
        <div class="project-actions">
          <button @click="openProject(project.project_id)" class="open-project-button">
            打开项目
          </button>
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
    // 获取项目数据
    fetchProjects() {
      // 示例静态数据，后续可替换为从数据库获取的数据

      this.projects = [
        {
          project_id: '1',
          project_name: '项目A',
          project_create: '2024-01-01',
          project_descirbe: '这是一个项目A的描述',
        },
        {
          project_id: '2',
          project_name: '项目B',
          project_create: '2024-02-15',
          project_descirbe: '这是一个项目B的描述',
        },
        {
          project_id: '3',
          project_name: '项目C',
          project_create: '2024-03-20',
          project_descirbe: '这是一个项目C的描述',
        },
      ]

      // 使用 Axios 从后端 API 获取项目数据
      /*
      axios.get('/api/projects')
        .then(response => {
          this.projects = response.data
        })
        .catch(error => {
          console.error('获取项目数据失败:', error)
        })
      */
    },
    // 格式化日期
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    // 打开项目
    openProject(projectId) {
      // 跳转到文档管理页面，并传递项目ID
      this.$router.push({ name: 'DocumentManagement', params: { projectId } })
    },
    // 创建新项目
    handleCreateProject() {
      // 跳转到创建项目页面
      this.$router.push('/create-project')
    },
  },
}
</script>

<style scoped>
/* 保持不变，或根据需要进行调整 */
.project-management {
  padding: 20px;
  background-color: #f9f9f9;
  height: 100%;
  width: 100%;
}

.create-project-button {
  padding: 10px 20px;
  font-size: 14px;
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
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.project-info h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 5px 0;
}
.project-info p {
  margin: 2px 0;
  font-size: 14px;
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
