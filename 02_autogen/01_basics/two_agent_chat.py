"""
Two-Agent Chat - 双智能体对话
==============================

展示 AutoGen 0.4+ 的核心特性：两个 Agent 之间的对话式协作

场景：Writer 和 Critic 的代码审查对话

对比 LangGraph：
- LangGraph: 图节点之间通过共享状态传递
- AutoGen: Agent 之间通过消息直接对话
"""

import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient


def get_model_client():
    """获取 Azure OpenAI 模型客户端"""
    return AzureOpenAIChatCompletionClient(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        model="gpt-4o",
    )


async def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           💬 Two-Agent Chat Demo                         ║
    ║                                                          ║
    ║   Writer 和 Critic 的对话式代码审查                      ║
    ║                                                          ║
    ║   流程：                                                  ║
    ║   User → Writer (写代码) → Critic (审查) → Writer...     ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    model_client = get_model_client()
    
    # 创建 Writer Agent
    writer = AssistantAgent(
        name="Writer",
        model_client=model_client,
        system_message="""你是一个 Python 开发者。
        
任务：根据需求编写代码。
- 收到需求时，编写完整的 Python 代码
- 收到审查反馈时，根据反馈修改代码
- 当 Critic 说 APPROVED 时，回复 TERMINATE

输出格式：只输出 Python 代码，用 ```python 包裹。""",
    )
    
    # 创建 Critic Agent
    critic = AssistantAgent(
        name="Critic",
        model_client=model_client,
        system_message="""你是一个代码审查专家。

任务：审查 Writer 的代码。
评审标准：
1. 代码是否有错误处理
2. 是否有类型提示
3. 是否有文档字符串
4. 是否遵循 PEP 8

如果代码满足所有标准，回复：APPROVED
如果需要改进，列出具体问题并要求修改。

保持简洁，每次只提出最重要的 2-3 个问题。""",
    )
    
    # 创建团队（轮询式对话）
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(10)
    
    team = RoundRobinGroupChat(
        [writer, critic],
        termination_condition=termination,
    )
    
    # 任务
    task = "写一个函数，计算列表中所有数字的平均值"
    
    print(f"📋 任务: {task}")
    print("\n" + "=" * 60)
    print("对话开始...")
    print("=" * 60)
    
    # 运行对话
    result = await team.run(task=task)
    
    # 输出对话历史
    print("\n" + "=" * 60)
    print("📜 对话历史:")
    print("=" * 60)
    
    for msg in result.messages:
        role = msg.source
        content = msg.content if hasattr(msg, 'content') else str(msg)
        
        if role == "user":
            print(f"\n👤 User:\n{content}")
        elif role == "Writer":
            print(f"\n✍️ Writer:\n{content}")
        elif role == "Critic":
            print(f"\n🔍 Critic:\n{content}")
        else:
            print(f"\n[{role}]:\n{content}")
    
    print("\n" + "=" * 60)
    print(f"✅ 对话结束！共 {len(result.messages)} 条消息")
    print("=" * 60)
    
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
