import axios from 'axios';

const apiClient = axios.create({
  // baseURL 直接设置为相对路径的 /api 前缀
  // 这会与 vite.config.js 中的代理规则完美匹配
  baseURL: '/sale/api', 
});

export default apiClient;