"""
AutoGen Code Execution - 代码执行能力
=====================================

AutoGen 的核心能力之一是让 Agent 生成代码并实际执行。

执行器类型：
1. LocalCommandLineCodeExecutor - 本地命令行执行
2. DockerCommandLineCodeExecutor - Docker 容器执行（安全）
3. JupyterCodeExecutor - Jupyter 内核执行

⚠️ 安全警告：本地执行器会在你的机器上运行代码，请谨慎使用！
"""

import os
import sys
import asyncio
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor


def get_model_client():
    """获取 Azure OpenAI 模型客户端"""
    return AzureOpenAIChatCompletionClient(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        model="gpt-4o",
    )


async def demo_code_execution():
    """演示代码执行能力"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           💻 AutoGen Code Execution Demo                     ║
    ║                                                              ║
    ║   Agent 生成代码 → 执行器运行 → 返回结果                    ║
    ║                                                              ║
    ║   ┌──────────┐    代码     ┌──────────┐                     ║
    ║   │  Coder   │ ─────────> │ Executor │                      ║
    ║   │  Agent   │ <───────── │  Agent   │                      ║
    ║   └──────────┘    结果     └──────────┘                     ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    model_client = get_model_client()
    
    # 创建临时工作目录
    work_dir = tempfile.mkdtemp()
    print(f"📁 工作目录: {work_dir}\n")
    
    # 创建本地代码执行器
    code_executor = LocalCommandLineCodeExecutor(
        work_dir=work_dir,
        timeout=60,  # 60秒超时
    )
    
    # 创建 Coder Agent（生成代码）
    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        system_message="""你是一个 Python 专家。

任务：根据用户需求编写 Python 代码。

要求：
1. 代码要完整可运行
2. 用 ```python 包裹代码
3. 包含 print 输出结果
4. 当 Executor 确认代码执行成功后，回复 TERMINATE

注意：不要使用任何需要额外安装的库，只用 Python 标准库。""",
    )
    
    # 创建 Executor Agent（执行代码）
    executor = CodeExecutorAgent(
        name="Executor",
        code_executor=code_executor,
    )
    
    # 创建团队
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(8)
    team = RoundRobinGroupChat(
        [coder, executor],
        termination_condition=termination,
    )
    
    # 任务
    task = "计算斐波那契数列的前 10 个数字，并打印出来"
    
    print(f"📋 任务: {task}")
    print("\n" + "=" * 60)
    print("开始执行...")
    print("=" * 60)
    
    # 运行
    result = await team.run(task=task)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📜 执行历史:")
    print("=" * 60)
    
    for msg in result.messages:
        role = msg.source
        content = msg.content if hasattr(msg, 'content') else str(msg)
        
        if role == "user":
            print(f"\n👤 User:\n{content}")
        elif role == "Coder":
            print(f"\n💻 Coder:\n{content}")
        elif role == "Executor":
            print(f"\n⚙️ Executor:\n{content}")
    
    print("\n" + "=" * 60)
    print("✅ 代码执行演示完成!")
    print("=" * 60)
    
    await model_client.close()


async def demo_data_analysis():
    """演示数据分析场景"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           📊 Data Analysis Demo                              ║
    ║                                                              ║
    ║   让 Agent 生成并执行数据分析代码                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    model_client = get_model_client()
    work_dir = tempfile.mkdtemp()
    
    code_executor = LocalCommandLineCodeExecutor(
        work_dir=work_dir,
        timeout=60,
    )
    
    analyst = AssistantAgent(
        name="DataAnalyst",
        model_client=model_client,
        system_message="""你是一个数据分析师。

任务：编写 Python 代码进行数据分析。

要求：
1. 只使用 Python 标准库（random, statistics, collections 等）
2. 生成示例数据进行分析
3. 打印清晰的分析结果
4. 当执行成功后，回复 TERMINATE""",
    )
    
    executor = CodeExecutorAgent(
        name="Executor",
        code_executor=code_executor,
    )
    
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(6)
    team = RoundRobinGroupChat(
        [analyst, executor],
        termination_condition=termination,
    )
    
    task = """生成 100 个随机考试成绩（0-100分），然后：
1. 计算平均分、最高分、最低分
2. 统计各分数段（优秀90+、良好80-89、中等70-79、及格60-69、不及格<60）的人数
3. 打印统计结果"""
    
    print(f"📋 任务: {task}")
    print("\n" + "=" * 60)
    
    result = await team.run(task=task)
    
    print("\n📜 执行结果:")
    print("=" * 60)
    
    for msg in result.messages:
        role = msg.source
        content = msg.content if hasattr(msg, 'content') else str(msg)
        
        if role == "Executor":
            print(f"\n⚙️ {role}:\n{content}")
        elif role == "DataAnalyst":
            # 只打印代码部分
            if "```python" in content:
                print(f"\n📊 {role} 生成的代码:")
                code_start = content.find("```python")
                code_end = content.find("```", code_start + 10)
                print(content[code_start:code_end + 3])
    
    await model_client.close()


async def demo_iterative_debugging():
    """演示迭代调试场景"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           🔧 Iterative Debugging Demo                        ║
    ║                                                              ║
    ║   Agent 生成代码 → 执行失败 → 修复 → 再执行                 ║
    ║                                                              ║
    ║   展示 Agent 如何处理错误并自我修复                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    model_client = get_model_client()
    work_dir = tempfile.mkdtemp()
    
    code_executor = LocalCommandLineCodeExecutor(
        work_dir=work_dir,
        timeout=60,
    )
    
    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        system_message="""你是一个 Python 开发者。

任务：根据需求编写代码。

如果执行器返回错误：
1. 分析错误原因
2. 修复代码
3. 重新提交

当执行成功后，回复 TERMINATE

只使用 Python 标准库。""",
    )
    
    executor = CodeExecutorAgent(
        name="Executor",
        code_executor=code_executor,
    )
    
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(10)
    team = RoundRobinGroupChat(
        [coder, executor],
        termination_condition=termination,
    )
    
    # 一个稍微复杂的任务，可能需要调试
    task = """写一个函数，实现以下功能：
1. 输入一个字符串
2. 统计每个字符出现的次数
3. 按出现次数降序排列
4. 打印结果

测试字符串："hello world, hello python!" """
    
    print(f"📋 任务: {task}")
    print("\n" + "=" * 60)
    
    result = await team.run(task=task)
    
    print("\n📜 迭代过程:")
    print("=" * 60)
    
    iteration = 0
    for msg in result.messages:
        role = msg.source
        content = msg.content if hasattr(msg, 'content') else str(msg)
        
        if role == "Coder":
            iteration += 1
            print(f"\n🔄 迭代 {iteration} - Coder:")
            # 简化输出
            if "```python" in content:
                print("  [生成代码...]")
            else:
                print(f"  {content[:100]}...")
        elif role == "Executor":
            if "Error" in content or "error" in content:
                print(f"  ❌ 执行错误")
            else:
                print(f"  ✅ 执行成功")
                # 打印输出
                lines = content.split('\n')
                for line in lines[:10]:
                    if line.strip():
                        print(f"     {line}")
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！共 {iteration} 次迭代")
    print("=" * 60)
    
    await model_client.close()


async def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                🚀 AutoGen Code Execution                     ║
    ║                                                              ║
    ║   探索 AutoGen 的代码执行能力                                ║
    ║                                                              ║
    ║   1. 基础代码执行                                            ║
    ║   2. 数据分析场景                                            ║
    ║   3. 迭代调试场景                                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\n" + "=" * 60)
    print("Demo 1: 基础代码执行")
    print("=" * 60)
    await demo_code_execution()
    
    print("\n\n" + "=" * 60)
    print("Demo 2: 数据分析场景")
    print("=" * 60)
    await demo_data_analysis()
    
    print("\n\n" + "=" * 60)
    print("Demo 3: 迭代调试场景")
    print("=" * 60)
    await demo_iterative_debugging()
    
    print("""
    
    ╔══════════════════════════════════════════════════════════════╗
    ║                    📚 学习要点                               ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║  1. CodeExecutorAgent 可以执行 Agent 生成的代码              ║
    ║                                                              ║
    ║  2. LocalCommandLineCodeExecutor 在本地执行                  ║
    ║     - 快速但不安全                                           ║
    ║     - 适合开发测试                                           ║
    ║                                                              ║
    ║  3. DockerCommandLineCodeExecutor 在容器中执行               ║
    ║     - 安全隔离                                               ║
    ║     - 适合生产环境                                           ║
    ║                                                              ║
    ║  4. Agent 可以根据执行结果自动调试修复代码                   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    asyncio.run(main())
