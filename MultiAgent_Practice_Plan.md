# 多智能体系统探索与实践计划

> 基于《Agent 编排与软件开发未来》研究报告制定

## 📋 项目目标

1. 掌握主流多智能体框架 (LangGraph, AutoGen, Beads)
2. 实现 Docker 沙盒化执行环境
3. 构建 Critic (批评家) 智能体架构
4. 建立可观测性和评估体系

---

## 🗓️ 学习路径 (6周计划)

### 第一阶段: 基础框架入门 (Week 1-2)

#### Week 1: LangGraph 深度学习

**为什么选择 LangGraph 开始？**
- 工程化的确定性选择，适合生产级应用
- 支持循环图结构 (编写 → 测试 → 失败 → 修复 → 测试 → 通过)
- 细粒度状态控制、持久化、人机回环 (HITL)

**学习任务:**
```
Week1/
├── 01_langgraph_basics/
│   ├── hello_graph.py          # 基础图结构
│   ├── state_management.py     # 状态管理
│   └── conditional_edges.py    # 条件边和循环
├── 02_langgraph_patterns/
│   ├── planner_worker.py       # 规划器-执行者模式
│   ├── reflection_loop.py      # 反思循环 (Critic基础)
│   └── human_in_loop.py        # 人机回环
└── 03_langgraph_tools/
    ├── tool_calling.py         # 工具调用
    └── code_execution.py       # 代码执行能力
```

**关键概念:**
- StateGraph: 有状态的图结构
- Nodes: 处理逻辑单元
- Edges: 转换逻辑 (条件/无条件)
- Checkpointing: 状态持久化与"时间旅行"

**参考资源:**
- [LangGraph 官方文档](https://python.langchain.com/docs/langgraph)
- [LangSmith](https://smith.langchain.com/) - 用于追踪调试

---

#### Week 2: AutoGen 群体智能

**为什么学习 AutoGen？**
- 对话式多智能体协作
- 灵活的拓扑结构
- 适合开放式探索性任务

**学习任务:**
```
Week2/
├── 01_autogen_basics/
│   ├── two_agent_chat.py       # 双智能体对话
│   ├── group_chat.py           # 群聊模式
│   └── code_executor.py        # 代码执行
├── 02_autogen_patterns/
│   ├── user_proxy_pattern.py   # UserProxy + Assistant 模式
│   ├── critic_pattern.py       # 批评家模式 ⭐
│   └── nested_chat.py          # 嵌套对话
└── 03_autogen_studio/
    └── studio_exploration.md   # AutoGen Studio UI 探索
```

**关键概念:**
- ConversableAgent: 可对话智能体
- UserProxyAgent: 用户代理 (可执行代码)
- GroupChat: 群聊管理器
- 终止条件和消息过滤

**对比 LangGraph:**
| 特性 | LangGraph | AutoGen |
|------|-----------|---------|
| 控制流 | 显式图定义 | 对话驱动 |
| 适用场景 | 确定性流程 | 探索性协作 |
| 状态管理 | 内置持久化 | 需自行实现 |
| 学习曲线 | 较陡峭 | 相对平缓 |

---

### 第二阶段: 沙盒化与基础设施 (Week 3)

#### Week 3: Docker 沙盒化执行

**为什么沙盒化至关重要？**
- 报告明确指出: "永远不要直接在主机操作系统上运行编码智能体"
- 隔离 LLM 生成代码的执行风险
- 确保可重复性和安全性

**学习任务:**
```
Week3/
├── 01_docker_basics/
│   ├── Dockerfile              # 智能体运行环境
│   ├── docker-compose.yml      # 多容器编排
│   └── sandbox_test.py         # 沙盒测试
├── 02_openhands_setup/
│   ├── docker-compose.yml      # OpenHands 本地部署
│   └── custom_runtime/         # 自定义运行时
│       ├── Dockerfile
│       └── requirements.txt
├── 03_secure_execution/
│   ├── volume_mounts.md        # 安全卷挂载
│   ├── network_isolation.md    # 网络隔离
│   └── resource_limits.md      # 资源限制
└── 04_cagent_exploration/
    ├── cagent.yaml             # Docker cagent 配置
    └── multi_agent_compose.yml # 多智能体 Docker 编排
```

**Docker Compose 模板 (OpenHands):**
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
      - ./workspace:/workspace
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

---

### 第三阶段: Beads 记忆系统 (Week 4)

#### Week 4: 智能体记忆管理

**为什么需要 Beads？**
- 解决"智能体失忆"问题
- 结构化状态管理 (而非 Markdown)
- Git 集成，随代码版本化

**学习任务:**
```
Week4/
├── 01_beads_setup/
│   ├── install_beads.md        # 安装配置
│   ├── basic_commands.md       # 基础命令
│   └── beads_workflow.py       # 工作流示例
├── 02_beads_integration/
│   ├── langgraph_beads.py      # LangGraph + Beads
│   ├── autogen_beads.py        # AutoGen + Beads
│   └── task_decomposition.py   # 任务分解
└── 03_beads_patterns/
    ├── dependency_graph.md     # 依赖图管理
    ├── compaction.md           # 语义记忆压缩
    └── multi_agent_tasks.py    # 多智能体任务分配
```

**Beads 核心功能:**
- 结构化任务 (ID, 状态, 优先级, 依赖)
- 基于哈希的唯一 ID (防合并冲突)
- "就绪工作" 查询
- 语义记忆衰减 (Compaction)

---

### 第四阶段: 批评家智能体 (Week 5) ⭐

#### Week 5: 构建 Critic 智能体架构

**Critic 模式核心思想 (来自报告):**
> 智能体 A 编写代码；智能体 B（批评家/Critic）根据一组规则审查代码；智能体 A 根据反馈进行修改。

**架构设计:**
```
Week5/
├── 01_critic_patterns/
│   ├── basic_critic.py         # 基础批评家
│   ├── multi_criteria.py       # 多维度评审
│   └── iterative_refinement.py # 迭代优化
├── 02_critic_implementations/
│   ├── langgraph_critic/
│   │   ├── graph.py            # LangGraph 实现
│   │   ├── coder_node.py       # 编码节点
│   │   ├── critic_node.py      # 批评节点
│   │   └── state.py            # 状态定义
│   └── autogen_critic/
│   │   ├── coder_agent.py      # 编码智能体
│   │   ├── critic_agent.py     # 批评智能体
│   │   └── orchestrator.py     # 编排器
├── 03_critic_rules/
│   ├── code_quality.py         # 代码质量规则
│   ├── security_check.py       # 安全检查规则
│   ├── style_guide.py          # 风格指南规则
│   └── logic_review.py         # 逻辑审查规则
└── 04_advanced_critic/
    ├── hierarchical_critic.py  # 层级批评家
    ├── specialized_critics.py  # 专门化批评家
    └── consensus_mechanism.py  # 共识机制
```

**LangGraph Critic 架构示例:**
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class CriticState(TypedDict):
    task: str
    code: str
    critique: str
    iteration: int
    max_iterations: int
    approved: bool

def coder_node(state: CriticState) -> CriticState:
    """生成或修改代码"""
    # 根据任务和批评反馈生成代码
    pass

def critic_node(state: CriticState) -> CriticState:
    """批评和审查代码"""
    # 根据规则评审代码
    # 返回批评意见或批准
    pass

def should_continue(state: CriticState) -> str:
    """决定是否继续迭代"""
    if state["approved"]:
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

app = workflow.compile()
```

**Critic 评审维度:**
1. **语法正确性** - 代码是否能运行
2. **逻辑正确性** - 是否解决问题
3. **代码质量** - 可读性、可维护性
4. **安全性** - 潜在漏洞检查
5. **性能** - 效率考量
6. **风格一致性** - 遵循项目规范

---

### 第五阶段: 可观测性与评估 (Week 6)

#### Week 6: 建立评估体系

**学习任务:**
```
Week6/
├── 01_observability/
│   ├── langsmith_setup.py      # LangSmith 追踪
│   ├── arize_phoenix.py        # Arize Phoenix 监控
│   └── custom_logging.py       # 自定义日志
├── 02_evaluation/
│   ├── deepeval_setup.py       # DeepEval 测试
│   ├── agent_metrics.py        # 智能体指标
│   └── benchmark_tests.py      # 基准测试
├── 03_ci_cd/
│   ├── prompt_versioning.md    # 提示词版本控制
│   ├── evaluation_gates.md     # 评估关卡
│   └── github_actions.yml      # CI/CD 配置
└── 04_red_teaming/
    ├── prompt_injection.py     # 提示注入测试
    ├── adversarial_tests.py    # 对抗性测试
    └── security_audit.md       # 安全审计
```

**DeepEval 示例:**
```python
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

def test_critic_effectiveness():
    correctness_metric = GEval(
        name="Critique Quality",
        criteria="评估批评是否具体、可操作、有建设性",
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT
        ]
    )
    
    test_case = LLMTestCase(
        input="审查这段代码的安全性",
        actual_output=critic_agent.review(code),
        expected_output="具体的安全改进建议"
    )
    
    assert_test(test_case, [correctness_metric])
```

---

## 🏗️ 项目结构

```
MultiAgents/
├── Agent 编排与软件开发未来.md    # 研究报告 (已有)
├── MultiAgent_Practice_Plan.md   # 本计划文档
├── Week1_LangGraph/
├── Week2_AutoGen/
├── Week3_Docker_Sandbox/
├── Week4_Beads/
├── Week5_Critic_Agent/           # 核心项目
│   ├── src/
│   │   ├── agents/
│   │   │   ├── coder.py
│   │   │   ├── critic.py
│   │   │   └── orchestrator.py
│   │   ├── rules/
│   │   │   ├── code_quality.py
│   │   │   ├── security.py
│   │   │   └── style.py
│   │   ├── state/
│   │   │   └── manager.py
│   │   └── utils/
│   │       ├── llm.py
│   │       └── tools.py
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── tests/
│   ├── examples/
│   └── README.md
└── Week6_Evaluation/
```

---

## 🎯 Critic 智能体推荐架构

### 架构一: 简单反思循环 (入门)

```
[用户任务] → [Coder] → [Critic] ─┐
                ↑                 │
                └─────────────────┘ (不通过则循环)
                        ↓
                   [完成输出]
```

### 架构二: 层级批评家 (中级)

```
                    [Manager/Orchestrator]
                           ↓
              ┌────────────┼────────────┐
              ↓            ↓            ↓
         [Coder A]    [Coder B]    [Coder C]
              ↓            ↓            ↓
         [Frontend   [Backend     [Database
          Critic]     Critic]      Critic]
              └────────────┼────────────┘
                           ↓
                    [Meta Critic]
                    (最终审查)
```

### 架构三: 多智能体共识 (高级)

```
[Task] → [Planner] → [Task Decomposition]
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
[Coder 1] [Coder 2] [Coder 3]
    ↓         ↓         ↓
[Critic 1] [Critic 2] [Critic 3]
    └─────────┼─────────┘
              ↓
      [Consensus Engine]
      (投票/加权聚合)
              ↓
      [Final Output]
```

---

## 📚 必备资源

### 官方文档
- [LangGraph](https://python.langchain.com/docs/langgraph)
- [AutoGen](https://microsoft.github.io/autogen/)
- [OpenHands](https://docs.openhands.dev/)
- [Beads](https://github.com/steveyegge/beads)
- [Docker cagent](https://github.com/docker/compose-ai)

### 工具
- [LangSmith](https://smith.langchain.com/) - LangChain 追踪
- [Arize Phoenix](https://phoenix.arize.com/) - 可观测性
- [DeepEval](https://github.com/confident-ai/deepeval) - 评估框架

### 推荐阅读
- Steve Yegge 的 Beads 系列文章
- LangGraph 官方教程
- AutoGen 多智能体示例

---

## ⏭️ 建议的起步顺序

### 立即开始:

1. **Week 1 Day 1**: 安装环境
   ```bash
   # 创建虚拟环境
   python -m venv multiagent-env
   multiagent-env\Scripts\activate
   
   # 安装核心依赖
   pip install langchain langgraph langchain-openai
   pip install pyautogen
   pip install deepeval
   pip install docker
   ```

2. **Week 1 Day 1**: 运行第一个 LangGraph 示例

3. **Week 5**: 开始构建 Critic 智能体 (核心目标)

---

## 💡 关键洞见 (来自报告)

1. **"2000小时定律"**: 需要约一年日常使用才能可靠预测 LLM 行为
2. **"合并墙"**: 智能体生成 PR 的速度超过人类审查能力
3. **"单一任务原则"**: 给智能体分配小的、原子的任务
4. **"频繁重启"**: 智能体会积累"上下文漂移"
5. **"始终沙盒化"**: 永远不要直接在主机上运行编码智能体

---

**创建日期**: 2025年12月31日  
**最后更新**: 2025年12月31日  
**状态**: 计划制定完成，待执行
