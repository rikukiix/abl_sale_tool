import axios from 'axios';

// 根据环境配置API基础路径
export const getApiBaseUrl = () => {
  // 开发环境：使用相对路径，通过Vite代理转发
  if (import.meta.env.DEV) {
    return '/sale/api';
  }
  
  // 生产环境：可以通过环境变量配置，如果没有则使用默认值
  // 支持通过 VITE_API_BASE_URL 环境变量自定义
  return import.meta.env.VITE_API_BASE_URL || '/sale/api';
};

const apiClient = axios.create({
  baseURL: getApiBaseUrl(),
});

// 添加请求拦截器，用于调试
apiClient.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.log(`🚀 API请求: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器，用于调试
apiClient.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`✅ API响应: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.status);
    }
    return response;
  },
  (error) => {
    if (import.meta.env.DEV) {
      console.error(`❌ API错误: ${error.config?.method?.toUpperCase()} ${error.config?.url}`, error.response?.status, error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient;