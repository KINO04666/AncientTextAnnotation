import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000//',
  // 创建 axios 实例', // 设置基础 URL
  timeout: 100000, // 设置请求超时时间（可选）
})

// 导出实例
export default api
