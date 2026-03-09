#!/bin/bash
# 仓库管理系统 - 统一停止脚本

echo "================================"
echo "  停止仓库管理系统"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

STOPPED=0

# 停止后端（开发模式）
echo "检查后端服务（开发模式）..."
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID
        echo -e "${GREEN}✓ 后端服务已停止 (PID: $BACKEND_PID)${NC}"
        STOPPED=1
    else
        echo -e "${YELLOW}⚠️  PID文件中的后端进程不存在${NC}"
    fi
    rm -f logs/backend.pid
else
    BACKEND_PID=$(lsof -ti:8080 2>/dev/null)
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID
        echo -e "${GREEN}✓ 后端服务已停止 (PID: $BACKEND_PID)${NC}"
        STOPPED=1
    else
        echo "后端服务未运行（开发模式）"
    fi
fi

echo ""

# 停止前端（开发模式）
echo "检查前端服务（开发模式）..."
if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID
        echo -e "${GREEN}✓ 前端服务已停止 (PID: $FRONTEND_PID)${NC}"
        STOPPED=1
    else
        echo -e "${YELLOW}⚠️  PID文件中的前端进程不存在${NC}"
    fi
    rm -f logs/frontend.pid
else
    FRONTEND_PID=$(lsof -ti:3000 2>/dev/null)
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID
        echo -e "${GREEN}✓ 前端服务已停止 (PID: $FRONTEND_PID)${NC}"
        STOPPED=1
    else
        echo "前端服务未运行（开发模式）"
    fi
fi

echo ""

# 停止生产模式服务
echo "检查服务（生产模式）..."
if [ -f "logs/app.pid" ]; then
    APP_PID=$(cat logs/app.pid)
    if ps -p $APP_PID > /dev/null 2>&1; then
        kill $APP_PID
        echo -e "${GREEN}✓ 服务已停止 (PID: $APP_PID)${NC}"
        STOPPED=1
    else
        echo -e "${YELLOW}⚠️  PID文件中的进程不存在${NC}"
    fi
    rm -f logs/app.pid
else
    # 如果没有PID文件，再次检查8080端口（可能是生产模式）
    APP_PID=$(lsof -ti:8080 2>/dev/null)
    if [ ! -z "$APP_PID" ]; then
        kill $APP_PID
        echo -e "${GREEN}✓ 服务已停止 (PID: $APP_PID)${NC}"
        STOPPED=1
    else
        echo "服务未运行（生产模式）"
    fi
fi

echo ""

if [ $STOPPED -eq 0 ]; then
    echo "没有找到运行中的服务"
else
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}  ✅ 所有服务已停止${NC}"
    echo -e "${GREEN}================================${NC}"
fi

echo ""
