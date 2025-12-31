# Critic Agent Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY src/ ./src/
COPY examples/ ./examples/

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "examples/simple_critic.py"]
