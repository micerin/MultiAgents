# Week 1: LangGraph 基础

> Graph-based agent orchestration with state management

**✅ 已完成** | 使用 **Azure OpenAI** 作为 LLM 提供商

## 📖 本周概述

LangGraph 是构建生产级多智能体系统的首选框架，它将智能体工作流视为**图（Graph）**结构，提供：

- **循环图结构** - 支持 `编写 → 测试 → 失败 → 修复 → 测试 → 通过` 的迭代流程
- **细粒度状态控制** - 由状态（State）驱动的确定性控制流
- **持久化** - 支持 checkpointing 和"时间旅行"功能
- **人机回环（HITL）** - 在关键节点插入人工审核

## 🎯 学习目标

完成本周学习后，你将能够：

1. 理解 `StateGraph` 的核心概念
2. 创建带有条件边的智能体工作流
3. 实现 Planner-Worker 模式
4. 构建基础的 Reflection Loop（为 Critic Agent 做准备）

## 📁 目录结构

```
01_langgraph/
├── README.md                          # 本文件
├── 01_basics/
│   ├── hello_graph.py                 # ✅ 第一个 LangGraph 程序
│   ├── state_management.py            # ✅ 状态管理详解
│   ├── conditional_edges.py           # ✅ 条件边与循环
│   └── llm_providers_example.py       # ✅ LLM 提供商配置（Azure OpenAI）
├── 02_patterns/
│   ├── planner_worker.py              # ✅ Planner-Worker 模式
│   ├── reflection_loop.py             # ✅ 反思循环（Critic 基础）
│   └── human_in_loop.py               # ✅ 人机回环
└── 03_advanced/
    ├── multi_critic_system.py         # ✅ 多维度 Critic 系统
    └── multi_critic_challenge.py      # ✅ 挑战模式（迭代改进演示）
```

## 🚀 快速开始

### 安装依赖

```bash
pip install langchain langgraph langchain-openai python-dotenv
```

### 配置 Azure OpenAI

```bash
# 复制环境模板
cp .env.example .env

# 编辑 .env 文件，填入 Azure OpenAI 配置
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-01
```

### 运行示例

```bash
# 基础示例
python 01_basics/hello_graph.py
python 01_basics/state_management.py
python 01_basics/conditional_edges.py

# 模式示例
python 02_patterns/planner_worker.py
python 02_patterns/reflection_loop.py

# 高级 Critic 系统（使用真实 LLM）
python 03_advanced/multi_critic_system.py
python 03_advanced/multi_critic_challenge.py
```

## 📚 核心概念

### 1. StateGraph 基础

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# 定义状态结构
class AgentState(TypedDict):
    messages: list
    current_step: str

# 创建图
graph = StateGraph(AgentState)

# 添加节点
graph.add_node("process", process_function)
graph.add_node("review", review_function)

# 添加边
graph.add_edge("process", "review")
graph.add_conditional_edges(
    "review",
    should_continue,
    {"continue": "process", "end": END}
)

# 编译并运行
app = graph.compile()
```

### 2. 条件边（Conditional Edges）

条件边是实现循环和分支的关键：

```python
def should_continue(state: AgentState) -> str:
    """决定下一步走向"""
    if state["approved"]:
        return "end"
    if state["iteration"] >= state["max_iterations"]:
        return "end"
    return "continue"
```

### 3. Checkpointing（状态持久化）

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# 使用 SQLite 持久化
memory = SqliteSaver.from_conn_string(":memory:")
app = graph.compile(checkpointer=memory)

# 支持从特定节点恢复（时间旅行）
```

## 🔗 LangGraph vs 其他框架

| 特性 | LangGraph | AutoGen | CrewAI |
|------|-----------|---------|--------|
| 控制流 | 显式图定义 | 对话驱动 | 角色层级 |
| 状态管理 | 内置持久化 | 需自行实现 | 有限支持 |
| 循环支持 | ✅ 原生支持 | ⚠️ 需要控制 | ❌ 有限 |
| 学习曲线 | 较陡峭 | 中等 | 平缓 |
| 生产就绪 | ✅ | ⚠️ | ⚠️ |

## 🎓 已完成示例详解

### 基础 (01_basics/)

| 文件 | 学到的概念 |
|------|------------|
| `hello_graph.py` | StateGraph, add_node, add_edge, compile |
| `state_management.py` | TypedDict, Annotated, operator.add (累加器) |
| `conditional_edges.py` | 多分支路由, 循环控制, 错误重试 |
| `llm_providers_example.py` | Azure OpenAI, LangChain 集成 |

### 模式 (02_patterns/)

| 文件 | 学到的概念 |
|------|------------|
| `planner_worker.py` | 任务分解 → 执行 → 综合 |
| `reflection_loop.py` | Writer → Critic → 修改循环 |
| `human_in_loop.py` | interrupt_before, checkpointing |

### 高级 (03_advanced/)

| 文件 | 学到的概念 |
|------|------------|
| `multi_critic_system.py` | 并行 Critics, 加权评分, 完整审查流程 |
| `multi_critic_challenge.py` | 故意缺陷代码 → 迭代修复 → 质量提升 |

## 📊 LangGraph 局限性

| 局限 | 说明 |
|------|------|
| 静态图结构 | 编译后无法动态添加节点 |
| 共享状态 | 所有节点必须协商状态结构 |
| 无直接通信 | Agent 间通过状态传递（非对话式） |
| 调试困难 | 需要 LangSmith 或手动打印 |

## 📖 参考资源

- [LangGraph 官方文档](https://python.langchain.com/docs/langgraph)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangSmith](https://smith.langchain.com/) - 用于追踪调试
- [Azure OpenAI 文档](https://learn.microsoft.com/azure/ai-services/openai/)

## ⏭️ 下一步

完成本周学习后，继续 [Week 2: AutoGen 多智能体](../02_autogen/)
