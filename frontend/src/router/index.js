import { createRouter, createWebHistory } from 'vue-router'

// 导入所有需要的布局和视图
import AdminLayout from '../views/AdminLayout.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminMasterProducts from '../views/AdminMasterProducts.vue'
import AdminEventProducts from '../views/AdminEventProducts.vue'
import VendorView from '../views/VendorView.vue'
import CustomerView from '../views/CustomerView.vue'
import EventPortalView from '../views/EventPortalView.vue'
import AdminEventOrders from '../views/AdminEventOrders.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // --- 路由组 1: 管理后台 ---
    // 所有 /admin 开头的路径都会使用 AdminLayout 布局
    {
      path: '/admin',
      component: AdminLayout,
      // 管理后台的所有子页面
      children: [
        {
          path: '', // 默认 /admin 路径
          name: 'admin-dashboard',
          component: AdminDashboard,
        },
        {
          path: 'master-products',
          name: 'admin-master-products',
          component: AdminMasterProducts,
        },
        {
          path: 'events/:id/products',
          name: 'admin-event-products',
          component: AdminEventProducts,
          props: true,
        },
        // 【新增】订单管理路由
        {
          path: 'events/:id/orders',
          name: 'admin-event-orders',
          component: AdminEventOrders,
          props: true
        }
      ],
    },

    // --- 路由组 2: 摊主页面 ---
    // 这是一个独立的顶层路由，不使用 AdminLayout
    {
      path: '/vendor',
      name: 'vendor',
      component: VendorView,
    },

    // --- 路由组 3: 顾客点单页面 ---
    // 这也是一个独立的顶层路由，同样不使用 AdminLayout
    {
      path: '/events/:id/order', // 例如 /events/2/order
      name: 'customer-order',
      component: CustomerView,
      props: true // 将 :id 作为 prop 传递给 CustomerView
    },
    {
      path: '/',
      name: 'event-portal',
      component: EventPortalView,
    },
    // 【可选但推荐】添加一个重定向
    // 如果有人意外访问了/admin/，确保他们被带到展会管理页
    {
      path: '/',
      name: 'event-portal',
      component: EventPortalView,
    },
  ],
})

export default router