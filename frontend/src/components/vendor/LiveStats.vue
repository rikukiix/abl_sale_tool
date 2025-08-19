<template>
  <div class="stats-container">
    <h3>实时销售统计</h3>
    
    <div class="stats-summary">
      <div class="stat-card">
        <span class="label">当前营业额</span>
        <span class="value revenue">¥{{ orderStore.totalRevenue.toFixed(2) }}</span>
      </div>
      <div class="stat-card">
        <span class="label">待处理订单</span>
        <span class="value">{{ orderStore.pendingOrders.length }}</span>
      </div>
    </div>

    <h4>库存速览</h4>
    <div v-if="eventDetailStore.isLoading" class="loading">加载库存中...</div>
    <div v-else class="stock-list">
      <div 
        v-for="product in eventDetailStore.products" 
        :key="product.id"
        class="stock-item"
      >
        <span class="product-name">{{ product.name }}</span>
        <div class="stock-bar-wrapper">
          <div class="stock-bar" :style="{ width: stockPercentage(product) + '%' }"></div>
        </div>
        <span class="stock-value">
          {{ product.current_stock }} / {{ product.initial_stock }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useOrderStore } from '@/stores/orderStore';
// 【重要】我们也需要 eventDetailStore 来获取商品列表和它们的 current_stock
import { useEventDetailStore } from '@/stores/eventDetailStore'; 

const orderStore = useOrderStore();
const eventDetailStore = useEventDetailStore();

function stockPercentage(product) {
  if (product.initial_stock === 0) return 0;
  return (product.current_stock / product.initial_stock) * 100;
}
</script>

<style scoped>
.stats-container {
  background-color: var(--card-bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}
.stats-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.stat-card {
  background-color: var(--bg-color);
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
}
.stat-card .label {
  display: block;
  font-size: 0.9rem;
  color: #aaa;
  margin-bottom: 0.5rem;
}
.stat-card .value {
  display: block;
  font-size: 1.8rem;
  font-weight: bold;
}
.stat-card .revenue {
  color: var(--accent-color);
}
h4 {
  margin-top: 2rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
}
.stock-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.stock-item {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  align-items: center;
  gap: 1rem;
}
.product-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.stock-bar-wrapper {
  background-color: var(--bg-color);
  border-radius: 4px;
  height: 10px;
  overflow: hidden;
}
.stock-bar {
  background-color: var(--accent-color);
  height: 100%;
  transition: width 0.5s ease;
}
.stock-value {
  text-align: right;
  font-family: monospace;
}
</style>