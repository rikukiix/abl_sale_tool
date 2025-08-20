import axios from 'axios';

const apiClient = axios.create({
  // 这是一个相对路径。浏览器会自动在它前面加上当前的域名
  // e.g., http://your_domain_or_ip/sale/api
  baseURL: '/sale/api',
});

export default apiClient;