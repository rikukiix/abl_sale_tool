<template>
  <div class="customer-view">
    <div class="product-panel">
      <ProductGrid 
        v-if="!store.isLoading"
        :products="store.products" 
        @add-to-cart="store.addToCart"
      />
      <div v-else>正在加载商品...</div>
      <div v-if="store.error">{{ store.error }}</div>
    </div>
    
    <div class="cart-panel">
      <ShoppingCart 
        :cart="store.cart"
        :total="store.cartTotal"
        :is-checking-out="isCheckingOut"
        @add-to-cart="store.addToCart"
        @remove-from-cart="store.removeFromCart"
        @checkout="handleCheckout"
      />
    </div>

    <PaymentModal 
      :show="showPaymentModal" 
      :total="orderTotal"
      @close="closePaymentModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useCustomerStore } from '@/stores/customerStore';
import { socket } from '@/services/socketService';
import ProductGrid from '@/components/customer/ProductGrid.vue';
import ShoppingCart from '@/components/customer/ShoppingCart.vue';
import PaymentModal from '@/components/customer/PaymentModal.vue';

// 【核心改动】通过 props 接收来自路由的展会 ID
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const store = useCustomerStore();
const showPaymentModal = ref(false);
const orderTotal = ref(0);
const isCheckingOut = ref(false); 

async function handleCheckout() {
  if (isCheckingOut.value) return; // 防止重复提交

  isCheckingOut.value = true;
  try {
    const newOrder = await store.submitOrder();
    if (newOrder) {
      orderTotal.value = store.cartTotal;
      showPaymentModal.value = true;
      store.clearCart();
    }
  } catch (error) {
    alert(error.message);
  } finally {
    isCheckingOut.value = false; // 无论成功失败，都解除禁用
  }
}
function closePaymentModal() {
  showPaymentModal.value = false;
}

onMounted(() => {
  store.setupStoreForEvent(props.id);;
});

</script>

<style scoped>
.customer-view {
  display: flex;
  height: 100vh;
  background-color: var(--bg-color); /* 确保背景色统一 */
}

.product-panel {
  flex: 3; /* 占据约 3/4 宽度 */
  padding: 2rem;
  overflow-y: auto; /* 当商品过多时，允许此区域独立滚动 */
}

.cart-panel {
  flex: 1; /* 占据约 1/4 宽度 */
  padding: 2rem;
  background-color: var(--card-bg-color);
  border-left: 1px solid var(--border-color);
  display: flex; /* 让购物车内容能更好地布局 */
  flex-direction: column;
  height: 100vh; /* 确保侧边栏与视口等高 */
  box-sizing: border-box; /* 防止 padding 导致溢出 */
}
</style>