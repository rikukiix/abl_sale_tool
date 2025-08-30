# 🚀 部署检查清单

## 概述

本文档提供了完整的部署检查清单，确保您的系统在不同环境下都能正常工作。

## 🔍 部署前检查

### 1. 环境配置检查

- [ ] 前端环境变量配置正确
- [ ] 后端环境变量配置正确
- [ ] 数据库连接配置正确
- [ ] 文件上传路径配置正确

### 2. 路由配置检查

- [ ] 前端API baseURL配置正确
- [ ] 后端蓝图路由配置正确
- [ ] Nginx代理配置与前端配置匹配
- [ ] 静态资源路径配置正确

## 🛠️ 环境配置检查

### 前端配置检查

#### 开发环境
```bash
cd frontend
# 检查是否有 .env.local 文件
ls -la .env*

# 检查环境变量内容
cat .env.local
```

**预期结果**：
```bash
VITE_API_BASE_URL=/sale/api
VITE_APP_TITLE=东方Project展会出摊辅助工具 (开发版)
VITE_DEBUG_MODE=true
```

#### 生产环境
```bash
cd frontend
# 检查是否有 .env.production 文件
ls -la .env*

# 检查环境变量内容
cat .env.production
```

**预期结果**：
```bash
VITE_API_BASE_URL=/sale/api
VITE_APP_TITLE=东方Project展会出摊辅助工具
VITE_DEBUG_MODE=false
```

### 后端配置检查

```bash
cd backend
# 检查环境变量文件
ls -la .env*

# 检查配置文件
cat config.py
```

**预期结果**：
- 数据库路径配置正确
- 上传文件夹路径配置正确
- 管理员密码配置正确

## 🌐 Nginx配置检查

### 配置示例（推荐）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 静态文件（前端）
    location / {
        root /path/to/your/vue/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API代理 - 保持 /sale/api 路径
    location /sale/api/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 静态资源代理
    location /sale/static/ {
        proxy_pass http://127.0.0.1:5000/static/;
    }
}
```

### 检查要点

- [ ] 前端静态文件路径正确
- [ ] API代理路径与前端配置匹配
- [ ] 后端服务地址正确（127.0.0.1:5000）
- [ ] 静态资源代理配置正确

## 🧪 功能测试检查

### 1. 基础功能测试

- [ ] 前端页面能正常加载
- [ ] 后端API能正常响应
- [ ] 数据库连接正常
- [ ] 文件上传功能正常

### 2. API接口测试

```bash
# 测试展会列表API
curl http://your-domain.com/sale/api/events

# 测试单个展会API
curl http://your-domain.com/sale/api/events/1

# 测试商品列表API
curl http://your-domain.com/sale/api/events/1/products
```

**预期结果**：
- 返回正确的JSON数据
- 状态码为200
- 没有CORS错误

### 3. 前端功能测试

- [ ] 游客页面能正常显示商品
- [ ] 购物车功能正常
- [ ] 支付弹窗能显示收款码
- [ ] 摊主页面能正常登录
- [ ] 管理员页面能正常访问

## 🔧 故障排除

### 常见问题及解决方案

#### 1. API 404错误

**症状**：前端请求API返回404
**可能原因**：
- Nginx代理配置错误
- 后端服务未启动
- API路径不匹配

**解决方案**：
```bash
# 检查后端服务状态
ps aux | grep gunicorn

# 检查Nginx配置
nginx -t

# 检查Nginx日志
tail -f /var/log/nginx/error.log
```

#### 2. CORS错误

**症状**：浏览器控制台显示CORS错误
**可能原因**：
- 后端CORS配置错误
- 前端请求地址错误

**解决方案**：
```python
# 检查后端CORS配置
from flask_cors import CORS
CORS(app)
```

#### 3. 静态资源404错误

**症状**：图片、CSS、JS文件无法加载
**可能原因**：
- 前端构建文件路径错误
- Nginx静态文件配置错误

**解决方案**：
```bash
# 检查前端构建文件
ls -la frontend/dist/

# 检查Nginx静态文件配置
nginx -t
```

## 📋 部署后检查清单

### 系统功能检查

- [ ] 所有页面能正常访问
- [ ] 用户登录功能正常
- [ ] 商品管理功能正常
- [ ] 订单管理功能正常
- [ ] 文件上传功能正常
- [ ] 数据统计功能正常

### 性能检查

- [ ] 页面加载速度正常
- [ ] API响应时间正常
- [ ] 数据库查询性能正常
- [ ] 文件上传速度正常

### 安全检查

- [ ] 敏感信息未暴露
- [ ] 用户权限控制正常
- [ ] 文件上传安全限制正常
- [ ] API访问控制正常

## 🚨 紧急情况处理

### 系统无法访问

1. **检查服务状态**
   ```bash
   # 检查后端服务
   systemctl status gunicorn
   
   # 检查Nginx服务
   systemctl status nginx
   ```

2. **重启服务**
   ```bash
   # 重启后端服务
   systemctl restart gunicorn
   
   # 重启Nginx服务
   systemctl restart nginx
   ```

3. **检查日志**
   ```bash
   # 查看后端日志
   tail -f /var/log/gunicorn/error.log
   
   # 查看Nginx日志
   tail -f /var/log/nginx/error.log
   ```

### 数据丢失

1. **检查数据库备份**
2. **检查文件上传备份**
3. **联系技术支持**

## 📞 技术支持

如果遇到无法解决的问题，请：

1. 检查本文档的故障排除部分
2. 查看相关日志文件
3. 在GitHub上提交Issue
4. 联系项目维护者

---

**记住**：部署前一定要仔细检查所有配置，确保开发环境和生产环境的一致性！
