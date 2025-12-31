# Week 3: Docker 沙盒化

> Secure execution environment for AI coding agents

## 📖 本周概述

> **"Always Sandbox"** - 永远不要直接在主机操作系统上运行编码智能体

运行 LLM 生成的代码存在重大安全风险。本周学习如何使用 Docker 创建安全的沙盒执行环境。

## 🎯 学习目标

完成本周学习后，你将能够：

1. 创建智能体专用的 Docker 镜像
2. 使用 Docker Compose 编排多智能体系统
3. 配置 OpenHands 本地开发环境
4. 实现安全的代码执行隔离

## 📁 目录结构

```
03_docker_sandbox/
├── README.md                 # 本文件
├── docker/
│   ├── Dockerfile.agent      # 智能体运行环境
│   ├── Dockerfile.sandbox    # 沙盒执行环境
│   └── docker-compose.yml    # 多容器编排
├── openhands/
│   └── setup.md              # OpenHands 安装指南
└── examples/
    └── secure_execution.py   # 安全执行示例
```

## 🚀 快速开始

### 前置要求

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Docker Compose (通常随 Docker Desktop 安装)

### 构建基础镜像

```bash
cd docker
docker build -f Dockerfile.sandbox -t agent-sandbox .
```

### 启动沙盒环境

```bash
docker-compose up -d
```

## 📚 核心概念

### 1. 沙盒 Dockerfile

```dockerfile
# Dockerfile.sandbox
FROM python:3.11-slim

# 创建非 root 用户
RUN useradd -m -s /bin/bash agent
USER agent
WORKDIR /home/agent/workspace

# 安装基础依赖
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# 限制网络访问（可选）
# 在 docker-compose.yml 中配置

CMD ["python"]
```

### 2. Docker Compose 配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  sandbox:
    build:
      context: .
      dockerfile: Dockerfile.sandbox
    volumes:
      - ./workspace:/home/agent/workspace:rw
      - ./output:/home/agent/output:rw
    # 安全配置
    security_opt:
      - no-new-privileges:true
    # 资源限制
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    # 网络隔离
    networks:
      - agent-network

networks:
  agent-network:
    driver: bridge
```

### 3. OpenHands 本地部署

OpenHands（前 OpenDevin）提供完整的 AI 编码平台：

```yaml
# openhands-compose.yml
version: '3.8'
services:
  openhands:
    image: docker.all-hands.dev/all-hands-ai/openhands:0.12
    ports:
      - "3000:3000"
    environment:
      - SANDBOX_USER_ID=1000
      - WORKSPACE_BASE=/workspace
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./my_project:/workspace
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

启动 OpenHands:

```bash
docker-compose -f openhands-compose.yml up -d
# 访问 http://localhost:3000
```

### 4. Python 中的安全执行

```python
import docker
import tempfile
import os

class SecureSandbox:
    def __init__(self):
        self.client = docker.from_env()
        
    def execute_code(self, code: str, timeout: int = 30) -> dict:
        """在隔离容器中执行代码"""
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        ) as f:
            f.write(code)
            code_path = f.name
        
        try:
            # 运行容器
            result = self.client.containers.run(
                image="agent-sandbox",
                command=f"python /code/script.py",
                volumes={
                    code_path: {'bind': '/code/script.py', 'mode': 'ro'}
                },
                remove=True,
                timeout=timeout,
                mem_limit='512m',
                network_disabled=True  # 禁用网络
            )
            return {
                "success": True,
                "output": result.decode('utf-8')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            os.unlink(code_path)
```

## 🔐 安全最佳实践

### 1. 最小权限原则

```yaml
# 以非 root 用户运行
user: "1000:1000"

# 只读根文件系统
read_only: true

# 禁止权限提升
security_opt:
  - no-new-privileges:true
```

### 2. 资源限制

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### 3. 网络隔离

```yaml
# 完全禁用网络
network_mode: "none"

# 或限制到特定网络
networks:
  - isolated-network
```

### 4. 卷挂载安全

```yaml
volumes:
  # 只读挂载代码
  - ./code:/app/code:ro
  # 限制输出目录
  - ./output:/app/output:rw
```

## 🛠️ Docker cagent

Docker 官方的 AI Agent 工具：

```yaml
# cagent.yaml
agents:
  - name: coder
    image: cagent/python-coder
    tools:
      - code_execution
      - file_system
    
  - name: reviewer
    image: cagent/code-reviewer
    tools:
      - code_analysis
```

## 📖 参考资源

- [OpenHands Documentation](https://docs.openhands.dev/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Docker cagent](https://github.com/docker/compose-ai)

## ⏭️ 下一步

完成本周学习后，继续 [Week 4: Beads 记忆系统](../04_beads/)
