import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/sale/api',
  // 【重要】我们删除了 headers 配置
  // 现在 Axios 可以根据请求体的内容自由地设置 Content-Type
});

export default apiClient;