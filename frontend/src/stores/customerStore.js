import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/services/api';
import { socket } from '@/services/socketService';

export const useCustomerStore = defineStore('customer', () => {
  // --- State ---
  const products = ref([]);
  const cart = ref([]);
  const isLoading = ref(false);
  const error = ref(null);
  const activeEventId = ref(null); 

  // --- Actions ---
  function setupStoreForEvent(eventId) {
    if (!eventId) {
      error.value = "未提供展会ID。";
      return;
    }
    activeEventId.value = parseInt(eventId, 10);
    // 获取到 eventId 后立即加载商品
    fetchProductsForEvent();
  }
  function initializeEventFromUrl() {
    
    const urlParams = new URLSearchParams(window.location.search);
    const eventIdFromUrl = urlParams.get('event');
    if (eventIdFromUrl) {
      activeEventId.value = parseInt(eventIdFromUrl, 10);
      fetchProductsForEvent(); // 获取到 eventId 后再加载商品
    } else {
      error.value = "未指定展会ID，无法加载商品。请使用包含 ?event=ID 的链接访问。";
    }
  }
  
  // 获取商品列表 (HTTP)
  async function fetchProductsForEvent() {
    if (!activeEventId.value) return;
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.get(`/events/${activeEventId.value}/products`);
      products.value = response.data;
    } catch (err) {
      error.value = '加载商品失败，请联系摊主。';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  }

  // --- 购物车操作 ---

  function addToCart(product) {
    const existingItem = cart.value.find(item => item.id === product.id);
    if (existingItem) {
      if (existingItem.quantity < product.current_stock) {
        existingItem.quantity++;
      } else {
        alert(`抱歉，"${product.name}" 库存不足！`);
      }
    } else {
      if (product.current_stock > 0) {
        cart.value.push({ ...product, quantity: 1 });
      }
    }
  }

  function removeFromCart(productId) {
    const itemIndex = cart.value.findIndex(item => item.id === productId);
    if (itemIndex !== -1) {
      if (cart.value[itemIndex].quantity > 1) {
        cart.value[itemIndex].quantity--;
      } else {
        cart.value.splice(itemIndex, 1);
      }
    }
  }

  function clearCart() {
    cart.value = [];
  }

  async function submitOrder() {
    if (!activeEventId.value || cart.value.length === 0) return;

    const orderData = {
      items: cart.value.map(item => ({
        product_id: item.id,
        quantity: item.quantity,
      })),
    };

    try {
      // 使用 axios.post 发送 HTTP 请求
      const response = await api.post(`/events/${activeEventId.value}/orders`, orderData);
      // 成功后返回订单数据，让视图可以触发后续操作（如弹窗）
      return response.data;
    } catch (err) {
      console.error("Order submission failed:", err);
      throw new Error(err.response?.data?.error || '下单失败，请重试。');
    }
  }


  // --- Getters ---
  const cartTotal = computed(() => {
    return cart.value.reduce((total, item) => total + item.price * item.quantity, 0);
  });
  
  const cartItemCount = computed(() => {
    return cart.value.reduce((total, item) => total + item.quantity, 0);
  });


  return {
    products,
    cart,
    isLoading,
    error,
    activeEventId,
    fetchProductsForEvent,
    addToCart,
    removeFromCart,
    clearCart,
    submitOrder,
    cartTotal,
    cartItemCount,
    initializeEventFromUrl,
    setupStoreForEvent,
  };
});
