"""
Critic Agent - 状态定义
"""

from typing import TypedDict, List, Optional
from enum import Enum


class ReviewStatus(Enum):
    """审查状态"""
    PENDING = "pending"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"
    REJECTED = "rejected"


class Issue(TypedDict):
    """代码问题"""
    severity: str  # "error", "warning", "info"
    category: str  # "correctness", "security", "style", "performance"
    line: Optional[int]
    message: str
    suggestion: Optional[str]


class CriticState(TypedDict):
    """Critic 工作流状态
    
    这是 LangGraph 状态图的核心数据结构。
    所有节点共享并修改这个状态。
    """
    
    # === 任务信息 ===
    task: str                    # 任务描述
    requirements: List[str]      # 具体要求
    context: Optional[str]       # 额外上下文
    
    # === 代码状态 ===
    code: str                    # 当前代码
    language: str                # 编程语言
    
    # === 审查状态 ===
    critique: str                # 批评文本
    review_status: str           # ReviewStatus 值
    issues: List[Issue]          # 结构化问题列表
    
    # === 迭代控制 ===
    iteration: int               # 当前迭代次数
    max_iterations: int          # 最大迭代次数
    
    # === 历史记录 ===
    history: List[dict]          # 每轮迭代的记录
    
    # === 元数据 ===
    metadata: Optional[dict]     # 额外信息


def create_initial_state(
    task: str,
    requirements: List[str],
    max_iterations: int = 3,
    language: str = "python"
) -> CriticState:
    """创建初始状态的工厂函数"""
    return CriticState(
        task=task,
        requirements=requirements,
        context=None,
        code="",
        language=language,
        critique="",
        review_status=ReviewStatus.PENDING.value,
        issues=[],
        iteration=0,
        max_iterations=max_iterations,
        history=[],
        metadata={}
    )
