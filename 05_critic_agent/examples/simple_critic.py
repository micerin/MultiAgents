"""
Simple Critic Agent - 简单批评家智能体
======================================

使用 LangGraph 实现的完整 Coder-Critic 循环
"""

import os
import sys
from typing import TypedDict, List, Literal
from enum import Enum

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# os.environ["OPENAI_API_KEY"] = "your-api-key"


class ReviewStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"


class CriticState(TypedDict):
    """Critic 工作流状态"""
    task: str
    requirements: List[str]
    code: str
    critique: str
    review_status: str
    iteration: int
    max_iterations: int
    history: List[dict]


# ============ 智能体定义 ============

class CoderAgent:
    """编码智能体"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Python developer.
Write clean, efficient, and well-documented code.
Follow PEP 8 style guidelines.
Include type hints and docstrings."""),
            ("human", """Task: {task}

Requirements:
{requirements}

{revision_instructions}

Write the Python code:""")
        ])
    
    def generate(self, state: CriticState) -> str:
        revision = ""
        if state["iteration"] > 0 and state["critique"]:
            revision = f"""
IMPORTANT: Your previous code was rejected.

Critic's feedback:
{state['critique']}

Please address ALL issues mentioned above."""
        
        chain = self.prompt | self.llm
        response = chain.invoke({
            "task": state["task"],
            "requirements": "\n".join(f"- {r}" for r in state["requirements"]),
            "revision_instructions": revision
        })
        return response.content


class CriticAgent:
    """批评家智能体"""
    
    REVIEW_CRITERIA = [
        "Code correctness - Does it solve the task?",
        "Syntax - Is the code syntactically correct?",
        "Type hints - Are type hints included?",
        "Docstrings - Are functions documented?",
        "Error handling - Are edge cases handled?",
        "Code style - Does it follow PEP 8?",
    ]
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code reviewer.
Review the code against these criteria:
{criteria}

Be specific and actionable in your feedback.
If ALL criteria are met, respond with exactly: "APPROVED"
Otherwise, list the specific issues that need to be fixed."""),
            ("human", """Task: {task}

Code to review:
```python
{code}
```

Provide your detailed review:""")
        ])
    
    def review(self, state: CriticState) -> dict:
        chain = self.prompt | self.llm
        response = chain.invoke({
            "criteria": "\n".join(f"- {c}" for c in self.REVIEW_CRITERIA),
            "task": state["task"],
            "code": state["code"]
        })
        
        content = response.content
        approved = "APPROVED" in content.upper() and "NOT APPROVED" not in content.upper()
        
        return {
            "critique": content,
            "approved": approved
        }


# ============ 工作流节点 ============

def coder_node(state: CriticState) -> CriticState:
    """编码节点"""
    print(f"\n{'='*50}")
    print(f"✍️ CODER (Iteration {state['iteration'] + 1})")
    print(f"{'='*50}")
    
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    coder = CoderAgent(llm)
    
    code = coder.generate(state)
    state["code"] = code
    state["iteration"] += 1
    
    print(f"\nGenerated code:\n{'-'*30}\n{code[:500]}...")
    return state


def critic_node(state: CriticState) -> CriticState:
    """批评节点"""
    print(f"\n{'='*50}")
    print(f"🔍 CRITIC")
    print(f"{'='*50}")
    
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    critic = CriticAgent(llm)
    
    result = critic.review(state)
    state["critique"] = result["critique"]
    state["review_status"] = (
        ReviewStatus.APPROVED.value if result["approved"] 
        else ReviewStatus.NEEDS_REVISION.value
    )
    
    # 记录历史
    state["history"].append({
        "iteration": state["iteration"],
        "code_preview": state["code"][:200],
        "critique_preview": state["critique"][:200],
        "status": state["review_status"]
    })
    
    status_emoji = "✅" if result["approved"] else "❌"
    print(f"\n{status_emoji} Status: {state['review_status']}")
    print(f"\nCritique:\n{'-'*30}\n{state['critique'][:300]}...")
    
    return state


def should_continue(state: CriticState) -> Literal["coder", "end"]:
    """决定是否继续"""
    if state["review_status"] == ReviewStatus.APPROVED.value:
        print("\n🎉 Code approved!")
        return "end"
    if state["iteration"] >= state["max_iterations"]:
        print(f"\n⚠️ Max iterations ({state['max_iterations']}) reached")
        return "end"
    print(f"\n🔄 Continuing to iteration {state['iteration'] + 1}...")
    return "coder"


# ============ 构建工作流 ============

def create_critic_workflow():
    """创建 Critic 工作流"""
    
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
    
    return workflow.compile()


# ============ 主函数 ============

def main():
    print("=" * 60)
    print("🤖 Simple Critic Agent Demo")
    print("=" * 60)
    
    # 创建工作流
    app = create_critic_workflow()
    
    # 定义任务
    task = "Write a function to validate email addresses"
    requirements = [
        "Use regular expressions",
        "Return True for valid emails, False otherwise",
        "Handle common edge cases",
        "Include type hints",
        "Include a docstring with examples",
    ]
    
    print(f"\n📋 Task: {task}")
    print(f"📝 Requirements:")
    for r in requirements:
        print(f"   - {r}")
    
    # 初始状态
    initial_state: CriticState = {
        "task": task,
        "requirements": requirements,
        "code": "",
        "critique": "",
        "review_status": ReviewStatus.PENDING.value,
        "iteration": 0,
        "max_iterations": 3,
        "history": []
    }
    
    # 运行
    result = app.invoke(initial_state)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📊 FINAL RESULT")
    print("=" * 60)
    print(f"Total iterations: {result['iteration']}")
    print(f"Final status: {result['review_status']}")
    print(f"\nFinal code:\n{'-'*30}")
    print(result["code"])
    
    return result


if __name__ == "__main__":
    main()
