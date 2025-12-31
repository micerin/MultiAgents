"""
DeepEval 测试示例
"""

from deepeval import assert_test
from deepeval.metrics import GEval, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams


# ============ 指标定义 ============

task_completion_metric = GEval(
    name="Task Completion",
    criteria="""Evaluate if the generated code:
    1. Fulfills all stated requirements
    2. Is syntactically correct Python
    3. Handles basic edge cases
    4. Would produce correct output for typical inputs""",
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    threshold=0.7,
)

critique_quality_metric = GEval(
    name="Critique Quality",
    criteria="""Evaluate if the code review:
    1. Is specific and points to exact issues
    2. Is actionable with clear suggestions
    3. Correctly identifies real problems (not false positives)
    4. Is constructive rather than just negative
    5. Prioritizes critical issues appropriately""",
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    threshold=0.7,
)

code_quality_metric = GEval(
    name="Code Quality",
    criteria="""Evaluate the code quality:
    1. Follows PEP 8 style guidelines
    2. Has appropriate type hints
    3. Has clear docstrings
    4. Uses meaningful variable names
    5. Has appropriate error handling""",
    evaluation_params=[
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    threshold=0.6,
)


# ============ 测试用例 ============

def test_coder_simple_function():
    """测试简单函数生成"""
    test_case = LLMTestCase(
        input="Write a Python function to calculate the factorial of a number",
        actual_output="""
def factorial(n: int) -> int:
    \"\"\"Calculate the factorial of a number.
    
    Args:
        n: A non-negative integer
        
    Returns:
        The factorial of n
        
    Raises:
        ValueError: If n is negative
    \"\"\"
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    return n * factorial(n - 1)
""",
    )
    assert_test(test_case, [task_completion_metric, code_quality_metric])


def test_critic_identifies_issues():
    """测试批评家能否识别问题"""
    bad_code = """
def f(x):
    return x * x
"""
    test_case = LLMTestCase(
        input=f"Review this code for a function that calculates square: {bad_code}",
        actual_output="""
Issues found:

1. **Missing Type Hints** (Style)
   - Function parameter `x` has no type annotation
   - Return type is not specified
   - Suggestion: `def f(x: int) -> int:`

2. **Poor Naming** (Style)
   - Function name `f` is not descriptive
   - Suggestion: Use `calculate_square` or `square`

3. **Missing Docstring** (Documentation)
   - No docstring explaining the function's purpose
   - Suggestion: Add a docstring with Args, Returns sections

4. **No Input Validation** (Correctness)
   - No check if input is valid (e.g., numeric type)
   - Suggestion: Add type checking or let type hints handle it

The code is functionally correct but needs improvements in style and documentation.
""",
    )
    assert_test(test_case, [critique_quality_metric])


def test_critic_approves_good_code():
    """测试批评家能否正确通过好代码"""
    good_code = """
def calculate_square(number: int) -> int:
    \"\"\"Calculate the square of a number.
    
    Args:
        number: The integer to square
        
    Returns:
        The square of the input number
        
    Examples:
        >>> calculate_square(4)
        16
        >>> calculate_square(-3)
        9
    \"\"\"
    return number * number
"""
    test_case = LLMTestCase(
        input=f"Review this code: {good_code}",
        actual_output="APPROVED - The code meets all criteria: proper type hints, clear docstring with examples, descriptive naming, and correct implementation.",
    )
    assert_test(test_case, [critique_quality_metric])


# ============ 运行测试 ============

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
