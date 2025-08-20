<template>
  <div class="list-container">
    <h2>商品列表</h2>
    <div class="search-box">
        <input 
          type="text" 
          v-model="store.searchTerm" 
          placeholder="搜索名称或编号..."
        />
    </div>
    <div v-if="store.isLoading">加载中...</div>
    <div v-else-if="store.error" class="error-message">{{ store.error }}</div>
    <table v-else-if="store.filteredProducts.length" class="product-table">
      <thead>
        <tr>
          <th>图像</th>
          <th>编号</th>
          <th>名称</th>
          <th>默认价格</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in store.filteredProducts" :key="product.id">
          <td>
            <!-- 新增图片预览 -->
            <img v-if="product.image_url" :src="product.image_url" :alt="product.name" class="preview-img">
            <span v-else class="no-img">无图</span>
          </td>
          <td>{{ product.product_code }}</td>
          <td>{{ product.name }}</td>
          <td>¥{{ product.default_price.toFixed(2) }}</td>
          <td>
                <button class="action-btn" @click="$emit('edit', product)">编辑</button>
                <button 
                  class="action-btn" 
                  :class="{ 'btn-success': !product.is_active, 'btn-danger': product.is_active }"
                  @click="$emit('toggleStatus', product)"
                >
                  {{ product.is_active ? '停用' : '启用' }}
                </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="store.searchTerm && !store.filteredProducts.length">
      没有找到匹配 "<strong>{{ store.searchTerm }}</strong>" 的商品。
    </p>
    <p v-else>商品库为空。</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useProductStore } from '@/stores/productStore';
const backendUrl = 'http://127.0.0.1:5000';
const store = useProductStore();
defineEmits(['edit', 'toggleStatus']);

onMounted(() => {
  // 组件加载时重置搜索词，并获取数据
  store.searchTerm = '';
  store.fetchMasterProducts();
});
</script>

<style scoped>
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.list-header h2 {
  margin: 0;
}
.search-box input {
  background-color: var(--card-bg-color);
  border: 1px solid var(--border-color);
  color: var(--primary-text-color);
  padding: 8px 12px;
  border-radius: 4px;
  min-width: 250px;
}

.action-btn {
  background: none;
  border: 1px solid transparent; /* 默认透明边框 */
  color: var(--primary-text-color);
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
  display: inline-flex; /* 让图标和文字对齐 */
  align-items: center;
  gap: 0.4rem; /* 图标和文字的间距 */
  white-space: nowrap; /* 防止文字换行 */
}

.action-btn:hover {
  background-color: var(--card-bg-color);
  border-color: var(--border-color);
}

/* 危险操作按钮的特定样式 */
.action-btn.btn-danger {
  color: var(--error-color);
}

.action-btn.btn-danger:hover {
  background-color: rgba(244, 67, 54, 0.1); /* 淡红色背景 */
  border-color: rgba(244, 67, 54, 0.4);
}
.product-table {
  width: 100%;
  margin-top: 2rem;
  border-collapse: collapse; /* 移除单元格间距 */
  border-spacing: 0;
  text-align: left;
  font-size: 0.95rem;
}

/* 表头样式 */
.product-table th {
  padding: 12px 16px;
  background-color: var(--card-bg-color); /* 使用卡片背景色 */
  color: var(--primary-text-color);
  font-weight: 600;
  border-bottom: 2px solid var(--accent-color); /* 用主题色作为高亮下边框 */
}

/* 数据单元格样式 */
.product-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color); /* 使用柔和的水平分隔线 */
  color: #ccc; /* 数据文字颜色稍暗，以突出标题 */
  vertical-align: middle;
}

/* 表格行的交互效果 */
.product-table tbody tr {
  transition: background-color 0.2s ease-in-out;
}

.product-table tbody tr:hover {
  background-color: rgba(3, 218, 198, 0.05); /* 鼠标悬浮时显示淡淡的主题色背景 */
}

/* --- 特定列的微调 --- */

/* 预览图列 */
.product-table th:first-child,
.product-table td:first-child {
  padding-left: 0;
}

/* 操作列 */
.product-table th:last-child,
.product-table td:last-child {
  text-align: right; /* 让操作按钮靠右对齐 */
  padding-right: 0;
}

.preview-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  vertical-align: middle;
}

.no-img {
  display: inline-block;
  width: 50px;
  height: 50px;
  line-height: 50px;
  text-align: center;
  font-size: 0.8rem;
  color: #888;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  vertical-align: middle;
}
.inactive {
  opacity: 0.5;
  background-color: rgba(100, 100, 100, 0.1);
}
.inactive td {
  text-decoration: line-through; /* 添加删除线 */
}
.btn-success {
  border-color: var(--success-color);
  color: var(--success-color);
}
.btn-success:hover {
  background-color: var(--success-color);
  color: white;
}
</style>