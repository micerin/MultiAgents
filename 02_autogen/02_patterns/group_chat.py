"""
GroupChat - 多智能体群聊
=========================

展示 AutoGen 的群聊能力：多个专业 Agent 协作完成任务

场景：Planner + Coder + Reviewer 三人协作开发
"""

import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
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
    ║           👥 GroupChat Demo                              ║
    ║                                                          ║
    ║   多智能体群聊协作                                        ║
    ║                                                          ║
    ║   参与者：                                                ║
    ║   📋 Planner - 任务规划和分解                             ║
    ║   💻 Coder - 编写代码                                     ║
    ║   🔍 Reviewer - 代码审查                                  ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    model_client = get_model_client()
    
    # 创建 Planner Agent
    planner = AssistantAgent(
        name="Planner",
        model_client=model_client,
        system_message="""你是项目规划师。

职责：
- 分析任务需求
- 将任务分解为具体步骤
- 协调团队工作

当收到任务时：
1. 分析需求
2. 列出实现步骤
3. 指定由 Coder 开始编码

保持简洁，用中文回复。""",
    )
    
    # 创建 Coder Agent
    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        system_message="""你是 Python 开发者。

职责：
- 根据 Planner 的计划编写代码
- 根据 Reviewer 的反馈修改代码

要求：
- 代码要有类型提示
- 代码要有文档字符串
- 代码要有错误处理

完成编码后，请 Reviewer 审查。
用 ```python 包裹代码。""",
    )
    
    # 创建 Reviewer Agent
    reviewer = AssistantAgent(
        name="Reviewer",
        model_client=model_client,
        system_message="""你是代码审查专家。

职责：
- 审查 Coder 的代码
- 检查代码质量、安全性、可读性

如果代码通过审查，回复 "APPROVED"，然后说 "TERMINATE"
如果需要修改，列出问题并要求 Coder 修改。

保持简洁，每次最多 3 个问题。""",
    )
    
    # 创建群聊团队（选择器模式 - LLM 决定下一个说话的人）
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(12)
    
    team = SelectorGroupChat(
        [planner, coder, reviewer],
        model_client=model_client,
        termination_condition=termination,
    )
    
    # 任务
    task = "开发一个简单的待办事项（Todo）类，支持添加、删除、列出任务"
    
    print(f"📋 任务: {task}")
    print("\n" + "=" * 60)
    print("群聊开始...")
    print("=" * 60)
    
    # 运行群聊
    result = await team.run(task=task)
    
    # 输出对话历史
    print("\n" + "=" * 60)
    print("📜 对话历史:")
    print("=" * 60)
    
    icons = {
        "user": "👤",
        "Planner": "📋",
        "Coder": "💻",
        "Reviewer": "🔍",
    }
    
    for msg in result.messages:
        role = msg.source
        content = msg.content if hasattr(msg, 'content') else str(msg)
        icon = icons.get(role, "🤖")
        print(f"\n{icon} {role}:\n{content}")
    
    print("\n" + "=" * 60)
    print(f"✅ 群聊结束！共 {len(result.messages)} 条消息")
    print("=" * 60)
    
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
