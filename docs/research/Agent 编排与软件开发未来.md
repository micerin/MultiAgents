# 代码的工业化革命：编排器时代、Vibe Coder 的崛起与多智能体系统架构深度研究报告

## 1. 引言：后 IDE 时代的各种可能性

软件工程领域正处于一场自汇编语言转向高级语言以来未曾有过的范式转移。几十年来，集成开发环境（IDE）一直是软件工匠的主要工作台——一个数字化的铁砧，人类在上面通过敲击键盘，一行行地锻造、重构和调试代码。然而，随着 2025 年的临近，这种"工匠模式"正面临着一种全新工业化范式的猛烈冲击。

以 Steve Yegge 为代表的行业先驱们提出了"IDE 已死"的激进论断，并宣告"编排器时代（Orchestrator Era）"的到来。这一转变不仅仅是关于更智能的代码补全，它代表着从"自给自足的农业模式"——开发者精心照料每一个函数——向"约翰·迪尔（John Deere）式的工厂化农业"转变。在这个新时代，工程师管理的不再是代码行，而是能够大规模生成、测试和维护软件的智能体（Agent）舰队 1。

本报告旨在对这一转型进行详尽的分析。我们将解构编排器时代的理论基础，剖析"Vibe Coder（直觉编码者）"这一新兴角色的解剖结构，并对在生产环境中管理多智能体系统（Multi-Agent Systems, MAS）所需的框架、工具和最佳实践进行严谨的技术调研。我们将探讨软件开发的抽象层是如何从语法上升到语义，以及工程师的角色是如何从代码的撰写者演变为智能的架构师。

### 1.1 核心论点：从工匠到工厂管理者

推动这一转变的核心论点是，大型语言模型（LLM）的能力已经跨越了一个临界点，在这个临界点上，人类在语法层面的干预正在从必要性转变为瓶颈。Steve Yegge 对 2025 年的预测指出，重写代码将比重构代码更快，这是由代理系统驱动的，它们可以在几分钟内根据新的规格说明重新生成整个代码库 1。在这种"代码工厂化农业"时代，工作的基本单位不再是 commit，而是**意图（Intent）**，由一群专门的智能体负责执行。

### 1.2 报告范围

本文件将深入探讨这场技术革命的三个同心圆：

1. **哲学与理论：** 分析 Yegge 的预测、"Vibe Coding"宣言以及"2000 小时定律"的社会技术影响 1。  
2. **架构与模式：** 评估支持多智能体协作的框架（LangGraph, CrewAI, AutoGen, MetaGPT）和设计模式（Planner-Worker, Swarms）4。  
3. **基础设施与工具：** 详细介绍实施这些系统所需的工具链（OpenHands, Beads, Docker）、可观测性（Arize Phoenix, DeepEval）以及针对智能体的 CI/CD 工作流 6。

---

## 2. IDE 的消亡与编排器的崛起：理论框架

"IDE 已死"这一断言虽然具有挑衅性，但它反映了开发者注意力从文本编辑器向代理仪表盘（Agent Dashboards）转移的切实趋势。随着抽象层的提升，软件创造的机制正日益与打字这一物理行为解耦。

### 2.1 "工厂化农业"假说与代码生产力

Steve Yegge 的"工厂化农业"隐喻描述了这样一个未来：代码由自主智能体以工业规模生产，人类负责监督过程而非产品。正如现代农业依赖联合收割机和 GPS 而非锄头和镰刀，现代软件工程正在转向运行编码智能体（如 Claude Code 或 OpenHands）的编排器，这些编排器在计划、实施、审查和测试的连续循环中运行 1。

这从根本上转移了工程瓶颈。在工匠时代，瓶颈是人类思考逻辑和输入有效语法的速度。在工厂化农业时代，瓶颈变成了**验证（Verification）和编排（Orchestration）**。挑战不再是编写代码，而是验证智能体生成的代码雪崩是否满足系统的约束，并在不破坏存储库稳定性的情况下将其集成。

#### 2.1.1 重构的过时性与"一次性代码"

这一假说的推论是重构（Refactoring）的衰落。Yegge 认为，对于越来越多的代码库类别，从头重写现在比重构更快 1。当智能体可以根据更新的提示在几秒钟内重新生成模块时，通过痛苦的重构来管理技术债务的传统做法变得不再经济。这种"一次性代码（Disposable Code）"范式从根本上改变了软件维护的经济学。如果修改一个功能的成本接近于零，那么维护旧代码的价值也就随之消失。

### 2.2 "2000 小时定律"与信任赤字

采用这种新范式的一个关键障碍是信任。Yegge 提出了"2000 小时定律"，表明工程师在能够可靠地预测 LLM 的行为之前，大约需要一整年的日常使用 1。对 AI 系统的信任不是由能力（Capability）定义的——能力通常很高但不均匀——而是由**可预测性（Predictability）**定义的。

工程师经常陷入"热手谬误（Hot Hand Fallacy）"，即一连串成功的智能体输出导致自满，随后是一次灾难性的失败，例如智能体幻觉出一个不存在的依赖项或引入一个微妙的安全漏洞，甚至修改了生产环境的密码导致停机 1。编排器时代要求从将智能体拟人化（将其视为聪明的初级开发人员）转变为将其视为需要严格防护和概率管理的随机组件。

### 2.3 编排器界面：从文本缓冲区到任务图

如果 IDE 正在消亡，什么将取而代之？答案是**智能体编排仪表盘（Agent Orchestration Dashboard）**。这个界面不是为文本编辑设计的，而是为"舰队管理"设计的。它提供了以下方面的可见性：

* **智能体状态（Agent State）：** 智能体 A 正在处理什么任务？智能体 B 是否受阻？  
* **计划执行（Plan Execution）：** 任务图和依赖关系的各类可视化。  
* **资源消耗（Resource Consumption）：** Token 使用量、功能成本和容器健康状况。  
* **验证状态（Verification Status）：** 来自测试运行器和静态分析工具的实时反馈。

工具如 **OpenHands**（前身为 OpenDevin）和 **Beads**（Yegge 开发的问题跟踪系统）是这一新界面层的早期原型，它们将开发者的焦点从文件缓冲区转移到了任务图上 6。

---

## 3. Vibe Coding：新工程师的解剖学

"Vibe Coding（直觉编码/氛围编码）"已成为这一新开发模式的通俗术语。它描述了一种工作流，在这种工作流中，工程师专注于高层系统设计、能力和"Vibes"（应用程序的定性行为），而将具体的实现细节留给 AI 1。

### 3.1 定义 Vibe Coder

Vibe Coder 与传统程序员在与机器的主要交互模式上截然不同：

* **传统程序员：** 输入语法，管理控制流，手动解决依赖关系，关注 for 循环和变量命名。  
* **Vibe Coder：** 输入意图，审查行为，管理智能体协调，关注系统架构和功能交付。

Steve Yegge 和 Gene Kim 在他们即将出版的书籍 *Vibe Coding* 中指出，这并非针对非技术用户的"低代码"解决方案，而是针对理解函数、类和架构但跳过语法的工程师的一种超高生产力模式 1。Vibe Coder 必须精通**上下文工程（Context Engineering）**——这是一门向智能体提供正确信息（需求、约束、现有代码模式）以确保输出连贯性的艺术 12。

### 3.2 技能断层与"合并墙（Merge Wall）"

这一转变产生了一个反直觉的人口统计学影响。Yegge 指出，拥有 12-15 年经验的工程师——那些身份认同与对语法和传统工具（如 Vim/Emacs）的掌握紧密结合的人——通常是对 Vibe Coding 最具抵抗力的群体 1。相反，初级开发人员和"非程序员"正在迅速适应，有时能实现 10 倍的生产力提升。

然而，这种速度引发了新的危机：**合并墙（Merge Wall）**。随着智能体以超人的速度生成拉取请求（PR），人类审查者无法跟上。Vibe Coder 必须发展自动验证和"智能体代码审查"的技能，即使用一个 AI 来检查另一个 AI 的工作，并辅以严格的实施规则（Implementation Rules）1。

### 3.3 Vibe Coding 的工具链

Vibe coding 需要一个支持自然语言交互而非语法操作的工具链。

* **Claude Code / Anthropic Tools:** 许多 Vibe Coder 的主要引擎，提供处理复杂重构的高级推理能力 1。  
* **Cursor / Windsurf:** 集成 IDE 的智能体，允许"Tab 补全"式的 Vibe Coding。尽管 Yegge 认为这些相对于全栈编排器来说是"去年的技术"，但它们仍是当前的主流过渡工具 1。  
* **Beads:** 一个专门设计的记忆系统和问题跟踪器，旨在为智能体提供持久的上下文，解决长运行任务中常见的"智能体失忆（Agent Amnesia）"问题 9。

---

## 4. 多智能体编排：框架、模式与架构

要实现"工厂化代码"的愿景，开发人员必须超越单轮提示，转向多智能体系统（MAS）。2025 年，MAS 框架的格局已经成熟，为协调和状态管理提供了截然不同的哲学。

### 4.1 主流框架的深度比较与选型

市场已经围绕几个关键框架整合，每个框架都在控制与自主性之间进行了不同的权衡优化。

| 框架名称 | 核心哲学 | 适用场景 | 关键特性 | 局限性/弱点 |
| :---- | :---- | :---- | :---- | :---- |
| **LangGraph** | 基于图的状态机 | 复杂、确定性的工程流 | 循环图结构、细粒度状态控制、持久化、人机回环（HITL） | 学习曲线陡峭，需要显式定义边和节点 4 |
| **CrewAI** | 角色扮演团队 | 流程导向的任务 | 易于理解的角色定义（如研究员、作家）、顺序/层级流 | 结构相对刚性，处理动态循环和复杂分支能力较弱 5 |
| **Microsoft AutoGen** | 对话式群体 (Swarm) | 开放式协作与探索 | 多智能体对话、代码执行、灵活的拓扑结构 | 日志冗长（Chatty），难以控制精确流程，可能导致 Token 成本激增 5 |
| **MetaGPT** | 基于 SOP 的模拟 | 软件公司全流程模拟 | 角色特定的标准作业程序（SOP）（PRD -> 设计 -> 代码）、结构化输出 | 提示词开销大，流程较为死板的"瀑布式"模型 19 |
| **LlamaIndex** | 数据中心化智能体 | 重度 RAG 工作流 | 与向量存储、文档解析深度集成 | 相比 LangGraph，在复杂智能体协商和控制流方面关注较少 21 |

#### 4.1.1 LangGraph：工程化的确定性选择

LangGraph 已成为生产级工程的首选，因为它将智能体工作流视为**图（Graph）**（节点和边）。这允许定义循环依赖（Cyclic Dependencies），这对于编码任务至关重要（例如：*编写 -> 测试 -> 失败 -> 修复 -> 测试 -> 通过*）。与 AutoGen 的对话式流动不同，LangGraph 提供了状态持久化和"时间旅行"功能（从特定节点恢复），这对于长运行的工程任务是必不可少的 5。它支持由状态（State）驱动的确定性控制流，这对于避免智能体陷入死循环至关重要。

#### 4.1.2 AutoGen 和 CrewAI：协作与角色的权衡

AutoGen 在需要动态协作的场景中大放异彩，例如"用户代理"与"工程师代理"聊天以迭代细化需求。然而，其对话性质如果缺乏严格的门控，可能导致无限循环。CrewAI 强制执行更严格的基于角色的层级结构（例如，研究员、作家、编辑），这很好地映射了既定的业务流程，但对于需要高度灵活性和探索性的软件开发来说，可能会感到束缚 5。

### 4.2 编码智能体的关键架构模式

成功的编排依赖于为特定任务选择正确的交互模式。

#### 4.2.1 规划器-执行者模式 (Planner-Worker Pattern)

这是编码任务的主导模式。**规划器（Planner）**智能体将高级目标（例如"添加 OAuth 支持"）分解为一系列细粒度的步骤。**执行者（Worker）**智能体然后逐一执行这些步骤。

* *优势：* 防止"上下文窗口溢出"问题，将工作者聚焦于小的、隔离的任务。  
* *实现：* **ReWOO**（Reasoning Without Observation）和 **HuggingGPT** 等工具体现了这一点，将推理计划与工具执行解耦 22。这种模式使得工具的使用更加可预测和策略可执行。

#### 4.2.2 层级/群体模式 (Hierarchical/Swarm Pattern)

在这个模型中，一个**经理（Manager）**智能体监督一群专门的子智能体（例如前端专家、后端专家、DBA）。经理委派任务并汇总结果。

* *优势：* 并行性。如果任务解耦，前端和后端智能体可以同时工作。  
* *挑战：* 结果合并。正如 Yegge 所指出的，"合并墙"是当多个智能体同时提交代码时的限制因素。需要复杂的冲突解决策略 1。

#### 4.2.3 代码审查循环 (Reflection/Critic Loop)

质量保证的关键模式是**反思（Reflection）**循环。智能体 A 编写代码；智能体 B（批评家/Critic）根据一组规则（安全性、风格、逻辑）审查代码；智能体 A 根据反馈进行修改。这模仿了人类的代码审查过程，已被证明能显著提高在 HumanEval 和 SWE-bench 等基准测试上的成功率 13。

---

## 5. "Beads"系统：智能体记忆管理的案例研究

Steve Yegge 对智能体生态系统最具体的贡献之一是 **Beads**，这是一个旨在解决"智能体失忆（Agent Amnesia）"问题的系统。

### 5.1 问题：Markdown 不是记忆

传统的智能体通常使用 Markdown 文件（例如 TODO.md 或 plan.md）跟踪其状态。Yegge 认为这种方法注定失败，因为 Markdown 是非结构化文本，这就迫使 LLM 承担高昂的认知负荷来解析和更新它。智能体经常对任务状态产生幻觉，或者在进展过程中未能更新计划，导致上下文的"比特腐烂（bit-rot）"15。

### 5.2 解决方案：基于图的分布式问题跟踪

Beads 充当智能体的"外部海马体"。它是一个分布式的、基于 Git 的图形问题跟踪器，将任务作为结构化的 JSONL 数据存储在存储库的 .beads/ 目录中 9。

* **结构化数据：** 问题具有明确的字段（ID、状态、优先级）和依赖链接（blocks, blocked-by, parent-of）。这使得智能体可以通过查询获取准确的"就绪工作（Ready Work）"。  
* **Git 集成：** 由于数据库只是仓库中的一个文件，它会随代码一起分支和合并。如果智能体在功能分支中创建任务，该任务只存在于该分支中，直到合并。  
* **压缩（Compaction）：** Beads 实现了"语义记忆衰减"，总结已关闭的任务以节省上下文窗口空间，同时保留已完成工作的高级历史记录 9。

### 5.3 技术实现与防冲突机制

Beads 为任务分配唯一的基于哈希的 ID（例如 bd-a1b2），以防止合并冲突——这是当多个智能体（或人类）试图同时更新顺序 ID 列表时常见的问题 9。这种设计允许"隐形模式（Stealth Mode）"，即用户可以在共享项目中使用 Beads 而不污染主仓库的历史记录，或者使用"同步分支模式"进行团队协作 9。

对于 Vibe Coder 而言，Beads 是指挥智能体舰队的 API。工程师不再提示"修复这个错误"，而是创建一个带有依赖关系的 Beads 问题，编排层随后将该问题分配给特定的智能体 26。

---

## 6. 管理智能体舰队：基础设施与工具链

向"工厂化农业"转型需要能够运行、监控和扩展智能体的强大基础设施。在终端窗口中运行智能体的"笔记本电脑级"设置已不足以满足生产工作流的需求。

### 6.1 容器化与隔离：Docker 的核心地位

运行 LLM 生成的代码会带来重大的安全风险。智能体通常需要"沙盒"环境，在其中执行 shell 命令和修改文件，而不会危及主机系统。

* **Docker & Docker Compose:** 隔离的标准。工具如 **cagent** 允许开发人员使用简单的 YAML 文件定义多智能体系统，并在 Docker 容器中运行它们。Docker Compose 现在被宣传为构建 AI 智能体的构建块，允许在 compose.yaml 中定义模型、智能体和工具 27。  
* **OpenHands (OpenDevin):** 这个平台创建了一个安全的、沙盒化的 Linux 环境（运行在 Docker 中），智能体在其中与终端、代码编辑器和浏览器交互。它支持定义自定义运行时（例如，具有特定 Go 或 Python 依赖项的容器）以匹配生产环境 6。

### 6.2 "Git 感知"智能体的崛起

为了在团队中有效运作，智能体必须理解版本控制系统（VCS）。

* **上下文感知:** 像 **Aider** 和 **Claude Code** 这样的智能体是"Git 感知"的，这意味着它们会检查 .git 目录以了解项目历史、最近的更改和分支结构 32。  
* **冲突解决:** 解决合并冲突是一项高级认知任务。工具如 **CodeGPT** 和 **Resolve.AI** 分析冲突标记（`<<<<<<<`）并利用代码的语义理解来提出解决方案，尽管目前人类审查仍然至关重要 34。  
* **分支管理:** 高级智能体可以自主创建功能分支，提交带有描述性消息的更改，并打开 PR。**Beads** 系统通过将提交直接链接到结构化任务来增强这一点 36。

### 6.3 专用智能体实现案例

2025 年，两个突出的实现代表了现有技术的水平：

#### 6.3.1 OpenHands (前 OpenDevin)

OpenHands 是一个完全开源的平台，提供"无头（Headless）"开发者体验。它包括一个专门的 **Software Agent SDK**，允许用户在 Python 中定义智能体并在本地或云端运行。它支持 **Model Context Protocol (MCP)**，使智能体能够安全地连接到外部工具（数据库、Slack、Jira）37。其架构是模块化的，将智能体逻辑与运行时沙盒分离，这允许任意代码的安全执行 31。

#### 6.3.2 IBM iSWE-Agent 与 CodeLLM DevKit (CLDK)

IBM 的 **iSWE-Agent** 针对企业级 Java 生态系统。与通用智能体不同，它依赖于源自 **CodeLLM DevKit (CLDK)** 的专用工具。CLDK 是一个多语言程序分析框架，它执行静态分析以精确定位代码位置和依赖关系。这个"定位"步骤减少了 LLM 的搜索空间，提高了复杂重构的准确性。它采用"推理缩放（Inference Scaling）"管道，运行多次尝试并使用"验证器"模型来选择最佳补丁——这种技术使其登上了 **Multi-SWE-bench** 排行榜的榜首 40。CLDK 提供了一个 Python SDK，允许开发者提取方法体、调用图和符号表，从而为 LLM 提供结构化的代码上下文 41。

---

## 7. 舰队的运营化：可观测性与 CI/CD

管理工厂需要传感器和质量控制。对于智能体软件，这转化为可观测性管道和专门的 CI/CD 工作流。

### 7.1 可观测性：透视黑盒

当智能体失败时，它通常会无声地失败或幻觉出成功。传统的日志不足以应对；工程师需要对智能体的思维过程（思维链）和工具使用进行**追踪（Traceability）**。

* **Arize Phoenix:** 专注于可视化智能体轨迹（Traces），检测循环（例如，智能体重复尝试相同的失败命令），并监控 Token 成本。它提供了系统级的洞察力，使在原始 JSON 日志中不可见的循环变得清晰 42。  
* **LangSmith:** 为 LangChain/LangGraph 智能体提供深度追踪，允许开发人员重放智能体通过会话，并识别推理与现实偏离的确切步骤 43。  
* **DeepEval:** 一个将智能体输出视为单元测试的测试框架。它允许定义"智能体指标（Agentic Metrics）"，如**任务完成度（Task Completion）和工具正确性（Tool Correctness）**，并使用 LLM 作为裁判（G-Eval）来评估代码生成的质量 44。

### 7.2 测试智能体：随机性的挑战

测试非确定性智能体需要从基于断言的测试（expect x == 5）转变为语义评估。

* **基准测试 (Benchmarks):** **SWE-bench**（及其多语言变体 **Multi-SWE-bench**）已成为黄金标准。它通过要求智能体解决真实的 GitHub 问题并检查生成的补丁是否通过存储库的测试套件来评估智能体 40。  
* **Ragas:** 一个专门用于评估 RAG（检索增强生成）管道的框架，对于必须阅读文档或搜索代码库的智能体至关重要。它测量诸如**上下文精确度（Context Precision）**（智能体是否找到了正确的文件？）和**答案忠实度（Answer Faithfulness）**等指标 46。

### 7.3 智能体的 CI/CD

部署智能体需要专门的 CI/CD 管道，将提示词和智能体配置视为代码。

* **提示词版本控制:** 系统提示词的更改必须进行版本控制，并针对"黄金数据集（Golden Dataset）"的任务进行测试，以确保能力没有退化 48。  
* **评估关卡 (Evaluation Gates):** 管道应运行基准测试的子集（例如 SWE-bench Lite）以在部署前验证智能体的编码能力 49。  
* **容器化环境:** 每次测试运行都应发生在临时的 Docker 容器中，以确保可重复性和安全性 27。

---

## 8. 多智能体协作的最佳实践

基于对现有研究的综合，建议 2025 年采用智能体工作流的工程团队遵循以下最佳实践。

### 8.1 架构与设计

1. **解耦规划与执行 (Decouple Planning from Execution):** 采用 **Planner-Worker** 模式。不要要求单个智能体在一个上下文窗口中规划功能并编写代码。规划器应生成结构化计划（例如在 Beads 或 JSON 中），然后由 Worker 执行 22。  
2. **通过数据库/文件系统共享状态:** 不要依赖于在智能体之间传递巨大的上下文字符串。使用共享持久层（如 .beads/ 目录或 Docker 中的共享卷）来维护项目状态的"真相" 50。  
3. **显式交接 (Explicit Handoffs):** 在 LangGraph 等框架中，定义明确的交接边。避免"嘈杂"的群体模式，即智能体向所有人广播消息；有向图能减少噪音和成本 5。

### 8.2 开发工作流

1. **"单一任务"原则:** 应给智能体分配小的、原子的任务（例如，"在类 Y 中实现方法 X"），而不是模糊的目标（"修复登录页面"）。Vibe Coder 必须将 Epic 分解为这些原子任务 52。  
2. **频繁重启 (Restart Frequently):** 智能体会随着时间的推移积累"上下文漂移"。依靠 Beads/Git 的持久状态来弥合差距，杀死智能体进程并为下一个任务启动一个新的进程通常更有效 52。  
3. **合并的人机回环 (HITL for Merges):** 虽然智能体可以生成代码，但**合并**操作应保留由人工审查或由运行严格静态分析（例如 CodeLLM DevKit）的高信任度"审查者智能体"进行把关 36。

### 8.3 基础设施与安全

1. **始终沙盒化:** 永远不要直接在主机操作系统上运行编码智能体。使用具有受限网络访问和明确卷挂载的 Docker 容器作为代码工作区 30。  
2. **红队测试 (Red Teaming):** 使用 DeepEval 等框架对智能体进行"红队测试"，专门测试**提示注入**（例如，代码中的恶意注释劫持智能体）和**SQL 注入**漏洞（如果智能体与数据库交互）44。  
3. **本地与云的混合:** 对于敏感 IP，首选使用通过 **Ollama** 和 **OpenHands** 编排的开放权重模型（如 Llama 3, Qwen 2.5）进行本地执行。对于复杂重构的最大推理能力，通过安全代理路由到前沿模型（Claude 3.5 Sonnet, GPT-4o）55。

---

## 9. 结论：工业化的未来

向编排器时代的过渡不仅仅是工具的改变；它是软件生产基本经济学的改变。正如 Steve Yegge 所预测的那样，我们正在迈向一个代码被"工厂化农业"生产的世界——由编排好的智能体舰队大量生产。

在这个世界里，**Vibe Coder** 就是农场经理。他们的价值不在于手动耕作田地（编写语法）的能力，而在于设计灌溉系统（架构）、管理舰队（编排）以及确保作物符合质量标准（验证）的能力。

"IDE 的消亡"并不是工程学的终结；它是*手工作坊式*工程学的终结。通过掌握 LangGraph 等框架，采用 Beads 等工具进行严格的状态管理，并建立强大的可观测性管道，今天的工程师可以转型为明天软件工厂的架构师。"合并墙"仍然是最后的边界——这一个瓶颈很可能不会通过更多的人类审查者来解决，而是通过下一代递归的、自我验证的智能体系统来解决。

---

## 附录：智能体实现技术参考

### A. 设置本地 OpenHands 环境

使用 Docker Compose 实例化本地智能体工作区，确保隔离和持久化：

```yaml
version: '3.8'
services:
  openhands:
    image: docker.all-hands.dev/all-hands-ai/openhands:0.12
    ports:
      - "3000:3000"
    environment:
      - SANDBOX_USER_ID=1000
      - WORKSPACE_BASE=/workspace
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./my_project:/workspace  # 将你的代码挂载到此处
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

[31]

### B. 使用 DeepEval 评估智能体性能

用于对编码智能体的输出进行功能正确性单元测试的 Python 脚本示例：

```python
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

def test_coding_agent():
    # 定义代码质量的自定义标准
    correctness_metric = GEval(
        name="Code Correctness",
        criteria="Determine if the code is syntactically correct and solves the task.",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT]
    )
    
    # 定义测试用例
    test_case = LLMTestCase(
        input="Write a Python function to calculate Fibonacci numbers.",
        actual_output="def fib(n): return n if n<=1 else fib(n-1)+fib(n-2)",  # 智能体输出
        expected_output="def fib(n):..."  # 预期参考
    )
    
    # 断言测试通过
    assert_test(test_case, [correctness_metric])
```

[44]

### C. 使用 CLDK 进行代码分析

使用 CodeLLM DevKit 提取 Java 项目中所有方法体的示例：

```python
from cldk import CLDK

# 初始化 Java 分析
cldk = CLDK(language="java")
analysis = cldk.analysis(project_path="/path/to/your/java/project")

# 遍历符号表并提取方法体
for class_file in analysis.get_symbol_table().values():
    for type_name, type_decl in class_file.type_declarations.items():
        for method in type_decl.callable_declarations.values():
            body = analysis.get_method_body(method.declaration)
            print(f"Method: {method.declaration}\nBody: {body}\n")
```

[41]

---

## 参考文献

1. Latent Space: The AI Engineer Podcast, accessed December 30, 2025, https://podcasts.apple.com/us/podcast/latent-space-the-ai-engineer-podcast/id1674008350
2. Latent Space: The AI Engineer Podcast | Free Listening on Podbean App, accessed December 30, 2025, https://www.podbean.com/podcast-detail/k6zzp-34cef6/Latent-Space-The-AI-Engineer-Podcast
3. Steve Yegge's Vibe Coding Manifesto: Why Claude Code Isn't It & What Comes After the IDE - Apple Podcasts, accessed December 30, 2025, https://podcasts.apple.com/fi/podcast/steve-yegges-vibe-coding-manifesto-why-claude-code/id1674008350?i=1000742822778
4. Best AI Agent Development Frameworks for 2025 - WillDom, accessed December 30, 2025, https://willdom.com/blog/best-ai-agent-development-frameworks/
5. CrewAI vs LangGraph vs AutoGen: Choosing the Right Multi-Agent AI Framework, accessed December 30, 2025, https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen
6. OpenHands | The Open Platform for Cloud Coding Agents, accessed December 30, 2025, https://openhands.dev/
7. 10 AI agent benchmarks - Evidently AI, accessed December 30, 2025, https://www.evidentlyai.com/blog/ai-agent-benchmarks
8. Build and Distribute AI Agents and Workflows with cagent - Docker, accessed December 30, 2025, https://www.docker.com/blog/cagent-build-and-distribute-ai-agents-and-workflows/
9. steveyegge/beads - A memory upgrade for your coding agent - GitHub, accessed December 30, 2025, https://github.com/steveyegge/beads
10. The Brute Squad | Sourcegraph Blog, accessed December 30, 2025, https://sourcegraph.com/blog/the-brute-squad
11. Essential Skills of a Vibe Coder - IT Revolution, accessed December 30, 2025, https://itrevolution.com/articles/essential-skills-of-a-vibe-coder/
12. From Vibe Coding to Professional AI-Powered Development: A Practical Handbook, accessed December 30, 2025, https://dev.to/phucnt/from-vibe-coding-to-professional-ai-powered-development-a-practical-handbook-mlp
13. An honest review as a professional developer : r/ClaudeCode - Reddit, accessed December 30, 2025, https://www.reddit.com/r/ClaudeCode/comments/1p8plcc/an_honest_review_as_a_professional_developer/
14. 20 Best AI Coding Assistant Tools [Updated Aug 2025] - Qodo, accessed December 30, 2025, https://www.qodo.ai/blog/best-ai-coding-assistant-tools/
15. Introducing Beads: A coding agent memory system | by Steve Yegge - Medium, accessed December 30, 2025, https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a
16. Let's Compare CrewAI, AutoGen, Vertex AI, and LangGraph Multi-Agent Frameworks | Infinite Lambda Blog, accessed December 30, 2025, https://infinitelambda.com/compare-crewai-autogen-vertexai-langgraph/
17. Top 9 AI Agent Frameworks as of December 2025 - Shakudo, accessed December 30, 2025, https://www.shakudo.io/blog/top-9-ai-agent-frameworks
18. Autogen vs LangChain vs CrewAI: Our AI Engineers' Ultimate Comparison Guide, accessed December 30, 2025, https://www.instinctools.com/blog/autogen-vs-langchain-vs-crewai/
19. FoundationAgents/MetaGPT: The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming - GitHub, accessed December 30, 2025, https://github.com/FoundationAgents/MetaGPT
20. MetaGPT Vs ChatDev: In-Depth Comparison And Analysis - SmythOS, accessed December 30, 2025, https://smythos.com/developers/agent-comparisons/metagpt-vs-chatdev/
21. Tested 5 agent frameworks in production - here's when to use each one : r/AI_Agents, accessed December 30, 2025, https://www.reddit.com/r/AI_Agents/comments/1oukxzx/tested_5_agent_frameworks_in_production_heres/
22. Customize agent workflows with advanced orchestration techniques using Strands Agents, accessed December 30, 2025, https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents/
23. Building a ReWOO Reasoning Agent Using IBM Granite, accessed December 30, 2025, https://www.ibm.com/think/tutorials/build-rewoo-reasoning-agent-granite
24. Agentic AI Engineering: Building AI Agents That Deliver | by Algorythmos AI - Medium, accessed December 30, 2025, https://medium.com/@algorythmos/agentic-ai-engineering-building-ai-agents-that-deliver-c9f4f8323df4
25. The Beads Revolution: How I Built The TODO System That AI Agents Actually Want to Use, accessed December 30, 2025, https://steve-yegge.medium.com/the-beads-revolution-how-i-built-the-todo-system-that-ai-agents-actually-want-to-use-228a5f9be2a9
26. Explore beads library and usage with AMP, accessed December 30, 2025, https://ampcode.com/threads/T-adc03ba9-db60-49e6-bae9-e5f9749f4312
27. How to Build a Multi-Agent AI System Fast with cagent | Docker, accessed December 30, 2025, https://www.docker.com/blog/how-to-build-a-multi-agent-system/
28. Docker cagent: Build and Orchestrate AI Agents Without Writing Code - Ajeet Singh Raina, accessed December 30, 2025, https://www.ajeetraina.com/docker-cagent-build-and-orchestrate-ai-agents-without-writing-code/
29. Docker Brings Compose to the Agent Era: Building AI Agents is Now Easy, accessed December 30, 2025, https://www.docker.com/blog/build-ai-agents-with-docker-compose/
30. OpenHands Review 2025 | Software Engineering Tool - Pricing & Features - AI Agents List, accessed December 30, 2025, https://aiagentslist.com/agents/openhands
31. Docker Runtime - OpenHands Docs, accessed December 30, 2025, https://docs.openhands.dev/openhands/usage/runtimes/docker
32. 6 best frameworks to build AI agents in 2025 - Codelevate, accessed December 30, 2025, https://www.codelevate.com/blog/6-best-frameworks-to-build-ai-agents-in-2025
33. pairup.nvim - real-time AI pair programming with git-aware context streaming : r/neovim, accessed December 30, 2025, https://www.reddit.com/r/neovim/comments/1nanw39/pairupnvim_realtime_ai_pair_programming_with/
34. Git AI Assistant | AI for Version Control & Git Commands - CodeGPT, accessed December 30, 2025, https://codegpt.co/agents/git-expert
35. The role of AI in merge conflict resolution - Graphite, accessed December 30, 2025, https://graphite.com/guides/ai-code-merge-conflict-resolution
36. Building With AI Coding Agents: Best Practices for Agent Workflows - Medium, accessed December 30, 2025, https://medium.com/@elisheba.t.anderson/building-with-ai-coding-agents-best-practices-for-agent-workflows-be1d7095901b
37. OpenHands: AI-Driven Development - GitHub, accessed December 30, 2025, https://github.com/OpenHands/OpenHands
38. Getting Started - OpenHands Docs, accessed December 30, 2025, https://docs.openhands.dev/sdk/getting-started
39. The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents - arXiv, accessed December 30, 2025, https://arxiv.org/html/2511.03690v1
40. IBM's software engineering agent tops leaderboard for Java - IBM Research, accessed December 30, 2025, https://research.ibm.com/blog/ibm-software-engineering-agent-tops-the-multi-swe-bench-leaderboard-for-java
41. cldk - PyPI, accessed December 30, 2025, https://pypi.org/project/cldk/
42. Debugging Agent Loops: Bridging the Observability Gap with Arize Phoenix - Medium, accessed December 30, 2025, https://medium.com/@ap3617180/debugging-agent-loops-bridging-the-observability-gap-with-arize-phoenix-de78cb093496
43. Any good analytics tool for AI Agents? : r/AI_Agents - Reddit, accessed December 30, 2025, https://www.reddit.com/r/AI_Agents/comments/1nj5y2q/any_good_analytics_tool_for_ai_agents/
44. confident-ai/deepeval: The LLM Evaluation Framework - GitHub, accessed December 30, 2025, https://github.com/confident-ai/deepeval
45. Evaluation Guide - SWE-bench, accessed December 30, 2025, https://www.swebench.com/SWE-bench/guides/evaluation/
46. List of available metrics - Ragas, accessed December 30, 2025, https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/
47. Metrics-Driven Agent Development - Pinecone, accessed December 30, 2025, https://www.pinecone.io/learn/series/rag/ragas/
48. CI/CD and automation for serverless AI - AWS Prescriptive Guidance, accessed December 30, 2025, https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/cicd-and-automation.html
49. A Guide to CI/CD for AI Agents that Don't Behave Deterministically | Datagrid, accessed December 30, 2025, https://datagrid.com/blog/cicd-pipelines-ai-agents-guide
50. Multi-User Memory Sharing in LLM Agents with Dynamic Access Control - arXiv, accessed December 30, 2025, https://arxiv.org/html/2505.18279v1
51. Experience with connecting 2 linux boxes to run coding AI agents on second box (in Docker), accessed December 30, 2025, https://www.reddit.com/r/selfhosted/comments/1o8egud/exeprience_with_connecting_2_linux_boxes_to_run/
52. Beads Best Practices - Steve Yegge, accessed December 30, 2025, https://steve-yegge.medium.com/beads-best-practices-2db636b9760c
53. AI Agent Orchestration Patterns - Azure Architecture Center - Microsoft Learn, accessed December 30, 2025, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
54. The Real-World Attacks Behind OWASP Agentic AI Top 10, accessed December 30, 2025, https://www.bleepingcomputer.com/news/security/the-real-world-attacks-behind-owasp-agentic-ai-top-10/
55. Run Your Own AI Coding Agent Locally with GPT-OSS and OpenHands - Clarifai, accessed December 30, 2025, https://www.clarifai.com/blog/run-your-own-ai-coding-agent-locally-with-gpt-oss-openhands
56. OpenHands - Lemonade Server Documentation, accessed December 30, 2025, https://lemonade-server.ai/docs/server/apps/open-hands/
57. How to Run OpenHands with a Local LLM Using LM Studio - DEV Community, accessed December 30, 2025, https://dev.to/udiko/how-to-run-openhands-with-a-local-llm-using-lm-studio-41j6
