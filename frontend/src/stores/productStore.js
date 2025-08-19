import { defineStore } from 'pinia';
import api from '@/services/api';
import { ref, computed } from 'vue';
export const useProductStore = defineStore('masterProduct', () => {
  // --- State ---
  const masterProducts = ref([]);
  const isLoading = ref(false);
  const error = ref(null);
  const searchTerm = ref('');
  const showInactive = ref(false);
  
  const filteredProducts = computed(() => {
    // 如果搜索词为空，直接返回原始列表
    if (!searchTerm.value.trim()) {
      return masterProducts.value;
    }
    
    // 将搜索词转为小写，以便进行不区分大小写的匹配
    const lowerCaseSearchTerm = searchTerm.value.toLowerCase();
    
    // 使用 Array.prototype.filter 方法
    return masterProducts.value.filter(product => {
      // 检查商品名称是否包含搜索词
      const nameMatch = product.name.toLowerCase().includes(lowerCaseSearchTerm);
      // 检查商品编号是否包含搜索词
      const codeMatch = product.product_code.toLowerCase().includes(lowerCaseSearchTerm);
      
      // 如果名称或编号任一匹配，则返回 true
      return nameMatch || codeMatch;
    });
  });
  // --- Actions ---
  async function fetchMasterProducts() {
    isLoading.value = true;
    error.value = null;
    try {
      const params = showInactive.value ? { all: true } : {};
      const response = await api.get('/master-products', { params });
      masterProducts.value = response.data;
    } catch (err) {
      error.value = '无法加载商品库列表。';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  }
  async function createMasterProduct(productData, imageFile) {
    const formData = new FormData();
    // 将所有文本字段添加到 FormData
    Object.keys(productData).forEach(key => {
      formData.append(key, productData[key]);
    });
    // 如果有图片文件，也添加进去
    if (imageFile) {
      formData.append('image', imageFile);
    }
    
    try {
      // 发送 FormData 时，Axios 会自动设置正确的 Content-Type
      const response = await api.post('/master-products', formData);
      masterProducts.value.unshift(response.data);
      return response.data;
    } catch (err) { /* ... error handling ... */ }
  }

  async function updateMasterProduct(productData, imageFile) {
    const formData = new FormData();
    const { id, ...dataToUpdate } = productData;
    Object.keys(dataToUpdate).forEach(key => {
      formData.append(key, dataToUpdate[key]);
    });
    if (imageFile) {
      formData.append('image', imageFile);
    }

    try {
      const response = await api.put(`/master-products/${id}`, formData);
      const index = masterProducts.value.findIndex(p => p.id === id);
      if (index !== -1) {
        masterProducts.value[index] = response.data;
      }
      return response.data;
    } catch (err) { /* ... error handling ... */ }
  }
  async function toggleProductStatus(product) {
    try {
      const newStatus = !product.is_active;
      const response = await api.put(`/master-products/${product.id}/status`, { is_active: newStatus });
      // 更新本地数据
      const index = masterProducts.value.findIndex(p => p.id === product.id);
      if (index !== -1) {
        masterProducts.value[index] = response.data;
      }
    } catch (err) {
      console.error(err);
      throw new Error(err.response?.data?.error || '更新商品状态失败。');
    }
  }
  return {
    masterProducts,
    isLoading,
    error,
    searchTerm,
    filteredProducts,
    fetchMasterProducts,
    createMasterProduct,
    updateMasterProduct,
    toggleProductStatus,
    showInactive,
  };
});