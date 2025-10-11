# Project3 虚拟环境使用指南

## 📦 虚拟环境说明

本项目已创建名为 **Project3** 的 Python 虚拟环境，用于隔离项目依赖，避免与系统 Python 包冲突。

---

## 🚀 快速启动（推荐）

### 方法 1: 使用批处理脚本（最简单）
双击运行或在终端执行：
```cmd
start_project3.bat
```

### 方法 2: 使用 PowerShell 脚本
```powershell
.\start_project3.ps1
```

这两个脚本会自动：
- ✅ 检查虚拟环境是否存在
- ✅ 检查并安装依赖
- ✅ 验证 .env 配置
- ✅ 启动应用

---

## 🔧 手动操作虚拟环境

### 1. 激活虚拟环境

#### PowerShell（如果遇到执行策略限制）
```powershell
# 临时允许执行脚本（本次会话）
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 激活虚拟环境
.\Project3\Scripts\Activate.ps1
```

#### CMD（推荐，无限制）
```cmd
.\Project3\Scripts\activate.bat
```

#### 直接使用 Python 可执行文件（无需激活）
```cmd
.\Project3\Scripts\python.exe <command>
```

### 2. 安装依赖
```cmd
# 激活后
pip install -r requirements.txt

# 或直接使用
.\Project3\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. 运行应用
```cmd
# 激活后
python app.py

# 或直接使用
.\Project3\Scripts\python.exe app.py
```

### 4. 退出虚拟环境
```cmd
deactivate
```

---

## 📋 常用命令速查

### 查看已安装的包
```cmd
.\Project3\Scripts\python.exe -m pip list
```

### 查看包详细信息
```cmd
.\Project3\Scripts\python.exe -m pip show <package_name>
```

### 更新单个包
```cmd
.\Project3\Scripts\python.exe -m pip install --upgrade <package_name>
```

### 初始化数据库
```cmd
.\Project3\Scripts\python.exe init_db.py
```

### 测试 AI 功能
```cmd
.\Project3\Scripts\python.exe test_ai.py
```

### 检查 Python 版本
```cmd
.\Project3\Scripts\python.exe --version
```

---

## 📦 已安装的依赖包

根据 `requirements.txt`，Project3 虚拟环境包含：

| 包名 | 版本 | 用途 |
|------|------|------|
| Flask | 3.0.0 | Web 框架 |
| pymongo | 4.6.0 | MongoDB 驱动 |
| python-dotenv | 1.0.0 | 环境变量管理 |
| openai | 1.3.0 | OpenAI/GitHub Models API |
| werkzeug | 3.0.1 | WSGI 工具库 |
| bcrypt | 4.1.1 | 密码加密 |
| pandas | 2.1.3 | CSV 数据处理 |

---

## 🔍 虚拟环境结构

```
Project3/
├── Scripts/           # Windows 可执行文件
│   ├── python.exe     # Python 解释器
│   ├── pip.exe        # 包管理器
│   ├── activate.bat   # CMD 激活脚本
│   ├── Activate.ps1   # PowerShell 激活脚本
│   └── flask.exe      # Flask 命令行工具
├── Lib/               # Python 库
│   └── site-packages/ # 安装的第三方包
├── Include/           # C 头文件
└── pyvenv.cfg         # 虚拟环境配置
```

---

## 🐛 常见问题

### Q1: PowerShell 无法运行激活脚本
**错误信息**：`无法加载文件...因为在此系统上禁止运行脚本`

**解决方案 1**：使用批处理文件
```cmd
.\Project3\Scripts\activate.bat
```

**解决方案 2**：临时修改执行策略
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\Project3\Scripts\Activate.ps1
```

**解决方案 3**：直接使用 Python 可执行文件（推荐）
```cmd
.\Project3\Scripts\python.exe app.py
```

### Q2: 依赖安装失败
**可能原因**：
- 网络连接问题
- pip 版本过旧

**解决方案**：
```cmd
# 升级 pip
.\Project3\Scripts\python.exe -m pip install --upgrade pip

# 使用国内镜像加速（可选）
.\Project3\Scripts\python.exe -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 如何确认虚拟环境已激活？
**CMD/PowerShell**：
- 命令提示符前会显示 `(Project3)`
- 例如：`(Project3) PS C:\...>`

**检查 Python 路径**：
```cmd
where python
# 应显示: C:\...\groupproject-team_3\Project3\Scripts\python.exe
```

### Q4: 如何重新创建虚拟环境？
```cmd
# 1. 删除现有虚拟环境
rmdir /s /q Project3

# 2. 重新创建
python -m venv Project3

# 3. 安装依赖
.\Project3\Scripts\python.exe -m pip install -r requirements.txt
```

### Q5: 虚拟环境占用多少空间？
通常约 **200-400 MB**，包括：
- Python 解释器副本
- 所有依赖包
- 编译的二进制文件

---

## 🎯 开发工作流程

### 首次设置
```cmd
1. python -m venv Project3                     # 创建虚拟环境
2. .\Project3\Scripts\python.exe -m pip install -r requirements.txt  # 安装依赖
3. 配置 .env 文件                               # 设置 API 密钥
4. .\Project3\Scripts\python.exe init_db.py    # 初始化数据库
5. .\Project3\Scripts\python.exe test_ai.py    # 测试 AI 功能
6. .\Project3\Scripts\python.exe app.py        # 启动应用
```

### 日常开发
```cmd
1. start_project3.bat                          # 一键启动
2. 访问 http://localhost:5000                  # 开发测试
3. Ctrl+C                                      # 停止服务器
```

### 添加新依赖
```cmd
1. .\Project3\Scripts\python.exe -m pip install <new_package>
2. .\Project3\Scripts\python.exe -m pip freeze > requirements.txt
3. git add requirements.txt
4. git commit -m "Add new dependency"
```

---

## 📊 虚拟环境 vs 全局 Python

| 特性 | 虚拟环境 (Project3) | 全局 Python |
|------|---------------------|-------------|
| 依赖隔离 | ✅ 独立 | ❌ 共享 |
| 版本冲突 | ✅ 无影响 | ❌ 可能冲突 |
| 项目可移植性 | ✅ 高 | ❌ 低 |
| 干净卸载 | ✅ 删除文件夹即可 | ❌ 需要逐个卸载 |
| 多项目管理 | ✅ 每个项目独立 | ❌ 共用同一环境 |

**推荐**：始终使用虚拟环境开发！

---

## 🔒 .gitignore 配置

`Project3/` 文件夹已添加到 `.gitignore`，不会被提交到 Git：

```gitignore
# Virtual Environment
Project3/
```

**原因**：
- 虚拟环境可以随时重建
- 包含大量文件（数千个）
- 不同操作系统不兼容

**团队协作**：
- 提交 `requirements.txt`
- 每个开发者创建自己的虚拟环境

---

## 🚀 部署到生产环境

### 1. 服务器上创建虚拟环境
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows Server
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### 2. 配置生产环境变量
```env
FLASK_ENV=production
SECRET_KEY=<生成强密钥>
```

### 3. 使用生产级服务器
```bash
# 安装 gunicorn (Linux)
pip install gunicorn

# 启动应用
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📚 相关文档

- **SETUP_GUIDE.md** - 完整安装配置指南
- **GITHUB_MODELS_SETUP.md** - GitHub Models API 使用指南
- **README.md** - 项目说明
- **QUICK_REFERENCE.md** - 快速参考指南

---

## ✅ 检查清单

开始开发前，确认：

- [ ] Python 3.8+ 已安装
- [ ] 虚拟环境 Project3 已创建
- [ ] 所有依赖已安装（7 个包）
- [ ] `.env` 文件已配置（API 密钥）
- [ ] 数据库已初始化（运行 init_db.py）
- [ ] AI 功能已测试（运行 test_ai.py）
- [ ] 应用可以正常启动

---

**最后更新**：2025年10月12日  
**虚拟环境名称**：Project3  
**Python 版本要求**：3.8+

🎉 **祝开发愉快！**
