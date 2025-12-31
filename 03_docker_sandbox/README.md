# Week 3: Docker 沙盒化

> Secure execution environment for AI coding agents

## 📖 本周概述

> **"Never trust LLM-generated code"** - 永远不要相信 LLM 生成的代码

运行 LLM 生成的代码存在重大安全风险。本周学习如何使用 Docker 创建安全的沙盒执行环境。

## ✅ 已完成示例

| 文件 | 功能 | 关键技术 |
|------|------|----------|
| [01_docker_basics.py](examples/01_docker_basics.py) | Docker SDK 基础操作 | 连接、镜像管理、容器运行 |
| [02_secure_sandbox.py](examples/02_secure_sandbox.py) | 安全沙盒执行器 | 资源限制、超时、网络隔离 |
| [03_autogen_docker_executor.py](examples/03_autogen_docker_executor.py) | AutoGen + Docker | DockerCommandLineCodeExecutor |
| [04_docker_compose_demo.py](examples/04_docker_compose_demo.py) | Docker Compose 多容器 | 服务编排、网络配置 |
| [05_openhands_setup.py](examples/05_openhands_setup.py) | OpenHands 部署指南 | AI 编程助手平台 |

## 🎯 为什么 Multi-Agent 需要 Docker？

### 架构图

```
┌─────────────────────────────────────────────────────┐
│                    Host System                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  Agent 1    │  │  Agent 2    │  │  Agent 3    │  │
│  │  Container  │  │  Container  │  │  Container  │  │
│  │  ─────────  │  │  ─────────  │  │  ─────────  │  │
│  │  独立文件系统 │  │  独立文件系统 │  │  独立文件系统 │  │
│  │  独立网络    │  │  独立网络    │  │  独立网络    │  │
│  │  资源限制    │  │  资源限制    │  │  资源限制    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
```

### 核心好处

| 好处 | 说明 |
|------|------|
| 🔒 **安全隔离** | LLM 生成的代码可能包含恶意操作，容器内执行保护主机 |
| ⚡ **资源控制** | 限制 CPU/内存/时间，防止失控代码耗尽系统资源 |
| 🧹 **环境一致** | 每次执行都是干净环境，可重现，无状态 |
| 🔄 **依赖隔离** | 不同 Agent 可使用不同 Python 版本和包 |

### 安全对比

| 危险场景 | 无 Docker | 有 Docker |
|----------|-----------|-----------|
| `os.system("rm -rf /")` | 💀 系统崩溃 | ✅ 只删容器内文件 |
| `while True: pass` | 💀 CPU 100% | ✅ 超时自动终止 |
| `requests.post(黑客服务器)` | 💀 数据泄露 | ✅ 网络隔离阻断 |
| `bytearray(10GB)` | 💀 内存耗尽 | ✅ OOM Killer 终止 |

### Multi-Agent 协作流程

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Coder      │────▶│   Executor   │────▶│   Reviewer   │
│   Agent      │     │   (Docker)   │     │   Agent      │
└──────────────┘     └──────────────┘     └──────────────┘
      │                    │                    │
      │    生成代码        │    安全执行         │    检查结果
      └────────────────────┴────────────────────┘
```

这就是为什么 **OpenHands、Devin、Claude Code** 等 AI 编程助手都使用 Docker 作为执行环境。

## 🎯 学习目标

完成本周学习后，你将能够：

1. 使用 Python Docker SDK 管理容器
2. 创建安全的代码执行沙盒
3. 配置资源限制和网络隔离
4. 将 Docker 与 AutoGen 集成

## 📁 目录结构

```
03_docker_sandbox/
├── README.md                 # 本文件
├── docker/
│   ├── Dockerfile.sandbox    # 沙盒执行环境
│   ├── docker-compose.yml    # 多容器编排
│   └── requirements.txt      # 容器内 Python 依赖
└── examples/
    ├── 01_docker_basics.py           # Docker SDK 基础
    ├── 02_secure_sandbox.py          # 安全沙盒实现
    ├── 03_autogen_docker_executor.py # AutoGen Docker 集成
    ├── 04_docker_compose_demo.py     # Docker Compose 演示
    └── 05_openhands_setup.py         # OpenHands 部署指南
```

## 🚀 快速开始

### 前置要求

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (已安装并运行)
- Python 3.11+
- `pip install docker autogen-ext[docker]`

### 运行示例

```bash
cd examples

# 1. Docker 基础操作
python 01_docker_basics.py

# 2. 安全沙盒（资源限制、超时、网络隔离）
python 02_secure_sandbox.py

# 3. AutoGen + Docker 集成
python 03_autogen_docker_executor.py
```

## 📚 核心概念

### 1. SecureSandbox 类

```python
class SecureSandbox:
    """安全沙盒执行器"""
    
    def __init__(self, image: str = "python:3.11-slim"):
        self.client = docker.from_env()
        self.config = {
            "mem_limit": "512m",        # 内存限制
            "cpu_quota": 50000,         # CPU 限制 50%
            "network_disabled": True,   # 禁用网络
            "security_opt": ["no-new-privileges:true"],
        }
    
    def execute_code(self, code: str, timeout: int = 30) -> dict:
        """在隔离容器中执行代码"""
        container = self.client.containers.create(
            self.image,
            command=f"python /tmp/code.py",
            mem_limit=self.config["mem_limit"],
            network_disabled=self.config["network_disabled"],
            # ... 其他安全配置
        )
        container.start()
        result = container.wait(timeout=timeout)
        return {"stdout": container.logs(), "exit_code": result["StatusCode"]}
```

### 2. AutoGen Docker 执行器

```python
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.agents import CodeExecutorAgent

# 创建 Docker 执行器
async with DockerCommandLineCodeExecutor(
    image="python:3.11-slim",
    timeout=60,
    work_dir=Path("./workspace")
) as executor:
    
    # 创建代码执行智能体
    code_executor_agent = CodeExecutorAgent(
        "executor",
        code_executor=executor,
    )
    
    # 与 Coder Agent 组成团队
    team = RoundRobinGroupChat([coder, code_executor_agent])
```

### 3. 资源限制配置

| 参数 | 作用 | 推荐值 |
|------|------|--------|
| `mem_limit` | 内存上限 | 512m - 4G |
| `cpu_quota` | CPU 配额 | 50000 (50%) |
| `timeout` | 执行超时 | 30-60s |
| `network_disabled` | 禁用网络 | True |
| `read_only` | 只读文件系统 | True (需 /tmp 可写) |

## 🔐 安全最佳实践

### 1. 最小权限原则

```python
config = {
    "user": "nobody",                           # 非 root 用户
    "read_only": True,                          # 只读文件系统
    "security_opt": ["no-new-privileges:true"], # 禁止权限提升
}
```

### 2. 资源限制

```python
config = {
    "mem_limit": "512m",    # 内存上限
    "cpu_period": 100000,   # CPU 周期
    "cpu_quota": 50000,     # 限制 50% CPU
}
```

### 3. 网络隔离

```python
config = {
    "network_disabled": True,  # 完全禁用网络
}
```

## 📖 参考资源

- [Docker Python SDK](https://docker-py.readthedocs.io/)
- [AutoGen Code Executors](https://microsoft.github.io/autogen/docs/reference/agentchat/agents/code_executor_agent)
- [OpenHands Documentation](https://docs.all-hands.dev/)

## ⏭️ 下一步

完成本周学习后，继续 [Week 4: Beads 记忆系统](../04_beads/)
