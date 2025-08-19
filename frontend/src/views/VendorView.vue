<template>
  <div class="vendor-view">
    <header class="page-header">
      <h1>实时订单</h1>
      
      <!-- 【新增】展会选择器 -->
      <div class="event-selector">
        <label for="event-select">当前展会:</label>
        <div class="custom-select-wrapper">
          <select id="event-select" v-model="selectedEventId" @change="onEventChange">
            <option :value="null" disabled>-- 请选择一个进行中的展会 --</option>
            <option v-for="event in ongoingEvents" :key="event.id" :value="event.id">
              {{ event.name }} ({{ event.date }})
            </option>
          </select>
        </div>
      </div>
    </header>

    <main class="order-feed">
      <div v-if="orderStore.activeEventId" class="stats-toggle-bar">
        <span>营业额: ¥{{ orderStore.totalRevenue.toFixed(2) }}</span>
        <button class="btn-toggle-stats" @click="isStatsVisible = !isStatsVisible">
          {{ isStatsVisible ? '收起统计' : '展开统计' }}
        </button>
      </div>
      <Transition name="slide-fade">
        <LiveStats v-if="orderStore.activeEventId && isStatsVisible" />
      </Transition>

      <h3 v-if="orderStore.activeEventId && orderStore.pendingOrders.length">待处理订单</h3>
      <div v-if="!orderStore.activeEventId" class="no-orders">
        请在上方选择一个展会以开始接收订单。
      </div>
      <div v-else-if="!orderStore.pendingOrders.length" class="no-orders">
        暂无待处理订单
      </div>
      
      <TransitionGroup name="list" tag="div">
        <OrderCard 
          v-for="order in orderStore.pendingOrders" 
          :key="order.id"
          :order="order"
          @complete="completeOrder"
          @cancel="cancelOrder"/>
      </TransitionGroup>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'; // 【新增】导入 watch
import { useOrderStore } from '@/stores/orderStore';
import { useEventStore } from '@/stores/eventStore';
import { useEventDetailStore } from '@/stores/eventDetailStore'; // 【新增】导入
import OrderCard from '@/components/order/OrderCard.vue';
import LiveStats from '@/components/vendor/LiveStats.vue'; // 【新增】导入

const orderStore = useOrderStore();
const eventStore = useEventStore();
const eventDetailStore = useEventDetailStore(); // 【新增】

const selectedEventId = ref(null);
const isStatsVisible = ref(false); 

// 【新增】一个计算属性，只筛选出“进行中”的展会用于选择
const ongoingEvents = computed(() => {
  return eventStore.events.filter(event => event.status === '进行中');
});

// 【新增】当选择器变化时，更新 orderStore
function onEventChange() {
  orderStore.setActiveEvent(selectedEventId.value);
  isStatsVisible.value = false;
}

// 【核心逻辑】使用 watch 监听当前活动展会 ID 的变化
watch(() => orderStore.activeEventId, (newEventId, oldEventId) => {
  if (newEventId) {
    // 当展会 ID 变化时，获取该展会的商品列表（为了库存）和已完成订单（为了营业额）
    eventDetailStore.fetchProductsForEvent(newEventId);
    orderStore.fetchCompletedOrders();
  }
});
async function cancelOrder(orderId) {
  // 添加一个浏览器确认框，防止误触
  if (window.confirm(`确定要取消订单 #${orderId} 吗？`)) {
    try {
      await orderStore.cancelOrder(orderId);
    } catch (error) {
      alert(error.message);
    }
  }
}
// 【核心逻辑】当订单完成时，需要重新获取商品列表以更新库存显示
async function completeOrder(orderId) {
  try {
    await orderStore.markOrderAsCompleted(orderId);
    // 订单完成后，重新获取一次商品列表，`current_stock` 就会刷新
    if (orderStore.activeEventId) {
      eventDetailStore.fetchProductsForEvent(orderStore.activeEventId);
    }
  } catch (error) {
    alert(error.message);
  }
}
onMounted(() => {
  // 页面加载时，获取所有展会列表以填充选择器
  eventStore.fetchEvents();
  // 将 orderStore 的 activeEventId 初始化为 null
  orderStore.setActiveEvent(null);
});

onUnmounted(() => {
  // 离开页面时，停止轮询
  orderStore.setActiveEvent(null); // 这会自动调用 stopPolling
});
</script>

<style scoped>
/* ... (已有样式) ... */
.event-selector {
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem; /* label 和 select 之间的间距 */
}

.event-selector label {
  font-size: 1rem;
  color: #aaa;
}

/* 1. 自定义 select 的包装器 */
.custom-select-wrapper {
  position: relative;
  display: inline-block;
  width: 100%;
  max-width: 400px; /* 限制最大宽度 */
}

/* 2. 创建自定义的下拉箭头 */
.custom-select-wrapper::after {
  content: '▼';
  font-size: 0.8rem;
  color: var(--accent-color);
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none; /* 让点击可以穿透到下面的 select 元素 */
  transition: transform 0.2s ease;
}

/* 3. 隐藏原始的 select 箭头，并设置基础样式 */
.custom-select-wrapper select {
  /* 隐藏默认箭头 */
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  
  /* 基础样式 */
  width: 100%;
  padding: 10px 40px 10px 15px; /* 右侧 padding 留出空间给自定义箭头 */
  background-color: var(--card-bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  color: var(--primary-text-color);
  font-size: 1rem;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

/* 4. 交互样式 */
.custom-select-wrapper select:hover {
  border-color: var(--accent-color);
}

.custom-select-wrapper select:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 5px rgba(3, 218, 198, 0.5);
}

/* 5. 选项的样式 (部分浏览器支持) */
.custom-select-wrapper select option {
  background-color: var(--card-bg-color);
  color: var(--primary-text-color);
}
/* 【新增】统计切换栏样式 */
.stats-toggle-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--card-bg-color);
  padding: 0.75rem 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-color);
}

.stats-toggle-bar span {
  font-weight: bold;
  color: var(--accent-color);
}

.btn-toggle-stats {
  background: none;
  border: 1px solid var(--accent-color);
  color: var(--accent-color);
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

/* 【新增】为展开/收起添加过渡动画 */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

/* 微调待处理订单标题的上边距 */
.order-feed h3 {
  margin-top: 0;
}
</style>