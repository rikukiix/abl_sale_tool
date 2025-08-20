<template>
  <!-- 这个组件没有自己的容器，因为它将被嵌入到模态框中 -->
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="edit-name">展会名称:</label>
      <input id="edit-name" v-model="editableEvent.name" type="text" required />
    </div>
    <div class="form-group">
      <label for="edit-date">日期:</label>
      <input id="edit-date" v-model="editableEvent.date" type="date" required />
    </div>
    <div class="form-group">
      <label for="edit-location">地点:</label>
      <input id="edit-location" v-model="editableEvent.location" type="text" />
    </div>
    <div class="form-group">
      <label for="edit-vendor_password">摊主密码 (可选):</label>
      <input id="edit-vendor_password" v-model="editableEvent.vendor_password" type="text" placeholder="留空则清除密码" />
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <!-- 提交按钮将由父组件（模态框）的 footer slot 提供 -->
  </form>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  event: {
    type: Object,
    required: true,
  },
});

const errorMessage = ref('');
// 创建一个可编辑的副本，避免直接修改 props
const editableEvent = ref({});

// 使用 watch 监听 props.event 的变化
// 当父组件传入新的 event 对象时（例如用户点击了另一个展会的编辑按钮），
// 更新我们的可编辑副本
watch(() => props.event, (newEvent) => {
  if (newEvent) {
    // 创建一个副本以避免直接修改 prop
    editableEvent.value = { ...newEvent,vendor_password: newEvent.vendor_password || '' };
  }
}, { immediate: true }); // immediate: true 确保组件初始化时就执行一次

// 定义一个暴露给父组件的方法，用于触发提交
function submit() {
  // 这里可以添加一些基础的验证
  if (!editableEvent.value.name || !editableEvent.value.date) {
    errorMessage.value = "展会名称和日期不能为空。";
    return null; // 返回 null 表示验证失败
  }
  errorMessage.value = '';
  return editableEvent.value;
}

// 使用 defineExpose 将 submit 方法暴露出去
defineExpose({
  submit,
});
</script>

<style scoped>
/* 样式与 CreateEventForm 类似 */
.form-group { margin-bottom: 1rem; }
label { display: block; margin-bottom: 0.5rem; }
input {
  width: 100%;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--primary-text-color);
  padding: 10px;
  border-radius: 4px;
  box-sizing: border-box;
}
.error-message { color: var(--error-color); }
</style>