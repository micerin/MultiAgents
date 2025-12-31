"""
Hello LangGraph - 第一个图结构智能体
=====================================

这是 LangGraph 的入门示例，展示：
1. StateGraph 基础结构
2. 节点（Node）定义
3. 边（Edge）连接
4. 编译和运行
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import os

# 确保设置了 API Key
# os.environ["OPENAI_API_KEY"] = "your-api-key"


# 1. 定义状态结构
class AgentState(TypedDict):
    """智能体状态
    
    TypedDict 确保状态的类型安全
    """
    messages: list[str]
    current_step: str
    result: str


# 2. 定义节点函数
def analyze_task(state: AgentState) -> AgentState:
    """分析任务节点"""
    print("📝 Analyzing task...")
    state["current_step"] = "analyze"
    state["messages"].append("Task analyzed")
    return state


def execute_task(state: AgentState) -> AgentState:
    """执行任务节点"""
    print("⚙️ Executing task...")
    state["current_step"] = "execute"
    state["messages"].append("Task executed")
    return state


def review_result(state: AgentState) -> AgentState:
    """审查结果节点"""
    print("🔍 Reviewing result...")
    state["current_step"] = "review"
    state["messages"].append("Result reviewed")
    state["result"] = "Success!"
    return state


# 3. 构建图
def create_simple_graph():
    """创建一个简单的顺序执行图"""
    
    # 初始化图，传入状态类型
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("analyze", analyze_task)
    workflow.add_node("execute", execute_task)
    workflow.add_node("review", review_result)
    
    # 设置入口点
    workflow.set_entry_point("analyze")
    
    # 添加边（顺序连接）
    workflow.add_edge("analyze", "execute")
    workflow.add_edge("execute", "review")
    workflow.add_edge("review", END)
    
    # 编译图
    app = workflow.compile()
    
    return app


# 4. 运行示例
def main():
    print("=" * 50)
    print("🚀 Hello LangGraph!")
    print("=" * 50)
    
    # 创建图
    app = create_simple_graph()
    
    # 初始状态
    initial_state = {
        "messages": [],
        "current_step": "start",
        "result": ""
    }
    
    # 运行图
    print("\n📊 Running graph...")
    result = app.invoke(initial_state)
    
    # 输出结果
    print("\n" + "=" * 50)
    print("✅ Final Result:")
    print(f"   Messages: {result['messages']}")
    print(f"   Result: {result['result']}")
    print("=" * 50)
    
    return result


if __name__ == "__main__":
    main()
