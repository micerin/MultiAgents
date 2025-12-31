# Week 2: AutoGen 多智能体

> Conversational multi-agent systems with flexible topology

## 📖 本周概述

Microsoft AutoGen 是一个强大的对话式多智能体框架，特别适合：

- **动态协作** - 智能体之间自由对话迭代
- **代码执行** - 内置安全的代码执行能力
- **灵活拓扑** - 支持多种智能体交互模式
- **群聊模式** - 多智能体同时参与讨论

## 🎯 学习目标

完成本周学习后，你将能够：

1. 创建 `ConversableAgent` 和 `UserProxyAgent`
2. 实现双智能体对话和群聊
3. 构建 Critic Pattern（批评家模式）
4. 理解 AutoGen 与 LangGraph 的差异

## 📁 目录结构

```
02_autogen/
├── README.md                 # 本文件
├── 01_basics/
│   ├── two_agent_chat.py     # 双智能体对话
│   ├── group_chat.py         # 群聊模式
│   └── code_executor.py      # 代码执行
├── 02_patterns/
│   ├── user_proxy_pattern.py # UserProxy + Assistant 模式
│   ├── critic_pattern.py     # 批评家模式 ⭐
│   └── nested_chat.py        # 嵌套对话
└── 03_advanced/
    └── custom_agents.py      # 自定义智能体
```

## 🚀 快速开始

### 安装依赖

```bash
pip install pyautogen
```

### 运行第一个示例

```bash
python 01_basics/two_agent_chat.py
```

## 📚 核心概念

### 1. 基础智能体类型

```python
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent

# 助手智能体（使用 LLM）
assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"}
)

# 用户代理（可执行代码）
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # ALWAYS, TERMINATE, NEVER
    code_execution_config={"work_dir": "coding"}
)
```

### 2. 双智能体对话

```python
# 启动对话
user_proxy.initiate_chat(
    assistant,
    message="Write a Python function to calculate fibonacci numbers."
)
```

### 3. 群聊模式（GroupChat）

```python
from autogen import GroupChat, GroupChatManager

# 创建多个智能体
coder = AssistantAgent(name="coder", ...)
reviewer = AssistantAgent(name="reviewer", ...)
tester = AssistantAgent(name="tester", ...)

# 创建群聊
groupchat = GroupChat(
    agents=[user_proxy, coder, reviewer, tester],
    messages=[],
    max_round=10
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
user_proxy.initiate_chat(manager, message="Build a REST API")
```

### 4. Critic Pattern（批评家模式）⭐

```python
# 编码智能体
coder = AssistantAgent(
    name="coder",
    system_message="You are a Python developer. Write clean, efficient code."
)

# 批评家智能体
critic = AssistantAgent(
    name="critic",
    system_message="""You are a code reviewer. Review code for:
    1. Correctness
    2. Security vulnerabilities
    3. Code style and best practices
    4. Performance issues
    
    Be specific and actionable in your feedback."""
)

# 对话流程：Coder -> Critic -> Coder (迭代)
```

## ⚠️ AutoGen 注意事项

### Token 成本控制

AutoGen 的对话模式可能导致大量 token 消耗：

```python
# 设置终止条件
def termination_check(msg):
    return "APPROVED" in msg.get("content", "")

assistant = AssistantAgent(
    name="assistant",
    is_termination_msg=termination_check,
    max_consecutive_auto_reply=5  # 限制自动回复次数
)
```

### 避免无限循环

```python
# 在群聊中设置最大轮次
groupchat = GroupChat(
    agents=[...],
    max_round=10,  # 重要！
    speaker_selection_method="round_robin"  # 或 "auto", "manual"
)
```

## 🔗 AutoGen vs LangGraph

| 场景 | 推荐框架 |
|------|----------|
| 确定性工作流 | LangGraph |
| 探索性对话 | AutoGen |
| 代码生成+执行 | AutoGen |
| 复杂状态管理 | LangGraph |
| 快速原型 | AutoGen |
| 生产部署 | LangGraph |

## 📖 参考资源

- [AutoGen 官方文档](https://microsoft.github.io/autogen/)
- [AutoGen GitHub](https://github.com/microsoft/autogen)
- [AutoGen Studio](https://github.com/microsoft/autogen/tree/main/samples/apps/autogen-studio) - 可视化界面

## ⏭️ 下一步

完成本周学习后，继续 [Week 3: Docker 沙盒化](../03_docker_sandbox/)
