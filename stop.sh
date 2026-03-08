#!/bin/bash
# 仓库管理系统 - 停止脚本 (macOS/Linux)

echo "正在停止仓库管理系统..."

# 方法1: 从PID文件读取
if [ -f "logs/app.pid" ]; then
    PID=$(cat logs/app.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✓ 服务已停止 (PID: $PID)"
        rm -f logs/app.pid
        exit 0
    else
        echo "⚠️  PID文件中的进程不存在，尝试通过端口查找..."
        rm -f logs/app.pid
    fi
fi

# 方法2: 通过端口查找
PID=$(lsof -ti:8080 2>/dev/null)

if [ -z "$PID" ]; then
    echo "没有找到运行中的服务"
else
    kill $PID
    echo "✓ 服务已停止 (PID: $PID)"
    rm -f logs/app.pid
fi
