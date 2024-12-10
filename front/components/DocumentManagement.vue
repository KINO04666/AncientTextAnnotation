<template>
  <div class="document-management">
    <header>
      <span class="document-text" style="font-weight: bold">文档管理：</span>
      <div class="document-actions-buttons">
        <button @click="handleImportDocuments" class="btn import-btn">导入文档</button>
        <button @click="handleExportDocuments" class="btn export-btn">导出文档</button>
        <button @click="handleCreateDocument" class="btn create-btn">创建文档</button>
      </div>
    </header>

    <div class="document-list">
      <div v-for="document in documents" :key="document.doc_id" class="document-item">
        <div class="document-info">
          <h3>{{ document.doc_name }}</h3>
          <p>创建日期: {{ formatDate(document.doc_create) }}</p>
          <p>文档描述: {{ document.doc_descirbe }}</p>
        </div>
        <div class="document-actions">
          <button @click="openDocument(document)" class="btn open-btn">打开文档</button>
          <!-- 其他操作按钮可以在这里添加 -->
        </div>
      </div>
    </div>

    <!-- 文件导入的隐藏输入框 -->
    <input
      type="file"
      ref="fileInput"
      multiple
      @change="importFiles"
      accept=".txt, .docx, .pdf, .xlsx"
      style="display: none"
    />
  </div>
</template>

<script>
export default {
  props: {
    projectId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      documents: [],
    }
  },
  created() {
    this.fetchDocuments()
  },
  methods: {
    // 模拟获取文档数据
    fetchDocuments() {
      // 假设这是从后端获取到的文档数据，根据 projectId 过滤
      this.documents = [
        {
          doc_id: 1,
          user_id: 101,
          project_id: this.projectId,
          doc_name: '文档1',
          doc_content: '这是文档1的内容',
          doc_descirbe: '文档1的描述',
          doc_create: '2024-04-01',
        },
        {
          doc_id: 2,
          user_id: 101,
          project_id: this.projectId,
          doc_name: '文档2',
          doc_content: '这是文档2的内容',
          doc_descirbe: '文档2的描述',
          doc_create: '2024-05-15',
        },
        // 更多文档...
      ]
    },
    // 格式化日期
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    // 打开单个文档
    openDocument(document) {
      // 这里可以通过路由跳转到文档详情页，或者打开一个模态框展示文档内容
      // 目前我们使用 alert 来示范
      alert(`打开文档: ${document.doc_name}\n内容: ${document.doc_content}`)
      // 示例：跳转到文档详情页
      // this.$router.push({ name: 'DocumentDetail', params: { docId: document.doc_id } })
    },
    // 导出所有文档
    handleExportDocuments() {
      // 导出所有文档，具体实现可根据需求调整
      this.documents.forEach((doc) => {
        this.exportDocument(doc)
      })
    },
    // 导出单个文档
    exportDocument(document) {
      let blob
      let fileName = document.doc_name

      // 根据文档类型设置不同的 MIME 类型和扩展名
      // 这里简单处理为txt，如果有需要，可以根据实际类型调整
      blob = new Blob([document.doc_content], { type: 'text/plain;charset=utf-8' })
      fileName += '.txt'

      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = fileName
      link.click()
      URL.revokeObjectURL(link.href)
    },
    // 处理导入文档按钮点击
    handleImportDocuments() {
      this.$refs.fileInput.click()
    },
    // 导入文件
    importFiles(event) {
      const files = event.target.files
      if (files.length === 0) return

      for (let file of files) {
        const reader = new FileReader()
        reader.onload = (e) => {
          const content = e.target.result
          // 根据文件类型处理不同格式
          const docName = file.name
          const docDesc = `导入的文件: ${file.name}`
          // 模拟将文件内容添加到文档列表
          this.documents.push({
            doc_id: this.documents.length + 1,
            user_id: 101, // 假设用户ID为101
            project_id: this.projectId,
            doc_name: docName,
            doc_content: content,
            doc_descirbe: docDesc,
            doc_create: new Date().toISOString().split('T')[0],
          })
        }
        if (file.type === 'text/plain') {
          reader.readAsText(file)
        } else if (
          file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ) {
          reader.readAsBinaryString(file) // 对于docx等格式，可能需要更复杂的解析
        } else {
          // 其他文件类型处理
          reader.readAsDataURL(file)
        }
      }

      // 清空文件输入
      event.target.value = ''
    },
    // 处理创建文档按钮点击
    handleCreateDocument() {
      // 跳转到创建文档页面
      this.$router.push(`/create-document?projectId=${this.projectId}`)
    },
  },
}
</script>

<style scoped>
.document-management {
  padding: 20px;
  background-color: #f9f9f9;
  height: 100%;
  width: 100%;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.document-actions-buttons {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 10px 20px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 不同按钮的颜色 */
.import-btn {
  background-color: #17a2b8;
  color: white;
}

.import-btn:hover {
  background-color: #138496;
}

.export-btn {
  background-color: #ffc107;
  color: white;
}

.export-btn:hover {
  background-color: #e0a800;
}

.create-btn {
  background-color: #28a745;
  color: white;
}

.create-btn:hover {
  background-color: #218838;
}

.document-list {
  margin-top: 20px;
}

.document-item {
  background-color: white;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.document-info h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 5px 0;
}

.document-info p {
  margin: 2px 0;
  font-size: 14px;
}

.document-actions .open-btn {
  padding: 8px 16px;
  font-size: 14px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.document-actions .open-btn:hover {
  background-color: #0056b3;
}
</style>
