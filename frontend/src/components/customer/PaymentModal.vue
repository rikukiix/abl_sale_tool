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
      <p class="scan-tip">
        手机浏览器用户请长按二维码图片保存后，<br>
        用微信/支付宝“扫一扫”识别付款
      </p>
      
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

/* 3. 标题和二维码样式 */
.payment-modal-content h3 {
  margin: 0;
  font-size: 1.8rem;
  color: var(--primary-text-color);
}

.payment-modal-content h3 strong {
  color: var(--accent-color);
  font-size: 1rem;
}

.payment-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 80vw;
  height: 80vh;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1300;
}

.payment-modal-content {
  background-color: var(--card-bg-color);
  padding: 1rem 1rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  text-align: center;
  max-width: 800px;
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.qr-code-container {
  width: 80%;
  display: flex;
  justify-content: center;
}

.qr-code {
  max-width: 600px;
  width: 80%;
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
@media (max-width: 600px) {
  .payment-modal-backdrop {
    width: 100vw;
    height: 100vh;
    left: 0;
    top: 0;
    padding: 0;
  }
  .payment-modal-content {
    width: 100vw;
    max-width: 100vw;
    min-width: 0;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
    padding: 0.5rem 0.5rem 1.2rem 0.5rem;
    justify-content: flex-start;
  }
  .qr-code-container {
    width: 100%;
    margin: 0.5rem 0 1rem 0;
  }
  .qr-code {
    width: 95vw;
    max-width: 95vw;
    height: auto;
    aspect-ratio: 1 / 1;
    border-radius: 8px;
  }
  .payment-modal-content .btn {
    font-size: 1.1rem;
    padding: 0.8rem;
  }
}
.scan-tip {
  color: var(--accent-color);
  font-size: 1.1rem;
  margin: 0.5rem 0 0.5rem 0;
  font-weight: bold;
  line-height: 1.5;
}
</style>
