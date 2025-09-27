<template>
  <div class="product-grid" :class="`card-size-${props.cardSize}`">
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
  products: { type: Array, required: true },
  cardSize: { type: String, default: 'medium' }
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
  
  gap: 0.8rem; /* 网格间距 */
}

/* --- 商品卡片 --- */
.product-card {
  background-color: var(--card-bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  display: flex;
  flex-direction: column;
}

.image-container {
  width: 100%;
  background-color: var(--bg-color);
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  overflow: hidden;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 等比例缩放并裁剪填满容器 */
  object-position: center;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  border-color: var(--accent-color);
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
  white-space: nowrap;         /* 不换行 */
  overflow: hidden;            /* 超出隐藏 */
  text-overflow: ellipsis;     /* 超出显示省略号 */
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
.product-grid.card-size-small .product-card {
  width: 120px;
  height: 180px;
}
.product-grid.card-size-medium .product-card {
  width: 180px;
  height: 260px;
}
.product-grid.card-size-large .product-card {
  width: 240px;
  height: 340px;
}
.product-grid.card-size-small .image-container {
  height: 126px;
}
.product-grid.card-size-medium .image-container {
  height: 182px;
}
.product-grid.card-size-large .image-container {
  height: 272px;
}
.product-grid.card-size-small {
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
}
.product-grid.card-size-medium {
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
}
.product-grid.card-size-large {
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
}

.product-grid.card-size-small .product-name {
  font-size: 0.65rem;
}
.product-grid.card-size-medium .product-name {
  font-size: 0.8rem;
}
.product-grid.card-size-large .product-name {
  font-size: 1rem;
}

.product-grid.card-size-small .product-price {
  font-size: 0.75rem;
}
.product-grid.card-size-medium .product-price {
  font-size: 1.05rem;
}
.product-grid.card-size-large .product-price {
  font-size: 1.25rem;
}
</style>