"""
Hello AutoGen - 第一个 AutoGen 程序
====================================

AutoGen 0.4+ 使用新的 API 结构：
- autogen_agentchat: 核心 Agent 和 Team 类
- autogen_ext: 扩展，包括 OpenAI 模型客户端
"""

import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
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
    ║              🤖 Hello AutoGen!                           ║
    ║                                                          ║
    ║   AutoGen 是微软的对话式多智能体框架                      ║
    ║   特点：Agent 之间通过消息传递协作                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # 创建模型客户端
    model_client = get_model_client()
    
    # 创建一个简单的 Assistant Agent
    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="你是一个友好的AI助手，用中文回答问题。保持回答简洁。",
    )
    
    print("📋 创建了一个 AssistantAgent")
    print("=" * 50)
    
    # 发送消息并获取响应
    print("\n👤 用户: 用一句话解释什么是多智能体系统？\n")
    
    response = await assistant.on_messages(
        [TextMessage(content="用一句话解释什么是多智能体系统？", source="user")],
        cancellation_token=None,
    )
    
    print(f"🤖 Assistant: {response.chat_message.content}")
    
    print("\n" + "=" * 50)
    print("✅ Hello AutoGen 完成!")
    
    # 关闭模型客户端
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
