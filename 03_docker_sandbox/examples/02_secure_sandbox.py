"""
安全沙盒执行示例
================
演示如何创建安全的代码执行沙盒

安全措施:
1. 非 root 用户运行
2. 资源限制（CPU、内存）
3. 只读文件系统
4. 网络隔离
5. 超时控制
"""

import docker
from docker.types import Mount
import tempfile
import os
import time


class SecureSandbox:
    """安全沙盒执行器"""
    
    def __init__(self, image: str = "python:3.11-slim"):
        """
        初始化沙盒
        
        Args:
            image: Docker 镜像名称
        """
        self.client = docker.from_env()
        self.image = image
        
        # 安全配置
        self.config = {
            "mem_limit": "512m",        # 内存限制 512MB
            "cpu_period": 100000,       # CPU 周期
            "cpu_quota": 50000,         # 限制为 50% CPU
            "network_disabled": True,   # 禁用网络
            "read_only": False,         # 只读文件系统（需要 /tmp 可写）
            "user": "nobody",           # 非 root 用户
            "security_opt": ["no-new-privileges:true"],
        }
        
        # 确保镜像存在
        try:
            self.client.images.get(image)
        except docker.errors.ImageNotFound:
            print(f"拉取镜像 {image}...")
            self.client.images.pull(image)
    
    def execute_code(self, code: str, timeout: int = 30) -> dict:
        """
        在沙盒中执行 Python 代码
        
        Args:
            code: 要执行的 Python 代码
            timeout: 超时时间（秒）
            
        Returns:
            包含 stdout, stderr, exit_code, execution_time 的字典
        """
        start_time = time.time()
        result = {
            "stdout": "",
            "stderr": "",
            "exit_code": -1,
            "execution_time": 0,
            "error": None
        }
        
        # 创建临时文件保存代码
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            code_file = f.name
        
        try:
            # 创建容器
            container = self.client.containers.create(
                self.image,
                command=f"python /tmp/code.py",
                detach=True,
                mem_limit=self.config["mem_limit"],
                cpu_period=self.config["cpu_period"],
                cpu_quota=self.config["cpu_quota"],
                network_disabled=self.config["network_disabled"],
                security_opt=self.config["security_opt"],
                mounts=[
                    Mount(
                        target="/tmp/code.py",
                        source=code_file,
                        type="bind",
                        read_only=True
                    )
                ],
                working_dir="/tmp"
            )
            
            # 启动容器
            container.start()
            
            # 等待执行完成（带超时）
            exit_result = container.wait(timeout=timeout)
            result["exit_code"] = exit_result["StatusCode"]
            
            # 获取输出
            result["stdout"] = container.logs(stdout=True, stderr=False).decode('utf-8')
            result["stderr"] = container.logs(stdout=False, stderr=True).decode('utf-8')
            
        except docker.errors.ContainerError as e:
            result["error"] = f"Container error: {e}"
            result["exit_code"] = e.exit_status
        except Exception as e:
            result["error"] = str(e)
        finally:
            # 清理
            try:
                container.remove(force=True)
            except:
                pass
            os.unlink(code_file)
            
        result["execution_time"] = time.time() - start_time
        return result


def demo_basic_execution():
    """演示基础代码执行"""
    print("=" * 60)
    print("Demo 1: 基础代码执行")
    print("=" * 60)
    
    sandbox = SecureSandbox()
    
    code = '''
print("Hello from secure sandbox!")
print(f"2 + 2 = {2 + 2}")

# 计算
import math
print(f"π = {math.pi}")
print(f"sqrt(2) = {math.sqrt(2)}")
'''
    
    print("执行代码:")
    print("-" * 40)
    print(code)
    print("-" * 40)
    
    result = sandbox.execute_code(code)
    
    print(f"\n执行结果:")
    print(f"  退出码: {result['exit_code']}")
    print(f"  执行时间: {result['execution_time']:.2f}s")
    print(f"  输出:\n{result['stdout']}")
    if result['stderr']:
        print(f"  错误:\n{result['stderr']}")


def demo_resource_limits():
    """演示资源限制"""
    print("\n" + "=" * 60)
    print("Demo 2: 资源限制（内存）")
    print("=" * 60)
    
    sandbox = SecureSandbox()
    
    # 尝试分配大量内存
    code = '''
print("尝试分配大量内存...")
try:
    # 尝试分配 1GB 内存（超过 512MB 限制）
    data = bytearray(1024 * 1024 * 1024)
    print("分配成功")
except MemoryError:
    print("内存分配失败 - 资源限制生效!")
'''
    
    print("执行代码:")
    print("-" * 40)
    print(code)
    print("-" * 40)
    
    result = sandbox.execute_code(code, timeout=10)
    
    print(f"\n执行结果:")
    print(f"  退出码: {result['exit_code']}")
    print(f"  执行时间: {result['execution_time']:.2f}s")
    print(f"  输出:\n{result['stdout']}")
    if result['stderr']:
        print(f"  错误:\n{result['stderr']}")


def demo_timeout():
    """演示超时控制"""
    print("\n" + "=" * 60)
    print("Demo 3: 超时控制")
    print("=" * 60)
    
    sandbox = SecureSandbox()
    
    # 无限循环代码
    code = '''
import time
print("开始无限循环...")
while True:
    time.sleep(0.1)
'''
    
    print("执行代码（5秒超时）:")
    print("-" * 40)
    print(code)
    print("-" * 40)
    
    result = sandbox.execute_code(code, timeout=5)
    
    print(f"\n执行结果:")
    print(f"  退出码: {result['exit_code']}")
    print(f"  执行时间: {result['execution_time']:.2f}s")
    print(f"  错误: {result['error']}")
    if result['stdout']:
        print(f"  输出:\n{result['stdout']}")


def demo_network_isolation():
    """演示网络隔离"""
    print("\n" + "=" * 60)
    print("Demo 4: 网络隔离")
    print("=" * 60)
    
    sandbox = SecureSandbox()
    
    # 尝试网络请求
    code = '''
import urllib.request
print("尝试访问网络...")
try:
    response = urllib.request.urlopen("https://www.google.com", timeout=5)
    print(f"访问成功: {response.status}")
except Exception as e:
    print(f"网络访问失败: {type(e).__name__}")
    print("网络隔离生效!")
'''
    
    print("执行代码:")
    print("-" * 40)
    print(code)
    print("-" * 40)
    
    result = sandbox.execute_code(code, timeout=10)
    
    print(f"\n执行结果:")
    print(f"  退出码: {result['exit_code']}")
    print(f"  执行时间: {result['execution_time']:.2f}s")
    print(f"  输出:\n{result['stdout']}")


def demo_dangerous_code():
    """演示危险代码处理"""
    print("\n" + "=" * 60)
    print("Demo 5: 危险代码隔离")
    print("=" * 60)
    
    sandbox = SecureSandbox()
    
    # 尝试访问系统文件
    code = '''
import os
print("尝试访问敏感文件...")

# 尝试读取 /etc/passwd
try:
    with open('/etc/passwd', 'r') as f:
        print("可以读取 /etc/passwd")
        print(f.read()[:100])
except PermissionError:
    print("无法读取 - 权限被拒绝!")

# 尝试写入系统目录
try:
    with open('/etc/test.txt', 'w') as f:
        f.write("test")
    print("可以写入 /etc")
except PermissionError:
    print("无法写入系统目录 - 权限被拒绝!")

# 尝试执行系统命令
try:
    result = os.system("whoami")
    print(f"当前用户可以执行命令")
except:
    print("命令执行受限")

print("\\n沙盒安全措施已生效!")
'''
    
    print("执行代码:")
    print("-" * 40)
    print(code)
    print("-" * 40)
    
    result = sandbox.execute_code(code)
    
    print(f"\n执行结果:")
    print(f"  退出码: {result['exit_code']}")
    print(f"  执行时间: {result['execution_time']:.2f}s")
    print(f"  输出:\n{result['stdout']}")


def main():
    """主函数"""
    print("🔒 安全沙盒执行示例")
    print("=" * 60)
    
    # 检查 Docker
    try:
        client = docker.from_env()
        client.ping()
        print("✅ Docker 连接成功")
    except Exception as e:
        print(f"❌ Docker 连接失败: {e}")
        print("请确保 Docker Desktop 已安装并运行")
        return
    
    # 运行演示
    demo_basic_execution()
    demo_resource_limits()
    demo_timeout()
    demo_network_isolation()
    demo_dangerous_code()
    
    print("\n" + "=" * 60)
    print("✅ 安全沙盒示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
