"""
Docker Compose 多容器编排示例
==============================
演示如何使用 Docker Compose 管理多个智能体容器

学习要点:
1. 理解 docker-compose.yml 配置
2. 启动/停止多容器环境
3. 容器间通信
4. 资源限制和网络隔离
"""

import docker
import subprocess
import os
from pathlib import Path


def check_docker_compose():
    """检查 Docker Compose 是否可用"""
    print("=" * 60)
    print("检查 Docker Compose")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # 尝试旧版 docker-compose
            result = subprocess.run(
                ["docker-compose", "version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ {result.stdout.strip()}")
            return True
        except:
            print("❌ Docker Compose 不可用")
            return False


def explain_docker_compose():
    """解释 docker-compose.yml 配置"""
    print("\n" + "=" * 60)
    print("Docker Compose 配置详解")
    print("=" * 60)
    
    compose_file = Path(__file__).parent.parent / "docker" / "docker-compose.yml"
    
    if compose_file.exists():
        print(f"\n📄 配置文件: {compose_file}")
        print("-" * 60)
        
        with open(compose_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 显示配置
        print(content)
        
        print("-" * 60)
        print("\n📌 关键配置说明:")
        print("""
1. sandbox 服务:
   - build: 使用 Dockerfile.sandbox 构建
   - volumes: 挂载 workspace 和 output 目录
   - security_opt: 禁止权限提升
   - deploy.resources: CPU/内存限制
   - networks: 使用隔离网络

2. openhands 服务 (可选):
   - profiles: [openhands] 需要显式启动
   - 挂载 docker.sock 用于嵌套容器
   - 端口 3000 访问 Web UI

3. 网络配置:
   - agent-network: 桥接网络，容器间可通信
   - 可选 network_mode: "none" 完全隔离
""")
    else:
        print(f"❌ 配置文件不存在: {compose_file}")


def demo_compose_commands():
    """演示 Docker Compose 常用命令"""
    print("\n" + "=" * 60)
    print("Docker Compose 常用命令")
    print("=" * 60)
    
    commands = [
        ("构建镜像", "docker compose build"),
        ("启动服务", "docker compose up -d"),
        ("查看状态", "docker compose ps"),
        ("查看日志", "docker compose logs -f"),
        ("停止服务", "docker compose down"),
        ("启动 OpenHands", "docker compose --profile openhands up -d"),
        ("进入容器", "docker compose exec sandbox bash"),
        ("执行命令", "docker compose exec sandbox python script.py"),
    ]
    
    print("\n常用命令:")
    print("-" * 60)
    for desc, cmd in commands:
        print(f"  {desc:20} | {cmd}")
    
    print("\n💡 提示:")
    print("  - 在 docker/ 目录下运行这些命令")
    print("  - 使用 -d 参数后台运行")
    print("  - 使用 --profile 启动特定服务")


def demo_multi_container():
    """演示多容器场景"""
    print("\n" + "=" * 60)
    print("Multi-Agent 多容器架构")
    print("=" * 60)
    
    print("""
┌─────────────────────────────────────────────────────────────┐
│                    Docker Host                               │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Coder      │  │   Executor   │  │   Reviewer   │       │
│  │   Container  │  │   Container  │  │   Container  │       │
│  │              │  │              │  │              │       │
│  │  LLM API     │  │  Python      │  │  LLM API     │       │
│  │  代码生成    │──▶│  代码执行    │──▶│  结果审查    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                 │                 │                │
│         └─────────────────┼─────────────────┘                │
│                           │                                  │
│                    agent-network                             │
└─────────────────────────────────────────────────────────────┘

扩展 docker-compose.yml 示例:

services:
  coder:
    build: .
    environment:
      - ROLE=coder
      - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
    networks:
      - agent-network

  executor:
    build:
      dockerfile: Dockerfile.sandbox
    network_mode: "none"  # 完全隔离
    deploy:
      resources:
        limits:
          memory: 512M

  reviewer:
    build: .
    environment:
      - ROLE=reviewer
    networks:
      - agent-network
""")


def main():
    """主函数"""
    print("🐳 Docker Compose 多容器编排示例")
    print("=" * 60)
    
    # 检查 Docker Compose
    if not check_docker_compose():
        return
    
    # 解释配置
    explain_docker_compose()
    
    # 演示命令
    demo_compose_commands()
    
    # 多容器架构
    demo_multi_container()
    
    print("\n" + "=" * 60)
    print("✅ Docker Compose 示例完成!")
    print("=" * 60)
    print("\n下一步:")
    print("  cd ../docker")
    print("  docker compose build")
    print("  docker compose up -d")


if __name__ == "__main__":
    main()
