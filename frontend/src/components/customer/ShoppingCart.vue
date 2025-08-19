<template>
  <div class="shopping-cart">
    <h3 class="cart-title">我的订单</h3>
    
    <div class="cart-list-wrapper">
      <ul v-if="cart.length" class="cart-list">
        <li v-for="item in cart" :key="item.id" class="cart-item">
          <div class="item-info">
            <span class="item-name">{{ item.name }}</span>
            <span class="item-price">¥{{ item.price.toFixed(2) }}</span>
          </div>
          <div class="item-controls">
            <button class="control-btn" @click="$emit('removeFromCart', item.id)">-</button>
            <span class="item-quantity">{{ item.quantity }}</span>
            <button class="control-btn" @click="$emit('addToCart', item)">+</button>
          </div>
        </li>
      </ul>
      <p v-else class="empty-cart">
        <span>🛒</span>
        请点击左侧商品添加到这里
      </p>
    </div>

    <div class="cart-summary">
      <div class="total">
        <span>总计:</span>
        <strong class="total-amount">¥{{ total.toFixed(2) }}</strong>
      </div>
      <button 
        class="btn btn-checkout" 
        :disabled="!cart.length || isCheckingOut" 
        @click="$emit('checkout')"
      >
        {{ isCheckingOut ? '下单中...' : '确认下单' }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  cart: { type: Array, required: true },
  total: { type: Number, required: true },
  isCheckingOut: { type: Boolean, default: false } // 新增 prop，用于禁用按钮
});
defineEmits(['addToCart', 'removeFromCart', 'checkout']);
</script>

<style scoped>
.shopping-cart {
  display: flex;
  flex-direction: column;
  height: 100%; /* 占满父容器 cart-panel 的高度 */
}

.cart-title {
  font-size: 2rem;
  color: var(--accent-color);
  text-align: center;
  margin-top: 0;
  margin-bottom: 2rem;
  flex-shrink: 0; /* 防止标题被压缩 */
}

.cart-list-wrapper {
  flex-grow: 1; /* 占据所有可用垂直空间 */
  overflow-y: auto; /* 当列表过长时，允许独立滚动 */
}

.cart-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
}

.item-info {
  display: flex;
  flex-direction: column;
}

.item-name {
  font-size: 1.2rem;
  font-weight: 600;
}

.item-price {
  font-size: 1rem;
  color: #aaa;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.control-btn {
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--accent-color);
  width: 40px;
  height: 40px;
  border-radius: 50%; /* 圆形按钮 */
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.item-quantity {
  font-size: 1.5rem;
  font-weight: bold;
  min-width: 30px; /* 保证宽度，防止数字变化时布局跳动 */
  text-align: center;
}

.empty-cart {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #888;
  font-size: 1.2rem;
}
.empty-cart span {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.cart-summary {
  flex-shrink: 0; /* 防止总结部分被压缩 */
  margin-top: auto; /* 将其推到底部 */
  padding-top: 2rem;
  border-top: 2px solid var(--border-color);
}

.total {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.total-amount {
  font-size: 2.2rem;
  font-weight: bold;
  color: var(--accent-color);
}

.btn-checkout {
  width: 100%;
  padding: 1.2rem;
  font-size: 1.5rem;
  font-weight: bold;
  background-color: var(--accent-color);
  color: var(--bg-color);
}

.btn-checkout:disabled {
  background-color: #555;
  border-color: #555;
  color: #888;
  cursor: not-allowed;
}
</style>