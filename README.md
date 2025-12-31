# 🤖 多智能体系统实战教程

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)](https://python.langchain.com/docs/langgraph)
[![AutoGen](https://img.shields.io/badge/AutoGen-0.4+-orange.svg)](https://microsoft.github.io/autogen/)

一个全面的动手实践教程，用于构建**多智能体AI系统**。学习使用 LangGraph、AutoGen 和 Docker 沙盒编排智能体，重点构建**批评家智能体**架构。

---

## 🌟 为什么是多智能体 AI？

> *"IDE 的消亡并不是工程学的终结；它是手工作坊式工程学的终结。"*
> 
> — 摘自 [Agent 编排与软件开发未来](./docs/research/Agent%20编排与软件开发未来.md)

我们正处于软件工程史上最重大的范式转移之一：从**工匠时代**进入**编排器时代**。

| 工匠时代 (Artisan Era) | 编排器时代 (Orchestrator Era) |
|----------------------|------------------------------|
| 开发者手动编写每一行代码 | 开发者管理 AI 智能体舰队 |
| 瓶颈：人类思考和打字速度 | 瓶颈：验证和编排能力 |
| 重构代码以管理技术债务 | 重写比重构更快更经济 |
| IDE 是核心工具 | Agent Orchestration Dashboard |

**关键洞见：**

- 🏭 **"工厂化农业"假说**: 代码将由智能体舰队大规模生产，人类负责监督过程而非产品
- ⏱️ **"2000小时定律"**: 需要约一年的日常使用才能可靠预测 LLM 行为，建立信任
- 🧱 **"合并墙"**: 智能体生成 PR 的速度将超过人类审查能力，需要 AI 审查 AI
- 🎯 **Vibe Coder**: 新一代工程师专注于意图和架构，而非语法

> 📖 **深入阅读**: 
> - [Agent 编排与软件开发未来](./docs/research/Agent%20编排与软件开发未来.md) - 中文深度研究报告
> - [Agent Orchestration and Future of Software Development](./docs/research/Agent_Orchestration_and_Future_of_Software_Development.md) - English Version

---

## 📖 概述

本教程受软件开发中**"编排器时代"**愿景的启发，工程师正从编写代码转向管理AI智能体舰队。基于前沿研究和最佳实践，您将学习：

- 🔄 使用 **LangGraph** 构建有状态的智能体工作流
- 💬 使用 **AutoGen** 创建对话式多智能体系统  
- 🐳 实现安全的 **Docker 沙盒化**执行环境
- 🧠 使用 **Beads** 系统管理智能体记忆
- ✅ 构建用于代码质量保证的**批评家智能体**
- 📊 建立可观测性和评估管道

---

## 🎯 学习路径 (Learning Path)

| Week | Topic | Description |
|------|-------|-------------|
| 1 | [LangGraph 基础](./01_langgraph/) | Graph-based workflows, state management, conditional edges |
| 2 | [AutoGen 多智能体](./02_autogen/) | Conversational agents, group chat, code execution |
| 3 | [Docker 沙盒化](./03_docker_sandbox/) | Secure execution, OpenHands, container orchestration |
| 4 | [Beads 记忆系统](./04_beads/) | Agent memory, task decomposition, Git integration |
| 5 | [Critic Agent](./05_critic_agent/) | **Core Project** - Build a code review agent system |
| 6 | [评估与可观测性](./06_evaluation/) | Testing, metrics, CI/CD for agents |

---

## 🚀 快速开始

### 环境要求

- Python 3.10 或更高版本
- Docker Desktop（用于沙盒化）
- **Azure OpenAI** 或 OpenAI API 密钥

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/micerin/MultiAgents.git
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

# 复制环境模板
cp .env.example .env
# 编辑 .env 文件，填入您的 Azure OpenAI 配置
```

### 配置 Azure OpenAI

本教程使用 **Azure OpenAI** 作为默认 LLM 提供商。在 `.env` 文件中配置：

```bash
# Azure OpenAI（推荐）
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-01

# 或使用 OpenAI（可选）
# OPENAI_API_KEY=your-openai-key
```

### 运行第一个智能体

```bash
# 运行简单的 LangGraph 示例
python 01_langgraph/01_basics/hello_graph.py

# 或者从批评家智能体演示开始
python 05_critic_agent/examples/simple_critic.py
```

---

## 📁 项目结构

```
multiagent-tutorial/
├── README.md                          # 本文件
├── requirements.txt                   # Python 依赖
├── .env.example                       # 环境变量模板
├── .gitignore                         # Git 忽略规则
│
├── docs/                              # 文档
│   ├── research/                      # 研究论文和笔记
│   │   └── agent_orchestration.md     # 核心研究文档
│   ├── architecture/                  # 架构图
│   └── best_practices.md              # 最佳实践指南
│
├── 01_langgraph/                      # 第1周: LangGraph
│   ├── README.md
│   ├── 01_basics/
│   │   ├── hello_graph.py
│   │   ├── state_management.py
│   │   └── conditional_edges.py
│   ├── 02_patterns/
│   │   ├── planner_worker.py
│   │   ├── reflection_loop.py
│   │   └── human_in_loop.py
│   └── 03_tools/
│       ├── tool_calling.py
│       └── code_execution.py
│
├── 02_autogen/                        # 第2周: AutoGen
│   ├── README.md
│   ├── 01_basics/
│   │   ├── two_agent_chat.py
│   │   ├── group_chat.py
│   │   └── code_executor.py
│   ├── 02_patterns/
│   │   ├── user_proxy_pattern.py
│   │   ├── critic_pattern.py
│   │   └── nested_chat.py
│   └── 03_advanced/
│       └── custom_agents.py
│
├── 03_docker_sandbox/                 # 第3周: Docker 沙盒化
│   ├── README.md
│   ├── docker/
│   │   ├── Dockerfile.agent
│   │   ├── Dockerfile.sandbox
│   │   └── docker-compose.yml
│   ├── openhands/
│   │   └── setup.md
│   └── examples/
│       └── secure_execution.py
│
├── 04_beads/                          # 第4周: Beads 记忆系统
│   ├── README.md
│   ├── setup/
│   │   └── installation.md
│   └── examples/
│       ├── basic_tasks.py
│       └── langgraph_integration.py
│
├── 05_critic_agent/                   # 第5周: 核心项目 ⭐
│   ├── README.md
│   ├── src/
│   │   ├── __init__.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── coder.py
│   │   │   ├── critic.py
│   │   │   └── orchestrator.py
│   │   ├── rules/
│   │   │   ├── __init__.py
│   │   │   ├── code_quality.py
│   │   │   ├── security.py
│   │   │   └── style.py
│   │   ├── graph/
│   │   │   ├── __init__.py
│   │   │   ├── state.py
│   │   │   └── workflow.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── llm.py
│   │       └── tools.py
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_critic.py
│   └── examples/
│       ├── simple_critic.py
│       ├── hierarchical_critic.py
│       └── consensus_critic.py
│
├── 06_evaluation/                     # 第6周: 评估
│   ├── README.md
│   ├── metrics/
│   │   ├── agent_metrics.py
│   │   └── deepeval_tests.py
│   ├── observability/
│   │   ├── langsmith_setup.py
│   │   └── phoenix_setup.py
│   └── ci_cd/
│       └── github_actions.yml
│
└── shared/                            # 共享工具
    ├── __init__.py
    ├── config.py
    ├── llm_providers.py
    └── prompts/
        ├── coder_prompts.py
        └── critic_prompts.py
```

---

## 🏗️ 核心架构：Critic Agent (批评家智能体)

本项目的主要目标是构建一个用于自动化代码审查的 **Critic Agent** 系统：

### 架构模式 (Architecture Patterns)

#### Pattern 1: Simple Reflection Loop (入门级)
```
[Task] → [Coder] → [Critic] ─┐
             ↑                │
             └────────────────┘ (loop if rejected)
                     ↓
               [Final Output]
```

#### Pattern 2: Hierarchical Critics (中级)
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

#### Pattern 3: Multi-Agent Consensus (高级)
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

---

## 🔧 核心技术栈 (Tech Stack)

| 技术 | 用途 | 周次 |
|------|------|------|
| [LangGraph](https://python.langchain.com/docs/langgraph) | Graph-based agent orchestration | 1 |
| [AutoGen](https://microsoft.github.io/autogen/) | Conversational multi-agent | 2 |
| [Docker](https://www.docker.com/) | Sandboxed execution | 3 |
| [OpenHands](https://openhands.dev/) | AI coding platform | 3 |
| [Beads](https://github.com/steveyegge/beads) | Agent memory system | 4 |
| [DeepEval](https://github.com/confident-ai/deepeval) | Agent evaluation | 6 |
| [LangSmith](https://smith.langchain.com/) | Observability & tracing | 6 |

---

## 📚 核心概念

> 📖 **深入阅读**: 本项目基于对多智能体系统和软件开发未来的深度研究。请参阅完整研究报告：
> - [Agent 编排与软件开发未来](./docs/research/Agent%20编排与软件开发未来.md) - 中文版深度研究报告
> - [Agent Orchestration and Future of Software Development](./docs/research/Agent_Orchestration_and_Future_of_Software_Development.md) - English Version

### 来自研究报告的关键洞见 (Key Insights)

1. **"2000 Hour Rule"** (2000小时定律)：需要约一年的日常使用才能可靠预测LLM行为
2. **"Merge Wall"** (合并墙)：智能体生成PR的速度超过人类审查能力
3. **"Single Task Principle"** (单一任务原则)：给智能体分配小的、原子性的任务
4. **"Restart Frequently"** (频繁重启)：智能体会积累 "context drift"（上下文漂移）
5. **"Always Sandbox"** (始终沙盒化)：永远不要直接在主机操作系统上运行编码智能体

### 最佳实践 (Best Practices)

- ✅ **Decouple Planning from Execution** - 解耦规划与执行（Planner-Worker 模式）
- ✅ **Share State via Database/Filesystem** - 通过数据库/文件系统共享状态，而非上下文字符串
- ✅ **Explicit Handoffs** - 定义智能体之间的显式交接
- ✅ **Structured Memory over Markdown** - 使用结构化记忆（Beads）而非 Markdown 文件
- ✅ **Human-in-the-Loop (HITL)** - 为关键决策实现人机回环

---

## 🤝 贡献指南

欢迎贡献！请先阅读我们的[贡献指南](CONTRIBUTING.md)。

```bash
# Fork 并克隆
git clone https://github.com/micerin/MultiAgents.git

# 创建功能分支
git checkout -b feature/your-feature

# 进行更改并测试
pytest tests/

# 提交 PR
```

---

## 📖 参考资源

- [Latent Space 播客 - Steve Yegge 谈 Vibe Coding](https://podcasts.apple.com/us/podcast/latent-space-the-ai-engineer-podcast/id1674008350)
- [LangGraph 文档](https://python.langchain.com/docs/langgraph)
- [AutoGen 文档](https://microsoft.github.io/autogen/)
- [OpenHands GitHub](https://github.com/OpenHands/OpenHands)
- [Beads by Steve Yegge](https://github.com/steveyegge/beads)
- [CrewAI vs LangGraph vs AutoGen 对比](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 👤 作者

- **micerin** - [micerin@hotmail.com](mailto:micerin@hotmail.com)
- GitHub: [@micerin](https://github.com/micerin)

---

## ⭐ 星标历史

如果您觉得本教程有帮助，请给它一个星标！⭐

---

<p align="center">
  用 ❤️ 为 AI 智能体社区打造
</p>
