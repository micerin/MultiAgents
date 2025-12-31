"""
LLM 提供商工厂
"""

from typing import Optional
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_anthropic import ChatAnthropic

from .config import config


def get_llm(
    provider: str = "openai",
    model: Optional[str] = None,
    temperature: float = 0,
    **kwargs
):
    """获取 LLM 实例
    
    Args:
        provider: "openai", "azure", "anthropic"
        model: 模型名称 (可选，使用默认)
        temperature: 温度参数
        **kwargs: 额外参数
    
    Returns:
        LangChain Chat Model 实例
    """
    
    if provider == "openai":
        return ChatOpenAI(
            model=model or config.OPENAI_MODEL,
            temperature=temperature,
            api_key=config.OPENAI_API_KEY,
            **kwargs
        )
    
    elif provider == "azure":
        return AzureChatOpenAI(
            deployment_name=model or config.AZURE_OPENAI_DEPLOYMENT,
            temperature=temperature,
            api_key=config.AZURE_OPENAI_API_KEY,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            **kwargs
        )
    
    elif provider == "anthropic":
        return ChatAnthropic(
            model=model or "claude-3-sonnet-20240229",
            temperature=temperature,
            api_key=config.ANTHROPIC_API_KEY,
            **kwargs
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_default_llm(**kwargs):
    """获取默认 LLM (OpenAI GPT-4)"""
    return get_llm(provider="openai", **kwargs)
