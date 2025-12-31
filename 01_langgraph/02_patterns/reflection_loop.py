"""
Reflection Loop - 反思循环模式
==============================

这是 Critic Agent 的基础模式，展示：
1. 条件边实现循环
2. 最大迭代控制
3. 基于状态的决策
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class ReflectionState(TypedDict):
    """反思循环状态"""
    task: str
    draft: str
    critique: str
    iteration: int
    max_iterations: int
    approved: bool


def writer_node(state: ReflectionState) -> ReflectionState:
    """写作节点 - 生成或修改内容"""
    print(f"\n✍️ Writer (Iteration {state['iteration'] + 1})")
    
    # 模拟 LLM 调用
    if state["iteration"] == 0:
        # 首次生成
        state["draft"] = f"Draft for: {state['task']}"
        print(f"   Generated initial draft")
    else:
        # 根据批评修改
        state["draft"] = f"Revised draft (v{state['iteration'] + 1}) addressing: {state['critique'][:50]}..."
        print(f"   Revised based on critique")
    
    state["iteration"] += 1
    return state


def critic_node(state: ReflectionState) -> ReflectionState:
    """批评节点 - 评审内容"""
    print(f"🔍 Critic reviewing...")
    
    # 模拟批评逻辑
    if state["iteration"] < 2:
        state["critique"] = f"Needs improvement: add more details, iteration {state['iteration']}"
        state["approved"] = False
        print(f"   ❌ Rejected: {state['critique']}")
    else:
        state["critique"] = "APPROVED - meets all criteria"
        state["approved"] = True
        print(f"   ✅ Approved!")
    
    return state


def should_continue(state: ReflectionState) -> Literal["writer", "end"]:
    """决定是否继续循环"""
    if state["approved"]:
        return "end"
    if state["iteration"] >= state["max_iterations"]:
        print(f"   ⚠️ Max iterations ({state['max_iterations']}) reached")
        return "end"
    return "writer"


def create_reflection_graph():
    """创建反思循环图"""
    
    workflow = StateGraph(ReflectionState)
    
    # 添加节点
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)
    
    # 设置入口
    workflow.set_entry_point("writer")
    
    # Writer -> Critic
    workflow.add_edge("writer", "critic")
    
    # Critic -> 条件分支
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "writer": "writer",  # 继续循环
            "end": END           # 结束
        }
    )
    
    return workflow.compile()


def main():
    print("=" * 60)
    print("🔄 Reflection Loop Demo")
    print("=" * 60)
    
    app = create_reflection_graph()
    
    initial_state = {
        "task": "Write a blog post about AI agents",
        "draft": "",
        "critique": "",
        "iteration": 0,
        "max_iterations": 5,
        "approved": False
    }
    
    print(f"\n📋 Task: {initial_state['task']}")
    print(f"   Max iterations: {initial_state['max_iterations']}")
    
    # 运行
    result = app.invoke(initial_state)
    
    print("\n" + "=" * 60)
    print("📊 Final Result:")
    print(f"   Iterations: {result['iteration']}")
    print(f"   Approved: {result['approved']}")
    print(f"   Final draft: {result['draft'][:100]}...")
    print("=" * 60)


if __name__ == "__main__":
    main()
