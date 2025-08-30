# 环境配置说明

## 概述

本项目支持多环境部署，通过环境变量来配置不同环境的API路径，避免开发环境和生产环境的路由不匹配问题。

## 环境变量配置

### 1. 开发环境 (.env.local)

```bash
# 开发环境：使用相对路径，通过Vite代理转发
VITE_API_BASE_URL=/sale/api
VITE_APP_TITLE=东方Project展会出摊辅助工具 (开发版)
VITE_DEBUG_MODE=true
```

### 2. 生产环境 (.env.production)

```bash
# 生产环境：根据实际部署情况配置
VITE_API_BASE_URL=/sale/api
VITE_APP_TITLE=东方Project展会出摊辅助工具
VITE_DEBUG_MODE=false
```

### 3. 自定义环境

如果您的生产环境使用不同的API路径，可以这样配置：

```bash
# 例如：如果生产环境使用 /api 前缀
VITE_API_BASE_URL=/api

# 或者使用完整的域名
VITE_API_BASE_URL=https://your-domain.com/api
```

## 部署配置

### Nginx配置示例

#### 方案1：保持 /sale/api 路径（推荐）

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

#### 方案2：使用 /api 路径

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

    # API代理 - 使用 /api 路径
    location /api/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**注意**：如果使用方案2，需要设置环境变量：
```bash
VITE_API_BASE_URL=/api
```

## 构建和部署

### 1. 开发环境

```bash
npm run dev
```

### 2. 生产环境构建

```bash
# 使用生产环境配置构建
npm run build

# 或者指定环境
npm run build -- --mode production
```

### 3. 环境变量优先级

1. `.env.local` (最高优先级，本地开发)
2. `.env.production` (生产环境)
3. `.env.example` (默认值，最低优先级)

## 调试和故障排除

### 1. 检查当前配置

在浏览器控制台中，API请求会显示完整的URL路径。

### 2. 常见问题

**问题**：API请求404错误
**解决**：检查 `VITE_API_BASE_URL` 配置和Nginx代理配置是否匹配

**问题**：开发环境正常，生产环境API失败
**解决**：确认生产环境的Nginx配置和前端环境变量配置一致

### 3. 日志查看

开发环境下，API请求和响应会在控制台显示详细日志，便于调试。

## 最佳实践

1. **保持一致性**：建议开发环境和生产环境使用相同的API路径前缀
2. **环境隔离**：使用不同的环境变量文件管理不同环境
3. **版本控制**：将 `.env.example` 提交到版本控制，但不要提交 `.env.local` 等实际配置文件
4. **文档同步**：当修改API路径时，及时更新相关文档和配置
