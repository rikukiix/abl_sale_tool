<template>
  <div v-if="show" class="payment-modal-backdrop">
    <div class="payment-modal-content">
      <h3>请扫码支付 <strong>¥{{ total.toFixed(2) }}</strong></h3>
      
      <!-- 动态显示收款码图片 -->
      <div v-if="qrCodeUrl" class="qr-code-container">
        <img :src="qrCodeUrl" alt="收款码" class="qr-code" />
      </div>
      
      <!-- 如果没有收款码，显示提示信息 -->
      <div v-else class="no-qr-code">
        <p>暂无收款码</p>
        <p>请联系摊主设置收款码</p>
      </div>
      
      <p>支付完成后，请等待摊主为您配货</p>
      <button class="btn" @click="$emit('close')">关闭</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: { type: Boolean, required: true },
  total: { type: Number, required: true },
  qrCodeUrl: { type: String, default: null } // 新增：收款码URL
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

.qr-code-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.qr-code {
  max-width: 300px;
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 8px;
  object-fit: contain;
}

.no-qr-code {
  padding: 2rem;
  color: #888;
  border: 2px dashed #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.no-qr-code p {
  margin: 0.5rem 0;
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
