"""
共享配置模块
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Config:
    """全局配置"""
    
    # LLM 配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0"))
    
    # Anthropic 配置 (可选)
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Azure OpenAI 配置 (可选)
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    
    # LangSmith 配置 (可观测性)
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "false")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "multiagent-tutorial")
    
    # 智能体配置
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "5"))
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "300"))
    
    @classmethod
    def validate(cls) -> bool:
        """验证必需的配置"""
        if not cls.OPENAI_API_KEY:
            print("⚠️ Warning: OPENAI_API_KEY not set")
            return False
        return True
    
    @classmethod
    def get_llm_config(cls, provider: str = "openai") -> dict:
        """获取 LLM 配置"""
        if provider == "openai":
            return {
                "model": cls.OPENAI_MODEL,
                "temperature": cls.OPENAI_TEMPERATURE,
                "api_key": cls.OPENAI_API_KEY,
            }
        elif provider == "azure":
            return {
                "model": cls.AZURE_OPENAI_DEPLOYMENT,
                "api_key": cls.AZURE_OPENAI_API_KEY,
                "azure_endpoint": cls.AZURE_OPENAI_ENDPOINT,
            }
        else:
            raise ValueError(f"Unknown provider: {provider}")


# 导出默认配置实例
config = Config()
