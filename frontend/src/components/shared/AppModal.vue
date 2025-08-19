<template>
  <!-- 使用 Vue 的 Transition 组件为模态框添加淡入淡出效果 -->
  <Transition name="modal-fade">
    <!-- 监听点击事件，如果点击的是背景遮罩，则触发 close 事件 -->
    <div v-if="show" class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal-container">
        <header class="modal-header">
          <!-- 使用 slot 让父组件可以自定义标题 -->
          <slot name="header">
            默认标题
          </slot>
          <button type="button" class="btn-close" @click="$emit('close')">×</button>
        </header>
        
        <section class="modal-body">
          <!-- 主内容区域 -->
          <slot name="body">
            默认内容
          </slot>
        </section>
        
        <footer class="modal-footer">
          <!-- 底部/操作区域 -->
          <slot name="footer">
            <button type="button" class="btn" @click="$emit('close')">关闭</button>
          </slot>
        </footer>
      </div>
    </div>
  </Transition>
</template>

<script setup>
// 定义组件可以接收的 props 和可以触发的 events
defineProps({
  show: {
    type: Boolean,
    required: true,
  },
});
defineEmits(['close']);
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-container {
  background-color: var(--card-bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 5px 15px rgba(0,0,0,0.5);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}
.modal-body {
  padding: 1.5rem 1rem;
}
.modal-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  text-align: right;
}
.btn-close {
  background: none;
  border: none;
  color: var(--primary-text-color);
  font-size: 1.5rem;
  cursor: pointer;
}
/* 过渡动画效果 */
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
</style>