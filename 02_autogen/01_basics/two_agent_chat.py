"""
AutoGen Two Agent Chat - 双智能体对话
=====================================

这是 AutoGen 的入门示例，展示：
1. AssistantAgent 创建
2. UserProxyAgent 配置
3. 双智能体对话流程
"""

from autogen import AssistantAgent, UserProxyAgent
import os

# 配置 LLM
# os.environ["OPENAI_API_KEY"] = "your-api-key"

llm_config = {
    "model": "gpt-4",
    "temperature": 0,
}


def create_agents():
    """创建智能体"""
    
    # 助手智能体 - 使用 LLM 进行推理
    assistant = AssistantAgent(
        name="assistant",
        system_message="""You are a helpful AI assistant.
You help users with coding tasks.
When you're done, say 'TERMINATE'.""",
        llm_config=llm_config,
    )
    
    # 用户代理 - 代表用户，可执行代码
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",  # ALWAYS, TERMINATE, NEVER
        max_consecutive_auto_reply=3,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,  # 生产环境建议设为 True
        },
    )
    
    return assistant, user_proxy


def main():
    print("=" * 60)
    print("💬 AutoGen Two Agent Chat Demo")
    print("=" * 60)
    
    assistant, user_proxy = create_agents()
    
    # 启动对话
    task = "Write a Python function to calculate the factorial of a number."
    
    print(f"\n📋 Task: {task}\n")
    print("-" * 60)
    
    # user_proxy 发起对话
    user_proxy.initiate_chat(
        assistant,
        message=task,
    )
    
    print("-" * 60)
    print("✅ Chat completed!")


if __name__ == "__main__":
    main()
