"""
AutoGen Critic Pattern - 批评家模式
===================================

展示使用 AutoGen 实现 Coder-Critic 循环：
1. Coder 生成代码
2. Critic 审查代码
3. 迭代直到通过
"""

from autogen import AssistantAgent, UserProxyAgent
import os

# os.environ["OPENAI_API_KEY"] = "your-api-key"

llm_config = {
    "model": "gpt-4",
    "temperature": 0,
}


def create_critic_agents():
    """创建 Coder 和 Critic 智能体"""
    
    # 编码智能体
    coder = AssistantAgent(
        name="Coder",
        system_message="""You are an expert Python developer.
Write clean, efficient, and well-documented code.
Follow PEP 8 style guidelines.
Include type hints and docstrings.

When the Critic approves your code, say 'TERMINATE'.""",
        llm_config=llm_config,
    )
    
    # 批评家智能体
    critic = AssistantAgent(
        name="Critic",
        system_message="""You are an expert code reviewer.
Review the code for:
1. Correctness - Does it solve the problem?
2. Code quality - Is it clean and readable?
3. Security - Any potential vulnerabilities?
4. Best practices - Does it follow Python conventions?

Be specific and constructive in your feedback.
If the code meets all criteria, respond with 'APPROVED'.
Otherwise, list specific issues to fix.""",
        llm_config=llm_config,
    )
    
    return coder, critic


def create_user_proxy():
    """创建用户代理"""
    return UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,  # 不自动回复
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
        code_execution_config=False,
    )


def run_critic_loop(task: str):
    """运行 Critic 循环"""
    
    coder, critic = create_critic_agents()
    user_proxy = create_user_proxy()
    
    print("=" * 60)
    print("🔄 Critic Pattern Demo")
    print("=" * 60)
    print(f"\n📋 Task: {task}\n")
    
    # 创建初始消息
    initial_message = f"""Task: {task}

Please write the code. After writing, the Critic will review it.
Address any feedback and iterate until the code is approved."""
    
    # 使用嵌套对话模式
    # Coder 写代码 -> Critic 审查 -> Coder 修改 -> ...
    
    def reflection_message(recipient, messages, sender, config):
        """生成反思消息"""
        last_msg = messages[-1]["content"]
        return f"Critic's feedback:\n{last_msg}\n\nPlease revise the code based on this feedback."
    
    # 注册嵌套对话
    coder.register_nested_chats(
        [
            {
                "recipient": critic,
                "message": reflection_message,
                "max_turns": 1,
                "summary_method": "last_msg",
            }
        ],
        trigger=user_proxy,
    )
    
    # 启动对话
    user_proxy.initiate_chat(
        coder,
        message=initial_message,
        max_turns=5,  # 最多 5 轮
    )
    
    print("\n" + "=" * 60)
    print("✅ Critic loop completed!")


def main():
    task = "Write a function to validate email addresses using regex"
    run_critic_loop(task)


if __name__ == "__main__":
    main()
