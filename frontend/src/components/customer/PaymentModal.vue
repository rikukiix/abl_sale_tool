<template>
  <div v-if="show" class="payment-modal-backdrop">
    <div class="payment-modal-content">
      <h3>请扫码支付 <strong>¥{{ total.toFixed(2) }}</strong></h3>
      <img src="/qr-code.png" alt="收款码" class="qr-code" />
      <p>支付完成后，请等待摊主为您配货</p>
      <button class="btn" @click="$emit('close')">关闭</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: { type: Boolean, required: true },
  total: { type: Number, required: true }
});
defineEmits(['close']);
</script>

<style scoped>
/* 1. 背景遮罩：使用 fixed 定位覆盖整个屏幕 */
.payment-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85); /* 更深的背景，突出内容 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 确保在最顶层 */
}

/* 2. 内容容器 */
.payment-modal-content {
  background-color: var(--card-bg-color);
  padding: 2rem 3rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  text-align: center;
  max-width: 450px; /* 限制最大宽度 */
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem; /* 内部元素的间距 */
}

/* 3. 标题和二维码样式 */
.payment-modal-content h3 {
  margin: 0;
  font-size: 1.8rem;
  color: var(--primary-text-color);
}

.payment-modal-content h3 strong {
  color: var(--accent-color);
  font-size: 2rem;
}

.qr-code {
  max-width: 300px;
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 8px;
}

.payment-modal-content p {
  margin: 0;
  color: #aaa;
}

/* 4. 关闭按钮样式 */
.payment-modal-content .btn {
  width: 100%;
  padding: 1rem;
  font-size: 1.2rem;
}
</style>