<template>
  <div class="form-container">
    <h3>创建新展会</h3>
    <!-- .prevent 修饰符可以阻止表单提交时的默认页面刷新行为 -->
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name">展会名称:</label>
        <input id="name" v-model="formData.name" type="text" placeholder="例如：COMICUP 31" required />
      </div>
      <div class="form-group">
        <label for="date">日期:</label>
        <input id="date" v-model="formData.date" type="date" required />
      </div>
      <div class="form-group">
        <label for="location">地点:</label>
        <input id="location" v-model="formData.location" type="text" placeholder="例如：上海" />
      </div>
      
      <!-- 按钮在提交过程中会被禁用，防止重复点击 -->
      <button type="submit" class="btn" :disabled="isSubmitting">
        {{ isSubmitting ? '创建中...' : '创建' }}
      </button>

      <!-- 如果提交时发生错误，在这里显示错误信息 -->
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useEventStore } from '@/stores/eventStore';

// 获取 event store 的实例
const store = useEventStore();
const isSubmitting = ref(false);
const errorMessage = ref('');

// 使用 ref 创建一个响应式对象来绑定表单数据
const formData = ref({
  name: '',
  date: '',
  location: '',
});

// 处理表单提交的函数
async function handleSubmit() {
  isSubmitting.value = true;
  errorMessage.value = '';
  try {
    // 调用 store 中的 createEvent action
    await store.createEvent(formData.value);
    
    // 创建成功后，重置表单
    formData.value = { name: '', date: '', location: '' };
    // 可以在这里给用户一个更友好的成功提示，而不是 alert
    // 例如：showSuccessToast('创建成功!');
    
  } catch (error) {
    // 如果 store action 抛出错误，在这里捕获并显示
    errorMessage.value = error.message;
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<style scoped>
/* 这里是专门为这个组件设计的样式 */
.form-container {
  background-color: var(--card-bg-color);
  border: 1px solid var(--border-color);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
}
input[type="text"],
input[type="date"] {
  width: 100%;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--primary-text-color);
  padding: 10px;
  border-radius: 4px;
  box-sizing: border-box; /* 确保 padding 不会撑大宽度 */
}
.error-message {
  color: var(--error-color);
  margin-top: 1rem;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>