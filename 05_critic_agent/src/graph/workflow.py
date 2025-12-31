"""
Critic Agent - 工作流定义
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from .state import CriticState, ReviewStatus


def should_continue(state: CriticState) -> Literal["coder", "end"]:
    """决定是否继续迭代
    
    Returns:
        "coder": 继续修改代码
        "end": 结束工作流
    """
    # 已通过审查
    if state["review_status"] == ReviewStatus.APPROVED.value:
        return "end"
    
    # 达到最大迭代次数
    if state["iteration"] >= state["max_iterations"]:
        return "end"
    
    # 继续迭代
    return "coder"


def create_workflow(
    coder_node,
    critic_node,
    with_memory: bool = False
):
    """创建 Critic 工作流
    
    Args:
        coder_node: 编码节点函数
        critic_node: 批评节点函数
        with_memory: 是否启用状态持久化
    
    Returns:
        编译后的工作流
    """
    # 创建状态图
    workflow = StateGraph(CriticState)
    
    # 添加节点
    workflow.add_node("coder", coder_node)
    workflow.add_node("critic", critic_node)
    
    # 设置入口点
    workflow.set_entry_point("coder")
    
    # 添加边
    # Coder -> Critic (总是)
    workflow.add_edge("coder", "critic")
    
    # Critic -> 条件分支
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "coder": "coder",  # 继续修改
            "end": END         # 结束
        }
    )
    
    # 编译
    if with_memory:
        # 使用 SQLite 持久化（支持时间旅行）
        memory = SqliteSaver.from_conn_string(":memory:")
        return workflow.compile(checkpointer=memory)
    else:
        return workflow.compile()


def create_hierarchical_workflow(
    coder_node,
    critics: dict,  # {"security": func, "style": func, "logic": func}
    meta_critic_node,
    with_memory: bool = False
):
    """创建层级批评家工作流
    
    架构:
        Coder -> [Security, Style, Logic Critics] -> Meta Critic -> ...
    """
    workflow = StateGraph(CriticState)
    
    # 添加编码节点
    workflow.add_node("coder", coder_node)
    
    # 添加各专业批评家
    for name, critic_func in critics.items():
        workflow.add_node(f"critic_{name}", critic_func)
    
    # 添加元批评家
    workflow.add_node("meta_critic", meta_critic_node)
    
    # 设置入口
    workflow.set_entry_point("coder")
    
    # Coder -> 所有批评家（并行）
    critic_names = [f"critic_{name}" for name in critics.keys()]
    for name in critic_names:
        workflow.add_edge("coder", name)
    
    # 所有批评家 -> 元批评家
    for name in critic_names:
        workflow.add_edge(name, "meta_critic")
    
    # 元批评家 -> 条件分支
    workflow.add_conditional_edges(
        "meta_critic",
        should_continue,
        {"coder": "coder", "end": END}
    )
    
    if with_memory:
        memory = SqliteSaver.from_conn_string(":memory:")
        return workflow.compile(checkpointer=memory)
    
    return workflow.compile()
