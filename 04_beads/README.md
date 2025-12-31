# Week 4: Beads 记忆系统

> Agent memory management with Git integration

## 📖 本周概述

> **"Markdown is not memory"** - Markdown 不是记忆系统

Beads 是 Steve Yegge 开发的智能体记忆系统，解决了 "Agent Amnesia"（智能体失忆）问题：

- **结构化数据** - 任务有明确的字段（ID、状态、优先级、依赖）
- **Git 集成** - 随代码版本化，支持分支和合并
- **防冲突设计** - 基于哈希的唯一 ID
- **语义压缩** - Compaction 机制节省上下文窗口

## 🎯 学习目标

完成本周学习后，你将能够：

1. 安装和配置 Beads
2. 创建和管理结构化任务
3. 将 Beads 集成到 LangGraph 工作流
4. 实现多智能体任务分配

## 📁 目录结构

```
04_beads/
├── README.md                     # 本文件
├── setup/
│   └── installation.md           # 安装指南
└── examples/
    ├── basic_tasks.py            # 基础任务管理
    └── langgraph_integration.py  # LangGraph 集成
```

## 🚀 快速开始

### 安装 Beads

```bash
# 克隆 Beads 仓库
git clone https://github.com/steveyegge/beads.git

# 或使用 pip（如果已发布）
pip install beads
```

### 初始化项目

```bash
cd your-project
beads init
```

这将创建 `.beads/` 目录：

```
.beads/
├── config.json     # 配置文件
├── tasks.jsonl     # 任务数据库
└── archive/        # 已完成任务归档
```

## 📚 核心概念

### 1. 为什么不用 Markdown？

传统智能体使用 `TODO.md` 或 `plan.md` 跟踪状态，但这存在问题：

| Markdown | Beads |
|----------|-------|
| 非结构化文本 | 结构化 JSONL |
| LLM 需要解析 | 直接查询 |
| 容易产生幻觉 | 精确状态 |
| 合并冲突 | 哈希 ID 防冲突 |
| 上下文膨胀 | 语义压缩 |

### 2. 任务结构

```json
{
  "id": "bd-a1b2c3d4",
  "title": "Implement user authentication",
  "status": "in_progress",
  "priority": "high",
  "created": "2025-01-15T10:00:00Z",
  "dependencies": ["bd-e5f6g7h8"],
  "blocked_by": [],
  "parent": "bd-x9y0z1a2",
  "metadata": {
    "assigned_agent": "coder-1",
    "estimated_tokens": 5000
  }
}
```

### 3. 基础命令

```bash
# 创建任务
beads add "Implement OAuth2 login" --priority high

# 列出任务
beads list --status ready

# 查看就绪任务（无阻塞依赖）
beads ready

# 更新状态
beads update bd-a1b2 --status done

# 添加依赖
beads link bd-a1b2 --blocks bd-c3d4
```

### 4. Python API

```python
from beads import BeadsDB

# 初始化数据库
db = BeadsDB(".beads/")

# 创建任务
task = db.create_task(
    title="Implement user authentication",
    priority="high",
    metadata={"assigned_agent": "coder-1"}
)

# 查询就绪任务
ready_tasks = db.get_ready_tasks()

# 获取特定任务
task = db.get_task("bd-a1b2c3d4")

# 更新状态
db.update_task(task.id, status="done")

# 获取任务依赖图
graph = db.get_dependency_graph()
```

### 5. LangGraph 集成

```python
from langgraph.graph import StateGraph
from beads import BeadsDB
from typing import TypedDict

class AgentState(TypedDict):
    current_task: dict
    code: str
    review: str

db = BeadsDB(".beads/")

def get_next_task(state: AgentState) -> AgentState:
    """从 Beads 获取下一个就绪任务"""
    ready_tasks = db.get_ready_tasks()
    if ready_tasks:
        task = ready_tasks[0]
        db.update_task(task.id, status="in_progress")
        state["current_task"] = task.to_dict()
    return state

def complete_task(state: AgentState) -> AgentState:
    """标记任务完成"""
    task_id = state["current_task"]["id"]
    db.update_task(task_id, status="done")
    return state

# 构建工作流
graph = StateGraph(AgentState)
graph.add_node("get_task", get_next_task)
graph.add_node("execute", execute_task)
graph.add_node("complete", complete_task)
# ...
```

### 6. Compaction（语义压缩）

长时间运行后，已完成的任务会占用上下文空间。Beads 的 Compaction 机制：

```python
# 压缩已完成任务
db.compact(
    older_than_days=7,
    keep_summary=True  # 保留高级摘要
)
```

压缩后的任务：

```json
{
  "id": "bd-a1b2c3d4",
  "title": "Implement user authentication",
  "status": "done",
  "completed": "2025-01-16T15:30:00Z",
  "summary": "Added OAuth2 login with Google and GitHub providers"
}
```

## 🔄 Git 工作流

Beads 与 Git 无缝集成：

```bash
# 任务随代码一起版本化
git add .beads/
git commit -m "Add authentication tasks"

# 分支中的任务独立
git checkout -b feature/oauth
beads add "Implement OAuth flow"  # 只在此分支存在

# 合并时任务也合并（哈希 ID 防冲突）
git merge feature/oauth
```

## 📖 参考资源

- [Beads GitHub](https://github.com/steveyegge/beads)
- [Introducing Beads](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a)
- [Beads Best Practices](https://steve-yegge.medium.com/beads-best-practices-2db636b9760c)

## ⏭️ 下一步

完成本周学习后，继续 [Week 5: Critic Agent](../05_critic_agent/) - 核心项目！
