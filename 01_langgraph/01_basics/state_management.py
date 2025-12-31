"""
State Management - 状态管理详解
================================

深入理解 LangGraph 的状态管理机制：
1. TypedDict 状态定义
2. Annotated 类型与 reducer
3. 状态更新策略
4. Checkpoint 持久化
"""

from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from operator import add
import json


# ==========================================
# 1. 基础状态定义
# ==========================================

class BasicState(TypedDict):
    """基础状态 - 简单的键值对"""
    user_input: str
    response: str
    step_count: int


# ==========================================
# 2. 带 Reducer 的状态
# ==========================================

class MessageState(TypedDict):
    """
    使用 Annotated 和 reducer 函数
    
    Reducer 决定如何合并新旧状态值：
    - add: 列表追加
    - 自定义函数: 灵活控制
    """
    # messages 使用 add reducer，新消息会追加而非覆盖
    messages: Annotated[list[str], add]
    # 普通字段，直接覆盖
    current_agent: str
    iteration: int


def append_with_limit(existing: list, new: list, limit: int = 10) -> list:
    """自定义 reducer: 保持列表长度限制"""
    combined = existing + new
    return combined[-limit:]  # 只保留最后 limit 条


class LimitedMessageState(TypedDict):
    """带长度限制的消息状态"""
    messages: Annotated[list[str], lambda x, y: append_with_limit(x, y, 5)]
    metadata: dict


# ==========================================
# 3. 复杂嵌套状态
# ==========================================

class AgentInfo(TypedDict):
    name: str
    role: str
    status: str


class TaskInfo(TypedDict):
    id: str
    description: str
    priority: int
    completed: bool


class ComplexState(TypedDict):
    """复杂嵌套状态结构"""
    # 智能体信息
    agents: dict[str, AgentInfo]
    # 任务队列
    tasks: list[TaskInfo]
    # 执行历史
    history: Annotated[list[str], add]
    # 全局配置
    config: dict
    # 当前焦点
    current_task_id: str | None


# ==========================================
# 4. 示例：状态流转演示
# ==========================================

def initialize_state(state: MessageState) -> MessageState:
    """初始化节点"""
    print("\n🚀 Initializing...")
    return {
        "messages": ["System initialized"],
        "current_agent": "initializer",
        "iteration": 0
    }


def process_step(state: MessageState) -> MessageState:
    """处理步骤节点"""
    iteration = state["iteration"]
    print(f"\n⚙️ Processing step {iteration + 1}...")
    
    # 注意：messages 会自动追加（因为使用了 add reducer）
    return {
        "messages": [f"Step {iteration + 1} completed"],
        "current_agent": "processor",
        "iteration": iteration + 1
    }


def finalize_state(state: MessageState) -> MessageState:
    """完成节点"""
    print("\n✅ Finalizing...")
    return {
        "messages": ["Process completed"],
        "current_agent": "finalizer",
        "iteration": state["iteration"]
    }


def should_continue(state: MessageState) -> str:
    """控制循环的条件函数"""
    if state["iteration"] >= 3:
        return "finalize"
    return "process"


def create_state_demo_graph():
    """创建状态演示图"""
    
    workflow = StateGraph(MessageState)
    
    workflow.add_node("init", initialize_state)
    workflow.add_node("process", process_step)
    workflow.add_node("finalize", finalize_state)
    
    workflow.set_entry_point("init")
    
    workflow.add_edge("init", "process")
    workflow.add_conditional_edges(
        "process",
        should_continue,
        {
            "process": "process",
            "finalize": "finalize"
        }
    )
    workflow.add_edge("finalize", END)
    
    return workflow.compile()


# ==========================================
# 5. Checkpoint 持久化（概念演示）
# ==========================================

def demonstrate_checkpoint_concept():
    """
    演示 Checkpoint 的概念
    
    实际使用时需要配置 checkpointer:
    
    from langgraph.checkpoint.sqlite import SqliteSaver
    
    memory = SqliteSaver.from_conn_string(":memory:")
    app = workflow.compile(checkpointer=memory)
    
    # 运行时指定 thread_id
    config = {"configurable": {"thread_id": "user-123"}}
    result = app.invoke(state, config)
    
    # 可以从任意 checkpoint 恢复（时间旅行）
    """
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Checkpoint 持久化功能                                      ║
    ╠════════════════════════════════════════════════════════════╣
    ║  • 自动保存每个节点执行后的状态                              ║
    ║  • 支持从任意历史状态恢复（时间旅行）                        ║
    ║  • 可配置存储后端：内存、SQLite、PostgreSQL                  ║
    ║  • 适用于长运行任务和 Human-in-the-Loop                     ║
    ╚════════════════════════════════════════════════════════════╝
    """)


def main():
    print("=" * 60)
    print("📊 LangGraph State Management Demo")
    print("=" * 60)
    
    # 运行状态演示
    app = create_state_demo_graph()
    
    initial_state = {
        "messages": [],
        "current_agent": "",
        "iteration": 0
    }
    
    print("\n📋 Initial State:")
    print(f"   messages: {initial_state['messages']}")
    print(f"   iteration: {initial_state['iteration']}")
    
    # 运行图
    result = app.invoke(initial_state)
    
    print("\n" + "=" * 60)
    print("📊 Final State:")
    print(f"   messages: {result['messages']}")
    print(f"   current_agent: {result['current_agent']}")
    print(f"   iteration: {result['iteration']}")
    
    # 演示 Checkpoint 概念
    print("\n" + "=" * 60)
    demonstrate_checkpoint_concept()


if __name__ == "__main__":
    main()
