"""
OpenHands 本地部署指南
=======================
OpenHands (前 OpenDevin) 是一个开源的 AI 编程助手平台

学习要点:
1. 什么是 OpenHands
2. 本地部署方式
3. 配置 Azure OpenAI
4. 使用技巧
"""

import subprocess
import os
from pathlib import Path


def intro_openhands():
    """介绍 OpenHands"""
    print("=" * 60)
    print("什么是 OpenHands?")
    print("=" * 60)
    
    print("""
OpenHands (前身 OpenDevin) 是一个开源的 AI 软件开发平台。

🎯 核心特性:
  - 🤖 AI 编程助手，可以编写和执行代码
  - 🐳 Docker 沙盒执行，安全隔离
  - 🌐 Web UI 界面，易于交互
  - 🔧 支持多种 LLM (OpenAI, Azure, Claude, 本地模型)
  - 📁 完整的文件系统访问

🏗️ 架构:
┌─────────────────────────────────────────────────────────┐
│                    OpenHands                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Web UI    │  │   Agent     │  │   Sandbox   │      │
│  │   (3000)    │──│   Runtime   │──│   (Docker)  │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                          │                               │
│                     LLM API                              │
│              (Azure OpenAI / OpenAI)                     │
└─────────────────────────────────────────────────────────┘

📖 官方文档: https://docs.all-hands.dev/
🐙 GitHub: https://github.com/All-Hands-AI/OpenHands
""")


def setup_docker():
    """Docker 方式部署"""
    print("\n" + "=" * 60)
    print("方式 1: Docker 快速部署 (推荐)")
    print("=" * 60)
    
    print("""
1️⃣ 拉取镜像:
   docker pull docker.all-hands.dev/all-hands-ai/openhands:latest

2️⃣ 启动 OpenHands:
   docker run -it --rm \\
     --name openhands \\
     -p 3000:3000 \\
     -v /var/run/docker.sock:/var/run/docker.sock \\
     -v $(pwd)/workspace:/opt/workspace_base \\
     -e SANDBOX_USER_ID=$(id -u) \\
     docker.all-hands.dev/all-hands-ai/openhands:latest

3️⃣ 访问 Web UI:
   http://localhost:3000

4️⃣ 配置 LLM (在 Web UI 中):
   - 选择 Azure OpenAI
   - 输入 Endpoint, API Key, Deployment Name
""")


def setup_docker_compose():
    """Docker Compose 方式部署"""
    print("\n" + "=" * 60)
    print("方式 2: Docker Compose 部署")
    print("=" * 60)
    
    compose_content = '''
# openhands-compose.yml
version: '3.8'

services:
  openhands:
    image: docker.all-hands.dev/all-hands-ai/openhands:latest
    container_name: openhands
    ports:
      - "3000:3000"
    environment:
      - SANDBOX_USER_ID=1000
      - WORKSPACE_BASE=/opt/workspace_base
      # Azure OpenAI 配置 (可选，也可在 UI 中配置)
      # - LLM_MODEL=azure/gpt-4o
      # - LLM_API_KEY=${AZURE_OPENAI_API_KEY}
      # - LLM_BASE_URL=${AZURE_OPENAI_ENDPOINT}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./workspace:/opt/workspace_base
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: unless-stopped
'''
    
    print(compose_content)
    
    print("""
启动命令:
   docker compose -f openhands-compose.yml up -d

停止命令:
   docker compose -f openhands-compose.yml down
""")


def setup_azure_openai():
    """配置 Azure OpenAI"""
    print("\n" + "=" * 60)
    print("配置 Azure OpenAI")
    print("=" * 60)
    
    print("""
在 OpenHands Web UI 中配置 Azure OpenAI:

1️⃣ 打开设置 (Settings)

2️⃣ LLM Provider 选择: Azure

3️⃣ 填写配置:
   - Model: gpt-4o (或你的 deployment name)
   - API Key: 你的 Azure OpenAI API Key
   - Base URL: https://你的资源名.openai.azure.com/

4️⃣ 高级配置 (可选):
   - API Version: 2024-02-15-preview
   - Max Tokens: 4096
   - Temperature: 0.7

💡 提示:
   - Azure deployment name 必须与 Model 字段匹配
   - Base URL 末尾需要 /
   - 确保你的 Azure OpenAI 资源已启用 gpt-4o 模型
""")


def tips_and_tricks():
    """使用技巧"""
    print("\n" + "=" * 60)
    print("OpenHands 使用技巧")
    print("=" * 60)
    
    print("""
🎯 最佳实践:

1. 任务描述要清晰
   ❌ "写个网站"
   ✅ "创建一个 Flask 网站，包含用户登录功能，使用 SQLite 数据库"

2. 分步骤执行
   - 先让 AI 分析需求
   - 确认方案后再编码
   - 逐个功能实现

3. 代码审查
   - AI 生成的代码需要人工审查
   - 特别注意安全相关代码
   - 检查依赖版本

4. 利用 Workspace
   - 在 workspace 目录放置参考文件
   - AI 可以读取已有代码
   - 基于现有项目扩展

⚠️ 注意事项:
   - 不要在 AI 环境中存放敏感信息
   - 定期清理 workspace
   - 注意 token 消耗
""")


def check_prerequisites():
    """检查前置条件"""
    print("\n" + "=" * 60)
    print("检查前置条件")
    print("=" * 60)
    
    checks = []
    
    # 检查 Docker
    try:
        result = subprocess.run(
            ["docker", "version", "--format", "{{.Server.Version}}"],
            capture_output=True,
            text=True,
            check=True
        )
        checks.append(("Docker", True, result.stdout.strip()))
    except:
        checks.append(("Docker", False, "未安装"))
    
    # 检查 Docker Compose
    try:
        result = subprocess.run(
            ["docker", "compose", "version", "--short"],
            capture_output=True,
            text=True,
            check=True
        )
        checks.append(("Docker Compose", True, result.stdout.strip()))
    except:
        checks.append(("Docker Compose", False, "未安装"))
    
    # 检查端口
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_available = sock.connect_ex(('localhost', 3000)) != 0
    sock.close()
    checks.append(("端口 3000", port_available, "可用" if port_available else "被占用"))
    
    # 显示结果
    for name, status, info in checks:
        icon = "✅" if status else "❌"
        print(f"  {icon} {name}: {info}")
    
    return all(status for _, status, _ in checks)


def main():
    """主函数"""
    print("🤖 OpenHands 本地部署指南")
    print("=" * 60)
    
    # 介绍
    intro_openhands()
    
    # 检查前置条件
    check_prerequisites()
    
    # Docker 部署
    setup_docker()
    
    # Docker Compose 部署
    setup_docker_compose()
    
    # Azure OpenAI 配置
    setup_azure_openai()
    
    # 使用技巧
    tips_and_tricks()
    
    print("\n" + "=" * 60)
    print("✅ OpenHands 部署指南完成!")
    print("=" * 60)
    print("\n快速开始:")
    print("  docker pull docker.all-hands.dev/all-hands-ai/openhands:latest")
    print("  # 然后按上述步骤启动")


if __name__ == "__main__":
    main()
