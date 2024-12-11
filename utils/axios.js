import axios from 'axios';

// 创建 Axios 实例
const instance = axios.create({
  baseURL: 'http://your-backend-api.com',  // 替换成你的后端 API 地址
  timeout: 5000,  // 设置请求超时
});

// 请求拦截器（如果需要添加认证 token 等）
instance.interceptors.request.use(
  (config) => {
    // 如果需要认证 token，可以在这里加上
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers['Authorization'] = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 登录请求方法
export const login = (credentials) => {
  return instance.post('/login', credentials); // 假设你的登录接口是 POST /login
};

// 注册请求方法
export const register = (userData) => {
  return instance.post('/register', userData); // 假设你的注册接口是 POST /register
};

export default instance;
