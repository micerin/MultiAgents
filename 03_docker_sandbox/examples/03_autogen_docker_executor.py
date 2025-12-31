"""
AutoGen Docker 执行器示例
=========================
使用 AutoGen 的 DockerCommandLineCodeExecutor 实现安全代码执行

这是从 Week 2 延续的内容，展示如何将 Docker 沙盒与 AutoGen 智能体结合
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# 加载环境变量
load_dotenv(project_root / ".env")

# AutoGen 导入
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

# Docker 执行器
try:
    from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False
    print("⚠️ Docker executor not available. Install with: pip install autogen-ext[docker]")


def get_azure_client():
    """获取 Azure OpenAI 客户端"""
    return AzureOpenAIChatCompletionClient(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
    )


async def demo_docker_executor():
    """演示 Docker 代码执行器"""
    print("=" * 60)
    print("Demo 1: AutoGen Docker 代码执行器")
    print("=" * 60)
    
    if not DOCKER_AVAILABLE:
        print("❌ Docker executor not available")
        return
    
    # 创建 Docker 执行器
    # 使用 async context manager 确保正确清理
    async with DockerCommandLineCodeExecutor(
        image="python:3.11-slim",
        timeout=60,
        work_dir=Path("./docker_work")
    ) as executor:
        
        # 创建代码执行智能体
        code_executor_agent = CodeExecutorAgent(
            "code_executor",
            code_executor=executor,
        )
        
        # 创建编程智能体
        coder = AssistantAgent(
            "coder",
            model_client=get_azure_client(),
            system_message="""你是一个 Python 专家程序员。
            
当用户提出编程任务时，你应该：
1. 编写完整、可执行的 Python 代码
2. 代码必须放在 ```python 代码块中
3. 代码应该打印输出结果以便验证
4. 如果代码执行失败，分析错误并修复

当任务完成时，说 "TERMINATE"。
""",
        )
        
        # 创建团队
        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(10)
        team = RoundRobinGroupChat(
            [coder, code_executor_agent],
            termination_condition=termination,
        )
        
        # 执行任务
        task = "编写 Python 代码计算并打印斐波那契数列的前 15 个数字"
        print(f"\n任务: {task}\n")
        print("-" * 60)
        
        async for message in team.run_stream(task=task):
            if hasattr(message, 'source') and hasattr(message, 'content'):
                print(f"\n[{message.source}]:")
                print(message.content[:500] if len(message.content) > 500 else message.content)
        
        print("-" * 60)
        print("✅ Demo 1 完成")


async def demo_docker_data_analysis():
    """演示 Docker 中的数据分析"""
    print("\n" + "=" * 60)
    print("Demo 2: Docker 中的数据分析")
    print("=" * 60)
    
    if not DOCKER_AVAILABLE:
        print("❌ Docker executor not available")
        return
    
    # 创建 Docker 执行器（安装了更多包的镜像）
    async with DockerCommandLineCodeExecutor(
        image="python:3.11-slim",
        timeout=120,
        work_dir=Path("./docker_work")
    ) as executor:
        
        code_executor_agent = CodeExecutorAgent(
            "executor",
            code_executor=executor,
        )
        
        analyst = AssistantAgent(
            "analyst",
            model_client=get_azure_client(),
            system_message="""你是一个数据分析专家。

任务要求：
1. 编写 Python 代码进行数据分析
2. 先安装必要的包（使用 pip install）
3. 生成示例数据并进行分析
4. 打印分析结果
5. 代码放在 ```python 代码块中

完成后说 "TERMINATE"。
""",
        )
        
        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(10)
        team = RoundRobinGroupChat(
            [analyst, code_executor_agent],
            termination_condition=termination,
        )
        
        task = """
        创建一个包含 100 个随机数的数据集（只使用标准库），
        计算并打印：
        1. 平均值
        2. 标准差
        3. 最大值和最小值
        4. 中位数
        """
        
        print(f"\n任务: {task}\n")
        print("-" * 60)
        
        async for message in team.run_stream(task=task):
            if hasattr(message, 'source') and hasattr(message, 'content'):
                print(f"\n[{message.source}]:")
                content = message.content
                print(content[:800] if len(content) > 800 else content)
        
        print("-" * 60)
        print("✅ Demo 2 完成")


async def demo_docker_security():
    """演示 Docker 的安全隔离"""
    print("\n" + "=" * 60)
    print("Demo 3: Docker 安全隔离验证")
    print("=" * 60)
    
    if not DOCKER_AVAILABLE:
        print("❌ Docker executor not available")
        return
    
    async with DockerCommandLineCodeExecutor(
        image="python:3.11-slim",
        timeout=30,
        work_dir=Path("./docker_work")
    ) as executor:
        
        code_executor_agent = CodeExecutorAgent(
            "executor",
            code_executor=executor,
        )
        
        security_tester = AssistantAgent(
            "tester",
            model_client=get_azure_client(),
            system_message="""你是一个安全测试专家。

任务：编写代码测试 Docker 容器的安全隔离：
1. 尝试读取 /etc/passwd 文件
2. 检查当前用户权限
3. 检查容器的网络状态
4. 打印所有检查结果

注意：这是安全测试，目的是验证隔离是否生效。
代码放在 ```python 代码块中。
完成后说 "TERMINATE"。
""",
        )
        
        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(8)
        team = RoundRobinGroupChat(
            [security_tester, code_executor_agent],
            termination_condition=termination,
        )
        
        task = "测试 Docker 容器的安全隔离特性，验证代码运行在受限环境中"
        
        print(f"\n任务: {task}\n")
        print("-" * 60)
        
        async for message in team.run_stream(task=task):
            if hasattr(message, 'source') and hasattr(message, 'content'):
                print(f"\n[{message.source}]:")
                content = message.content
                print(content[:600] if len(content) > 600 else content)
        
        print("-" * 60)
        print("✅ Demo 3 完成")


async def main():
    """主函数"""
    print("🐳 AutoGen Docker 执行器示例")
    print("=" * 60)
    
    # 检查环境变量
    required_vars = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"❌ 缺少环境变量: {missing}")
        print("请在 .env 文件中设置这些变量")
        return
    
    if not DOCKER_AVAILABLE:
        print("❌ Docker executor 不可用")
        print("请安装: pip install autogen-ext[docker]")
        return
    
    # 检查 Docker
    import docker
    try:
        client = docker.from_env()
        client.ping()
        print("✅ Docker 连接成功")
    except Exception as e:
        print(f"❌ Docker 连接失败: {e}")
        print("请确保 Docker Desktop 已安装并运行")
        return
    
    # 运行演示
    await demo_docker_executor()
    await demo_docker_data_analysis()
    await demo_docker_security()
    
    print("\n" + "=" * 60)
    print("✅ 所有 Docker 执行器示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
