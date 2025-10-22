# Vercel Deployment Guide for Learning Activity System
# 学习活动系统 Vercel 部署指南

## 📋 前置要求 | Prerequisites

- Vercel 账号 (https://vercel.com)
- MongoDB Atlas 账号 (https://www.mongodb.com/cloud/atlas)
- GitHub 仓库已推送所有代码
- OpenAI API Key 或 GitHub Personal Access Token (for AI features)

---

## 🚀 部署步骤 | Deployment Steps

### 1️⃣ 准备 MongoDB Atlas

1. **登录 MongoDB Atlas** (https://cloud.mongodb.com)
2. **获取连接字符串**:
   - 进入 Database → Connect → Connect your application
   - 复制连接字符串，格式如下:
     ```
     mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
     ```
3. **配置网络访问**:
   - Network Access → Add IP Address → Allow Access from Anywhere (0.0.0.0/0)
   - 这是 Vercel serverless functions 所需的

---

### 2️⃣ 部署到 Vercel

#### 方法 A: 通过 Vercel Dashboard (推荐)

1. **访问 Vercel** (https://vercel.com)
2. **点击 "New Project"**
3. **导入 Git 仓库**:
   - 选择 GitHub
   - 授权 Vercel 访问您的仓库
   - 选择 `groupproject-team_3` 仓库
4. **配置项目**:
   - Framework Preset: **Other** (或留空)
   - Root Directory: `./` (保持默认)
   - Build Command: 留空
   - Output Directory: 留空
5. **添加环境变量** (Environment Variables):
   ```
   SECRET_KEY=your-random-secret-key-here
   FLASK_ENV=production
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/learning_activity_system?retryWrites=true&w=majority
   OPENAI_API_KEY=github_pat_your_token_here_or_sk_openai_key
   OPENAI_MODEL=gpt-4o-mini
   ```
   
   **重要**: 将上述值替换为您的实际值！

6. **点击 "Deploy"** 🚀

#### 方法 B: 通过 Vercel CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 在项目目录中部署
cd c:\Users\admin\Desktop\groupproject-team_3
vercel

# 按提示操作，配置环境变量
```

---

### 3️⃣ 配置环境变量详解

在 Vercel Dashboard → Settings → Environment Variables 中添加:

| 变量名 | 示例值 | 说明 |
|--------|--------|------|
| `SECRET_KEY` | `your-random-secret-key-change-this` | Flask session 密钥 (随机字符串) |
| `FLASK_ENV` | `production` | 环境设置 |
| `MONGODB_URI` | `mongodb+srv://user:pass@cluster.mongodb.net/...` | MongoDB Atlas 连接字符串 |
| `OPENAI_API_KEY` | `github_pat_...` 或 `sk-...` | AI 功能的 API 密钥 |
| `OPENAI_MODEL` | `gpt-4o-mini` | 使用的 AI 模型 |

---

### 4️⃣ 验证部署

部署完成后，Vercel 会提供一个 URL，如:
```
https://groupproject-team-3.vercel.app
```

**测试步骤**:
1. 访问 URL
2. 应该重定向到登录页面
3. 尝试登录 (使用已有账号或注册新账号)
4. 检查功能是否正常

---

## 📁 项目文件说明 | Project Files

### 新增文件 (为 Vercel 部署创建)

1. **`vercel.json`** - Vercel 配置文件
   - 定义构建和路由规则
   - 配置 Python serverless function
   
2. **`api/index.py`** - Serverless function 入口
   - Vercel 要求的入口文件
   - 导入并运行 Flask app

3. **`.vercelignore`** - 部署时忽略的文件
   - 类似 .gitignore
   - 排除测试文件、本地环境等

4. **`VERCEL_DEPLOYMENT.md`** - 本文档

---

## ⚙️ Vercel 配置说明

### `vercel.json` 解析

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",     // 入口文件
      "use": "@vercel/python"     // 使用 Python runtime
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",      // 静态文件路由
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",             // 所有其他请求
      "dest": "api/index.py"      // 路由到 Flask app
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  },
  "regions": ["hkg1"]             // 香港区域 (亚洲用户最佳)
}
```

---

## 🔧 常见问题 | Troubleshooting

### 问题 1: 部署失败 - "Module not found"

**解决方案**:
- 确保 `requirements.txt` 包含所有依赖
- 检查 Python 版本兼容性 (Vercel 支持 Python 3.9+)

### 问题 2: 数据库连接失败

**解决方案**:
- 检查 MongoDB Atlas 网络访问设置
- 确认 `MONGODB_URI` 环境变量正确
- 验证用户名和密码没有特殊字符需要 URL 编码

### 问题 3: 静态文件 404

**解决方案**:
- 确保 `static/` 文件夹存在
- 检查 `vercel.json` 中的静态文件路由配置
- Vercel 会自动处理 `/static` 路径

### 问题 4: Session 问题

**解决方案**:
- 确保 `SECRET_KEY` 环境变量已设置
- 使用强随机字符串作为 SECRET_KEY
- 生成方法: `python -c "import secrets; print(secrets.token_hex(32))"`

### 问题 5: 超时错误

**解决方案**:
- Vercel 免费版有 10 秒执行时间限制
- 优化数据库查询
- 考虑升级到 Pro 计划 (60 秒限制)

---

## 📊 性能优化建议

### 1. 数据库优化
- 在 MongoDB 中添加索引:
  ```python
  db.users.createIndex({ "username": 1 })
  db.courses.createIndex({ "teacher_id": 1 })
  db.activities.createIndex({ "course_id": 1 })
  ```

### 2. 缓存策略
- 使用 MongoDB 聚合管道减少查询次数
- 考虑添加 Redis 缓存层 (Vercel KV)

### 3. 静态文件
- Vercel 自动优化静态文件
- 考虑使用 CDN 托管大文件

---

## 🔐 安全建议

1. **永远不要**提交 `.env` 文件到 Git
2. **使用强密码**作为 SECRET_KEY
3. **MongoDB 用户权限**:
   - 创建专门的数据库用户
   - 只授予必要的权限
4. **定期更新**依赖包:
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```

---

## 📈 监控和日志

### Vercel Dashboard
- **Deployments** - 查看部署历史
- **Analytics** - 访问统计
- **Logs** - 实时日志查看 (Runtime Logs)

### 查看日志
```bash
# 使用 Vercel CLI
vercel logs <deployment-url>
```

---

## 🔄 更新部署

### 自动部署
- 每次 push 到 GitHub 主分支 (`ZmhPre` 或 `main`)
- Vercel 自动检测并重新部署

### 手动部署
```bash
# 使用 CLI
vercel --prod

# 或在 Dashboard 中点击 "Redeploy"
```

---

## 📝 部署清单 | Deployment Checklist

部署前检查:

- [ ] 所有代码已提交到 GitHub
- [ ] `requirements.txt` 包含所有依赖
- [ ] MongoDB Atlas 集群已创建
- [ ] MongoDB 网络访问已配置 (0.0.0.0/0)
- [ ] 已获取 MongoDB 连接字符串
- [ ] 已准备 OpenAI API Key 或 GitHub PAT
- [ ] 已生成强 SECRET_KEY
- [ ] `vercel.json` 文件存在
- [ ] `api/index.py` 文件存在
- [ ] 已测试本地环境

部署后检查:

- [ ] 网站可访问
- [ ] 登录功能正常
- [ ] 数据库连接正常
- [ ] AI 功能正常 (如果使用)
- [ ] 静态文件加载正常
- [ ] 测试所有主要功能

---

## 🆘 获取帮助

- **Vercel 文档**: https://vercel.com/docs
- **Vercel Python Runtime**: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- **MongoDB Atlas 文档**: https://docs.atlas.mongodb.com/
- **项目 GitHub**: https://github.com/COMP5241-2526Sem1/groupproject-team_3

---

## 🎉 部署成功后

您的应用现在:
- ✅ 可通过 HTTPS 全球访问
- ✅ 自动 SSL 证书
- ✅ CDN 加速
- ✅ 自动扩展
- ✅ 零服务器管理

**分享您的项目**: 
```
https://your-project.vercel.app
```

---

**部署日期**: 2024-10-22  
**版本**: v1.0  
**维护者**: COMP5241-2526Sem1 Team 3
