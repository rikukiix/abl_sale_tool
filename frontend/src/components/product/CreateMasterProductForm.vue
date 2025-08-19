<template>
  <div class="form-container">
    <h3>添加新商品</h3>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>商品编号:</label>
        <input v-model="formData.product_code" type="text" placeholder="A01" required />
      </div>
      <div class="form-group">
        <label>商品名称:</label>
        <input v-model="formData.name" type="text" placeholder="灵梦亚克力立牌" required />
      </div>
      <div class="form-group">
        <label>默认价格:</label>
        <input v-model.number="formData.default_price" type="number" step="0.01" placeholder="45.00" required />
      </div>
      <button type="submit" class="btn">添加</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script setup>
// (这部分代码与 CreateEventForm 非常类似, 只是字段不同)
import { ref } from 'vue';
import { useProductStore } from '@/stores/productStore';

const store = useProductStore();
const errorMessage = ref('');
const formData = ref({
  product_code: '',
  name: '',
  default_price: null,
});

async function handleSubmit() {
  errorMessage.value = '';
  try {
    await store.createMasterProduct(formData.value);
    formData.value = { product_code: '', name: '', default_price: null };
  } catch (error) {
    errorMessage.value = error.message;
  }
}
</script>

<style scoped>
/* 样式与 CreateEventForm.vue 完全可以共享 */
</style>