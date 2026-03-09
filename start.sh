#!/bin/bash
# 仓库管理系统 - 统一启动脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示使用说明
show_usage() {
    echo "================================"
    echo "  仓库管理系统 - 启动脚本"
    echo "================================"
    echo ""
    echo "用法: ./start.sh [模式]"
    echo ""
    echo "模式:"
    echo "  dev   - 开发模式（前后端分离，支持热更新）"
    echo "  prod  - 生产模式（构建前端，单一服务）"
    echo ""
    echo "示例:"
    echo "  ./start.sh dev    # 启动开发环境"
    echo "  ./start.sh prod   # 启动生产环境"
    echo ""
    exit 1
}

# 检查端口占用
check_port() {
    local port=$1
    local name=$2
    PID=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo -e "${YELLOW}⚠️  警告: 端口 $port 已被占用 (PID: $PID)${NC}"
        echo "这可能是 $name 的旧进程"
        read -p "是否终止该进程并继续? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill $PID 2>/dev/null
            sleep 1
        else
            return 1
        fi
    fi
    return 0
}

# 开发模式
start_dev() {
    echo "================================"
    echo "  🚀 启动开发模式"
    echo "================================"
    echo ""

    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo -e "${RED}❌ 错误: 虚拟环境不存在${NC}"
        echo "请先运行: ./install.sh"
        exit 1
    fi

    # 检查前端依赖
    if [ ! -d "frontend/node_modules" ]; then
        echo -e "${YELLOW}⚠️  前端依赖未安装，正在安装...${NC}"
        cd frontend && npm install && cd ..
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ 前端依赖安装失败${NC}"
            exit 1
        fi
    fi

    # 创建logs目录
    mkdir -p logs

    # 检查端口
    check_port 8080 "后端服务"
    if [ $? -ne 0 ]; then
        echo -e "${RED}请先停止占用端口的进程，或运行: ./stop.sh${NC}"
        exit 1
    fi

    check_port 3000 "前端服务"
    if [ $? -ne 0 ]; then
        echo -e "${RED}请先停止占用端口的进程，或运行: ./stop.sh${NC}"
        exit 1
    fi

    # 激活虚拟环境
    source venv/bin/activate

    # 检查flask-cors
    python3 -c "import flask_cors" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  flask-cors 未安装，正在安装...${NC}"
        pip3 install flask-cors > /dev/null 2>&1
    fi

    # 启动后端
    echo "启动后端服务器..."
    BACKEND_LOG="logs/backend_$(date +%Y%m%d_%H%M%S).log"
    nohup python3 app.py > "$BACKEND_LOG" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > logs/backend.pid

    sleep 3

    if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo -e "${RED}❌ 后端启动失败${NC}"
        echo "请查看日志: cat $BACKEND_LOG"
        exit 1
    fi

    echo -e "${GREEN}✓ 后端服务启动成功 (PID: $BACKEND_PID)${NC}"
    echo ""

    # 启动前端
    echo "启动前端开发服务器..."
    FRONTEND_LOG="logs/frontend_$(date +%Y%m%d_%H%M%S).log"
    cd frontend
    nohup npm run dev > "../$FRONTEND_LOG" 2>&1 &
    FRONTEND_PID=$!
    cd ..
    echo $FRONTEND_PID > logs/frontend.pid

    sleep 5

    if ! ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo -e "${RED}❌ 前端启动失败${NC}"
        echo "请查看日志: cat $FRONTEND_LOG"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi

    echo -e "${GREEN}✓ 前端服务启动成功 (PID: $FRONTEND_PID)${NC}"
    echo ""

    # 显示信息
    echo "================================"
    echo "  ✅ 开发环境启动成功！"
    echo "================================"
    echo ""
    echo -e "${GREEN}后端服务 (Flask):${NC}"
    echo "  地址: http://localhost:8080"
    echo "  PID: $BACKEND_PID"
    echo "  日志: $BACKEND_LOG"
    echo ""
    echo -e "${GREEN}前端服务 (Vue + Vite):${NC}"
    echo "  地址: http://localhost:3000"
    echo "  PID: $FRONTEND_PID"
    echo "  日志: $FRONTEND_LOG"
    echo ""
    echo -e "${BLUE}👉 请访问: http://localhost:3000${NC}"
    echo ""
    echo "================================"
    echo "  常用命令"
    echo "================================"
    echo "查看状态: ./status.sh"
    echo "停止服务: ./stop.sh"
    echo "查看日志: tail -f $BACKEND_LOG"
    echo "================================"
    echo ""
}

# 生产模式
start_prod() {
    echo "================================"
    echo "  🚀 启动生产模式"
    echo "================================"
    echo ""

    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo -e "${RED}❌ 错误: 虚拟环境不存在${NC}"
        echo "请先运行: ./install.sh"
        exit 1
    fi

    # 检查前端依赖
    if [ ! -d "frontend/node_modules" ]; then
        echo -e "${YELLOW}⚠️  前端依赖未安装，正在安装...${NC}"
        cd frontend && npm install && cd ..
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ 前端依赖安装失败${NC}"
            exit 1
        fi
    fi

    # 检查是否已有构建文件
    if [ ! -f "static/index.html" ]; then
        echo -e "${YELLOW}⚠️  未找到构建文件，开始构建前端...${NC}"
        # 构建前端
        echo "构建前端资源..."
        cd frontend
        npm run build
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ 前端构建失败${NC}"
            cd ..
            exit 1
        fi
        cd ..
        echo -e "${GREEN}✓ 前端构建完成${NC}"
    else
        echo -e "${GREEN}✓ 找到已构建的前端文件${NC}"
        read -p "是否重新构建前端? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "构建前端资源..."
            cd frontend
            npm run build
            if [ $? -ne 0 ]; then
                echo -e "${RED}❌ 前端构建失败${NC}"
                cd ..
                exit 1
            fi
            cd ..
            echo -e "${GREEN}✓ 前端构建完成${NC}"
        fi
    fi
    echo ""

    # 创建logs目录
    mkdir -p logs

    # 检查端口
    check_port 8080 "后端服务"
    if [ $? -ne 0 ]; then
        echo -e "${RED}请先停止占用端口的进程，或运行: ./stop.sh${NC}"
        exit 1
    fi

    # 激活虚拟环境
    source venv/bin/activate

    # 检查flask-cors
    python3 -c "import flask_cors" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  flask-cors 未安装，正在安装...${NC}"
        pip3 install flask-cors > /dev/null 2>&1
    fi

    # 启动服务
    echo "启动服务器（生产模式）..."
    LOG_FILE="logs/app_$(date +%Y%m%d_%H%M%S).log"
    nohup python3 app.py > "$LOG_FILE" 2>&1 &
    APP_PID=$!

    sleep 3

    if ps -p $APP_PID > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 服务启动成功！${NC}"
        echo ""
        echo "================================"
        echo "  ✅ 生产环境启动成功！"
        echo "================================"
        echo "进程ID: $APP_PID"
        echo "访问地址: http://localhost:8080"
        echo "日志文件: $LOG_FILE"
        echo ""
        echo "================================"
        echo "  常用命令"
        echo "================================"
        echo "查看状态: ./status.sh"
        echo "停止服务: ./stop.sh"
        echo "查看日志: tail -f $LOG_FILE"
        echo "================================"
        echo ""
        
        echo $APP_PID > logs/app.pid
    else
        echo -e "${RED}❌ 服务启动失败${NC}"
        echo "请查看日志: cat $LOG_FILE"
        exit 1
    fi
}

# 主逻辑
MODE=${1:-}

if [ -z "$MODE" ]; then
    show_usage
fi

case "$MODE" in
    dev)
        start_dev
        ;;
    prod)
        start_prod
        ;;
    *)
        echo -e "${RED}❌ 错误: 未知模式 '$MODE'${NC}"
        echo ""
        show_usage
        ;;
esac
