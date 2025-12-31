"""
Planner-Worker Pattern - 规划器-执行者模式
==========================================

这是多智能体协作的核心模式之一：
1. Planner 将复杂任务分解为子任务
2. Worker 执行具体子任务
3. 通过状态管理任务队列
4. 支持并行和顺序执行

研究报告参考：
> "规划器-执行者模式是编码任务的主导模式。
> 规划器智能体将高级目标分解为一系列细粒度的步骤，
> 执行者智能体然后逐一执行这些步骤。"
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
import json


# ==========================================
# 状态定义
# ==========================================

class SubTask(TypedDict):
    id: str
    description: str
    status: Literal["pending", "in_progress", "completed", "failed"]
    result: str | None


class PlannerWorkerState(TypedDict):
    # 原始任务
    original_task: str
    # 分解后的子任务
    subtasks: list[SubTask]
    # 当前执行的子任务索引
    current_index: int
    # 最终结果
    final_result: str
    # 执行日志
    execution_log: list[str]


# ==========================================
# Planner 节点
# ==========================================

def planner_node(state: PlannerWorkerState) -> PlannerWorkerState:
    """
    规划器：将任务分解为子任务
    
    在生产环境中，这里会调用 LLM 进行智能分解
    """
    print("\n📋 PLANNER: Decomposing task...")
    
    task = state["original_task"]
    
    # 模拟任务分解（实际应用中使用 LLM）
    subtasks = [
        {
            "id": "1",
            "description": f"Analyze requirements for: {task}",
            "status": "pending",
            "result": None
        },
        {
            "id": "2",
            "description": f"Design solution architecture",
            "status": "pending",
            "result": None
        },
        {
            "id": "3",
            "description": f"Implement core functionality",
            "status": "pending",
            "result": None
        },
        {
            "id": "4",
            "description": f"Write tests and documentation",
            "status": "pending",
            "result": None
        }
    ]
    
    state["subtasks"] = subtasks
    state["current_index"] = 0
    state["execution_log"].append(f"Planned {len(subtasks)} subtasks")
    
    print(f"   Created {len(subtasks)} subtasks:")
    for st in subtasks:
        print(f"   - [{st['id']}] {st['description']}")
    
    return state


# ==========================================
# Worker 节点
# ==========================================

def worker_node(state: PlannerWorkerState) -> PlannerWorkerState:
    """
    执行者：执行当前子任务
    """
    idx = state["current_index"]
    subtask = state["subtasks"][idx]
    
    print(f"\n⚙️ WORKER: Executing subtask [{subtask['id']}]")
    print(f"   Task: {subtask['description']}")
    
    # 更新状态为进行中
    state["subtasks"][idx]["status"] = "in_progress"
    
    # 模拟执行（实际应用中调用 LLM 或工具）
    result = f"Completed: {subtask['description']}"
    
    # 更新为完成
    state["subtasks"][idx]["status"] = "completed"
    state["subtasks"][idx]["result"] = result
    state["execution_log"].append(f"Completed subtask {subtask['id']}")
    
    print(f"   ✅ Result: {result}")
    
    # 移动到下一个
    state["current_index"] += 1
    
    return state


# ==========================================
# 路由逻辑
# ==========================================

def should_continue(state: PlannerWorkerState) -> Literal["worker", "synthesize"]:
    """决定是继续执行还是综合结果"""
    if state["current_index"] < len(state["subtasks"]):
        return "worker"
    return "synthesize"


# ==========================================
# Synthesizer 节点
# ==========================================

def synthesizer_node(state: PlannerWorkerState) -> PlannerWorkerState:
    """
    综合器：汇总所有子任务结果
    """
    print("\n📊 SYNTHESIZER: Aggregating results...")
    
    results = []
    for subtask in state["subtasks"]:
        if subtask["status"] == "completed":
            results.append(f"✅ [{subtask['id']}] {subtask['result']}")
        else:
            results.append(f"❌ [{subtask['id']}] {subtask['status']}")
    
    state["final_result"] = "\n".join(results)
    state["execution_log"].append("Synthesized final result")
    
    print("   All subtasks completed!")
    
    return state


# ==========================================
# 构建图
# ==========================================

def create_planner_worker_graph():
    """创建规划器-执行者图"""
    
    workflow = StateGraph(PlannerWorkerState)
    
    # 添加节点
    workflow.add_node("planner", planner_node)
    workflow.add_node("worker", worker_node)
    workflow.add_node("synthesizer", synthesizer_node)
    
    # 设置入口
    workflow.set_entry_point("planner")
    
    # Planner -> Worker
    workflow.add_edge("planner", "worker")
    
    # Worker -> 条件路由
    workflow.add_conditional_edges(
        "worker",
        should_continue,
        {
            "worker": "worker",
            "synthesize": "synthesizer"
        }
    )
    
    # Synthesizer -> END
    workflow.add_edge("synthesizer", END)
    
    return workflow.compile()


# ==========================================
# 可视化
# ==========================================

def visualize_workflow():
    """打印工作流程图"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║              Planner-Worker Pattern                       ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║    ┌──────────┐                                          ║
    ║    │  START   │                                          ║
    ║    └────┬─────┘                                          ║
    ║         │                                                 ║
    ║         ▼                                                 ║
    ║    ┌──────────┐      Decompose task                      ║
    ║    │ PLANNER  │ ───► into subtasks                       ║
    ║    └────┬─────┘                                          ║
    ║         │                                                 ║
    ║         ▼                                                 ║
    ║    ┌──────────┐                                          ║
    ║ ┌─►│  WORKER  │ Execute current subtask                  ║
    ║ │  └────┬─────┘                                          ║
    ║ │       │                                                 ║
    ║ │       ▼                                                 ║
    ║ │  ┌──────────┐                                          ║
    ║ │  │  MORE?   │ Check if more subtasks                   ║
    ║ │  └────┬─────┘                                          ║
    ║ │       │                                                 ║
    ║ │  Yes  │  No                                            ║
    ║ └───────┘  │                                             ║
    ║            ▼                                              ║
    ║    ┌────────────┐                                        ║
    ║    │ SYNTHESIZER│ Aggregate results                      ║
    ║    └────┬───────┘                                        ║
    ║         │                                                 ║
    ║         ▼                                                 ║
    ║    ┌──────────┐                                          ║
    ║    │   END    │                                          ║
    ║    └──────────┘                                          ║
    ║                                                           ║
    ╚══════════════════════════════════════════════════════════╝
    """)


# ==========================================
# Main
# ==========================================

def main():
    print("=" * 60)
    print("🏗️ Planner-Worker Pattern Demo")
    print("=" * 60)
    
    visualize_workflow()
    
    # 创建图
    app = create_planner_worker_graph()
    
    # 初始状态
    initial_state = {
        "original_task": "Build a user authentication system",
        "subtasks": [],
        "current_index": 0,
        "final_result": "",
        "execution_log": []
    }
    
    print(f"\n📋 Original Task: {initial_state['original_task']}")
    print("\n" + "-" * 60)
    
    # 运行
    result = app.invoke(initial_state)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    print(result["final_result"])
    
    print("\n📝 Execution Log:")
    for log in result["execution_log"]:
        print(f"   • {log}")


if __name__ == "__main__":
    main()
