# 贡献指南 | Contributing Guide

首先，感谢您考虑为本项目做出贡献！🎉

---

## 如何贡献？

### 报告 Bug

在创建 Bug 报告之前，请先检查现有 issues。创建 Bug 报告时，请包含尽可能多的详细信息：

- **使用清晰、描述性的标题**
- **描述重现问题的确切步骤**
- **提供具体示例**
- **描述您观察到的行为以及您期望的行为**
- **包含您的环境详情**（Python 版本、操作系统等）

### 功能建议

功能建议通过 GitHub Issues 跟踪。创建功能建议时：

- **使用清晰、描述性的标题**
- **提供建议功能的详细描述**
- **解释为什么这个功能会有用**

### Pull Requests

1. **Fork 仓库**并从 `main` 创建您的分支
2. **安装依赖**: `pip install -r requirements.txt`
3. **进行更改**
4. **添加测试**（如适用）
5. **确保测试通过**: `pytest tests/`
6. **更新文档**（如需要）
7. **提交您的 PR**

---

## 开发环境设置

```bash
# 克隆您的 fork
git clone https://github.com/your-username/MultiAgents.git
cd MultiAgents

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境文件
cp .env.example .env
# 编辑 .env 填入您的 API 密钥

# 运行测试
pytest tests/
```

---

## 代码风格

- 遵循 **PEP 8** 规范
- 使用 **Black** 格式化: `black .`
- 使用 **isort** 排序导入: `isort .`
- 尽可能添加**类型提示**
- 为函数和类编写**文档字符串**

---

## Commit 信息规范

- 使用现在时态（"Add feature" 而非 "Added feature"）
- 使用祈使语气（"Move cursor to..." 而非 "Moves cursor to..."）
- 第一行保持在 72 个字符以内
- 在相关时引用 issues 和 pull requests

### Commit 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（不增加功能或修复 bug）
- `test`: 添加或修改测试
- `chore`: 构建过程或辅助工具变动

示例：
```
feat: 添加 LangGraph reflection loop 示例
fix: 修复 critic agent 的状态管理问题
docs: 更新 README 安装说明
```

---

## 项目结构指南

添加新内容时：

- **周次模块** (`01_langgraph/` 等): 每个模块应有自己的 `README.md`
- **示例**: 应自包含且可运行
- **测试**: 放在 `tests/` 目录中，保持相应结构
- **文档**: 更新 `docs/` 中的相关文档

### 文件命名规范

- Python 文件: `snake_case.py`
- Markdown 文件: 描述性名称，可用中文
- 目录: `snake_case` 或数字前缀 (`01_langgraph`)

---

## 有问题？

欢迎开一个 issue 提出您的问题，或联系维护者。

- 📧 Email: [micerin@hotmail.com](mailto:micerin@hotmail.com)
- 🐙 GitHub: [@micerin](https://github.com/micerin)

感谢您的贡献！🙏
