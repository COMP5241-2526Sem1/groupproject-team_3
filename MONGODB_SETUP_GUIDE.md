# MongoDB Atlas 配置指南 | MongoDB Atlas Setup Guide

[中文](#中文配置指南) | [English](#english-setup-guide)

---

## 中文配置指南

### 📋 概述

本指南将帮助你在 MongoDB Atlas 上创建免费的云数据库，并配置到本项目中。

**时间**: 约 10-15 分钟  
**费用**: 完全免费 (M0 免费层)

---

### 步骤 1: 注册 MongoDB Atlas 账号

1. **访问官网**: https://www.mongodb.com/cloud/atlas/register
2. **选择注册方式**:
   - 使用 Google 账号
   - 使用 GitHub 账号
   - 使用邮箱注册

3. **填写基本信息**:
   - 组织名称 (可随意填写)
   - 项目名称: `Learning Platform` (或自定义)

---

### 步骤 2: 创建免费集群

1. **选择部署方式**:
   - 点击 **"Build a Database"** (或 "Create")
   - 选择 **"Shared"** (共享集群 - 免费)

2. **选择云服务提供商和区域**:
   ```
   Provider: AWS / Google Cloud / Azure (任选)
   Region: 选择离你最近的区域
   
   推荐:
   - 中国用户: Singapore (ap-southeast-1)
   - 美国用户: N. Virginia (us-east-1)
   - 欧洲用户: Ireland (eu-west-1)
   ```

3. **选择集群层级**:
   - 选择 **M0 Sandbox** (免费)
   - 512 MB 存储
   - 共享 RAM

4. **命名集群**:
   - Cluster Name: `Cluster0` (默认) 或自定义

5. **点击**: **"Create Cluster"**

⏳ **等待 3-5 分钟创建集群**

---

### 步骤 3: 配置数据库访问

#### 3.1 创建数据库用户

1. **进入 Database Access**:
   - 左侧菜单 → **"Database Access"**
   - 点击 **"Add New Database User"**

2. **选择认证方式**:
   - 选择 **"Password"** (密码认证)

3. **设置用户名和密码**:
   ```
   Username: learningplatform_user
   Password: [自动生成] 或 [自定义密码]
   
   ⚠️ 重要: 记录好密码，稍后需要使用
   ```

4. **设置权限**:
   - Database User Privileges: **"Read and write to any database"**
   - 或选择 **"Atlas admin"** (管理员权限)

5. **点击**: **"Add User"**

#### 3.2 配置网络访问

1. **进入 Network Access**:
   - 左侧菜单 → **"Network Access"**
   - 点击 **"Add IP Address"**

2. **选择访问方式**:

   **选项 A - 允许所有访问 (开发环境推荐)**:
   ```
   点击: "Allow Access from Anywhere"
   IP Address: 0.0.0.0/0
   Description: Allow all access
   ```

   **选项 B - 仅允许当前 IP**:
   ```
   点击: "Add Current IP Address"
   IP Address: [自动检测你的 IP]
   Description: My current IP
   ```

3. **点击**: **"Confirm"**

---

### 步骤 4: 获取连接字符串

1. **返回 Database**:
   - 左侧菜单 → **"Database"** (或 "Deployment")

2. **点击 Connect**:
   - 找到你的集群 (Cluster0)
   - 点击 **"Connect"** 按钮

3. **选择连接方式**:
   - 选择 **"Connect your application"** (连接应用程序)

4. **选择驱动和版本**:
   ```
   Driver: Python
   Version: 3.6 or later
   ```

5. **复制连接字符串**:
   ```
   mongodb+srv://learningplatform_user:<password>@cluster0.xxxxx.mongodb.net/
   ```

   **示例**:
   ```
   mongodb+srv://learningplatform_user:MySecurePass123@cluster0.ab1cd.mongodb.net/
   ```

---

### 步骤 5: 配置项目

#### 5.1 创建 .env 文件

在项目根目录创建 `.env` 文件:

**Windows**:
```powershell
New-Item -Path .env -ItemType File
notepad .env
```

**macOS/Linux**:
```bash
touch .env
nano .env
```

#### 5.2 添加配置信息

将以下内容粘贴到 `.env` 文件:

```env
# MongoDB Atlas 配置
MONGO_URI=mongodb+srv://learningplatform_user:YOUR_PASSWORD_HERE@cluster0.xxxxx.mongodb.net/
DB_NAME=learning_platform

# Flask 配置
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# 可选: GitHub Models API
GITHUB_TOKEN=your_github_token_here
```

#### 5.3 替换占位符

1. **替换 `YOUR_PASSWORD_HERE`**:
   - 用你在步骤 3.1 创建的密码替换
   - ⚠️ **密码中的特殊字符需要 URL 编码**:
     ```
     @ → %40
     : → %3A
     / → %2F
     # → %23
     ? → %3F
     & → %26
     = → %3D
     ```

   **示例**:
   ```
   原密码: Pass@word#123
   编码后: Pass%40word%23123
   
   完整 URI:
   mongodb+srv://learningplatform_user:Pass%40word%23123@cluster0.ab1cd.mongodb.net/
   ```

2. **生成 SECRET_KEY**:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   复制输出结果替换 `your_secret_key_here`

---

### 步骤 6: 测试连接

#### 6.1 创建测试脚本

创建 `test_mongodb_connection.py`:

```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 获取连接字符串
mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')

print(f"Testing connection to: {db_name}")
print(f"URI: {mongo_uri[:50]}...")

try:
    # 连接数据库
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # 测试连接
    client.server_info()
    
    # 获取数据库
    db = client[db_name]
    
    # 列出集合
    collections = db.list_collection_names()
    
    print("✅ Connection successful!")
    print(f"✅ Database: {db_name}")
    print(f"✅ Collections: {collections if collections else 'No collections yet'}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check MONGO_URI in .env file")
    print("2. Verify password is URL encoded")
    print("3. Check Network Access in MongoDB Atlas")
    print("4. Ensure IP is whitelisted")
```

#### 6.2 运行测试

```bash
# 激活虚拟环境
.\Project3\Scripts\Activate.ps1  # Windows
source Project3/bin/activate      # macOS/Linux

# 运行测试
python test_mongodb_connection.py
```

**预期输出**:
```
Testing connection to: learning_platform
URI: mongodb+srv://learningplatform_user:***...
✅ Connection successful!
✅ Database: learning_platform
✅ Collections: No collections yet
```

---

### 步骤 7: 初始化数据库

连接成功后，运行初始化脚本:

```bash
# 创建数据库结构
python init_db.py

# 添加示例数据
python seed_database.py

# 创建测试账号
python create_test_accounts.py
```

**预期输出**:
```
✅ Database initialized successfully
✅ Created 5 courses
✅ Created 13 activities
✅ Created 5 test accounts
```

---

### 🔍 验证安装

1. **启动应用**:
   ```bash
   python app.py
   ```

2. **访问应用**: http://localhost:5000

3. **登录测试**:
   ```
   用户名: student_demo
   密码: student123
   ```

4. **检查 Dashboard**:
   - 应显示课程数据
   - 不应出现 ERROR

---

### ❓ 常见问题

#### 问题 1: ServerSelectionTimeoutError

**错误信息**:
```
pymongo.errors.ServerSelectionTimeoutError: 
No servers found yet, trying for 5 more seconds
```

**可能原因**:
1. 网络访问未配置
2. IP 未添加到白名单
3. 连接字符串错误

**解决方案**:
```bash
1. 检查 MongoDB Atlas Network Access
2. 添加 0.0.0.0/0 或当前 IP
3. 等待 2-3 分钟让配置生效
4. 检查 .env 文件中的 MONGO_URI
```

#### 问题 2: Authentication failed

**错误信息**:
```
pymongo.errors.OperationFailure: 
Authentication failed
```

**解决方案**:
```bash
1. 检查用户名是否正确
2. 检查密码是否正确
3. 特殊字符是否已 URL 编码
4. 确认用户已创建且权限正确
```

#### 问题 3: 密码包含特殊字符

**问题**: 密码中有 `@`, `#`, `/` 等特殊字符

**解决方案**:

**方法 A - URL 编码** (推荐):
```python
# 使用 Python 编码密码
from urllib.parse import quote_plus

password = "Pass@word#123"
encoded = quote_plus(password)
print(encoded)  # Pass%40word%23123
```

**方法 B - 重新设置简单密码**:
1. 在 MongoDB Atlas Database Access 中删除用户
2. 创建新用户
3. 使用不含特殊字符的密码 (如 `LearningPlatform123`)

#### 问题 4: 无法创建 .env 文件

**Windows 用户**:
```powershell
# 使用记事本创建
notepad .env

# 或使用 PowerShell
New-Item -Path .env -ItemType File -Force

# 或使用 VS Code
code .env
```

**确保**:
- 文件名确实是 `.env` (不是 `.env.txt`)
- 文件在项目根目录
- 包含正确的配置项

---

### 🔐 安全建议

#### 开发环境
- ✅ 使用 `.env` 文件存储敏感信息
- ✅ `.env` 文件已添加到 `.gitignore`
- ✅ 不要将 `.env` 提交到 Git

#### 生产环境
- ⚠️ 不要使用 `0.0.0.0/0` 允许所有 IP
- ⚠️ 使用强密码 (至少 16 字符)
- ⚠️ 启用 MongoDB Atlas 的审计日志
- ⚠️ 定期轮换密码和密钥
- ⚠️ 使用环境变量或密钥管理服务

#### .gitignore 检查

确认 `.gitignore` 包含:
```
.env
.env.local
.env.*.local
*.pyc
__pycache__/
```

---

### 📊 MongoDB Atlas 免费层限制

| 项目 | 免费 M0 | 说明 |
|------|---------|------|
| 存储空间 | 512 MB | 足够小型项目 |
| RAM | 共享 | 性能有限 |
| 连接数 | 500 | 并发连接 |
| 备份 | 无 | 需手动备份 |
| 集群数 | 1 个 | 每个项目 |
| 升级 | 随时 | 付费升级 |

---

### 🎯 下一步

✅ MongoDB Atlas 配置完成后:

1. **返回主指南**: 查看 `QUICK_START_GUIDE.md`
2. **运行应用**: `python app.py`
3. **测试功能**: 使用测试账号登录
4. **开始开发**: 创建新功能

---

## English Setup Guide

### 📋 Overview

This guide helps you create a free cloud database on MongoDB Atlas and configure it for this project.

**Time**: ~10-15 minutes  
**Cost**: Completely free (M0 free tier)

---

### Step 1: Register MongoDB Atlas Account

1. **Visit**: https://www.mongodb.com/cloud/atlas/register
2. **Choose registration method**:
   - Use Google account
   - Use GitHub account
   - Use email

3. **Fill basic information**:
   - Organization name (can be anything)
   - Project name: `Learning Platform` (or custom)

---

### Step 2: Create Free Cluster

1. **Choose deployment**:
   - Click **"Build a Database"** (or "Create")
   - Select **"Shared"** (free cluster)

2. **Choose cloud provider and region**:
   ```
   Provider: AWS / Google Cloud / Azure (any)
   Region: Choose closest to you
   
   Recommended:
   - China: Singapore (ap-southeast-1)
   - USA: N. Virginia (us-east-1)
   - Europe: Ireland (eu-west-1)
   ```

3. **Choose cluster tier**:
   - Select **M0 Sandbox** (free)
   - 512 MB storage
   - Shared RAM

4. **Name cluster**:
   - Cluster Name: `Cluster0` (default) or custom

5. **Click**: **"Create Cluster"**

⏳ **Wait 3-5 minutes for cluster creation**

---

### Step 3: Configure Database Access

#### 3.1 Create Database User

1. **Go to Database Access**:
   - Left menu → **"Database Access"**
   - Click **"Add New Database User"**

2. **Choose authentication**:
   - Select **"Password"**

3. **Set username and password**:
   ```
   Username: learningplatform_user
   Password: [Auto-generate] or [Custom]
   
   ⚠️ Important: Save the password, you'll need it
   ```

4. **Set privileges**:
   - Database User Privileges: **"Read and write to any database"**
   - Or select **"Atlas admin"**

5. **Click**: **"Add User"**

#### 3.2 Configure Network Access

1. **Go to Network Access**:
   - Left menu → **"Network Access"**
   - Click **"Add IP Address"**

2. **Choose access method**:

   **Option A - Allow all access (recommended for development)**:
   ```
   Click: "Allow Access from Anywhere"
   IP Address: 0.0.0.0/0
   Description: Allow all access
   ```

   **Option B - Only current IP**:
   ```
   Click: "Add Current IP Address"
   IP Address: [Auto-detected]
   Description: My current IP
   ```

3. **Click**: **"Confirm"**

---

### Step 4: Get Connection String

1. **Return to Database**:
   - Left menu → **"Database"** (or "Deployment")

2. **Click Connect**:
   - Find your cluster (Cluster0)
   - Click **"Connect"** button

3. **Choose connection method**:
   - Select **"Connect your application"**

4. **Choose driver and version**:
   ```
   Driver: Python
   Version: 3.6 or later
   ```

5. **Copy connection string**:
   ```
   mongodb+srv://learningplatform_user:<password>@cluster0.xxxxx.mongodb.net/
   ```

   **Example**:
   ```
   mongodb+srv://learningplatform_user:MySecurePass123@cluster0.ab1cd.mongodb.net/
   ```

---

### Step 5: Configure Project

#### 5.1 Create .env File

Create `.env` file in project root:

**Windows**:
```powershell
New-Item -Path .env -ItemType File
notepad .env
```

**macOS/Linux**:
```bash
touch .env
nano .env
```

#### 5.2 Add Configuration

Paste into `.env` file:

```env
# MongoDB Atlas Configuration
MONGO_URI=mongodb+srv://learningplatform_user:YOUR_PASSWORD_HERE@cluster0.xxxxx.mongodb.net/
DB_NAME=learning_platform

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Optional: GitHub Models API
GITHUB_TOKEN=your_github_token_here
```

#### 5.3 Replace Placeholders

1. **Replace `YOUR_PASSWORD_HERE`**:
   - Use password from Step 3.1
   - ⚠️ **Special characters need URL encoding**:
     ```
     @ → %40
     : → %3A
     / → %2F
     # → %23
     ? → %3F
     & → %26
     = → %3D
     ```

   **Example**:
   ```
   Original: Pass@word#123
   Encoded: Pass%40word%23123
   
   Full URI:
   mongodb+srv://learningplatform_user:Pass%40word%23123@cluster0.ab1cd.mongodb.net/
   ```

2. **Generate SECRET_KEY**:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy output and replace `your_secret_key_here`

---

### Step 6: Test Connection

#### 6.1 Create Test Script

Create `test_mongodb_connection.py`:

```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get connection string
mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')

print(f"Testing connection to: {db_name}")
print(f"URI: {mongo_uri[:50]}...")

try:
    # Connect to database
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # Test connection
    client.server_info()
    
    # Get database
    db = client[db_name]
    
    # List collections
    collections = db.list_collection_names()
    
    print("✅ Connection successful!")
    print(f"✅ Database: {db_name}")
    print(f"✅ Collections: {collections if collections else 'No collections yet'}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check MONGO_URI in .env file")
    print("2. Verify password is URL encoded")
    print("3. Check Network Access in MongoDB Atlas")
    print("4. Ensure IP is whitelisted")
```

#### 6.2 Run Test

```bash
# Activate virtual environment
.\Project3\Scripts\Activate.ps1  # Windows
source Project3/bin/activate      # macOS/Linux

# Run test
python test_mongodb_connection.py
```

**Expected output**:
```
Testing connection to: learning_platform
URI: mongodb+srv://learningplatform_user:***...
✅ Connection successful!
✅ Database: learning_platform
✅ Collections: No collections yet
```

---

### Step 7: Initialize Database

After successful connection, run initialization:

```bash
# Create database structure
python init_db.py

# Add sample data
python seed_database.py

# Create test accounts
python create_test_accounts.py
```

**Expected output**:
```
✅ Database initialized successfully
✅ Created 5 courses
✅ Created 13 activities
✅ Created 5 test accounts
```

---

### 🔍 Verify Installation

1. **Start application**:
   ```bash
   python app.py
   ```

2. **Visit**: http://localhost:5000

3. **Test login**:
   ```
   Username: student_demo
   Password: student123
   ```

4. **Check Dashboard**:
   - Should display course data
   - Should not show ERROR

---

### ❓ Common Issues

#### Issue 1: ServerSelectionTimeoutError

**Error message**:
```
pymongo.errors.ServerSelectionTimeoutError: 
No servers found yet, trying for 5 more seconds
```

**Possible causes**:
1. Network access not configured
2. IP not whitelisted
3. Connection string incorrect

**Solution**:
```bash
1. Check MongoDB Atlas Network Access
2. Add 0.0.0.0/0 or current IP
3. Wait 2-3 minutes for config to apply
4. Check MONGO_URI in .env file
```

#### Issue 2: Authentication failed

**Error message**:
```
pymongo.errors.OperationFailure: 
Authentication failed
```

**Solution**:
```bash
1. Check username is correct
2. Check password is correct
3. Verify special characters are URL encoded
4. Confirm user is created with correct permissions
```

#### Issue 3: Password contains special characters

**Problem**: Password has `@`, `#`, `/` etc.

**Solution**:

**Method A - URL encode** (recommended):
```python
# Use Python to encode password
from urllib.parse import quote_plus

password = "Pass@word#123"
encoded = quote_plus(password)
print(encoded)  # Pass%40word%23123
```

**Method B - Reset with simple password**:
1. Delete user in MongoDB Atlas Database Access
2. Create new user
3. Use password without special characters (e.g., `LearningPlatform123`)

---

### 🔐 Security Recommendations

#### Development Environment
- ✅ Use `.env` file for sensitive data
- ✅ `.env` is in `.gitignore`
- ✅ Don't commit `.env` to Git

#### Production Environment
- ⚠️ Don't use `0.0.0.0/0` to allow all IPs
- ⚠️ Use strong password (at least 16 characters)
- ⚠️ Enable MongoDB Atlas audit logs
- ⚠️ Rotate passwords and keys regularly
- ⚠️ Use environment variables or key management service

---

### 📊 MongoDB Atlas Free Tier Limits

| Item | Free M0 | Notes |
|------|---------|-------|
| Storage | 512 MB | Enough for small projects |
| RAM | Shared | Limited performance |
| Connections | 500 | Concurrent |
| Backup | None | Manual backup needed |
| Clusters | 1 | Per project |
| Upgrade | Anytime | Paid upgrade |

---

### 🎯 Next Steps

✅ After MongoDB Atlas configuration:

1. **Return to main guide**: See `QUICK_START_GUIDE.md`
2. **Run application**: `python app.py`
3. **Test features**: Login with test accounts
4. **Start development**: Create new features

---

**Last Updated**: 2025-10-12  
**Version**: 1.0  
**Maintainer**: Team 3
