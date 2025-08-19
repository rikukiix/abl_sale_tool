<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div> <!-- 新增一个 div 将主要导航和次要导航分开 -->
        <h2>管理后台</h2>
        <nav>
          <RouterLink to="/admin">展会管理</RouterLink>
          <RouterLink to="/admin/master-products">全局商品库</RouterLink>
        </nav>

        <!-- 动态上下文导航 -->
        <div v-if="event" class="context-nav">
          <hr>
          <h3 class="event-title">{{ event.name }}</h3>
          <nav>
            <RouterLink :to="`/admin/events/${event.id}/products`">
              商品管理
            </RouterLink>
            <RouterLink :to="`/admin/events/${event.id}/orders`">
              订单管理
            </RouterLink>
          </nav>
        </div>
      </div>

      <!-- 【核心改动】新增“功能视图”区块 -->
      <div class="view-links">
        <hr>
        <h4>快捷视图</h4>
        <!-- 
          使用 <a> 标签和 target="_blank" 
          可以在新的浏览器标签页中打开这些页面，
          这对于同时查看管理后台和摊主/顾客页面非常方便。
        -->
        <a href="/vendor" target="_blank" class="view-link-btn">
          <span>摊主视图</span>
          <!-- 一个小图标，表示“新窗口打开” -->
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
        </a>
        <a href="/" target="_blank" class="view-link-btn">
          <span>顾客视图</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
        </a>
      </div>
    </aside>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>
<script setup>
import { computed } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router';
// 导入 eventStore 以获取展会名称
import { useEventStore } from '@/stores/eventStore'; 

const route = useRoute();
const eventStore = useEventStore();

// 创建一个计算属性，用于在侧边栏显示当前展会的信息
const event = computed(() => {
  // 检查当前路由是否匹配 'admin-event-products' 或其他展会详情路由
  const eventId = route.params.id;
  if (!eventId) {
    return null; // 如果不在展会详情页，则不显示
  }
  
  // 从 eventStore 的列表中查找对应的展会，以获取其名称
  // find 方法可能返回 undefined，所以需要处理
  return eventStore.events.find(e => e.id === parseInt(eventId, 10)) || { name: '加载中...', id: eventId };
});
</script>
<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background-color: var(--card-bg-color);
  padding: 1.5rem;
  border-right: 1px solid var(--border-color);
  /* 【新增】让主要导航和次要导航两端对齐 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.context-nav {
  margin-top: 1.5rem;
}
.context-nav hr {
  border-color: var(--border-color);
  margin: 1rem 0;
}
.event-title {
  font-size: 1rem;
  color: var(--primary-text-color);
  margin-bottom: 0.5rem;
  word-break: break-all; /* 防止长标题溢出 */
}
.admin-layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 220px;
  background-color: var(--card-bg-color);
  padding: 1.5rem;
  border-right: 1px solid var(--border-color);
}
.sidebar h2 {
  color: var(--accent-color);
  margin-top: 0;
}
.sidebar nav {
  display: flex;
  flex-direction: column;
}
.sidebar nav a {
  color: var(--primary-text-color);
  text-decoration: none;
  padding: 0.75rem 0;
  border-radius: 4px;
  transition: background-color 0.2s;
}
.sidebar nav a:hover {
  background-color: rgba(3, 218, 198, 0.1);
}
/* 当前激活路由的链接样式 */
.sidebar nav a.router-link-exact-active {
  color: var(--accent-color);
  font-weight: bold;
}
.content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
.view-links hr {
  border-color: var(--border-color);
  margin: 1rem 0;
}

.view-links h4 {
  font-size: 0.9rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.75rem;
}

.view-link-btn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--primary-text-color);
  text-decoration: none;
  transition: all 0.2s;
}

.view-link-btn:hover {
  border-color: var(--accent-color);
  color: var(--accent-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.view-link-btn svg {
  opacity: 0.7;
  transition: opacity 0.2s;
}

.view-link-btn:hover svg {
  opacity: 1;
}
</style>