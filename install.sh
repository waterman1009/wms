#!/bin/bash
# 仓库管理系统 - 安装脚本 (macOS/Linux)

echo "================================"
echo "  仓库管理系统 - 安装向导"
echo "================================"
echo ""

# 检查Python版本
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3"
    echo "请先安装Python 3.8或更高版本"
    echo "访问: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ 找到Python版本: $PYTHON_VERSION"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到pip3"
    exit 1
fi
echo "✓ pip3 已安装"

# 创建虚拟环境
echo ""
echo "创建虚拟环境..."
if [ -d "venv" ]; then
    echo "虚拟环境已存在，跳过创建"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✓ 虚拟环境创建成功"
    else
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
fi

# 激活虚拟环境
echo ""
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo ""
echo "升级pip..."
pip install --upgrade pip -q

# 安装依赖
echo ""
echo "安装项目依赖..."
pip install -r requirements.txt -q

if [ $? -eq 0 ]; then
    echo "✓ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 检查数据库
echo ""
if [ -f "warehouse.db" ]; then
    echo "✓ 数据库文件已存在"
else
    echo "首次运行，将自动创建数据库"
fi

echo ""
echo "================================"
echo "  安装完成！"
echo "================================"
echo ""
echo "下一步："
echo "1. 运行 ./start.sh 启动服务器"
echo "2. 在浏览器访问 http://localhost:8888"
echo "3. 使用 admin / admin123 登录"
echo ""
echo "提示: 首次登录后请立即修改密码"
echo ""
