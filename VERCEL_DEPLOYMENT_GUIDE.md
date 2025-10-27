# Vercel 部署指南 / Vercel Deployment Guide

## 🎯 已修复的问题 / Fixed Issues

✅ **Read-only filesystem error** - 修复了在 Vercel serverless 环境中尝试创建 uploads 目录的问题  
✅ **Lazy database connection** - 数据库连接延迟到首次使用时，避免导入时崩溃  
✅ **Missing app variable** - 确保 `app` 变量始终被定义，即使初始化失败

## 📋 部署步骤 / Deployment Steps

### 1. 在 Vercel 设置环境变量 / Set Environment Variables in Vercel

**重要：不要把敏感信息提交到 Git！/ IMPORTANT: Do not commit sensitive data to Git!**

进入 Vercel Dashboard → 选择项目 → Settings → Environment Variables

添加以下环境变量（Add these environment variables）：

```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority

OPENAI_API_KEY=<your-openai-api-key-or-github-pat>

OPENAI_MODEL=gpt-4o-mini

SECRET_KEY=<生成一个安全的密钥 / Generate a secure key>

FLASK_ENV=production
```

**⚠️ 使用你自己的实际值替换上面的占位符！**  
**⚠️ Replace the placeholders above with your actual values!**

从本地 `.env` 文件复制实际的值到 Vercel 环境变量中。

**生成 SECRET_KEY / Generate SECRET_KEY:**
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. 配置 MongoDB Atlas IP 白名单 / Configure MongoDB Atlas IP Whitelist

1. 登录 MongoDB Atlas
2. 选择你的集群 → Network Access
3. 添加 IP Address：`0.0.0.0/0` (允许所有来源，用于开发)
   - 或者添加 Vercel 的 IP 范围（更安全）

### 3. 触发重新部署 / Trigger Redeployment

设置好环境变量后，Vercel 会自动重新部署。或者：

- 方法 1：在 Vercel Dashboard → Deployments → 点击最新部署旁的 "⋯" → Redeploy
- 方法 2：推送新的 commit 到 GitHub（已完成！）

### 4. 查看部署日志 / Check Deployment Logs

1. 进入 Vercel Dashboard → 你的项目
2. 点击 Deployments → 选择最新的部署
3. 点击 "Building" 或 "Function Logs" 查看日志

**如果看到错误 / If you see errors:**
- 检查环境变量是否正确设置
- 确认 MongoDB Atlas 允许 Vercel 的 IP 访问
- 查看完整的 traceback 并寻找具体错误信息

### 5. 测试部署 / Test Deployment

访问你的 Vercel URL：
```
https://<your-project>.vercel.app/
```

应该会重定向到登录页面。

## 🔍 常见问题排查 / Troubleshooting

### 问题 1：仍然看到 "Read-only file system" 错误
**解决方案：** 最新代码已修复，确保 Vercel 正在使用最新的 commit (a96e953)

### 问题 2：数据库连接失败
**可能原因：**
- MongoDB Atlas IP 白名单未配置
- MONGODB_URI 环境变量未设置或格式错误
- 数据库用户名/密码错误

**检查步骤：**
1. 在 Vercel 环境变量中确认 MONGODB_URI 正确
2. 在 MongoDB Atlas 检查 Network Access 设置
3. 测试连接字符串是否有效

### 问题 3：OpenAI API 错误
**解决方案：**
- 确认 OPENAI_API_KEY 在 Vercel 环境变量中正确设置
- 如使用 GitHub Models，确保 token 有效
- 检查 OPENAI_MODEL 设置为 `gpt-4o-mini`

### 问题 4：Static files (CSS/JS) 无法加载
**检查：**
- `vercel.json` 中的 routes 配置是否正确
- static 文件是否在仓库中
- 浏览器开发者工具 Network 标签查看请求状态

## 📁 重要文件说明 / Important Files

- **`vercel.json`** - Vercel 配置文件，定义构建和路由规则
- **`api/index.py`** - Serverless 函数入口点
- **`app.py`** - Flask 应用主文件
- **`requirements.txt`** - Python 依赖列表
- **`runtime.txt`** - 指定 Python 版本（如果需要）

## 🔐 安全建议 / Security Recommendations

1. ✅ **已完成：** 使用 Vercel 环境变量存储敏感信息
2. ⚠️ **待完成：** 从 Git 仓库中移除 `.env` 文件或确保它在 `.gitignore` 中
3. ⚠️ **建议：** 定期轮换密钥和访问令牌
4. ⚠️ **建议：** 在 MongoDB Atlas 中配置更严格的 IP 白名单

## 📊 监控和日志 / Monitoring and Logs

### 查看实时日志 / View Real-time Logs
```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 查看日志
vercel logs <deployment-url>
```

### 或者使用 Dashboard / Or use Dashboard
Vercel Dashboard → Project → Deployments → [Latest] → View Function Logs

## 🚀 下一步 / Next Steps

1. ✅ 环境变量已设置
2. ✅ 代码已推送到 GitHub
3. ⏳ 等待 Vercel 自动部署
4. ✅ 检查部署日志
5. ✅ 访问应用并测试功能

## 💡 提示 / Tips

- Vercel 的 serverless 函数有 10 秒超时限制（Hobby plan）
- 使用 `/tmp` 目录存储临时文件（已在代码中处理）
- 静态文件通过 Vercel CDN 自动优化
- 考虑使用 Vercel Analytics 监控性能

## 📞 需要帮助？/ Need Help?

如果遇到问题：
1. 查看 Vercel 部署日志
2. 检查上述常见问题排查部分
3. 确认所有环境变量正确设置
4. 测试 MongoDB Atlas 连接

---

**最后更新 / Last Updated:** 2024-10-23  
**部署状态 / Deployment Status:** ✅ 修复已推送，等待验证
