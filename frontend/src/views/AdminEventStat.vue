<template>
  <div class="admin-event-stat">
    <header class="stat-header">
      <h1>{{ pageTitle }}</h1>
      <a 
        v-if="statStore.stats && statStore.stats.summary.length > 0"
        :href="statStore.downloadUrl" 
        class="btn btn-primary download-btn"
        download
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        下载 Excel 报告
      </a>
    </header>

    <div v-if="statStore.isLoading" class="loading-indicator">
      <div class="spinner"></div>
      <p>正在从数据库中提取统计信息...</p>
    </div>

    <div v-else-if="statStore.error" class="error-message">
      <p><strong>[ 后端数据库寄了！ ]</strong></p>
      <p>{{ statStore.error }}</p>
      <button @click="statStore.fetchStats" class="btn btn-secondary">重新建立连接</button>
    </div>

    <div v-else-if="statStore.stats" class="stats-content">
      <!-- 关键数据总览 -->
      <div class="summary-cards">
        <div class="card">
          <span class="label">总销售额</span>
          <span class="value">{{ formatCurrency(statStore.stats.total_revenue) }}</span>
        </div>
        <div class="card">
          <span class="label">总销售件数</span>
          <span class="value">{{ totalItemsSold }}</span>
        </div>
        <div class="card">
          <span class="label">销售品类数</span>
          <span class="value">{{ productVarietyCount }}</span>
        </div>
      </div>

      <!-- 销售详情表格 -->
      <div class="details-table-container">
        <h3>销售数据表</h3>
        <p v-if="!statStore.stats.summary.length" class="no-data">
          // 无有效销售数据记录...
        </p>
        <table v-else>
          <thead>
            <tr>
              <th>制品编号</th>
              <th>制品名</th>
              <th class="text-right">单价</th>
              <th class="text-center">销售量</th>
              <th class="text-right">销售额</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in statStore.stats.summary" :key="item.product_id">
              <td class="id-cell">#{{ item.product_code }}</td>
              <td>{{ item.product_name }}</td>
              <td class="text-right currency-cell">{{ formatCurrency(item.unit_price) }}</td>
              <td class="text-center quantity-cell">{{ item.total_quantity }}</td>
              <td class="text-right currency-cell">{{ formatCurrency(item.total_revenue_per_item) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
// ... 您的 <script setup> 内容保持不变 ...
import { onMounted, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useEventStatStore } from '@/stores/eventStatStore';

const route = useRoute();
const statStore = useEventStatStore();

const pageTitle = computed(() => statStore.stats?.event_name ? `${statStore.stats.event_name} - 数据统计` : '数据统计');
const totalItemsSold = computed(() => statStore.stats?.summary.reduce((sum, item) => sum + item.total_quantity, 0) || 0);
const productVarietyCount = computed(() => statStore.stats?.summary.length || 0);

function formatCurrency(value) {
  if (typeof value !== 'number') return '¥ 0.00';
  return `¥ ${value.toFixed(2)}`;
}

onMounted(() => {
  const eventId = route.params.id;
  if (eventId) statStore.setActiveEvent(eventId);
});

watch(() => route.params.id, (newEventId) => {
  if (newEventId) statStore.setActiveEvent(newEventId);
});
</script>

<style scoped>
/* 假设你的主题色定义在 :root 或其他全局样式中 */
/* :root {
  --bg-color: #1a1a1a;
  --card-bg-color: #242424;
  --border-color: #3a3a3a;
  --primary-text-color: #e0e0e0;
  --secondary-text-color: #a0a0a0;
  --accent-color: #03dac6;
  --accent-color-dark: #018786;
} */

.admin-event-stat {
  padding: 2rem;
  color: var(--primary-text-color);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

h1 {
  font-size: 2rem;
  font-weight: 300; /* 更纤细的字体 */
  color: var(--accent-color);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin: 0;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease-in-out;
}

.download-btn {
  background-color: transparent;
  border-color: var(--accent-color);
  color: var(--accent-color);
}
.download-btn:hover {
  background-color: rgba(3, 218, 198, 0.1);
  box-shadow: 0 0 15px rgba(3, 218, 198, 0.3);
  transform: translateY(-2px);
}

.loading-indicator, .error-message {
  text-align: center;
  padding: 5rem 2rem;
  color: var(--secondary-text-color);
  border: 1px dashed var(--border-color);
  border-radius: 8px;
  background-color: rgba(0,0,0,0.1);
}
.error-message p { margin: 0.5rem 0; }
.error-message strong { color: #ff5555; }
.btn-secondary { background-color: var(--card-bg-color); color: var(--primary-text-color); margin-top: 1rem;}
.btn-secondary:hover { border-color: var(--primary-text-color); }

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--accent-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.card {
  background-color: var(--card-bg-color);
  padding: 2rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}
.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--accent-color);
  opacity: 0.7;
}

.card .label {
  font-size: 1rem;
  color: var(--secondary-text-color);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.75rem;
  display: block;
}

.card .value {
  font-size: 2.5rem;
  font-weight: 500;
  color: var(--primary-text-color);
  line-height: 1;
}

.details-table-container {
  background-color: var(--card-bg-color);
  padding: 2rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
}
.details-table-container h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-weight: 400;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

thead th {
  color: var(--secondary-text-color);
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 1px;
}

tbody tr {
  transition: background-color 0.2s;
}
tbody tr:hover {
  background-color: rgba(3, 218, 198, 0.05);
}
tbody td {
  color: var(--primary-text-color);
}
.id-cell {
  color: var(--secondary-text-color);
  font-family: 'Courier New', Courier, monospace;
}
.quantity-cell {
  font-weight: bold;
  font-size: 1.1rem;
}
.currency-cell {
  color: var(--accent-color);
  font-weight: 500;
}
.text-right { text-align: right; }
.text-center { text-align: center; }

.no-data {
  color: var(--secondary-text-color);
  padding: 3rem;
  text-align: center;
  font-family: 'Courier New', Courier, monospace;
}
</style>