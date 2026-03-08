#!/bin/bash
# 仓库管理系统 - 启动脚本 (macOS/Linux)

echo "================================"
echo "  仓库管理系统 - 启动中..."
echo "================================"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 错误: 虚拟环境不存在"
    echo "请先运行 ./install.sh 进行安装"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查依赖
echo "检查依赖..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 错误: 依赖未安装"
    echo "请先运行 ./install.sh 进行安装"
    exit 1
fi

echo "✓ 环境检查通过"
echo ""

# 创建logs目录
if [ ! -d "logs" ]; then
    mkdir -p logs
    echo "✓ 创建日志目录: logs/"
fi

# 检查是否已经在运行
PID=$(lsof -ti:8080 2>/dev/null)
if [ ! -z "$PID" ]; then
    echo "⚠️  警告: 端口8080已被占用 (PID: $PID)"
    echo "如果是本系统进程，请先运行 ./stop.sh 停止服务"
    exit 1
fi

# 生成日志文件名（带时间戳）
LOG_FILE="logs/app_$(date +%Y%m%d_%H%M%S).log"

# 后台启动应用
echo "启动服务器（后台运行）..."
nohup python3 app.py > "$LOG_FILE" 2>&1 &
APP_PID=$!

# 等待服务启动
sleep 2

# 检查进程是否还在运行
if ps -p $APP_PID > /dev/null 2>&1; then
    echo "✓ 服务启动成功！"
    echo ""
    echo "================================"
    echo "  服务信息"
    echo "================================"
    echo "进程ID: $APP_PID"
    echo "访问地址: http://localhost:8080"
    echo "局域网访问: http://$(ipconfig getifaddr en0 2>/dev/null || hostname -I | awk '{print $1}'):8080"
    echo "日志文件: $LOG_FILE"
    echo ""
    echo "查看日志: tail -f $LOG_FILE"
    echo "停止服务: ./stop.sh"
    echo "================================"
    echo ""
    
    # 保存PID到文件
    echo $APP_PID > logs/app.pid
else
    echo "❌ 服务启动失败"
    echo "请查看日志: cat $LOG_FILE"
    exit 1
fi
