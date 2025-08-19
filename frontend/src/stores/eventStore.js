import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/services/api';

export const useEventStore = defineStore('event', () => {
  const events = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  async function fetchEvents() {
    // ... 此函数保持不变 ...
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.get('/events');
      events.value = response.data;
    } catch (err) {
      error.value = '无法加载展会列表，请检查后端服务是否开启。';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  }

  async function createEvent(eventData) {
    // ... 此函数保持不变 ...
    try {
      const response = await api.post('/events', eventData);
      events.value.unshift(response.data);
      return response.data;
    } catch (err) {
      console.error(err);
      throw new Error(err.response?.data?.error || '创建展会失败，请重试。');
    }
  }

  // 【新增】Action: 更新展会状态
  async function updateEventStatus(eventId, newStatus) {
    try {
      // 调用后端的 PUT /api/events/<event_id>/status 接口
      const response = await api.put(`/events/${eventId}/status`, { status: newStatus });
      
      // 更新成功后，为了避免重新请求整个列表，我们直接在前端更新状态
      // 找到本地 events 数组中对应的展会
      const index = events.value.findIndex(e => e.id === eventId);
      if (index !== -1) {
        // 直接修改该展会对象的状态，Vue 的响应式系统会自动更新 UI
        events.value[index].status = response.data.status;
      }
      return response.data;
    } catch (err) {
      console.error(err);
      // 抛出错误，让组件可以捕获并通知用户更新失败
      throw new Error(err.response?.data?.error || '更新状态失败，请重试。');
    }
  }

  async function updateEvent(eventData) {
    try {
      const { id, ...dataToUpdate } = eventData;
      // 调用我们刚在后端创建的 PUT /api/events/<id> 接口
      const response = await api.put(`/events/${id}`, dataToUpdate);
      
      // 更新成功后，同样在前端直接更新数据
      const index = events.value.findIndex(e => e.id === id);
      if (index !== -1) {
        // 使用 Object.assign 来合并更新后的字段
        Object.assign(events.value[index], response.data);
      }
      return response.data;
    } catch (err) {
      console.error(err);
      throw new Error(err.response?.data?.error || '更新展会信息失败。');
    }
  }

  return {
    events,
    isLoading,
    error,
    fetchEvents,
    createEvent,
    updateEventStatus, // 【新增】将新函数导出
    updateEvent,
  };
});