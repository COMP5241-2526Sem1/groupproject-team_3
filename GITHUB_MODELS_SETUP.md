# 🚀 使用 GitHub Models API 指南

## 什么是 GitHub Models？

GitHub Models 是 GitHub 提供的免费 AI 模型访问服务，让开发者可以使用包括 GPT-4o-mini 在内的多个 AI 模型，而无需直接支付 OpenAI API 费用。

### ✨ 优势
- ✅ **免费使用**：使用 GitHub 账号即可访问
- ✅ **兼容 OpenAI API**：代码无需大改
- ✅ **支持多个模型**：包括 GPT-4o-mini, GPT-4o 等
- ✅ **适合开发测试**：无需信用卡

### ⚠️ 限制
- 有请求速率限制（通常足够开发使用）
- 不适合大规模生产环境
- 需要有效的 GitHub 账号

---

## 📝 获取 GitHub Personal Access Token (PAT)

### 步骤 1: 访问 GitHub 设置
前往：https://github.com/settings/tokens

或者：
1. 登录 GitHub
2. 点击右上角头像 → Settings
3. 左侧菜单最底部 → Developer settings
4. Personal access tokens → Tokens (classic)

### 步骤 2: 生成新 Token
1. 点击 **Generate new token** → **Generate new token (classic)**
2. 填写 Note（例如：`Learning Activity System AI`）
3. 设置过期时间（建议选择 90 days 或 No expiration）
4. **不需要勾选任何权限**（用于 GitHub Models 不需要仓库权限）
5. 点击底部 **Generate token** 按钮

### 步骤 3: 复制 Token
⚠️ **重要**：Token 只显示一次！立即复制保存！

Token 格式：
- 新版：`github_pat_11XXXXXXXXXXXXXX...`
- 旧版：`ghp_XXXXXXXXXXXXXXXX...`

---

## ⚙️ 配置您的应用

### 1. 编辑 `.env` 文件

打开项目根目录的 `.env` 文件，更新以下内容：

```env
# 使用 GitHub Models API
OPENAI_API_KEY=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
OPENAI_MODEL=gpt-4o-mini
```

### 2. 验证配置

运行以下命令测试 API 连接：

```powershell
python -c "from services.genai_service import GenAIService; service = GenAIService(); print('✅ GitHub Models API 配置成功!')"
```

如果看到 `✅ GitHub Models API 配置成功!`，说明配置正确！

---

## 🔄 程序已自动适配

我们的程序已经自动检测 API key 类型：

```python
# services/genai_service.py 中的智能检测
if api_key.startswith('github_pat_') or api_key.startswith('ghp_'):
    # 自动使用 GitHub Models API 端点
    self.client = OpenAI(
        api_key=api_key,
        base_url="https://models.inference.ai.azure.com"
    )
    logger.info("Using GitHub Models API endpoint")
else:
    # 使用标准 OpenAI API
    self.client = OpenAI(api_key=api_key)
    logger.info("Using OpenAI API endpoint")
```

**您无需修改任何代码**，只需在 `.env` 中填入正确的 GitHub PAT！

---

## 🎯 支持的 AI 功能

使用 GitHub Models，您可以完整使用所有 AI 功能：

### 1. ✅ AI 生成学习活动
- **投票活动** (Poll)：自动生成选择题
- **简答题** (Short Answer)：生成开放式问题
- **词云活动** (Word Cloud)：生成关键词提示

**示例**：
```
输入教学内容："TCP/IP protocol and three-way handshake"
→ AI 自动生成相关的学习活动
```

### 2. ✅ AI 智能分组答案
- 语义相似度分析
- 自动分组学生回答
- 生成每组总结
- 识别常见误解

**示例**：
```
学生提交 20 份简答题答案
→ AI 自动分为 3-5 组（理解程度相似）
→ 每组显示共同特点和关键词
```

---

## 🧪 测试 AI 功能

### 快速测试脚本

创建 `test_ai.py` 文件：

```python
from services.genai_service import GenAIService

# 初始化服务
service = GenAIService()

# 测试 1: 生成活动
print("测试 1: 生成学习活动")
result = service.generate_activity(
    teaching_content="TCP/IP protocol",
    activity_type="poll"
)
print(f"✅ 生成成功: {result.get('title', 'N/A')}")

# 测试 2: 分组答案
print("\n测试 2: 分组答案")
test_answers = [
    {"student_name": "Alice", "text": "TCP uses a three-way handshake with SYN, SYN-ACK, and ACK"},
    {"student_name": "Bob", "text": "Three-way handshake establishes connection between client and server"}
]
result = service.group_answers(test_answers, "Explain TCP handshake")
print(f"✅ 分组成功: {len(result.get('groups', []))} 组")

print("\n🎉 所有测试通过！GitHub Models API 工作正常！")
```

运行测试：
```powershell
python test_ai.py
```

---

## 📊 速率限制说明

GitHub Models 有以下限制（可能会变化）：

| 模型 | 每分钟请求数 | 每天请求数 |
|------|-------------|-----------|
| gpt-4o-mini | 10-15 | 150-200 |
| gpt-4o | 5-10 | 50-100 |

**建议**：
- 开发测试完全够用
- 生产环境考虑 OpenAI API
- 可以实现请求缓存减少调用

---

## 🔄 切换回 OpenAI API

如果您以后想切换回 OpenAI API：

### 1. 获取 OpenAI API Key
访问：https://platform.openai.com/api-keys

### 2. 更新 `.env`
```env
# 切换为 OpenAI API
OPENAI_API_KEY=sk-proj-your-openai-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 3. 重启应用
程序会自动检测并使用 OpenAI API！

---

## 🐛 常见问题

### Q1: Token 无效错误
```
Error: Invalid API key
```

**解决方案**：
1. 确认 Token 复制完整（包括 `github_pat_` 前缀）
2. 检查 Token 是否过期
3. 重新生成新 Token

### Q2: 速率限制错误
```
Error: Rate limit exceeded
```

**解决方案**：
1. 等待几分钟后重试
2. 减少 AI 功能使用频率
3. 考虑升级到 OpenAI API

### Q3: 模型不支持错误
```
Error: Model not found
```

**解决方案**：
确保 `.env` 中的模型名称为：
- `gpt-4o-mini` ✅ （推荐）
- `gpt-4o` ✅
- `gpt-4-turbo-preview` ❌ （不支持）

---

## 🎓 推荐使用场景

### ✅ 适合使用 GitHub Models：
- 课程开发和测试
- 小规模班级（<50 学生）
- 演示和原型验证
- 预算有限的项目

### ⚠️ 考虑使用 OpenAI API：
- 大规模部署（>100 学生）
- 高频率使用（每天 >100 次 AI 调用）
- 生产环境
- 需要更高速率限制

---

## 📞 获取帮助

### GitHub Models 文档
- 官方文档：https://github.com/marketplace/models

### 本项目支持
- 查看 `SETUP_GUIDE.md` 完整安装指南
- 查看 `README.md` 项目说明
- 查看应用日志了解 API 调用情况

---

## ✅ 配置检查清单

在启动应用前，确认：

- [ ] 已获取 GitHub Personal Access Token
- [ ] Token 已正确填入 `.env` 文件的 `OPENAI_API_KEY`
- [ ] `.env` 中 `OPENAI_MODEL=gpt-4o-mini`
- [ ] 运行测试脚本验证连接
- [ ] MongoDB 配置正确
- [ ] 已安装所有依赖 (`pip install -r requirements.txt`)

---

**最后更新**：2025年10月12日  
**适用版本**：Learning Activity System v1.0.0

🎉 **现在您可以免费使用 AI 功能了！**
