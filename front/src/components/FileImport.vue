<template>
  <div class="file-import">
    <h2>导入文件并显示内容</h2>
    <input type="file" @change="handleFileUpload" accept=".txt, .docx" />
    <button @click="submitFile" :disabled="!selectedFile">上传并转换</button>

    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-if="content" class="content">
      <h3>文件内容:</h3>
      <pre>{{ content }}</pre>
      <button @click="downloadContent">下载为 TXT 文件</button>
    </div>
  </div>
</template>

<script>
import mammoth from 'mammoth'
import { saveAs } from 'file-saver' // 如果安装了 file-saver

export default {
  name: 'FileImport',
  data() {
    return {
      selectedFile: null,
      content: '',
      error: '',
    }
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.selectedFile = file
        this.content = ''
        this.error = ''
      }
    },
    async submitFile() {
      if (!this.selectedFile) return

      const file = this.selectedFile
      const fileExt = file.name.split('.').pop().toLowerCase()

      try {
        if (fileExt === 'txt') {
          this.content = await this.readFileAsText(file)
        } else if (fileExt === 'docx') {
          this.content = await this.convertDocxToText(file)
        } else {
          this.error = '不支持的文件类型'
          return
        }
      } catch (err) {
        console.error(err)
        this.error = '文件处理失败'
        this.content = ''
      }
    },
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
    downloadContent() {
      const blob = new Blob([this.content], { type: 'text/plain;charset=utf-8' })
      saveAs(blob, `${this.selectedFile.name}.txt`)
    },
  },
}
</script>

<style scoped>
.file-import {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
}

input[type='file'] {
  display: block;
  margin: 20px auto;
}

button {
  display: block;
  margin: 0 auto 20px auto;
  padding: 10px 20px;
  font-size: 14px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #218838;
}

.error {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.content {
  margin-top: 20px;
  background-color: #ffffff;
  padding: 15px;
  border-radius: 5px;
  overflow: auto;
}

pre {
  white-space: pre-wrap; /* 保持换行 */
  word-wrap: break-word;
}

.content button {
  margin-top: 10px;
  background-color: #007bff;
}

.content button:hover {
  background-color: #0056b3;
}
</style>
