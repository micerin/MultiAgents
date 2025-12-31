"""
Multi-Critic Challenge - 挑战性场景
====================================

故意生成有问题的代码，观察 Critic 系统的迭代改进过程
"""

import os
import sys
from typing import TypedDict, Annotated, Literal, Optional
import operator
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage


# ==========================================
# 状态定义
# ==========================================

class ChallengeState(TypedDict):
    task: str
    code: str
    critic_scores: Annotated[list[dict], operator.add]
    final_score: float
    aggregated_feedback: str
    iteration: int
    approved: bool
    max_iterations: int
    revision_history: Annotated[list[str], operator.add]


# ==========================================
# LLM
# ==========================================

def get_llm(temperature=0.3):
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        temperature=temperature,
    )


# ==========================================
# Nodes
# ==========================================

def bad_writer_node(state: ChallengeState) -> ChallengeState:
    """故意生成有问题的代码（第一次）"""
    print(f"\n{'='*60}")
    print(f"✍️  WRITER (Iteration {state['iteration'] + 1})")
    print('='*60)
    
    if state["iteration"] == 0:
        # 第一次：故意写有安全问题的代码
        print("   📋 Generating initial (flawed) code...")
        
        # 这段代码有多个问题：SQL 注入、无错误处理、硬编码密码
        flawed_code = '''def get_user(user_id):
    import mysql.connector
    
    # 硬编码的数据库凭证 (Security Issue!)
    password = "admin123"
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="users"
    )
    
    cursor = conn.cursor()
    
    # SQL 注入漏洞! (Security Issue!)
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.close()
    
    return result
'''
        print("   ⚠️ Code has intentional security flaws!")
        return {
            "code": flawed_code,
            "iteration": 1,
            "revision_history": ["Iteration 1: Generated flawed code with security issues"]
        }
    
    else:
        # 后续迭代：使用 LLM 修复
        llm = get_llm()
        prompt = f"""Fix this Python code based on the feedback.

Current Code:
```python
{state['code']}
```

Feedback:
{state['aggregated_feedback']}

Requirements:
1. Fix ALL security issues (SQL injection, hardcoded passwords)
2. Add proper error handling
3. Use environment variables for credentials
4. Add type hints and docstrings
5. Follow PEP 8

Output ONLY the fixed Python code."""

        print("   🔧 Fixing code based on feedback...")
        response = llm.invoke([HumanMessage(content=prompt)])
        
        code = response.content
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        print(f"   ✅ Code revised ({len(code)} chars)")
        
        return {
            "code": code,
            "iteration": state["iteration"] + 1,
            "revision_history": [f"Iteration {state['iteration'] + 1}: Revised based on {len(state['aggregated_feedback'])} chars of feedback"]
        }


def security_critic_strict(state: ChallengeState) -> ChallengeState:
    """严格的安全审查"""
    print("\n   🔒 Security Critic (STRICT MODE)...")
    
    llm = get_llm(temperature=0)
    
    prompt = f"""You are a strict security auditor. Analyze this code for security vulnerabilities.

Code:
```python
{state['code']}
```

Security checklist:
1. SQL Injection vulnerabilities
2. Hardcoded credentials/secrets
3. Insecure connections
4. Missing input validation
5. Error message information leakage

BE STRICT. Any security issue should result in a low score.

Output JSON:
{{
    "score": X.X,
    "risk_level": "critical/high/medium/low/none",
    "vulnerabilities": ["list of issues found"],
    "feedback": "detailed assessment",
    "suggestions": ["how to fix each issue"]
}}"""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        result = json.loads(content)
        score = result.get("score", 3.0)
        risk = result.get("risk_level", "high")
        feedback = result.get("feedback", "")
        suggestions = result.get("suggestions", [])
        vulns = result.get("vulnerabilities", [])
    except:
        score = 3.0
        risk = "high"
        feedback = response.content[:300]
        suggestions = []
        vulns = []
    
    status = "✅" if score >= 7 else "❌"
    print(f"      {status} Score: {score}/10 (Risk: {risk})")
    if vulns:
        print(f"      🚨 Found {len(vulns)} vulnerabilities")
    
    return {
        "critic_scores": [{
            "critic_name": "Security",
            "score": score,
            "feedback": f"[SECURITY] {feedback}\nVulnerabilities: {vulns}",
            "suggestions": suggestions,
            "passed": score >= 7.0
        }]
    }


def code_quality_critic_node(state: ChallengeState) -> ChallengeState:
    """代码质量审查"""
    print("   🔍 Code Quality Critic...")
    
    llm = get_llm(temperature=0)
    
    prompt = f"""Evaluate this Python code for quality.

Code:
```python
{state['code']}
```

Evaluate: readability, error handling, type hints, documentation.

Output JSON:
{{
    "score": X.X,
    "feedback": "assessment",
    "suggestions": ["improvements"]
}}"""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        result = json.loads(content)
        score = result.get("score", 5.0)
        feedback = result.get("feedback", "")
        suggestions = result.get("suggestions", [])
    except:
        score = 5.0
        feedback = response.content[:200]
        suggestions = []
    
    status = "✅" if score >= 7 else "❌"
    print(f"      {status} Score: {score}/10")
    
    return {
        "critic_scores": [{
            "critic_name": "Quality",
            "score": score,
            "feedback": f"[QUALITY] {feedback}",
            "suggestions": suggestions,
            "passed": score >= 7.0
        }]
    }


def aggregator(state: ChallengeState) -> ChallengeState:
    """聚合评分"""
    print(f"\n{'='*60}")
    print("📊 AGGREGATOR")
    print('='*60)
    
    scores = state["critic_scores"]
    
    # 安全权重更高
    weights = {"Security": 0.6, "Quality": 0.4}
    
    total = 0
    weight_sum = 0
    all_feedback = []
    
    for s in scores:
        name = s["critic_name"]
        score = s["score"]
        w = weights.get(name, 0.5)
        total += score * w
        weight_sum += w
        all_feedback.append(s["feedback"])
        print(f"   {name}: {score}/10 (weight: {w})")
    
    final = total / weight_sum if weight_sum > 0 else 0
    print(f"\n   🎯 Weighted Score: {final:.1f}/10")
    
    return {
        "final_score": final,
        "aggregated_feedback": "\n\n".join(all_feedback),
        "critic_scores": []  # Reset
    }


def decision(state: ChallengeState) -> ChallengeState:
    """决策"""
    print(f"\n{'='*60}")
    print("⚖️  DECISION")
    print('='*60)
    
    passed = state["final_score"] >= 7.0
    
    if passed:
        print(f"   ✅ APPROVED ({state['final_score']:.1f} >= 7.0)")
    else:
        remaining = state["max_iterations"] - state["iteration"]
        if remaining > 0:
            print(f"   ❌ REJECTED - {remaining} iterations remaining")
        else:
            print(f"   ⚠️  FORCE APPROVED - max iterations reached")
            passed = True
    
    return {"approved": passed}


def route_decision(state: ChallengeState) -> Literal["end", "writer"]:
    if state["approved"] or state["iteration"] >= state["max_iterations"]:
        return "end"
    return "writer"


# ==========================================
# Build Graph
# ==========================================

def build_challenge_graph():
    workflow = StateGraph(ChallengeState)
    
    workflow.add_node("writer", bad_writer_node)
    workflow.add_node("security_critic", security_critic_strict)
    workflow.add_node("quality_critic", code_quality_critic_node)
    workflow.add_node("aggregator", aggregator)
    workflow.add_node("decision", decision)
    
    workflow.set_entry_point("writer")
    
    # Writer → Critics (parallel fan-out)
    workflow.add_edge("writer", "security_critic")
    workflow.add_edge("writer", "quality_critic")
    
    # Critics → Aggregator
    workflow.add_edge("security_critic", "aggregator")
    workflow.add_edge("quality_critic", "aggregator")
    
    # Aggregator → Decision
    workflow.add_edge("aggregator", "decision")
    
    # Decision → Loop or End
    workflow.add_conditional_edges("decision", route_decision, {"end": END, "writer": "writer"})
    
    return workflow.compile()


# ==========================================
# Main
# ==========================================

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║          🔥 Multi-Critic Challenge Mode                    ║
    ║                                                            ║
    ║    Starting with INTENTIONALLY FLAWED code to test:        ║
    ║    • Security detection (SQL injection, hardcoded creds)   ║
    ║    • Iterative improvement loop                            ║
    ║    • Critic feedback integration                           ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    app = build_challenge_graph()
    
    initial_state: ChallengeState = {
        "task": "Write a function to get user from database",
        "code": "",
        "critic_scores": [],
        "final_score": 0.0,
        "aggregated_feedback": "",
        "iteration": 0,
        "approved": False,
        "max_iterations": 3,
        "revision_history": []
    }
    
    result = app.invoke(initial_state)
    
    print("\n" + "="*60)
    print("📊 CHALLENGE RESULTS")
    print("="*60)
    
    print(f"\n✅ Final Status: {'APPROVED' if result['approved'] else 'REJECTED'}")
    print(f"📈 Final Score: {result['final_score']:.1f}/10")
    print(f"🔄 Total Iterations: {result['iteration']}")
    
    print("\n📜 Revision History:")
    for entry in result["revision_history"]:
        print(f"   • {entry}")
    
    print("\n📝 Final Code:")
    print("-"*60)
    print(result["code"])
    print("-"*60)


if __name__ == "__main__":
    main()
