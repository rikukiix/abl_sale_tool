<template>
  <div class="login-container">
    <div class="login-box">
      <h2>{{ title }}</h2>
      <p>{{ subtitle }}</p>
      <form @submit.prevent="handleLogin">
        <input v-model="password" type="password" placeholder="请输入密码" required />
        <button type="submit" class="btn">进入</button>
        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const props = defineProps({
  role: { type: String, required: true } // 'admin' or 'vendor'
});

const store = useAuthStore();
const router = useRouter();
const route = useRoute();
const password = ref('');
const error = ref('');

const title = computed(() => props.role === 'admin' ? '管理员后台' : '摊主页面');
const subtitle = computed(() => `请输入${title.value}密码以继续`);

async function handleLogin() {
  error.value = '';
  try {
    // 1. 【核心改动】从路由的 query 中获取 eventId
    const eventId = route.query.eventId;
    
    // 2. 准备重定向路径
    const redirectPath = route.query.redirect || (props.role === 'admin' ? '/admin' : '/');
    
    // 3. 【核心改动】将 eventId 和 redirectPath 都传给 store 的 login action
    await store.login(password.value, props.role, eventId, redirectPath);

  } catch (err) {
    error.value = err.message;
  }
}
</script>

<style scoped>
/* 登录页面的居中样式 */
.login-container { display: flex; justify-content: center; align-items: center; height: 100vh; }
.login-box { width: 350px; padding: 2rem; background-color: var(--card-bg-color); border-radius: 8px; text-align: center; }
input { width: 100%; padding: 10px; margin-bottom: 1rem; /* ... */ }
</style>