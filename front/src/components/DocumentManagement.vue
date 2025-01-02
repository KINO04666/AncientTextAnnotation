<template>
  <div class="document-management">
    <header>
      <span class="document-text" style="font-weight: bold">文档管理：</span>
      <div class="document-actions-buttons">
        <button @click="handleImportDocuments" class="btn import-btn">导入文档</button>
        <!--<button @click="handleExportDocuments" class="btn export-btn">导出文档</button>-->
        <button @click="handleCreateDocument" class="btn create-btn">创建文档</button>
      </div>
    </header>

    <div class="document-list">
      <div v-for="document in documents" :key="document.doc_id" class="document-item">
        <div class="document-info">
          <h3>{{ document.doc_name }}</h3>
          <p>创建日期: {{ formatDate(document.doc_create) }}</p>
          <p>文档描述: {{ document.doc_describe }}</p>
        </div>
        <div class="document-actions">
          <button @click="openDocument(document)" class="btn open-btn">打开文档</button>
          <!-- 其他操作按钮可以在这里添加 -->
          <button @click="deleteDocument(document)" class="btn delete-btn">删除文档</button>
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
<<<<<<< HEAD
      accept=".txt, .docx, .pdf,.xlsx"
=======
      accept=".txt, .docx, .pdf,.xlsx,.json"
>>>>>>> dev
      style="display: none"
    />
  </div>
</template>

<script>
import axios from 'axios'
<<<<<<< HEAD
=======
import api from '@/axios/axios'
>>>>>>> dev
import mammoth from 'mammoth'
import Cookies from 'js-cookie'
import * as XLSX from 'xlsx' // 导入 SheetJS
import * as pdfjsLib from 'pdfjs-dist'
pdfjsLib.GlobalWorkerOptions.workerSrc =
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js'

export default {
  props: {
    projectId: {
      type: String,
      required: true,
    },
    userId: {
      // 添加 userId 作为 prop，确保每个文档关联到用户
      type: Number,
      required: false,
    },
  },
  data() {
    return {
      documents: [],
      user_id: Cookies.get('userId'),
    }
  },
  created() {
    this.fetchDocuments()
  },
  methods: {
    // 获取文档数据
    fetchDocuments() {
      //console.log('User ID:', this.user_id)
      //   this.documents = [
      //     {
      //       doc_id: 1,
      //       user_id: 101,
      //       project_id: this.projectId,
      //       doc_name: '文档1',
      //       doc_content: '这是文档1的内容',
      //       doc_descirbe: '文档1的描述',
      //       doc_create: '2024-04-01',
      //     },
      //     {
      //       doc_id: 2,
      //       user_id: 101,
      //       project_id: this.projectId,
      //       doc_name: '文档2',
      //       doc_content: '这是文档2的内容',
      //       doc_descirbe: '文档2的描述',
      //       doc_create: '2024-05-15',
      //     },
      //   ]
      // 使用 Axios 从后端 API 获取文档数据，根据 projectId 过滤

<<<<<<< HEAD
      axios
        .get(`http://127.0.0.1:5000/projects/${this.projectId}/documents`)
=======
      api
        .get(`/projects/${this.projectId}/documents`, {
          headers: {
            Authorization: `Bearer ${this.user_id}`,
          },
        })
>>>>>>> dev
        .then((response) => {
          this.documents = response.data
        })
        .catch((error) => {
          console.error('获取文档数据失败:', error)
<<<<<<< HEAD
=======
          alert('此项目不是你的项目！')
          this.$router.push('/project-management')
>>>>>>> dev
        })

      // 如果使用代理，则可以简化为：
      /*
      axios.get(`/api/projects/${this.projectId}/documents`)
        .then(response => {
          this.documents = response.data
        })
        .catch(error => {
          console.error('获取文档数据失败:', error)
        })
      */
    },
    // 格式化日期
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    // 打开单个文档
    openDocument(document) {
      // 这里可以通过路由跳转到文档详情页，或者打开一个模态框展示文档内容
      // 目前我们使用 alert 来示范
      //alert(`打开文档: ${document.doc_name}\n内容: ${document.doc_content}`)
      // 示例：跳转到文档详情页
      // this.$router.push({ name: 'DocumentDetail', params: { docId: document.doc_id } })
      // 跳转到创建文档页面
<<<<<<< HEAD
      this.$router.push(`/entitytagging?doc_id=${document.doc_id}`)
=======
      this.$router.push(`/struct?doc_id=${document.doc_id}`)
>>>>>>> dev
    },
    deleteDocument(document) {
      const confirmDelete = window.confirm('确定要删除该文档吗？')

      if (confirmDelete) {
        // 发送DELETE请求
<<<<<<< HEAD
        axios
          .delete('http://127.0.0.1:5000/api/deleteDocument', {
=======
        api
          .delete('/api/deleteDocument', {
>>>>>>> dev
            data: { doc_id: document.doc_id }, // 通过data发送JSON数据
          })
          .then((response) => {
            if (response.status === 200) {
              alert('文档已删除')
              this.fetchDocuments() // 删除成功后重新获取文档列表
            }
          })
          .catch((error) => {
            console.error('删除文档失败:', error)
            alert('删除文档失败，请稍后再试')
          })
      }
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
    async importFiles(event) {
      const files = event.target.files
      if (files.length === 0) return

      for (let file of files) {
        try {
          let content = ''

          if (file.type === 'text/plain') {
            content = await this.readFileAsText(file)
          } else if (
            file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
          ) {
            content = await this.convertDocxToText(file)
          } else if (file.type === 'application/pdf') {
            content = await this.convertPdfToText(file)
          } else if (
            file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
          ) {
            content = await this.convertXlsxToText(file)
<<<<<<< HEAD
=======
          } else if (file.type === 'application/json') {
            let content = null
            content = await this.convertJsonToText(file)
            console.log(content)
            const newDocument = {
              user_id: this.user_id, // 使用 data 中的 user_id
              project_id: this.projectId,
              doc_name: content.doc_name,
              text: content.doc_content,
              doc_describe: content.doc_describe,
              entities: content.entities,
              enti: content.enti,
              relations: content.relations,
              relation_types: content.relation_types,
            }
            console.log(newDocument)
            await api.post(`/upload`, newDocument).catch((error) => {
              console.error(`导入文档失败:`, error)
            })
            // 清空文件输入
            event.target.value = ''
            this.fetchDocuments()
            continue
>>>>>>> dev
          } else {
            content = `不支持的文件类型: ${file.type}`
          }

          const docName = file.name
          const docDesc = `导入的文件: ${file.name}`

          // 创建文档对象
          const newDocument = {
            user_id: this.user_id, // 使用 data 中的 user_id
            project_id: this.projectId,
            name: docName,
            content: content,
            describe: docDesc,
          }

          // 发送 POST 请求到后端 API 以保存文档
<<<<<<< HEAD
          await axios
            .post(`http://127.0.0.1:5000/projects/${this.projectId}/documents`, newDocument)
            .then((response) => {
              // 假设后端返回新创建的文档数据
              this.documents.push(response.data)
            })
            .catch((error) => {
              console.error(`导入文档 "${docName}" 失败:`, error)
            })
=======
          await api
            .post(`/projects/${this.projectId}/documents`, newDocument)

            .catch((error) => {
              console.error(`导入文档 "${docName}" 失败:`, error)
            })
          this.fetchDocuments()
>>>>>>> dev
        } catch (error) {
          console.error(`处理文件 "${file.name}" 时出错:`, error)
        }
      }

      // 清空文件输入
      event.target.value = ''
    },
<<<<<<< HEAD
=======

>>>>>>> dev
    // 读取文件为文本
    readFileAsText(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => {
          resolve(e.target.result)
        }
        reader.onerror = (e) => {
          reject(e)
        }
        reader.readAsText(file)
      })
    },
<<<<<<< HEAD
=======
    // 将 .json 文件转换为文本
    convertJsonToText(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = async (e) => {
          try {
            const jsonString = e.target.result // 读取文件的内容
            const jsonObject = JSON.parse(jsonString) // 将 JSON 字符串解析为对象

            resolve(jsonObject) // 返回格式化的 JSON 字符串
          } catch (error) {
            reject(error) // 如果解析失败，则抛出错误
          }
        }
        reader.onerror = (e) => {
          reject(e) // 如果读取文件失败，则抛出错误
        }
        reader.readAsText(file) // 将 JSON 文件读取为文本
      })
    },

>>>>>>> dev
    // 将 .docx 文件转换为文本
    convertDocxToText(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => {
          const arrayBuffer = e.target.result
          mammoth
            .extractRawText({ arrayBuffer: arrayBuffer })
            .then((result) => {
              resolve(result.value)
            })
            .catch((err) => {
              reject(err)
            })
        }
        reader.onerror = (e) => {
          reject(e)
        }
        reader.readAsArrayBuffer(file)
      })
    },

    // 将 .xlsx 文件转换为文本
    convertXlsxToText(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => {
          try {
            const data = new Uint8Array(e.target.result)
            const workbook = XLSX.read(data, { type: 'array' })
            let text = ''

            workbook.SheetNames.forEach((sheetName) => {
              const worksheet = workbook.Sheets[sheetName]
              const sheetText = XLSX.utils.sheet_to_csv(worksheet)
              text += sheetText + '\n'
            })

            resolve(text)
          } catch (error) {
            reject(error)
          }
        }
        reader.onerror = (e) => {
          reject(e)
        }
        reader.readAsArrayBuffer(file)
      })
    },

    // 将 .pdf 文件转换为文本
    convertPdfToText(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = async (e) => {
          const arrayBuffer = e.target.result
          try {
            // 使用 pdf.js 加载 PDF 文件
            const pdf = await pdfjsLib.getDocument(arrayBuffer).promise
            let textContent = ''

            // 遍历 PDF 页数并提取每页的文本
            for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
              const page = await pdf.getPage(pageNum)
              const text = await page.getTextContent()
              text.items.forEach((item) => {
                textContent += item.str + ' '
              })
            }

            resolve(textContent)
          } catch (error) {
            reject(error)
          }
        }
        reader.onerror = (e) => {
          reject(e)
        }
        reader.readAsArrayBuffer(file)
      })
    },

    // 读取文件为 ArrayBuffer
    readFileAsArrayBuffer(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => {
          resolve(e.target.result)
        }
        reader.onerror = (e) => {
          reject(e)
        }
        reader.readAsArrayBuffer(file)
      })
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
.delete-btn {
  padding: 8px 16px;
  font-size: 14px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}
.document-actions .open-btn:hover {
  background-color: #0056b3;
}
</style>
