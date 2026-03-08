#!/bin/bash
# 仓库管理系统 - 状态检查脚本 (macOS/Linux)

echo "================================"
echo "  仓库管理系统 - 状态检查"
echo "================================"
echo ""

# 检查端口
PID=$(lsof -ti:8080 2>/dev/null)

if [ -z "$PID" ]; then
    echo "状态: ❌ 未运行"
    echo ""
    echo "启动服务: ./start.sh"
else
    echo "状态: ✅ 运行中"
    echo "进程ID: $PID"
    echo "端口: 8080"
    echo ""
    
    # 检查PID文件
    if [ -f "logs/app.pid" ]; then
        SAVED_PID=$(cat logs/app.pid)
        if [ "$PID" = "$SAVED_PID" ]; then
            echo "PID文件: ✓ 一致"
        else
            echo "PID文件: ⚠️  不一致 (文件中: $SAVED_PID)"
        fi
    else
        echo "PID文件: ⚠️  不存在"
    fi
    
    echo ""
    echo "访问地址: http://localhost:8080"
    echo "局域网访问: http://$(ipconfig getifaddr en0 2>/dev/null || hostname -I | awk '{print $1}'):8080"
    echo ""
    
    # 检查最新日志
    if [ -d "logs" ]; then
        LATEST_LOG=$(ls -t logs/app_*.log 2>/dev/null | head -1)
        if [ ! -z "$LATEST_LOG" ]; then
            echo "最新日志: $LATEST_LOG"
            LOG_SIZE=$(du -h "$LATEST_LOG" | awk '{print $1}')
            echo "日志大小: $LOG_SIZE"
        fi
    fi
    
    echo ""
    echo "查看日志: ./logs.sh"
    echo "停止服务: ./stop.sh"
fi

echo "================================"
