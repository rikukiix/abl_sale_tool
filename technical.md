[29 tools called]

基于我对这个项目的深入分析，我来为您编写一份详细的技术文档。

# 东方Project展会出摊辅助工具 - 技术文档

## 项目概述

这是一个专为东方Project同人展会设计的现代化销售与库存管理系统。该系统采用前后端分离架构，为展会摊主提供完整的销售流程管理解决方案。

## 技术栈

### 前端技术栈
- **框架**: Vue 3 (Composition API)
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP客户端**: Axios
- **实时通信**: Socket.IO Client
- **UI组件**: Headless UI
- **构建工具**: Vite

### 后端技术栈
- **框架**: Flask (Python)
- **数据库ORM**: SQLAlchemy + Flask-Migrate
- **数据库**: SQLite
- **跨域支持**: Flask-CORS
- **文件处理**: Werkzeug + PIL
- **部署**: Gunicorn + Nginx

## 系统架构

### 整体架构图
```
┌─────────────────┐    ┌─────────────────┐
│   游客页面      │    │   摊主页面      │
│ - 商品展示      │    │ - 订单管理      │
│ - 购物车        │    │ - 配货操作      │
│ - 支付引导      │    │ - 实时统计      │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     │
          ┌─────────────────────┐
          │   管理员页面        │
          │ - 展会管理          │
          │ - 商品管理          │
          │ - 订单监控          │
          │ - 数据统计          │
          └─────────┬───────────┘
                    │
          ┌─────────────────────┐
          │     Flask后端       │
          │ - RESTful API       │
          │ - 数据模型          │
          │ - 文件上传          │
          │ - 认证授权          │
          └─────────────────────┘
```

## 数据库设计

### 核心数据模型

#### 1. Event (展会) 模型
```sql
- id: Integer (主键)
- name: String (展会名称)
- date: Date (展会日期)
- location: String (展会地点)
- status: String (展会状态: 未进行/进行中/已结束)
- vendor_password: String (摊主密码)
- qrcode_url: String (支付二维码路径)
```

#### 2. MasterProduct (主商品) 模型
```sql
- id: Integer (主键)
- product_code: String (商品编号，唯一)
- name: String (商品名称)
- default_price: Float (默认价格)
- image_url: String (商品图片路径)
- is_active: Boolean (是否激活)
```

#### 3. Product (展会商品) 模型
```sql
- id: Integer (主键)
- price: Float (展会售价)
- initial_stock: Integer (初始库存)
- event_id: Integer (外键关联展会)
- master_product_id: Integer (外键关联主商品)
```

#### 4. Order (订单) 模型
```sql
- id: Integer (主键)
- timestamp: DateTime (订单时间)
- status: String (订单状态: pending/completed/cancelled)
- total_amount: Float (订单总金额)
- event_id: Integer (外键关联展会)
```

#### 5. OrderItem (订单项) 模型
```sql
- id: Integer (主键)
- quantity: Integer (购买数量)
- order_id: Integer (外键关联订单)
- product_id: Integer (外键关联商品)
```

## 后端API接口

### 1. 展会管理API

#### 获取展会列表
```
GET /sale/api/events
GET /sale/api/events?status=进行中
```
**响应**: 返回展会列表，包含状态筛选功能

#### 创建展会
```
POST /sale/api/events
Content-Type: multipart/form-data

参数:
- name: 展会名称
- date: 展会日期 (YYYY-MM-DD)
- location: 展会地点
- vendor_password: 摊主密码
- payment_qr_code: 支付二维码文件
```

#### 更新展会信息
```
PUT /sale/api/events/{event_id}
POST /sale/api/events/{event_id}
Content-Type: multipart/form-data

参数:
- name: 展会名称
- date: 展会日期
- location: 展会地点
- vendor_password: 摊主密码
- payment_qr_code: 支付二维码文件
- remove_payment_qr_code: 是否删除二维码
```

#### 更新展会状态
```
PUT /sale/api/events/{event_id}/status
Content-Type: application/json

参数:
- status: 新状态 (未进行/进行中/已结束)
```

### 2. 主商品管理API

#### 获取主商品列表
```
GET /sale/api/master-products
GET /sale/api/master-products?all=true  # 显示所有商品(包括停用的)
```

#### 创建主商品
```
POST /sale/api/master-products
Content-Type: multipart/form-data

参数:
- product_code: 商品编号
- name: 商品名称
- default_price: 默认价格
- image: 商品图片文件
```

#### 更新主商品
```
PUT /sale/api/master-products/{mp_id}
POST /sale/api/master-products/{mp_id}
Content-Type: multipart/form-data

参数:
- product_code: 商品编号
- name: 商品名称
- default_price: 默认价格
- image: 商品图片文件
- remove_image: 是否删除图片
```

#### 切换商品状态
```
PUT /sale/api/master-products/{mp_id}/status
Content-Type: application/json

参数:
- is_active: 激活状态 (true/false)
```

### 3. 展会商品管理API

#### 获取展会商品列表
```
GET /sale/api/events/{event_id}/products
```

#### 为展会添加商品
```
POST /sale/api/events/{event_id}/products
Content-Type: application/json

参数:
- product_code: 主商品编号
- initial_stock: 初始库存
- price: 展会价格 (可选，默认使用主商品价格)
```

#### 更新展会商品
```
PUT /sale/api/products/{product_id}
Content-Type: application/json

参数:
- price: 新价格
- initial_stock: 新库存
```

#### 删除展会商品
```
DELETE /sale/api/products/{product_id}
```

### 4. 订单管理API

#### 获取展会订单列表
```
GET /sale/api/events/{event_id}/orders
GET /sale/api/events/{event_id}/orders?status=pending
```

#### 创建新订单
```
POST /sale/api/events/{event_id}/orders
Content-Type: application/json

参数:
- items: [
    {
      "product_id": 商品ID,
      "quantity": 购买数量
    }
  ]
```

#### 更新订单状态
```
PUT /sale/api/events/{event_id}/orders/{order_id}/status
Content-Type: application/json

参数:
- status: 新状态 (pending/completed/cancelled)
```

### 5. 数据统计API

#### 获取展会统计数据
```
GET /sale/api/events/{event_id}/stats
```

**响应数据结构**:
```json
{
  "event_info": {
    "id": 展会ID,
    "name": 展会名称,
    "status": 展会状态
  },
  "summary": {
    "total_revenue": 总营业额,
    "completed_orders_count": 已完成订单数,
    "total_items_sold": 总售出件数
  },
  "product_details": [
    {
      "product_id": 商品ID,
      "name": 商品名称,
      "price": 单价,
      "initial_stock": 初始库存,
      "sold_count": 已售出数量,
      "current_stock": 当前库存,
      "revenue": 该商品收入
    }
  ]
}
```

### 6. 认证API

#### 用户登录
```
POST /sale/api/auth/login
Content-Type: application/json

参数:
- password: 密码
- role: 角色 (admin/vendor)
- eventId: 展会ID (摊主登录时可选)
```

## 前端页面结构

### 1. 游客页面 (`/events/{id}/order`)

#### 功能特性
- **商品网格展示**: 以网格形式展示所有在售商品
- **购物车管理**: 支持添加/移除商品，实时计算总价
- **库存实时更新**: 显示商品剩余库存
- **支付引导**: 提交订单后显示支付二维码
- **响应式设计**: 适配移动设备和平板

#### 核心组件
- `ProductGrid.vue`: 商品网格展示组件
- `ShoppingCart.vue`: 购物车组件
- `PaymentModal.vue`: 支付引导弹窗

#### 状态管理
```javascript
// customerStore.js
- products: 商品列表
- cart: 购物车商品
- cartTotal: 购物车总价
- isLoading: 加载状态
- error: 错误信息
```

### 2. 摊主页面 (`/vendor/{id}`)

#### 功能特性
- **实时订单监控**: 自动轮询获取新订单
- **订单状态管理**: 支持标记订单为完成/取消
- **实时统计**: 显示当前销售数据和库存情况
- **手动刷新**: 支持手动刷新订单列表
- **订单历史**: 查看已完成的订单

#### 核心组件
- `OrderCard.vue`: 订单卡片组件
- `LiveStats.vue`: 实时统计组件

#### 状态管理
```javascript
// orderStore.js
- pendingOrders: 待处理订单列表
- completedOrders: 已完成订单列表
- totalRevenue: 总收入
- isPolling: 是否正在轮询
```

### 3. 管理员页面 (`/admin`)

#### 功能特性
- **展会管理**: 创建、编辑展会信息
- **商品库管理**: 维护全局商品模板
- **展会商品配置**: 为特定展会配置商品和价格
- **订单监控**: 查看所有订单状态
- **数据导出**: 导出销售数据

#### 核心组件
- `CreateEventForm.vue`: 创建展会表单
- `EventList.vue`: 展会列表
- `MasterProductList.vue`: 主商品列表
- `ImageUploader.vue`: 图片上传组件

## 前端路由配置

```javascript
// 主要路由结构
const routes = [
  // 管理员后台
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', component: AdminDashboard },
      { path: 'master-products', component: AdminMasterProducts },
      { path: 'events/:id/products', component: AdminEventProducts },
      { path: 'events/:id/orders', component: AdminEventOrders }
    ]
  },
  
  // 摊主页面
  { path: '/vendor', component: VendorEventSelection },
  { path: '/vendor/:id', component: VendorView },
  
  // 游客页面
  { path: '/', component: EventPortalView },
  { path: '/events/:id/order', component: CustomerView },
  
  // 登录页面
  { path: '/login/:role', component: LoginView }
]
```

## 部署配置

### 开发环境
```bash
# 后端启动
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run

# 前端启动
cd frontend
npm install
npm run dev
```

### 生产环境
```nginx
# Nginx 配置
server {
    listen 80;
    server_name your-domain.com;
    
    # 静态文件（前端）
    location / {
        root /path/to/vue/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    # API代理到后端
    location /sale/api/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 安全特性

### 认证机制
- **管理员认证**: 通过环境变量 `ADMIN_PASSWORD` 设置
- **摊主认证**: 支持全局密码和展会专用密码
- **会话管理**: 使用 SessionStorage 存储登录状态
- **路由守卫**: 基于角色的页面访问控制

### 数据验证
- **输入验证**: 前后端双重数据验证
- **文件上传**: 文件类型和大小限制
- **SQL注入防护**: 使用 SQLAlchemy ORM 参数化查询
- **XSS防护**: Vue.js 自动转义用户输入

## 性能优化

### 前端优化
- **组件懒加载**: 按需加载页面组件
- **图片压缩**: 自动压缩上传的商品图片
- **状态缓存**: 合理使用 Pinia 状态缓存
- **防抖处理**: 购物车操作和搜索防抖

### 后端优化
- **数据库索引**: 为常用查询字段添加索引
- **连接池**: 使用 SQLAlchemy 默认连接池
- **文件缓存**: 静态文件缓存策略
- **API限流**: 防止恶意请求

## 扩展性设计

### 模块化架构
- **蓝图模式**: Flask 蓝图实现功能模块化
- **组件复用**: Vue 组件设计支持复用
- **Store隔离**: Pinia Store 按功能划分

### 配置管理
- **环境变量**: 敏感配置通过环境变量管理
- **配置文件**: 支持不同环境的配置切换
- **热重载**: 开发环境支持热重载

这个系统采用了现代化的技术栈和架构设计，为展会摊主提供了完整的销售管理解决方案，具有良好的可维护性和扩展性。