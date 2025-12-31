"""
Human-in-the-Loop (HITL) - 人机回环模式
=======================================

在关键决策点引入人工审核：
1. 使用 interrupt_before/after 暂停执行
2. 等待人工输入
3. 基于人工反馈继续执行
4. 支持修改状态后继续

研究报告参考：
> "虽然智能体可以生成代码，但合并操作应保留由人工审查
> 或由运行严格静态分析的高信任度"审查者智能体"进行把关。"
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
import time


# ==========================================
# 状态定义
# ==========================================

class HITLState(TypedDict):
    # 任务描述
    task: str
    # 智能体生成的方案
    proposal: str
    # 人工审核结果
    human_feedback: str | None
    # 是否批准
    approved: bool | None
    # 最终输出
    final_output: str
    # 流程阶段
    stage: str


# ==========================================
# 节点定义
# ==========================================

def generate_proposal(state: HITLState) -> HITLState:
    """智能体生成方案"""
    print("\n🤖 AI Agent: Generating proposal...")
    
    task = state["task"]
    
    # 模拟 AI 生成（实际使用 LLM）
    proposal = f"""
    === AI Generated Proposal ===
    Task: {task}
    
    Recommended approach:
    1. Create new feature branch
    2. Implement core logic with TDD
    3. Add error handling
    4. Write documentation
    5. Submit for review
    
    Estimated effort: 3 days
    Risk level: Low
    ==============================
    """
    
    state["proposal"] = proposal
    state["stage"] = "awaiting_review"
    
    print("   ✅ Proposal generated")
    print(proposal)
    
    return state


def await_human_review(state: HITLState) -> HITLState:
    """
    等待人工审核
    
    在实际的 LangGraph 应用中，这里会使用:
    - interrupt_before 或 interrupt_after
    - 外部系统（Web UI、Slack）收集反馈
    - 然后通过 app.update_state() 更新状态
    
    这里用命令行模拟人工输入
    """
    print("\n" + "=" * 50)
    print("⏸️  HUMAN REVIEW REQUIRED")
    print("=" * 50)
    print("\nProposal to review:")
    print(state["proposal"])
    print("-" * 50)
    
    # 模拟人工输入
    print("\n[Simulating human review...]")
    time.sleep(1)
    
    # 在演示中自动批准，实际应用会等待真实输入
    # feedback = input("Enter feedback (or 'approve'/'reject'): ")
    feedback = "approve"  # 模拟批准
    
    if feedback.lower() == "approve":
        state["human_feedback"] = "Approved by human reviewer"
        state["approved"] = True
        print("   ✅ Human approved the proposal")
    elif feedback.lower() == "reject":
        state["human_feedback"] = "Rejected - needs revision"
        state["approved"] = False
        print("   ❌ Human rejected the proposal")
    else:
        state["human_feedback"] = feedback
        state["approved"] = True  # 带反馈批准
        print(f"   📝 Human provided feedback: {feedback}")
    
    state["stage"] = "reviewed"
    
    return state


def execute_approved(state: HITLState) -> HITLState:
    """执行已批准的方案"""
    print("\n🚀 Executing approved proposal...")
    
    state["final_output"] = f"""
    Execution complete!
    
    Task: {state['task']}
    Human Feedback: {state['human_feedback']}
    Status: Successfully implemented
    """
    state["stage"] = "completed"
    
    print("   ✅ Execution completed")
    
    return state


def handle_rejection(state: HITLState) -> HITLState:
    """处理被拒绝的方案"""
    print("\n🔄 Handling rejection...")
    
    state["final_output"] = f"""
    Proposal rejected.
    
    Feedback: {state['human_feedback']}
    Next step: Revise proposal based on feedback
    """
    state["stage"] = "rejected"
    
    return state


def route_after_review(state: HITLState) -> Literal["execute", "reject"]:
    """审核后路由"""
    if state["approved"]:
        return "execute"
    return "reject"


# ==========================================
# 构建图
# ==========================================

def create_hitl_graph():
    """创建人机回环图"""
    
    workflow = StateGraph(HITLState)
    
    workflow.add_node("generate", generate_proposal)
    workflow.add_node("human_review", await_human_review)
    workflow.add_node("execute", execute_approved)
    workflow.add_node("handle_reject", handle_rejection)
    
    workflow.set_entry_point("generate")
    
    workflow.add_edge("generate", "human_review")
    
    workflow.add_conditional_edges(
        "human_review",
        route_after_review,
        {
            "execute": "execute",
            "reject": "handle_reject"
        }
    )
    
    workflow.add_edge("execute", END)
    workflow.add_edge("handle_reject", END)
    
    return workflow.compile()


# ==========================================
# 可视化
# ==========================================

def visualize_hitl_flow():
    """显示 HITL 流程"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           Human-in-the-Loop (HITL) Pattern               ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║    ┌──────────┐                                          ║
    ║    │  START   │                                          ║
    ║    └────┬─────┘                                          ║
    ║         │                                                 ║
    ║         ▼                                                 ║
    ║    ┌──────────┐                                          ║
    ║    │ GENERATE │  AI generates proposal                   ║
    ║    └────┬─────┘                                          ║
    ║         │                                                 ║
    ║         ▼                                                 ║
    ║    ┌──────────┐                                          ║
    ║    │  HUMAN   │  ⏸️ Pause for human review               ║
    ║    │  REVIEW  │                                          ║
    ║    └────┬─────┘                                          ║
    ║         │                                                 ║
    ║    ┌────┴────┐                                           ║
    ║    │         │                                            ║
    ║    ▼         ▼                                            ║
    ║ Approved   Rejected                                       ║
    ║    │         │                                            ║
    ║    ▼         ▼                                            ║
    ║ ┌──────┐  ┌──────┐                                       ║
    ║ │EXECUTE│  │REVISE│                                       ║
    ║ └───┬──┘  └───┬──┘                                       ║
    ║     │        │                                            ║
    ║     ▼        ▼                                            ║
    ║    ┌──────────┐                                          ║
    ║    │   END    │                                          ║
    ║    └──────────┘                                          ║
    ║                                                           ║
    ╚══════════════════════════════════════════════════════════╝
    
    Key LangGraph Features for HITL:
    
    • interrupt_before=["node_name"]  - Pause before a node
    • interrupt_after=["node_name"]   - Pause after a node  
    • app.update_state(config, new_state)  - Update state externally
    • Checkpointing enables state persistence across pauses
    """)


# ==========================================
# 高级：带 Checkpoint 的 HITL
# ==========================================

def demonstrate_checkpoint_hitl():
    """演示带 Checkpoint 的 HITL（概念代码）"""
    print("""
    ═══════════════════════════════════════════════════════════
    Advanced HITL with Checkpointing (Conceptual Code)
    ═══════════════════════════════════════════════════════════
    
    ```python
    from langgraph.checkpoint.sqlite import SqliteSaver
    
    # 配置持久化存储
    memory = SqliteSaver.from_conn_string(":memory:")
    
    # 编译时启用中断
    app = workflow.compile(
        checkpointer=memory,
        interrupt_before=["human_review"]  # 在此节点前暂停
    )
    
    # 初始运行 - 会在 human_review 前暂停
    config = {"configurable": {"thread_id": "task-123"}}
    result = app.invoke(initial_state, config)
    
    # ... 时间流逝，人工完成审核 ...
    
    # 更新状态并继续
    app.update_state(
        config,
        {
            "human_feedback": "Looks good!",
            "approved": True
        }
    )
    
    # 从暂停点继续执行
    final_result = app.invoke(None, config)
    ```
    ═══════════════════════════════════════════════════════════
    """)


# ==========================================
# Main
# ==========================================

def main():
    print("=" * 60)
    print("👥 Human-in-the-Loop (HITL) Pattern Demo")
    print("=" * 60)
    
    visualize_hitl_flow()
    
    # 创建图
    app = create_hitl_graph()
    
    # 初始状态
    initial_state = {
        "task": "Implement new payment gateway integration",
        "proposal": "",
        "human_feedback": None,
        "approved": None,
        "final_output": "",
        "stage": "init"
    }
    
    print(f"\n📋 Task: {initial_state['task']}")
    print("\n" + "-" * 60)
    
    # 运行（在演示中自动模拟人工审核）
    result = app.invoke(initial_state)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📊 FINAL OUTPUT")
    print("=" * 60)
    print(result["final_output"])
    
    # 演示高级功能
    print("\n")
    demonstrate_checkpoint_hitl()


if __name__ == "__main__":
    main()
