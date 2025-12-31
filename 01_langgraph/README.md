# Week 1: LangGraph 基础

> Graph-based agent orchestration with state management

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
├── README.md                 # 本文件
├── 01_basics/
│   ├── hello_graph.py        # 第一个 LangGraph 程序
│   ├── state_management.py   # 状态管理详解
│   └── conditional_edges.py  # 条件边与循环
├── 02_patterns/
│   ├── planner_worker.py     # Planner-Worker 模式
│   ├── reflection_loop.py    # 反思循环（Critic 基础）
│   └── human_in_loop.py      # 人机回环
└── 03_tools/
    ├── tool_calling.py       # 工具调用
    └── code_execution.py     # 代码执行能力
```

## 🚀 快速开始

### 安装依赖

```bash
pip install langchain langgraph langchain-openai
```

### 运行第一个示例

```bash
python 01_basics/hello_graph.py
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

## 📖 参考资源

- [LangGraph 官方文档](https://python.langchain.com/docs/langgraph)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangSmith](https://smith.langchain.com/) - 用于追踪调试

## ⏭️ 下一步

完成本周学习后，继续 [Week 2: AutoGen 多智能体](../02_autogen/)
