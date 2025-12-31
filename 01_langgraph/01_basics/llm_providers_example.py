"""
LLM Provider Examples - 多种 LLM 提供商示例
===========================================

展示如何使用不同的 LLM 提供商：
1. OpenAI
2. Azure OpenAI ⭐
3. Anthropic Claude
4. 本地 Ollama

Azure OpenAI 配置指南：
- 在 Azure Portal 创建 OpenAI 资源
- 部署一个模型（如 gpt-4o）
- 获取 endpoint 和 API key
"""

import os
import sys
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dotenv import load_dotenv
load_dotenv()


# ==========================================
# 方式 1: 直接使用 LangChain
# ==========================================

def get_azure_openai_direct():
    """
    直接使用 LangChain 的 AzureChatOpenAI
    
    需要设置以下环境变量：
    - AZURE_OPENAI_API_KEY
    - AZURE_OPENAI_ENDPOINT
    - AZURE_OPENAI_DEPLOYMENT (部署名称)
    """
    from langchain_openai import AzureChatOpenAI
    
    llm = AzureChatOpenAI(
        # Azure 资源的 endpoint
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        # API 密钥
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        # 部署名称（不是模型名称！）
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        # API 版本
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        # 温度参数
        temperature=0,
    )
    
    return llm


def get_openai_direct():
    """直接使用 OpenAI"""
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
    )
    
    return llm


# ==========================================
# 方式 2: 使用项目的统一工厂
# ==========================================

def get_llm_from_factory(provider: str = "azure"):
    """
    使用 shared/llm_providers.py 的统一工厂
    
    支持: "openai", "azure", "anthropic"
    """
    try:
        from shared.llm_providers import get_llm
        return get_llm(provider=provider)
    except ImportError:
        print("请从项目根目录运行")
        return None


# ==========================================
# 测试函数
# ==========================================

def test_llm(llm, provider_name: str):
    """测试 LLM 是否正常工作"""
    print(f"\n{'='*50}")
    print(f"Testing {provider_name}")
    print('='*50)
    
    try:
        response = llm.invoke("Say 'Hello from Azure!' in Chinese")
        print(f"✅ Response: {response.content}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


# ==========================================
# 在 LangGraph 中使用 Azure OpenAI
# ==========================================

def langgraph_with_azure_example():
    """
    在 LangGraph 中使用 Azure OpenAI
    """
    from typing import TypedDict
    from langgraph.graph import StateGraph, END
    from langchain_core.messages import HumanMessage, AIMessage
    
    # 获取 Azure OpenAI LLM
    llm = get_azure_openai_direct()
    
    class ChatState(TypedDict):
        messages: list
        response: str
    
    def chat_node(state: ChatState) -> ChatState:
        """使用 Azure OpenAI 聊天"""
        messages = state["messages"]
        
        # 调用 Azure OpenAI
        response = llm.invoke(messages)
        
        state["response"] = response.content
        state["messages"].append(AIMessage(content=response.content))
        
        return state
    
    # 构建图
    workflow = StateGraph(ChatState)
    workflow.add_node("chat", chat_node)
    workflow.set_entry_point("chat")
    workflow.add_edge("chat", END)
    
    app = workflow.compile()
    
    # 运行
    result = app.invoke({
        "messages": [HumanMessage(content="你好，请用中文介绍一下 Azure OpenAI")],
        "response": ""
    })
    
    print("\n" + "="*50)
    print("LangGraph + Azure OpenAI Result:")
    print("="*50)
    print(result["response"])


# ==========================================
# Main
# ==========================================

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║        LLM Provider Configuration Guide                  ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║  Azure OpenAI 配置步骤：                                   ║
    ║                                                           ║
    ║  1. 在 Azure Portal 创建 OpenAI 资源                      ║
    ║  2. 在资源中部署模型（如 gpt-4o, gpt-4-turbo）            ║
    ║  3. 获取 endpoint 和 API key                              ║
    ║  4. 复制 .env.example 为 .env 并填入：                    ║
    ║                                                           ║
    ║     AZURE_OPENAI_API_KEY=your-key                        ║
    ║     AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/  ║
    ║     AZURE_OPENAI_DEPLOYMENT=your-deployment-name         ║
    ║     AZURE_OPENAI_API_VERSION=2024-02-01                  ║
    ║                                                           ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # 检查环境变量
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print("\n📋 Environment Check:")
    print(f"   AZURE_OPENAI_API_KEY: {'✅ Set' if azure_key else '❌ Not set'}")
    print(f"   AZURE_OPENAI_ENDPOINT: {'✅ Set' if azure_endpoint else '❌ Not set'}")
    print(f"   OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Not set'}")
    
    # 测试 Azure OpenAI（如果配置了）
    if azure_key and azure_endpoint:
        print("\n🔄 Testing Azure OpenAI...")
        try:
            llm = get_azure_openai_direct()
            test_llm(llm, "Azure OpenAI")
            
            # 运行 LangGraph 示例
            print("\n🔄 Running LangGraph + Azure OpenAI example...")
            langgraph_with_azure_example()
            
        except Exception as e:
            print(f"❌ Azure OpenAI test failed: {e}")
    else:
        print("\n⚠️ Azure OpenAI not configured. Please set environment variables.")
    
    # 测试 OpenAI（如果配置了）
    if openai_key and not (azure_key and azure_endpoint):
        print("\n🔄 Testing OpenAI...")
        try:
            llm = get_openai_direct()
            test_llm(llm, "OpenAI")
        except Exception as e:
            print(f"❌ OpenAI test failed: {e}")


if __name__ == "__main__":
    main()
