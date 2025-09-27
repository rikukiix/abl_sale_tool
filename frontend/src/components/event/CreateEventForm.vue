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
      <div class="form-group">
        <label for="vendor_password">摊主密码 (可选):</label>
        <input id="vendor_password" v-model="formData.vendor_password" type="text" placeholder="留空则使用全局密码" />
      </div>
      <!-- 【新增】收款码图片上传区域 -->
      <div class="form-group">
        <label for="payment_qr_code">展会收款码图片 (可选):</label>
        <!-- 隐藏默认的文件输入框 -->
        <input 
          id="payment_qr_code" 
          ref="fileInput"
          type="file" 
          @change="handleFileChange" 
          accept="image/*"
          style="display: none;" 
        />
        <!-- 自定义上传按钮 -->
        <button type="button" class="btn btn-secondary" @click="triggerFileInput">
          选择图片
        </button>

        <!-- 【新增】图片预览 -->
        <div v-if="qrCodePreviewUrl" class="image-preview-container">
          <img :src="qrCodePreviewUrl" alt="收款码预览" class="image-preview" />
          <button type="button" @click="removeImage" class="remove-image-btn">×</button>
        </div>
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
  vendor_password: '' 
});
// 【新增】用于处理文件上传的状态
const paymentQrCodeFile = ref(null); // 存储文件对象
const qrCodePreviewUrl = ref(null); // 存储预览图片的URL
const fileInput = ref(null); // 用于引用文件输入框DOM元素

// 【新增】触发隐藏的文件输入框
function triggerFileInput() {
  fileInput.value.click();
}
function handleFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    paymentQrCodeFile.value = file;
    // 创建一个临时的URL用于图片预览
    qrCodePreviewUrl.value = URL.createObjectURL(file);
  }
}

// 【新增】移除已选图片的函数
function removeImage() {
  paymentQrCodeFile.value = null;
  // 释放之前创建的URL以避免内存泄漏
  URL.revokeObjectURL(qrCodePreviewUrl.value);
  qrCodePreviewUrl.value = null;
  // 重置文件输入框的值，这样用户才能再次选择同一个文件
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

async function handleSubmit() {
  isSubmitting.value = true;
  errorMessage.value = '';

  // 【修改】因为有文件上传，我们需要使用 FormData 来构建请求体
  const submissionData = new FormData();
  submissionData.append('name', formData.value.name);
  submissionData.append('date', formData.value.date);
  submissionData.append('location', formData.value.location);
  submissionData.append('vendor_password', formData.value.vendor_password);
  
  // 如果用户选择了图片文件，则添加到 FormData
  if (paymentQrCodeFile.value) {
    submissionData.append('payment_qr_code', paymentQrCodeFile.value);
  }

  try {
    // 调用 store 中的 createEvent action，传入 FormData
    await store.createEvent(submissionData);
    
    // 创建成功后，重置表单
    formData.value = { name: '', date: '', location: '', vendor_password: '' };
    removeImage(); // 同时清除图片选择
    
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
  padding: 1rem;           /* 缩小内边距 */
  border-radius: 6px;      /* 稍微缩小圆角 */
  margin-bottom: 1rem;     /* 缩小底部间距 */
  font-size: 0.96rem;      /* 字体略小 */
}
.form-group {
  margin-bottom: 0.6rem;   /* 缩小组间距 */
}
label {
  margin-bottom: 0.3rem;   /* 缩小label间距 */
  font-size: 0.95em;
}
input[type="text"],
input[type="date"] {
  width: 100%;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--primary-text-color);
  padding: 6px 8px;        /* 缩小输入框内边距 */
  border-radius: 3px;
  font-size: 0.96em;
  height: 32px;            /* 限制高度更紧凑 */
  box-sizing: border-box;
}
button,
.btn,
.btn-secondary {
  padding: 6px 14px;       /* 缩小按钮 */
  font-size: 0.96em;
  border-radius: 3px;
}
.image-preview-container {
  margin-top: 0.5rem;      /* 缩小预览间距 */
  padding: 3px;
  border-radius: 3px;
}
.image-preview {
  max-width: 120px;        /* 缩小图片预览 */
  max-height: 120px;
}
.remove-image-btn {
  width: 20px;
  height: 20px;
  font-size: 13px;
  line-height: 18px;
  top: -8px;
  right: -8px;
}
.error-message {
  margin-top: 0.5rem;
  font-size: 0.95em;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
/* 【新增】图片上传和预览相关的样式 */
.btn-secondary {
  background-color: #555;
  border-color: #555;
}
.btn-secondary:hover {
  background-color: #666;
}
.image-preview-container {
  position: relative;
  display: inline-block;
  margin-top: 1rem;
  border: 1px solid var(--border-color);
  padding: 5px;
  border-radius: 4px;
}
.image-preview {
  max-width: 200px;
  max-height: 200px;
  display: block;
}
.remove-image-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  background-color: #cc0000;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 16px;
  font-weight: bold;
  line-height: 22px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
</style>