<template>
  <div>
    <header class="page-header">
      <h1>全局商品库</h1>
      <p>在这里管理所有可复用的商品模板。添加后，即可在展会中通过编号上架。</p>
    </header>

    <main>
      <!-- 创建表单 -->
      <div class="form-container">
        <h3>添加新商品到仓库</h3>
        <form @submit.prevent="handleCreate">
          <div class="form-grid">
            <div class="form-group">
              <label for="create-code">商品编号:</label>
              <input id="create-code" v-model="createFormData.product_code" type="text" placeholder="A01" required />
            </div>
            <div class="form-group">
              <label for="create-name">商品名称:</label>
              <input id="create-name" v-model="createFormData.name" type="text" placeholder="灵梦亚克力立牌" required />
            </div>
            <div class="form-group">
              <label for="create-price">默认价格 (¥):</label>
              <input id="create-price" v-model.number="createFormData.default_price" type="number" step="0.01" placeholder="45.00" required />
            </div>
            <div class="form-group form-group-file">
              <label for="create-image">预览图:</label>
              <input id="create-image" type="file" @change="handleCreateFileChange" accept="image/*" />
              <img v-if="createPreviewUrl" :src="createPreviewUrl" alt="预览" class="preview-img-form" />
            </div>
          </div>
          <button type="submit" class="btn" :disabled="isCreating">
            {{ isCreating ? '添加中...' : '添加到仓库' }}
          </button>
          <p v-if="createError" class="error-message">{{ createError }}</p>
        </form>
      </div>
      <div class="filters">
        <label>
          <input type="checkbox" v-model="store.showInactive" @change="store.fetchMasterProducts()" />
          显示已停用的商品
        </label>
      </div>
      <!-- 商品列表 -->
      <MasterProductList @edit="openEditModal" @toggleStatus="handleToggleStatus" />
    </main>

    <!-- 编辑模态框 -->
    <AppModal :show="isEditModalVisible" @close="closeEditModal">
      <template #header><h3>编辑商品</h3></template>
      <template #body>
        <form v-if="editableProduct" class="edit-form" @submit.prevent="handleUpdate">
          <div class="form-group">
            <label>商品编号:</label>
            <input v-model="editableProduct.product_code" type="text" required />
          </div>
          <div class="form-group">
            <label>商品名称:</label>
            <input v-model="editableProduct.name" type="text" required />
          </div>
          <div class="form-group">
            <label>默认价格 (¥):</label>
            <input v-model.number="editableProduct.default_price" type="number" step="0.01" required />
          </div>
          <div class="form-group">
            <label>更换预览图:</label>
            <input type="file" @change="handleEditFileChange" accept="image/*" />
            <img v-if="editPreviewUrl" :src="editPreviewUrl" alt="预览" class="preview-img-form" />
          </div>
          <p v-if="editError" class="error-message">{{ editError }}</p>
        </form>
      </template>
      <template #footer>
        <button type="button" class="btn" @click="closeEditModal">取消</button>
        <button type="button" class="btn btn-primary" @click="handleUpdate" :disabled="isUpdating">
          {{ isUpdating ? '保存中...' : '保存更改' }}
        </button>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useProductStore } from '@/stores/productStore';
import MasterProductList from '@/components/product/MasterProductList.vue';
import AppModal from '@/components/shared/AppModal.vue';

const store = useProductStore();
const backendUrl = 'http://127.0.0.1:5000'; // 用于正确显示已上传的图片

// --- 创建逻辑的状态 ---
const isCreating = ref(false);
const createError = ref('');
const createFormData = ref({ product_code: '', name: '', default_price: null });
const createFormFile = ref(null);
const createPreviewUrl = ref('');

function handleCreateFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    createFormFile.value = file;
    createPreviewUrl.value = URL.createObjectURL(file);
  } else {
    createFormFile.value = null;
    createPreviewUrl.value = '';
  }
}

async function handleCreate() {
  isCreating.value = true;
  createError.value = '';
  try {
    await store.createMasterProduct(createFormData.value, createFormFile.value);
    // 成功后重置表单
    createFormData.value = { product_code: '', name: '', default_price: null };
    createFormFile.value = null;
    createPreviewUrl.value = '';
    // 如果<input type="file">不是组件，需要手动清空
    document.getElementById('create-image').value = null;
  } catch (error) {
    createError.value = error.message;
  } finally {
    isCreating.value = false;
  }
}

// --- 编辑逻辑的状态 ---
const isEditModalVisible = ref(false);
const isUpdating = ref(false);
const editError = ref('');
const editableProduct = ref({}); // 用于编辑的副本
const editFormFile = ref(null);
const editPreviewUrl = ref('');

function openEditModal(product) {
  editableProduct.value = { ...product }; // 创建副本以供编辑
  editFormFile.value = null;
  // 如果商品已有图片，显示现有图片；否则不显示
  editPreviewUrl.value = product.image_url ? `${backendUrl}${product.image_url}` : '';
  isEditModalVisible.value = true;
}

function closeEditModal() {
  isEditModalVisible.value = false;
  editError.value = '';
}

function handleEditFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    editFormFile.value = file;
    editPreviewUrl.value = URL.createObjectURL(file);
  }
}

async function handleUpdate() {
  isUpdating.value = true;
  editError.value = '';
  try {
    await store.updateMasterProduct(editableProduct.value, editFormFile.value);
    closeEditModal();
  } catch (error) {
    editError.value = error.message;
  } finally {
    isUpdating.value = false;
  }
}
async function handleToggleStatus(product) {
  const actionText = product.is_active ? '停用' : '启用';
  if (window.confirm(`确定要"${actionText}"商品 "${product.name}" 吗？`)) {
    try {
      await store.toggleProductStatus(product);
    } catch (error) {
      alert(error.message);
    }
  }
}
</script>

<style scoped>
/* 页面和表单的通用样式 */
.page-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}
.page-header h1 { color: var(--accent-color); margin: 0; }
.page-header p { color: #aaa; margin-top: 0.5rem; }

.form-container {
  background-color: var(--card-bg-color);
  border: 1px solid var(--border-color);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.form-group { display: flex; flex-direction: column; }
.form-group-file { grid-column: 1 / -1; } /* 文件上传占满整行 */
label { margin-bottom: 0.5rem; }
input[type="text"], input[type="number"] {
  width: 100%;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--primary-text-color);
  padding: 10px;
  border-radius: 4px;
  box-sizing: border-box;
}
.error-message { color: var(--error-color); margin-top: 1rem; }
.preview-img-form {
  width: 120px;
  height: 120px;
  object-fit: cover; /* 【核心】同样使用 cover */
  margin-top: 1rem;
  display: block;
  border-radius: 4px;
  border: 1px solid var(--border-color);
}
.btn-primary {
  background-color: var(--accent-color);
  color: var(--bg-color);
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.edit-form { /* 模态框内的表单样式 */
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.filters {
  margin-top: 2rem;
  margin-bottom: 1rem;
}
</style>