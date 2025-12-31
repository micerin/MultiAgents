# Week 5: Critic Agent ⭐

> 核心项目 - 构建代码审查智能体系统

## 📖 项目概述

本周是整个教程的核心项目，我们将综合前四周所学，构建一个完整的 **Critic Agent（批评家智能体）** 系统，用于自动化代码审查。

> **Reflection/Critic Loop**: 智能体 A 编写代码；智能体 B（批评家）根据规则审查代码；智能体 A 根据反馈修改。这模仿了人类的代码审查过程。

## 🎯 学习目标

完成本周学习后，你将能够：

1. 设计和实现 Coder-Critic 循环架构
2. 定义多维度的代码审查规则
3. 使用 LangGraph 构建状态化工作流
4. 在 Docker 沙盒中安全执行代码
5. 集成 Beads 进行任务管理

## 📁 项目结构

```
05_critic_agent/
├── README.md                 # 本文件
├── src/
│   ├── __init__.py
│   ├── agents/               # 智能体定义
│   │   ├── __init__.py
│   │   ├── coder.py          # 编码智能体
│   │   ├── critic.py         # 批评家智能体
│   │   └── orchestrator.py   # 编排器
│   ├── rules/                # 审查规则
│   │   ├── __init__.py
│   │   ├── code_quality.py   # 代码质量
│   │   ├── security.py       # 安全检查
│   │   └── style.py          # 代码风格
│   ├── graph/                # LangGraph 工作流
│   │   ├── __init__.py
│   │   ├── state.py          # 状态定义
│   │   └── workflow.py       # 工作流图
│   └── utils/                # 工具函数
│       ├── __init__.py
│       ├── llm.py            # LLM 配置
│       └── tools.py          # 工具集
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/
│   ├── __init__.py
│   └── test_critic.py
└── examples/
    ├── simple_critic.py      # 简单示例
    ├── hierarchical_critic.py # 层级批评家
    └── consensus_critic.py   # 共识机制
```

## 🚀 快速开始

### 安装依赖

```bash
cd 05_critic_agent
pip install -r requirements.txt
```

### 运行简单示例

```bash
python examples/simple_critic.py
```

## 🏗️ 架构设计

### Pattern 1: Simple Reflection Loop

最基础的 Coder-Critic 循环：

```
[Task] → [Coder] → [Critic] ─┐
             ↑                │
             └────────────────┘ (loop if rejected)
                     ↓
               [Final Output]
```

### Pattern 2: Hierarchical Critics

多专业批评家层级：

```
                [Orchestrator]
                      ↓
         ┌───────────┼───────────┐
         ↓           ↓           ↓
    [Frontend]  [Backend]   [Security]
     [Critic]   [Critic]    [Critic]
         └───────────┼───────────┘
                     ↓
              [Meta Critic]
```

### Pattern 3: Multi-Agent Consensus

多智能体投票共识：

```
[Task] → [Planner] → [Decompose]
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
[Agent 1] [Agent 2] [Agent 3]
    ↓         ↓         ↓
[Critic 1] [Critic 2] [Critic 3]
    └─────────┼─────────┘
              ↓
      [Consensus Engine]
```

## 📚 核心代码

### 1. 状态定义 (`src/graph/state.py`)

```python
from typing import TypedDict, List, Optional
from enum import Enum

class ReviewStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"

class CriticState(TypedDict):
    # 任务信息
    task: str
    requirements: List[str]
    
    # 代码状态
    code: str
    language: str
    
    # 审查状态
    critique: str
    review_status: ReviewStatus
    issues: List[dict]
    
    # 迭代控制
    iteration: int
    max_iterations: int
    
    # 历史记录
    history: List[dict]
```

### 2. 编码智能体 (`src/agents/coder.py`)

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class CoderAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Python developer.
Write clean, efficient, and well-documented code.
Follow PEP 8 style guidelines.
Include type hints and docstrings."""),
            ("human", """Task: {task}

Requirements:
{requirements}

{revision_instructions}

Write the code:""")
        ])
    
    def generate(self, state: CriticState) -> str:
        revision = ""
        if state["iteration"] > 0:
            revision = f"""
Previous code was rejected. Issues found:
{state['critique']}

Please fix these issues and regenerate the code."""
        
        chain = self.prompt | self.llm
        response = chain.invoke({
            "task": state["task"],
            "requirements": "\n".join(state["requirements"]),
            "revision_instructions": revision
        })
        return response.content
```

### 3. 批评家智能体 (`src/agents/critic.py`)

```python
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class CriticAgent:
    def __init__(self, llm: ChatOpenAI, rules: List[str]):
        self.llm = llm
        self.rules = rules
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code reviewer.
Review the code against the following criteria:
{rules}

Be specific and actionable in your feedback.
If the code passes all criteria, respond with "APPROVED".
Otherwise, list specific issues that need to be fixed."""),
            ("human", """Task: {task}

Code to review:
```{language}
{code}
```

Provide your review:""")
        ])
    
    def review(self, state: CriticState) -> dict:
        chain = self.prompt | self.llm
        response = chain.invoke({
            "rules": "\n".join(f"- {r}" for r in self.rules),
            "task": state["task"],
            "language": state["language"],
            "code": state["code"]
        })
        
        content = response.content
        approved = "APPROVED" in content.upper()
        
        return {
            "critique": content,
            "approved": approved,
            "issues": self._parse_issues(content) if not approved else []
        }
    
    def _parse_issues(self, critique: str) -> List[dict]:
        # 解析批评中的具体问题
        issues = []
        # ... 解析逻辑
        return issues
```

### 4. LangGraph 工作流 (`src/graph/workflow.py`)

```python
from langgraph.graph import StateGraph, END
from .state import CriticState, ReviewStatus

def create_critic_workflow(coder: CoderAgent, critic: CriticAgent):
    
    def coder_node(state: CriticState) -> CriticState:
        """生成或修改代码"""
        code = coder.generate(state)
        state["code"] = code
        state["iteration"] += 1
        return state
    
    def critic_node(state: CriticState) -> CriticState:
        """审查代码"""
        result = critic.review(state)
        state["critique"] = result["critique"]
        state["issues"] = result["issues"]
        state["review_status"] = (
            ReviewStatus.APPROVED if result["approved"] 
            else ReviewStatus.NEEDS_REVISION
        )
        
        # 记录历史
        state["history"].append({
            "iteration": state["iteration"],
            "code": state["code"],
            "critique": state["critique"],
            "status": state["review_status"].value
        })
        return state
    
    def should_continue(state: CriticState) -> str:
        """决定是否继续迭代"""
        if state["review_status"] == ReviewStatus.APPROVED:
            return "end"
        if state["iteration"] >= state["max_iterations"]:
            return "end"
        return "coder"
    
    # 构建图
    workflow = StateGraph(CriticState)
    
    workflow.add_node("coder", coder_node)
    workflow.add_node("critic", critic_node)
    
    workflow.set_entry_point("coder")
    workflow.add_edge("coder", "critic")
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {"coder": "coder", "end": END}
    )
    
    return workflow.compile()
```

### 5. 审查规则 (`src/rules/`)

```python
# code_quality.py
CODE_QUALITY_RULES = [
    "Code should be DRY (Don't Repeat Yourself)",
    "Functions should do one thing and do it well",
    "Variable names should be descriptive",
    "Complex logic should be commented",
    "Error handling should be comprehensive",
]

# security.py
SECURITY_RULES = [
    "No hardcoded credentials or secrets",
    "Input should be validated and sanitized",
    "SQL queries should use parameterized statements",
    "File operations should check for path traversal",
    "Sensitive data should not be logged",
]

# style.py
STYLE_RULES = [
    "Follow PEP 8 style guidelines",
    "Use type hints for function parameters and returns",
    "Include docstrings for classes and functions",
    "Line length should not exceed 88 characters",
    "Imports should be organized (stdlib, third-party, local)",
]
```

## 🧪 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_critic.py -v

# 带覆盖率
pytest tests/ --cov=src
```

## 🐳 Docker 部署

```bash
# 构建镜像
docker build -t critic-agent .

# 运行
docker-compose up -d
```

## 📊 评估指标

使用 DeepEval 评估 Critic Agent 效果：

```python
from deepeval import assert_test
from deepeval.metrics import GEval

def test_critic_effectiveness():
    metric = GEval(
        name="Critique Quality",
        criteria="""Evaluate if the critique is:
        1. Specific and actionable
        2. Correctly identifies issues
        3. Provides constructive feedback""",
    )
    # ... 测试代码
```

## 📖 参考资源

- [LangGraph Reflection Tutorial](https://langchain-ai.github.io/langgraph/tutorials/reflection/reflection/)
- [AutoGen Critic Pattern](https://microsoft.github.io/autogen/docs/topics/prompting-and-reasoning/reflection/)

## ⏭️ 下一步

完成本周学习后，继续 [Week 6: 评估与可观测性](../06_evaluation/)
