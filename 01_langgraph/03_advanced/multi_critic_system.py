"""
Advanced Multi-Critic System - 高级多维度批评家系统
====================================================

一个真实的代码审查系统，包含：
1. 多个专业 Critic（代码质量、安全性、风格、性能）
2. 评分聚合与冲突解决
3. 迭代改进循环
4. 人工介入机制

架构图：
                    ┌─────────────────────────────────────────────┐
                    │                                             │
                    ▼                                             │
              ┌──────────┐                                        │
              │  WRITER  │  生成/修改代码                          │
              └────┬─────┘                                        │
                   │                                              │
                   ▼                                              │
         ┌─────────────────────┐                                  │
         │   PARALLEL CRITICS  │  并行评审                        │
         │  ┌─────┬─────┬─────┐│                                  │
         │  │Code │Sec  │Style││                                  │
         │  │Qual │urity│     ││                                  │
         │  └─────┴─────┴─────┘│                                  │
         └─────────┬───────────┘                                  │
                   │                                              │
                   ▼                                              │
            ┌────────────┐                                        │
            │ AGGREGATOR │  汇总评分，解决冲突                     │
            └─────┬──────┘                                        │
                  │                                               │
                  ▼                                               │
            ┌────────────┐     ┌──────────┐                       │
            │  DECISION  │────►│ HUMAN    │ (可选)                │
            │   MAKER    │     │ REVIEW   │                       │
            └─────┬──────┘     └────┬─────┘                       │
                  │                 │                             │
                  ├─────────────────┘                             │
                  │                                               │
             Pass?│                                               │
                  │ No ────────────────────────────────────────────
                  │ Yes
                  ▼
            ┌──────────┐
            │   END    │
            └──────────┘
"""

import os
import sys
from typing import TypedDict, Annotated, Literal, Optional
from dataclasses import dataclass
import operator
import json

# 添加项目根目录
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


# ==========================================
# 配置
# ==========================================

@dataclass
class CriticConfig:
    """Critic 系统配置"""
    max_iterations: int = 3
    pass_threshold: float = 7.0  # 总分 10 分，7 分及格
    require_human_review: bool = False  # 是否需要人工审核
    human_review_threshold: float = 6.0  # 低于此分数需人工审核


# ==========================================
# 状态定义
# ==========================================

@dataclass
class CriticScore:
    """单个 Critic 的评分"""
    critic_name: str
    score: float  # 0-10
    feedback: str
    suggestions: list[str]
    passed: bool


class MultiCriticState(TypedDict):
    """多 Critic 系统状态"""
    # 输入
    task: str
    code: str
    
    # Critic 评分
    critic_scores: Annotated[list[dict], operator.add]
    
    # 聚合结果
    final_score: float
    aggregated_feedback: str
    conflicts: list[str]
    
    # 控制流
    iteration: int
    approved: bool
    needs_human_review: bool
    human_decision: Optional[str]
    
    # 历史
    revision_history: Annotated[list[str], operator.add]


# ==========================================
# LLM 初始化
# ==========================================

def get_llm():
    """获取 Azure OpenAI LLM"""
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        temperature=0.3,
    )


# ==========================================
# Writer Node
# ==========================================

def writer_node(state: MultiCriticState) -> MultiCriticState:
    """代码生成/修改节点"""
    print(f"\n{'='*60}")
    print(f"✍️  WRITER (Iteration {state['iteration'] + 1})")
    print('='*60)
    
    llm = get_llm()
    
    if state["iteration"] == 0:
        # 首次生成
        prompt = f"""You are an expert Python developer. Write clean, well-documented code.

Task: {state['task']}

Requirements:
1. Follow PEP 8 style guidelines
2. Add type hints
3. Include docstrings
4. Handle potential errors
5. Consider security best practices

Output ONLY the Python code, no explanations."""
        
        print(f"   📋 Task: {state['task']}")
        print("   🔄 Generating initial code...")
        
    else:
        # 基于反馈修改
        feedback = state.get("aggregated_feedback", "")
        prompt = f"""You are an expert Python developer. Revise the code based on feedback.

Original Task: {state['task']}

Current Code:
```python
{state['code']}
```

Feedback to address:
{feedback}

Revision Requirements:
1. Address ALL feedback points
2. Maintain existing functionality
3. Improve code quality

Output ONLY the revised Python code, no explanations."""
        
        print(f"   📋 Revising based on feedback...")
        print(f"   📝 Feedback summary: {feedback[:100]}...")
    
    response = llm.invoke([HumanMessage(content=prompt)])
    code = response.content
    
    # 清理代码块标记
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    print(f"   ✅ Code generated ({len(code)} chars)")
    
    return {
        "code": code,
        "iteration": state["iteration"] + 1,
        "revision_history": [f"Iteration {state['iteration'] + 1}: Generated/Revised code"]
    }


# ==========================================
# Critic Nodes
# ==========================================

def code_quality_critic(state: MultiCriticState) -> MultiCriticState:
    """代码质量 Critic"""
    print("\n   🔍 Code Quality Critic evaluating...")
    
    llm = get_llm()
    
    prompt = f"""You are a code quality expert. Evaluate this Python code.

Code:
```python
{state['code']}
```

Evaluate on these criteria (score 0-10 for each):
1. Readability (clear naming, structure)
2. Maintainability (modularity, DRY)
3. Documentation (docstrings, comments)
4. Error Handling (exceptions, edge cases)
5. Type Hints (completeness, correctness)

Output JSON format:
{{
    "scores": {{"readability": X, "maintainability": X, "documentation": X, "error_handling": X, "type_hints": X}},
    "average_score": X.X,
    "feedback": "Overall assessment...",
    "suggestions": ["suggestion1", "suggestion2", ...]
}}"""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        # 解析 JSON
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content)
        score = result.get("average_score", 5.0)
        feedback = result.get("feedback", "No feedback")
        suggestions = result.get("suggestions", [])
    except:
        score = 5.0
        feedback = response.content[:200]
        suggestions = []
    
    print(f"      Score: {score}/10")
    
    return {
        "critic_scores": [{
            "critic_name": "Code Quality",
            "score": score,
            "feedback": feedback,
            "suggestions": suggestions,
            "passed": score >= 7.0
        }]
    }


def security_critic(state: MultiCriticState) -> MultiCriticState:
    """安全性 Critic"""
    print("   🔒 Security Critic evaluating...")
    
    llm = get_llm()
    
    prompt = f"""You are a security expert. Analyze this Python code for security issues.

Code:
```python
{state['code']}
```

Check for:
1. Injection vulnerabilities (SQL, Command, etc.)
2. Hardcoded secrets/credentials
3. Insecure data handling
4. Input validation issues
5. Authentication/Authorization flaws

Output JSON format:
{{
    "security_score": X.X,
    "vulnerabilities_found": ["vuln1", "vuln2"],
    "risk_level": "low/medium/high/critical",
    "feedback": "Security assessment...",
    "suggestions": ["fix1", "fix2", ...]
}}"""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content)
        score = result.get("security_score", 5.0)
        feedback = result.get("feedback", "No feedback")
        suggestions = result.get("suggestions", [])
        risk = result.get("risk_level", "unknown")
    except:
        score = 5.0
        feedback = response.content[:200]
        suggestions = []
        risk = "unknown"
    
    print(f"      Score: {score}/10 (Risk: {risk})")
    
    return {
        "critic_scores": [{
            "critic_name": "Security",
            "score": score,
            "feedback": feedback,
            "suggestions": suggestions,
            "passed": score >= 7.0
        }]
    }


def style_critic(state: MultiCriticState) -> MultiCriticState:
    """代码风格 Critic"""
    print("   🎨 Style Critic evaluating...")
    
    llm = get_llm()
    
    prompt = f"""You are a Python style expert (PEP 8). Review this code for style compliance.

Code:
```python
{state['code']}
```

Check for:
1. PEP 8 compliance (naming, spacing, line length)
2. Import organization
3. Code formatting consistency
4. Pythonic idioms usage
5. Clean code principles

Output JSON format:
{{
    "style_score": X.X,
    "pep8_issues": ["issue1", "issue2"],
    "feedback": "Style assessment...",
    "suggestions": ["improvement1", "improvement2", ...]
}}"""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content)
        score = result.get("style_score", 5.0)
        feedback = result.get("feedback", "No feedback")
        suggestions = result.get("suggestions", [])
    except:
        score = 5.0
        feedback = response.content[:200]
        suggestions = []
    
    print(f"      Score: {score}/10")
    
    return {
        "critic_scores": [{
            "critic_name": "Style",
            "score": score,
            "feedback": feedback,
            "suggestions": suggestions,
            "passed": score >= 7.0
        }]
    }


# ==========================================
# Aggregator Node
# ==========================================

def aggregator_node(state: MultiCriticState) -> MultiCriticState:
    """聚合所有 Critic 评分"""
    print(f"\n{'='*60}")
    print("📊 AGGREGATOR")
    print('='*60)
    
    scores = state["critic_scores"]
    
    # 计算加权平均分
    weights = {
        "Code Quality": 0.4,
        "Security": 0.35,
        "Style": 0.25
    }
    
    total_weight = 0
    weighted_sum = 0
    all_feedback = []
    all_suggestions = []
    conflicts = []
    
    print("\n   📋 Critic Scores:")
    for score_dict in scores:
        name = score_dict["critic_name"]
        score = score_dict["score"]
        weight = weights.get(name, 0.33)
        
        weighted_sum += score * weight
        total_weight += weight
        
        status = "✅" if score_dict["passed"] else "❌"
        print(f"      {status} {name}: {score}/10 (weight: {weight})")
        
        all_feedback.append(f"[{name}] {score_dict['feedback']}")
        all_suggestions.extend(score_dict.get("suggestions", []))
    
    final_score = weighted_sum / total_weight if total_weight > 0 else 0
    
    # 检测冲突（不同 Critic 意见相差太大）
    score_values = [s["score"] for s in scores]
    if max(score_values) - min(score_values) > 3:
        conflicts.append(f"Large score variance: {min(score_values)}-{max(score_values)}")
    
    # 聚合反馈
    aggregated = f"""
Final Score: {final_score:.1f}/10

Feedback Summary:
{chr(10).join(all_feedback)}

Top Suggestions:
{chr(10).join(['- ' + s for s in all_suggestions[:5]])}
"""
    
    print(f"\n   🎯 Final Score: {final_score:.1f}/10")
    
    config = CriticConfig()
    needs_human = (
        config.require_human_review or 
        final_score < config.human_review_threshold or
        len(conflicts) > 0
    )
    
    return {
        "final_score": final_score,
        "aggregated_feedback": aggregated,
        "conflicts": conflicts,
        "needs_human_review": needs_human,
        "critic_scores": []  # 重置以避免累积
    }


# ==========================================
# Decision Node
# ==========================================

def decision_node(state: MultiCriticState) -> MultiCriticState:
    """决策节点"""
    print(f"\n{'='*60}")
    print("⚖️  DECISION MAKER")
    print('='*60)
    
    config = CriticConfig()
    
    passed = state["final_score"] >= config.pass_threshold
    
    if passed:
        print(f"   ✅ APPROVED (Score: {state['final_score']:.1f} >= {config.pass_threshold})")
    else:
        print(f"   ❌ REJECTED (Score: {state['final_score']:.1f} < {config.pass_threshold})")
        if state["iteration"] >= config.max_iterations:
            print(f"   ⚠️  Max iterations ({config.max_iterations}) reached")
            passed = True  # 强制通过，避免无限循环
    
    return {
        "approved": passed
    }


# ==========================================
# Human Review Node (Optional)
# ==========================================

def human_review_node(state: MultiCriticState) -> MultiCriticState:
    """人工审核节点（模拟）"""
    print(f"\n{'='*60}")
    print("👤 HUMAN REVIEW")
    print('='*60)
    
    print(f"\n   Score: {state['final_score']:.1f}/10")
    print(f"   Conflicts: {state['conflicts']}")
    print("\n   [Simulating human review...]")
    
    # 模拟人工决策
    # 实际场景中这里会暂停等待真人输入
    if state["final_score"] >= 5.0:
        decision = "approve"
        print("   👍 Human approved with minor concerns")
    else:
        decision = "reject"
        print("   👎 Human requested revisions")
    
    return {
        "human_decision": decision,
        "approved": decision == "approve"
    }


# ==========================================
# Routing Functions
# ==========================================

def route_after_decision(state: MultiCriticState) -> Literal["human_review", "end", "writer"]:
    """决策后的路由"""
    config = CriticConfig()
    
    if state["approved"]:
        return "end"
    
    if state["needs_human_review"]:
        return "human_review"
    
    if state["iteration"] >= config.max_iterations:
        return "end"
    
    return "writer"


def route_after_human(state: MultiCriticState) -> Literal["end", "writer"]:
    """人工审核后的路由"""
    if state["approved"]:
        return "end"
    return "writer"


# ==========================================
# 构建图
# ==========================================

def build_multi_critic_graph():
    """构建多 Critic 系统图"""
    
    workflow = StateGraph(MultiCriticState)
    
    # 添加节点
    workflow.add_node("writer", writer_node)
    workflow.add_node("code_quality_critic", code_quality_critic)
    workflow.add_node("security_critic", security_critic)
    workflow.add_node("style_critic", style_critic)
    workflow.add_node("aggregator", aggregator_node)
    workflow.add_node("decision", decision_node)
    workflow.add_node("human_review", human_review_node)
    
    # 设置入口
    workflow.set_entry_point("writer")
    
    # Writer → 并行 Critics
    # 注意：LangGraph 的"并行"是通过扇出实现的
    workflow.add_edge("writer", "code_quality_critic")
    workflow.add_edge("writer", "security_critic")
    workflow.add_edge("writer", "style_critic")
    
    # Critics → Aggregator
    workflow.add_edge("code_quality_critic", "aggregator")
    workflow.add_edge("security_critic", "aggregator")
    workflow.add_edge("style_critic", "aggregator")
    
    # Aggregator → Decision
    workflow.add_edge("aggregator", "decision")
    
    # Decision → 条件路由
    workflow.add_conditional_edges(
        "decision",
        route_after_decision,
        {
            "end": END,
            "human_review": "human_review",
            "writer": "writer"
        }
    )
    
    # Human Review → 条件路由
    workflow.add_conditional_edges(
        "human_review",
        route_after_human,
        {
            "end": END,
            "writer": "writer"
        }
    )
    
    return workflow.compile()


# ==========================================
# Main
# ==========================================

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║         🔍 Advanced Multi-Critic System                      ║
    ║                                                              ║
    ║    A production-grade code review system with:               ║
    ║    • Multiple specialized Critics (Quality, Security, Style) ║
    ║    • Weighted score aggregation                              ║
    ║    • Conflict detection                                      ║
    ║    • Iterative improvement loop                              ║
    ║    • Optional human review                                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 构建图
    app = build_multi_critic_graph()
    
    # 测试任务
    task = """Write a Python function that:
1. Connects to a database
2. Fetches user data by ID
3. Returns the user info as a dictionary
4. Handles errors gracefully"""

    print(f"📋 Task: {task}")
    print("\n" + "="*60)
    print("Starting Multi-Critic Review Process...")
    print("="*60)
    
    # 初始状态
    initial_state: MultiCriticState = {
        "task": task,
        "code": "",
        "critic_scores": [],
        "final_score": 0.0,
        "aggregated_feedback": "",
        "conflicts": [],
        "iteration": 0,
        "approved": False,
        "needs_human_review": False,
        "human_decision": None,
        "revision_history": []
    }
    
    # 运行
    result = app.invoke(initial_state)
    
    # 输出结果
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    
    print(f"\n✅ Approved: {result['approved']}")
    print(f"📈 Final Score: {result['final_score']:.1f}/10")
    print(f"🔄 Iterations: {result['iteration']}")
    
    print("\n📝 Final Code:")
    print("-"*40)
    print(result["code"])
    print("-"*40)
    
    print("\n📜 Revision History:")
    for entry in result["revision_history"]:
        print(f"   • {entry}")


if __name__ == "__main__":
    main()
