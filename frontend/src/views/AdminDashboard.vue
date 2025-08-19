<template>
  <div class="dashboard-container">
    <header>
      <h1>管理后台</h1>
      <p>在这里管理您的所有展会和商品。</p>
    </header>
    <main>
      <!-- 创建展会的表单组件 -->
      <CreateEventForm />
      
      <!-- 显示展会列表的组件 -->
      <EventList />
    </main>
  </div>
</template>

<script setup>
// 导入需要的组件
import CreateEventForm from '@/components/event/CreateEventForm.vue';
import EventList from '@/components/event/EventList.vue';
</script>

<style scoped>
.dashboard-container {
  max-width: 800px;
  margin: 0 auto;
}
header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}
header h1 {
  color: var(--accent-color);
  margin: 0;
}
header p {
  color: #aaa;
  margin-top: 0.5rem;
}
</style>