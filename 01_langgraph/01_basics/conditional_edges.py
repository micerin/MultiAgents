"""
Conditional Edges - 条件边与分支
=================================

条件边是实现复杂工作流的核心机制：
1. 基于状态的路由决策
2. 多分支选择
3. 循环控制
4. 错误处理分支
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
import random


# ==========================================
# 1. 基础条件边
# ==========================================

class SimpleState(TypedDict):
    value: int
    path_taken: str
    result: str


def check_value(state: SimpleState) -> Literal["high", "low", "medium"]:
    """
    条件函数：根据值决定走向
    
    返回值必须匹配 add_conditional_edges 的映射键
    """
    value = state["value"]
    if value > 70:
        return "high"
    elif value < 30:
        return "low"
    else:
        return "medium"


def high_path(state: SimpleState) -> SimpleState:
    print("🔴 Taking HIGH path")
    state["path_taken"] = "high"
    state["result"] = "Processed as high value"
    return state


def low_path(state: SimpleState) -> SimpleState:
    print("🔵 Taking LOW path")
    state["path_taken"] = "low"
    state["result"] = "Processed as low value"
    return state


def medium_path(state: SimpleState) -> SimpleState:
    print("🟢 Taking MEDIUM path")
    state["path_taken"] = "medium"
    state["result"] = "Processed as medium value"
    return state


def create_branching_graph():
    """创建多分支图"""
    
    workflow = StateGraph(SimpleState)
    
    # 添加起始节点
    workflow.add_node("start", lambda s: s)
    workflow.add_node("high_handler", high_path)
    workflow.add_node("low_handler", low_path)
    workflow.add_node("medium_handler", medium_path)
    
    workflow.set_entry_point("start")
    
    # 条件边：从 start 根据条件分流
    workflow.add_conditional_edges(
        "start",
        check_value,
        {
            "high": "high_handler",
            "low": "low_handler",
            "medium": "medium_handler"
        }
    )
    
    # 所有分支都通向结束
    workflow.add_edge("high_handler", END)
    workflow.add_edge("low_handler", END)
    workflow.add_edge("medium_handler", END)
    
    return workflow.compile()


# ==========================================
# 2. 循环控制
# ==========================================

class LoopState(TypedDict):
    counter: int
    max_count: int
    history: list[str]
    should_stop: bool


def increment_counter(state: LoopState) -> LoopState:
    """递增计数器"""
    state["counter"] += 1
    state["history"].append(f"Count: {state['counter']}")
    print(f"   Counter: {state['counter']}")
    return state


def check_random_stop(state: LoopState) -> LoopState:
    """随机决定是否停止"""
    # 20% 概率随机停止
    if random.random() < 0.2:
        state["should_stop"] = True
        print("   🎲 Random stop triggered!")
    return state


def should_loop(state: LoopState) -> Literal["continue", "stop"]:
    """循环控制条件"""
    if state["should_stop"]:
        return "stop"
    if state["counter"] >= state["max_count"]:
        print(f"   ⚠️ Max count ({state['max_count']}) reached")
        return "stop"
    return "continue"


def create_loop_graph():
    """创建循环控制图"""
    
    workflow = StateGraph(LoopState)
    
    workflow.add_node("increment", increment_counter)
    workflow.add_node("check", check_random_stop)
    
    workflow.set_entry_point("increment")
    
    workflow.add_edge("increment", "check")
    
    workflow.add_conditional_edges(
        "check",
        should_loop,
        {
            "continue": "increment",
            "stop": END
        }
    )
    
    return workflow.compile()


# ==========================================
# 3. 错误处理分支
# ==========================================

class TaskState(TypedDict):
    task: str
    result: str | None
    error: str | None
    retry_count: int
    max_retries: int


def execute_task(state: TaskState) -> TaskState:
    """执行任务（模拟可能失败）"""
    print(f"\n⚙️ Executing task (attempt {state['retry_count'] + 1})...")
    
    # 模拟 40% 失败率
    if random.random() < 0.4:
        state["error"] = f"Task failed on attempt {state['retry_count'] + 1}"
        state["retry_count"] += 1
        print(f"   ❌ Failed: {state['error']}")
    else:
        state["result"] = f"Task '{state['task']}' completed successfully!"
        state["error"] = None
        print(f"   ✅ Success!")
    
    return state


def handle_error(state: TaskState) -> TaskState:
    """错误处理节点"""
    print(f"   🔧 Handling error: {state['error']}")
    return state


def check_result(state: TaskState) -> Literal["success", "retry", "fail"]:
    """检查执行结果"""
    if state["result"] and not state["error"]:
        return "success"
    if state["retry_count"] < state["max_retries"]:
        return "retry"
    return "fail"


def final_success(state: TaskState) -> TaskState:
    print("\n🎉 Task completed successfully!")
    return state


def final_failure(state: TaskState) -> TaskState:
    print(f"\n💀 Task failed after {state['retry_count']} attempts")
    state["result"] = "FAILED"
    return state


def create_error_handling_graph():
    """创建错误处理图"""
    
    workflow = StateGraph(TaskState)
    
    workflow.add_node("execute", execute_task)
    workflow.add_node("handle_error", handle_error)
    workflow.add_node("success", final_success)
    workflow.add_node("failure", final_failure)
    
    workflow.set_entry_point("execute")
    
    workflow.add_conditional_edges(
        "execute",
        check_result,
        {
            "success": "success",
            "retry": "handle_error",
            "fail": "failure"
        }
    )
    
    # 错误处理后重试
    workflow.add_edge("handle_error", "execute")
    
    workflow.add_edge("success", END)
    workflow.add_edge("failure", END)
    
    return workflow.compile()


# ==========================================
# Main Demo
# ==========================================

def main():
    print("=" * 60)
    print("🔀 Conditional Edges Demo")
    print("=" * 60)
    
    # Demo 1: 多分支
    print("\n" + "-" * 40)
    print("Demo 1: Multi-Branch Routing")
    print("-" * 40)
    
    branch_graph = create_branching_graph()
    for value in [85, 15, 50]:
        print(f"\n📊 Input value: {value}")
        result = branch_graph.invoke({
            "value": value,
            "path_taken": "",
            "result": ""
        })
        print(f"   Result: {result['result']}")
    
    # Demo 2: 循环控制
    print("\n" + "-" * 40)
    print("Demo 2: Loop Control")
    print("-" * 40)
    
    loop_graph = create_loop_graph()
    result = loop_graph.invoke({
        "counter": 0,
        "max_count": 10,
        "history": [],
        "should_stop": False
    })
    print(f"\n📊 Final counter: {result['counter']}")
    print(f"   History: {result['history']}")
    
    # Demo 3: 错误处理
    print("\n" + "-" * 40)
    print("Demo 3: Error Handling & Retry")
    print("-" * 40)
    
    error_graph = create_error_handling_graph()
    result = error_graph.invoke({
        "task": "Important Task",
        "result": None,
        "error": None,
        "retry_count": 0,
        "max_retries": 3
    })
    print(f"\n📊 Final result: {result['result']}")


if __name__ == "__main__":
    main()
