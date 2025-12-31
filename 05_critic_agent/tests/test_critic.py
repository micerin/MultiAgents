"""
Critic Agent 单元测试
"""

import pytest
from src.graph.state import CriticState, ReviewStatus, create_initial_state


class TestCriticState:
    """测试状态定义"""
    
    def test_create_initial_state(self):
        """测试初始状态创建"""
        state = create_initial_state(
            task="Write a hello world function",
            requirements=["Print 'Hello, World!'"],
            max_iterations=3
        )
        
        assert state["task"] == "Write a hello world function"
        assert state["requirements"] == ["Print 'Hello, World!'"]
        assert state["max_iterations"] == 3
        assert state["iteration"] == 0
        assert state["code"] == ""
        assert state["review_status"] == ReviewStatus.PENDING.value
    
    def test_review_status_enum(self):
        """测试审查状态枚举"""
        assert ReviewStatus.PENDING.value == "pending"
        assert ReviewStatus.APPROVED.value == "approved"
        assert ReviewStatus.NEEDS_REVISION.value == "needs_revision"


class TestWorkflow:
    """测试工作流"""
    
    def test_should_continue_approved(self):
        """测试通过审查时停止"""
        from src.graph.workflow import should_continue
        
        state = create_initial_state("test", [], 5)
        state["review_status"] = ReviewStatus.APPROVED.value
        
        assert should_continue(state) == "end"
    
    def test_should_continue_max_iterations(self):
        """测试达到最大迭代时停止"""
        from src.graph.workflow import should_continue
        
        state = create_initial_state("test", [], max_iterations=3)
        state["iteration"] = 3
        state["review_status"] = ReviewStatus.NEEDS_REVISION.value
        
        assert should_continue(state) == "end"
    
    def test_should_continue_needs_revision(self):
        """测试需要修改时继续"""
        from src.graph.workflow import should_continue
        
        state = create_initial_state("test", [], max_iterations=5)
        state["iteration"] = 1
        state["review_status"] = ReviewStatus.NEEDS_REVISION.value
        
        assert should_continue(state) == "coder"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
