<template>
  <div class="product-grid">
    <div 
      v-for="product in products" 
      :key="product.id"
      class="product-card"
      :class="{ 'out-of-stock': product.current_stock === 0 }"
      @click="handleCardClick(product)"
    >
      <div class="image-container">
        <img v-if="product.image_url" :src="product.image_url" :alt="product.name" />
        <div v-else class="no-img-placeholder">
          <span>{{ product.name.charAt(0) }}</span>
        </div>
      </div>
      <div class="product-info">
        <span class="product-name" :title="product.name">{{ product.name }}</span>
        <span class="product-price">¥{{ product.price.toFixed(2) }}</span>
      </div>
      <div v-if="product.current_stock === 0" class="stock-overlay">
        <span>完售</span>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  products: { type: Array, required: true }
});
const emit = defineEmits(['addToCart']);
const backendUrl = 'http://127.0.0.1:5000';

function handleCardClick(product) {
  if (product.current_stock > 0) {
    emit('addToCart', product);
  }
}
</script>

<style scoped>
/* --- 网格布局 --- */
.product-grid {
  display: grid;
  /* 
    - 响应式布局：自动填充，每列最小 140px，最大 1fr (弹性填充)
    - 这将确保在不同尺寸的平板上都能良好显示
  */
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1.5rem; /* 网格间距 */
}

/* --- 商品卡片 --- */
.product-card {
  background-color: var(--card-bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden; /* 防止图片溢出圆角 */
  cursor: pointer;
  position: relative; /* 为完售遮罩定位 */
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  border-color: var(--accent-color);
}

/* --- 图片容器 --- */
.image-container {
  width: 100%;
  /* 关键：使用 aspect-ratio 确保图片容器总是正方形 */
  aspect-ratio: 1 / 1; 
  background-color: var(--bg-color);
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保证图片填满容器且不变形 */
}

.no-img-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 3rem;
  color: var(--accent-color);
  opacity: 0.5;
}

/* --- 商品信息 --- */
.product-info {
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1; /* 填充剩余空间，使所有卡片高度一致 */
}

.product-name {
  font-weight: 600;
  color: var(--primary-text-color);
  /* 防止长名称换行破坏布局 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-grow: 1;
}

.product-price {
  margin-top: 0.25rem;
  color: var(--accent-color);
  font-weight: bold;
}

/* --- 完售状态 --- */
.out-of-stock {
  cursor: not-allowed;
}

.out-of-stock:hover {
  transform: none;
  box-shadow: none;
  border-color: var(--border-color);
}

.stock-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  backdrop-filter: blur(2px);
}
</style>