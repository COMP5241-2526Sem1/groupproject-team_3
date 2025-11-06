# Vercel 部署快速参考卡
# Vercel Deployment Quick Reference

## 🚀 一键部署 | One-Click Deploy

### 第一步：准备 MongoDB Atlas
```
1. 访问: https://cloud.mongodb.com
2. 创建免费集群 (M0 Sandbox)
3. 获取连接字符串 → Database → Connect → Connect your application
4. 配置网络访问 → Network Access → Add IP: 0.0.0.0/0
```

### 第二步：部署到 Vercel
```
1. 访问: https://vercel.com
2. 点击 "New Project"
3. 导入 GitHub 仓库: groupproject-team_3
4. 配置环境变量 (见下方)
5. 点击 "Deploy"
```

---

## 🔐 必需的环境变量

在 Vercel Dashboard → Settings → Environment Variables 添加:

```bash
# 1. Flask 密钥 (生成命令见下方)
SECRET_KEY=your-random-secret-key-here

# 2. 环境设置
FLASK_ENV=production

# 3. MongoDB 连接 (从 Atlas 获取)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/learning_activity_system?retryWrites=true&w=majority

# 4. AI 功能 (可选，用于活动生成)
OPENAI_API_KEY=github_pat_your_token_or_sk_openai_key
OPENAI_MODEL=gpt-4o-mini
```

---

## 🔑 生成 SECRET_KEY

### Windows PowerShell:
```powershell
.\Project3\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

### macOS/Linux:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## ✅ 部署前检查清单

运行验证脚本:
```bash
python validate_deployment.py
```

应该看到:
```
✅ All checks passed! Ready for Vercel deployment.
```

---

## 📊 部署后测试

访问您的 Vercel URL (例如 `https://your-app.vercel.app`):

1. ✅ 首页加载正常
2. ✅ 可以注册新账号
3. ✅ 可以登录
4. ✅ 教师可以创建课程
5. ✅ 学生可以选课
6. ✅ 活动功能正常

---

## 🐛 常见问题

### 问题: "Module not found" 错误
**解决**: 确保 `requirements.txt` 包含所有依赖

### 问题: 数据库连接失败
**解决**: 
- 检查 `MONGODB_URI` 是否正确
- MongoDB Atlas 网络访问是否允许 0.0.0.0/0

### 问题: 500 Internal Server Error
**解决**:
- 查看 Vercel Logs: Dashboard → Deployments → [Your Deployment] → Runtime Logs
- 检查环境变量是否全部设置

### 问题: 静态文件 404
**解决**: Vercel 会自动处理 `/static` 路径，通常不需要额外配置

---

## 🔄 更新部署

### 自动部署 (推荐)
每次 push 到 GitHub，Vercel 自动重新部署

### 手动触发
Vercel Dashboard → Deployments → Redeploy

---

## 📞 获取帮助

- 📖 **详细文档**: 查看 `VERCEL_DEPLOYMENT.md`
- 🌐 **Vercel 文档**: https://vercel.com/docs
- 💬 **MongoDB 支持**: https://docs.atlas.mongodb.com/

---

## 📌 重要链接

| 服务 | URL |
|------|-----|
| Vercel Dashboard | https://vercel.com/dashboard |
| MongoDB Atlas | https://cloud.mongodb.com |
| GitHub 仓库 | https://github.com/COMP5241-2526Sem1/groupproject-team_3 |
| Vercel Python 文档 | https://vercel.com/docs/functions/serverless-functions/runtimes/python |

---

**创建日期**: 2024-10-22  
**项目**: Learning Activity Management System  
**团队**: COMP5241-2526Sem1 Team 3
