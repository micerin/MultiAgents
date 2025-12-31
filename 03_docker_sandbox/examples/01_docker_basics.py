"""
Docker 基础操作示例
====================
演示如何使用 Python Docker SDK 进行容器管理

学习要点:
1. 连接 Docker 守护进程
2. 镜像管理（拉取、列出、删除）
3. 容器管理（创建、运行、停止）
4. 在容器中执行命令
"""

import docker
from docker.errors import DockerException, ImageNotFound, ContainerError
import sys


def check_docker_connection():
    """检查 Docker 是否可用"""
    print("=" * 60)
    print("检查 Docker 连接")
    print("=" * 60)
    
    try:
        client = docker.from_env()
        info = client.info()
        print(f"✅ Docker 连接成功!")
        print(f"   Docker 版本: {client.version()['Version']}")
        print(f"   操作系统: {info['OSType']}")
        print(f"   容器数量: {info['Containers']}")
        print(f"   镜像数量: {info['Images']}")
        return client
    except DockerException as e:
        print(f"❌ Docker 连接失败: {e}")
        print("\n请确保:")
        print("1. Docker Desktop 已安装并运行")
        print("2. 当前用户有权限访问 Docker")
        return None


def list_images(client):
    """列出本地 Docker 镜像"""
    print("\n" + "=" * 60)
    print("本地 Docker 镜像")
    print("=" * 60)
    
    images = client.images.list()
    if not images:
        print("没有找到本地镜像")
        return
    
    for img in images[:10]:  # 只显示前10个
        tags = img.tags if img.tags else ["<none>"]
        size_mb = img.attrs['Size'] / (1024 * 1024)
        print(f"  📦 {tags[0]:<40} {size_mb:.1f} MB")
    
    if len(images) > 10:
        print(f"  ... 还有 {len(images) - 10} 个镜像")


def run_simple_container(client):
    """运行一个简单的容器"""
    print("\n" + "=" * 60)
    print("运行简单容器")
    print("=" * 60)
    
    try:
        # 拉取 alpine 镜像（非常小）
        print("拉取 alpine:latest 镜像...")
        client.images.pull("alpine", tag="latest")
        print("✅ 镜像拉取成功")
        
        # 运行容器执行命令
        print("\n在容器中执行 'echo Hello from Docker!'...")
        result = client.containers.run(
            "alpine:latest",
            "echo Hello from Docker!",
            remove=True  # 自动删除容器
        )
        print(f"输出: {result.decode('utf-8').strip()}")
        
        # 运行更复杂的命令
        print("\n在容器中获取系统信息...")
        result = client.containers.run(
            "alpine:latest",
            "cat /etc/os-release",
            remove=True
        )
        print("系统信息:")
        for line in result.decode('utf-8').strip().split('\n')[:5]:
            print(f"  {line}")
            
        print("✅ 容器运行成功")
        
    except ImageNotFound:
        print("❌ 镜像未找到")
    except ContainerError as e:
        print(f"❌ 容器运行错误: {e}")


def run_python_in_container(client):
    """在容器中运行 Python 代码"""
    print("\n" + "=" * 60)
    print("在 Docker 容器中运行 Python")
    print("=" * 60)
    
    try:
        # 使用 python:3.11-slim 镜像
        print("拉取 python:3.11-slim 镜像（可能需要一些时间）...")
        client.images.pull("python", tag="3.11-slim")
        print("✅ 镜像拉取成功")
        
        # 在容器中运行 Python 代码（使用 base64 编码避免引号问题）
        python_code = '''
import sys
import platform

print(f"Python 版本: {sys.version}")
print(f"平台: {platform.platform()}")
print(f"2 + 2 = {2 + 2}")

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(f"fib(10) = {fib(10)}")
'''
        
        # 使用 base64 编码避免 shell 引号问题
        import base64
        encoded_code = base64.b64encode(python_code.encode()).decode()
        
        print("\n执行 Python 代码...")
        result = client.containers.run(
            "python:3.11-slim",
            f'python -c "import base64; exec(base64.b64decode(\'{encoded_code}\').decode())"',
            remove=True
        )
        print("输出:")
        for line in result.decode('utf-8').strip().split('\n'):
            print(f"  {line}")
            
        print("✅ Python 代码执行成功")
        
    except Exception as e:
        print(f"❌ 错误: {e}")


def list_containers(client):
    """列出运行中的容器"""
    print("\n" + "=" * 60)
    print("运行中的容器")
    print("=" * 60)
    
    containers = client.containers.list()
    if not containers:
        print("没有运行中的容器")
        return
    
    for container in containers:
        print(f"  🐳 {container.short_id} | {container.name} | {container.status}")


def main():
    """主函数"""
    print("🐳 Docker 基础操作示例")
    print("=" * 60)
    
    # 检查 Docker 连接
    client = check_docker_connection()
    if not client:
        sys.exit(1)
    
    # 列出镜像
    list_images(client)
    
    # 列出容器
    list_containers(client)
    
    # 运行简单容器
    run_simple_container(client)
    
    # 在容器中运行 Python
    run_python_in_container(client)
    
    print("\n" + "=" * 60)
    print("✅ Docker 基础操作示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
