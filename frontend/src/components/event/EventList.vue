<template>
  <div class="list-container">
    <h2>展会列表</h2>
    
    <div v-if="store.isLoading" class="loading-message">正在加载展会数据...</div>
    <div v-else-if="store.error" class="error-message">{{ store.error }}</div>
    
    <ul v-else-if="store.events.length" class="event-list">
      <!-- 在 li 标签上添加一个 :class 绑定，用于视觉区分正在更新的项 -->
      <RouterLink
      v-for="event in store.events"
      :key="event.id"
      :to="`/admin/events/${event.id}/products`"
      custom
      v-slot="{ navigate }"
      >
      <li @click="navigate" class="event-card clickable" role="link">
        <div class="event-info">
          <h3>{{ event.name }}</h3>
          <p>日期: {{ event.date }}</p>
          <p>地点: {{ event.location || '未指定' }}</p>
        </div>
        <div class="event-status">
          <span class="status-badge" :class="statusClass(event.status)">
            {{ event.status }}
          </span>
          <!-- 【新增】状态操作按钮 -->
          <div class="status-actions">
            <button 
              v-if="event.status === '未进行'" 
              @click.stop="changeStatus(event.id, '进行中')" 
              class="action-btn"
            >
              ► 开始
            </button>
            <button 
              v-if="event.status === '进行中'" 
              @click.stop="changeStatus(event.id, '已结束')" 
              class="action-btn"
            >
              ■ 结束
            </button>
            <button v-if="event.status === '已结束'"
              @click.stop="changeStatus(event.id,'未进行')
              " class="action-btn">
              ► 重新开始
            </button>
            <!-- 已结束的展会没有操作 -->
            <button @click.stop="openEditModal(event)" class="action-btn edit-btn">
              编辑
            </button>
          </div>
        </div>
      </li>
      </RouterLink>
    </ul>

    <p v-else>还没有任何展会，请在上方创建一个。</p>


        <!-- 【新增】编辑模态框 -->
    <AppModal :show="isEditModalVisible" @close="closeEditModal">
      <template #header>
        <h3>编辑展会</h3>
      </template>
      <template #body>
        <EditEventForm v-if="selectedEvent" ref="editForm" :event="selectedEvent" />
      </template>
      <template #footer>
        <button type="button" class="btn" @click="closeEditModal">取消</button>
        <button type="button" class="btn btn-primary" @click="handleUpdateEvent">保存更改</button>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'; // 【新增】导入 ref
import { useEventStore } from '@/stores/eventStore';
import AppModal from '@/components/shared/AppModal.vue';
import EditEventForm from '@/components/event/EditEventForm.vue';
import { RouterLink } from 'vue-router';
const store = useEventStore();
const updatingStatusId = ref(null);

// 【新增】编辑模态框相关的状态
const isEditModalVisible = ref(false);
const selectedEvent = ref(null);
const editForm = ref(null); // 用于获取 EditEventForm 组件的实例

onMounted(() => {
  store.fetchEvents();
});

const statusClass = (status) => {
  return {
    'status-ongoing': status === '进行中',
    'status-finished': status === '已结束',
    'status-upcoming': status === '未进行',
  };
};

// 【新增】处理状态变更的函数
async function changeStatus(eventId, newStatus) {
  // 防止重复点击
  if (updatingStatusId.value) return;

  updatingStatusId.value = eventId;
  try {
    await store.updateEventStatus(eventId, newStatus);
  } catch (error) {
    // 如果 store 抛出错误，在这里通知用户
    alert(error.message);
  } finally {
    // 无论成功或失败，最后都清除更新中的状态
    updatingStatusId.value = null;
  }
}
function openEditModal(event) {
  selectedEvent.value = event;
  isEditModalVisible.value = true;
}

// 【新增】关闭编辑模态框的函数
function closeEditModal() {
  isEditModalVisible.value = false;
  selectedEvent.value = null;
}

// 【新增】处理更新提交的函数
async function handleUpdateEvent() {
  // 增加对 selectedEvent 的检查，更安全
  if (editForm.value && selectedEvent.value) { 
    const formData = editForm.value.submit();
    if (formData) {
      try {
        // 【核心修正】
        // 第一个参数传入 event ID
        // 第二个参数传入 FormData
        console.log('尝试进行更新')
        await store.updateEvent(selectedEvent.value.id, formData);
        console.log('更新成功');
        closeEditModal(); // 成功后关闭模态框
      } catch (error) {
        alert(error.message); // 显示错误
      }
    }
  }
}
</script>

<style scoped>
/* ... 此前已有的样式保持不变 ... */
.event-card {
  /* ... */
  transition: opacity 0.3s; /* 添加一个过渡效果 */
}
/* 【新增】正在更新的卡片的样式 */
.event-card.updating {
  opacity: 0.5;
  pointer-events: none; /* 防止在更新时进行其他操作 */
}
.event-status {
  text-align: right;
}
.status-actions {
  margin-top: 0.5rem;
}
.action-btn {
  background: none;
  border: 1px solid var(--primary-text-color);
  color: var(--primary-text-color);
  padding: 4px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}
.action-btn:hover {
  background-color: var(--primary-text-color);
  color: var(--bg-color);
}
.event-card.clickable {
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s;
}
.event-card.clickable:hover {
  background-color: rgba(3, 218, 198, 0.05);
  border-color: rgba(3, 218, 198, 0.3);
}
</style>