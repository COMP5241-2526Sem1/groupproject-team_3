# Vercel 静态文件问题修复指南

## 问题描述

部署到 Vercel 后,页面虽然返回 200 状态码,但是:
- 界面显示混乱,没有样式
- CSS 文件加载失败
- JavaScript 文件加载失败
- 无法正常登录

从 Vercel 日志中看到大量 **404 错误**,特别是对 `/static/css/` 和 `/static/js/` 的请求。

## 根本原因

Vercel 的 Serverless 架构需要**显式声明静态文件的构建配置**。原来的 `vercel.json` 只配置了 Python 函数,没有配置静态文件构建器,导致:

1. **静态文件未被正确部署到 CDN**
2. **路由无法正确解析静态资源请求**
3. **所有 `/static/` 请求都被转发到 Python 函数,返回 404**

## 解决方案

### 修改 `vercel.json`

添加 `@vercel/static` 构建器来处理静态文件:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "static/**",           // ← 新增:静态文件构建
      "use": "@vercel/static"       // ← 使用 Vercel 静态文件构建器
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"          // 静态文件路由保持不变
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"        // 其他请求转发到 Python 函数
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  },
  "regions": ["hkg1"]
}
```

### 工作原理

1. **构建阶段**:
   - `@vercel/python`: 构建 Python 函数 (api/index.py)
   - `@vercel/static`: 将 `static/**` 目录下的所有文件上传到 Vercel CDN

2. **请求阶段**:
   - `/static/css/style.css` → 直接从 CDN 返回
   - `/login` → 转发到 Python 函数处理
   - `/api/courses` → 转发到 Python 函数处理

## 验证步骤

### 1. 等待 Vercel 自动重新部署

推送代码后,Vercel 会自动触发新的部署:
- 前往 Vercel Dashboard → Deployments
- 查看最新部署状态(应该显示 "Building...")
- 等待部署完成(通常 1-2 分钟)

### 2. 检查浏览器开发者工具

打开网站后,按 **F12** 打开开发者工具:

**Network 标签页**:
```
✅ status.css         200  (from static/)
✅ script.js          200  (from static/)
✅ /login             200
✅ /register          200
```

**Console 标签页**:
- 应该**没有** "Failed to load resource" 错误
- 应该**没有** "404 Not Found" 错误

### 3. 测试页面功能

1. **样式检查**:
   - 页面布局正常显示
   - 按钮、表单有正确的样式
   - 颜色、字体、间距符合预期

2. **登录测试**:
   ```
   用户名: admin
   密码: admin123
   ```
   - 应该能成功登录
   - 跳转到对应的仪表板页面

3. **静态资源检查**:
   - 右键页面 → "查看源代码"
   - 检查 `<link>` 和 `<script>` 标签的 URL
   - 应该是: `/static/css/...` 和 `/static/js/...`

## 常见问题

### Q1: 部署后仍然看到 404 错误

**可能原因**:
- 浏览器缓存了旧的错误响应
- Vercel CDN 需要时间刷新

**解决方法**:
1. 强制刷新浏览器: `Ctrl + Shift + R` (Windows) 或 `Cmd + Shift + R` (Mac)
2. 清除浏览器缓存
3. 使用隐身模式访问
4. 等待 5-10 分钟让 CDN 完全更新

### Q2: CSS 加载了但样式还是不对

**检查**:
```bash
# 查看 Vercel 日志中的警告
```

**可能原因**:
- CSS 文件路径错误
- 模板中使用了错误的 `url_for()` 语法

**验证**:
- 在浏览器中直接访问: `https://your-app.vercel.app/static/css/style.css`
- 应该能看到 CSS 文件内容

### Q3: 登录后立即退出登录

**可能原因**:
- `SECRET_KEY` 环境变量未设置或为默认值
- Session 配置问题

**解决方法**:
1. 确认 Vercel 环境变量中设置了唯一的 `SECRET_KEY`
2. 不要使用 `your-secret-key-here-change-in-production`
3. 生成新的密钥:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

## 技术细节

### Vercel 静态文件架构

```
用户请求
    │
    ├─> /static/css/style.css
    │       │
    │       └─> Vercel CDN (全球边缘节点)
    │               │
    │               └─> 返回静态文件 (超快!)
    │
    └─> /login
            │
            └─> Vercel Serverless Function
                    │
                    └─> Python Flask 应用
                            │
                            └─> 返回 HTML 响应
```

### 为什么需要 @vercel/static

Vercel 不会自动识别哪些目录是静态资源。如果不明确配置:
- `static/` 目录的文件不会被上传
- 即使上传了,路由也不知道如何处理
- 请求会错误地转发到 Python 函数

使用 `@vercel/static` 后:
- ✅ 文件被优化并上传到 CDN
- ✅ 启用 gzip/brotli 压缩
- ✅ 自动设置正确的 Cache-Control 头
- ✅ 支持 HTTP/2 推送
- ✅ 全球 CDN 加速

## 下一步

部署成功后,建议:

1. **监控性能**:
   - 检查 Vercel Analytics
   - 查看静态资源加载时间

2. **优化资源**:
   - 压缩 CSS/JS 文件
   - 使用 CDN 加速字体

3. **安全检查**:
   - 确保所有敏感信息都在环境变量中
   - 启用 HTTPS (Vercel 默认启用)

---

**修复完成!** 🎉

现在你的应用应该可以正常显示样式和功能了。如果还有问题,请查看 Vercel 的实时日志获取更多信息。
