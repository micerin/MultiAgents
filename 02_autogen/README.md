# Week 2: AutoGen 多智能体

> Conversational multi-agent systems with flexible topology

**使用 AutoGen 0.4+ 新 API** | **Azure OpenAI**

## 📖 本周概述

Microsoft AutoGen 是一个强大的对话式多智能体框架，特别适合：

- **动态协作** - 智能体之间自由对话迭代
- **代码执行** - 内置安全的代码执行能力
- **灵活拓扑** - 支持多种智能体交互模式
- **群聊模式** - 多智能体同时参与讨论

## 🆚 AutoGen vs LangGraph

| 特性 | AutoGen | LangGraph |
|------|---------|-----------|
| 编排方式 | 对话驱动 | 图结构驱动 |
| 通信方式 | 直接消息传递 | 共享状态 |
| 控制流 | 隐式/动态 | 显式/确定性 |
| 代码量 | 较少 | 较多 |
| 灵活性 | 高 | 中 |
| 可预测性 | 低 | 高 |

## 🎯 学习目标

完成本周学习后，你将能够：

1. 使用 AutoGen 0.4+ 新 API 创建 Agent
2. 实现双智能体对话和群聊
3. 构建 Critic Pattern（批评家模式）
4. 理解 AutoGen 与 LangGraph 的差异

## 📁 目录结构

```
02_autogen/
├── README.md                          # 本文件
├── 01_basics/
│   ├── hello_autogen.py               # ✅ 第一个 AutoGen 程序
│   └── two_agent_chat.py              # ✅ 双智能体对话（Writer + Critic）
├── 02_patterns/
│   ├── group_chat.py                  # ✅ 群聊模式（Planner + Coder + Reviewer）
│   └── critic_pattern.py              # ✅ Critic 模式 + AutoGen vs LangGraph 对比
└── 03_advanced/
    └── (coming soon)
```

## 🚀 快速开始

### 安装依赖

```bash
pip install autogen-agentchat autogen-ext[openai]
```

### 运行示例

```bash
# 基础
python 01_basics/hello_autogen.py
python 01_basics/two_agent_chat.py

# 模式
python 02_patterns/group_chat.py
python 02_patterns/critic_pattern.py
```

## 📚 核心概念（AutoGen 0.4+）

### 1. 模型客户端（Azure OpenAI）

```python
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

model_client = AzureOpenAIChatCompletionClient(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment="gpt-4o",
    api_version="2024-02-01",
    model="gpt-4o",
)
```

### 2. AssistantAgent

```python
from autogen_agentchat.agents import AssistantAgent

agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    system_message="你是一个友好的AI助手。",
)
```

### 3. 团队协作（RoundRobinGroupChat）

```python
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

team = RoundRobinGroupChat(
    [writer, critic],
    termination_condition=TextMentionTermination("TERMINATE"),
)
result = await team.run(task="写代码...")
```

### 4. 代码执行（CodeExecutorAgent）

```python
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

# 创建本地执行器
code_executor = LocalCommandLineCodeExecutor(work_dir="/tmp", timeout=60)

# 创建执行 Agent
executor = CodeExecutorAgent(
    name="Executor",
    code_executor=code_executor,
)
```

## ⚠️ AutoGen 注意事项

### Token 成本控制

```python
# 使用终止条件限制对话轮数
from autogen_agentchat.conditions import MaxMessageTermination

termination = MaxMessageTermination(10)  # 最多 10 条消息
```

### 代码执行安全

```python
# 开发环境：LocalCommandLineCodeExecutor（快但不安全）
# 生产环境：DockerCommandLineCodeExecutor（Week 3 详解）
```

```python
# 在群聊中设置最大轮次
groupchat = GroupChat(
    agents=[...],
## 🔗 AutoGen vs LangGraph

| 场景 | 推荐框架 |
|------|----------|
| 确定性工作流 | LangGraph |
| 探索性对话 | AutoGen |
| 代码生成+执行 | AutoGen |
| 复杂状态管理 | LangGraph |
| 快速原型 | AutoGen |
| 生产部署 | LangGraph |

## 🎓 已完成示例

| 文件 | 功能 | 关键概念 |
|------|------|----------|
| `01_basics/hello_autogen.py` | 单 Agent 对话 | AssistantAgent, 模型客户端 |
| `01_basics/two_agent_chat.py` | Writer + Critic 对话 | RoundRobinGroupChat, 终止条件 |
| `02_patterns/group_chat.py` | 三人群聊协作 | SelectorGroupChat, LLM 选择发言者 |
| `02_patterns/critic_pattern.py` | Critic 模式对比 | AutoGen vs LangGraph 差异 |
| `02_patterns/code_executor.py` | 本地代码执行 | CodeExecutorAgent, LocalExecutor |

## 📖 参考资源

- [AutoGen 官方文档](https://microsoft.github.io/autogen/)
- [AutoGen GitHub](https://github.com/microsoft/autogen)
- [AutoGen 0.4 迁移指南](https://microsoft.github.io/autogen/docs/migration-guide)

## ⏭️ 下一步

完成本周学习后，继续 [Week 3: Docker 沙盒化](../03_docker_sandbox/)
