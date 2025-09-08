<template>
  <RouterView />
  <GlobalAlert />
  <!-- 将测试组件放在这里，它会悬浮在所有页面之上 -->
</template>

<script setup>
import { RouterView } from 'vue-router';
import GlobalAlert from '@/components/GlobalAlert.vue';
// 导入测试组件
import WebSocketTester from './components/WebSocketTester.vue';

</script>