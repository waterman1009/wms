#!/bin/bash
# 仓库管理系统 - 状态查看脚本

echo "================================"
echo "  仓库管理系统 - 运行状态"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查后端服务 (端口 8080)
echo "后端服务 (Flask - 端口 8080):"
BACKEND_PID=$(lsof -ti:8080 2>/dev/null)

if [ -z "$BACKEND_PID" ]; then
    echo -e "${RED}  ✗ 未运行${NC}"
else
    echo -e "${GREEN}  ✓ 运行中${NC}"
    echo "  PID: $BACKEND_PID"
    
    # 检查是否有PID文件
    if [ -f "logs/backend.pid" ]; then
        SAVED_PID=$(cat logs/backend.pid)
        if [ "$BACKEND_PID" == "$SAVED_PID" ]; then
            echo "  模式: 开发模式"
        fi
    elif [ -f "logs/app.pid" ]; then
        SAVED_PID=$(cat logs/app.pid)
        if [ "$BACKEND_PID" == "$SAVED_PID" ]; then
            echo "  模式: 生产模式"
        fi
    fi
    
    # 显示进程信息
    ps -p $BACKEND_PID -o pid,ppid,%cpu,%mem,etime,comm 2>/dev/null | tail -n 1
fi

echo ""

# 检查前端服务 (端口 3000)
echo "前端服务 (Vue/Vite - 端口 3000):"
FRONTEND_PID=$(lsof -ti:3000 2>/dev/null)

if [ -z "$FRONTEND_PID" ]; then
    echo -e "${YELLOW}  ✗ 未运行 (开发模式)${NC}"
else
    echo -e "${GREEN}  ✓ 运行中 (开发模式)${NC}"
    echo "  PID: $FRONTEND_PID"
    
    # 显示进程信息
    ps -p $FRONTEND_PID -o pid,ppid,%cpu,%mem,etime,comm 2>/dev/null | tail -n 1
fi

echo ""
echo "================================"
echo "  访问地址"
echo "================================"

if [ ! -z "$FRONTEND_PID" ]; then
    echo -e "${GREEN}开发模式:${NC}"
    echo "  前端: http://localhost:3000"
    echo "  后端: http://localhost:8080"
elif [ ! -z "$BACKEND_PID" ]; then
    echo -e "${GREEN}生产模式:${NC}"
    echo "  访问: http://localhost:8080"
else
    echo -e "${RED}服务未运行${NC}"
fi

echo ""
echo "================================"
echo "  最近日志"
echo "================================"

# 显示最新的日志文件
if [ -d "logs" ]; then
    LATEST_LOG=$(ls -t logs/app_*.log logs/backend_*.log 2>/dev/null | head -n 1)
    if [ ! -z "$LATEST_LOG" ]; then
        echo "最新日志: $LATEST_LOG"
        echo ""
        echo "最后10行:"
        tail -n 10 "$LATEST_LOG"
    else
        echo "没有找到日志文件"
    fi
else
    echo "日志目录不存在"
fi

echo ""
