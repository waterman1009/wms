#!/bin/bash
# 仓库管理系统 - 安装脚本

echo "================================"
echo "  仓库管理系统 - 安装向导"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Python版本
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到Python3${NC}"
    echo "请先安装Python 3.8或更高版本"
    echo "访问: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ 找到Python版本: $PYTHON_VERSION${NC}"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到pip3${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pip3 已安装${NC}"

# 检查Node.js和npm
echo ""
echo "检查Node.js环境..."
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  警告: 未找到Node.js${NC}"
    echo "前端开发需要Node.js 16+，请访问: https://nodejs.org/"
    echo "如果只使用生产模式，可以跳过此步骤"
    read -p "是否继续安装后端? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    SKIP_FRONTEND=true
else
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ 找到Node.js版本: $NODE_VERSION${NC}"
    
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ 错误: 未找到npm${NC}"
        exit 1
    fi
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ npm版本: $NPM_VERSION${NC}"
    SKIP_FRONTEND=false
fi

# 创建虚拟环境
echo ""
echo "创建Python虚拟环境..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}虚拟环境已存在，跳过创建${NC}"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
    else
        echo -e "${RED}❌ 虚拟环境创建失败${NC}"
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

# 安装后端依赖
echo ""
echo "安装后端依赖..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 后端依赖安装成功${NC}"
else
    echo -e "${RED}❌ 后端依赖安装失败${NC}"
    exit 1
fi

# 安装前端依赖
if [ "$SKIP_FRONTEND" = false ]; then
    echo ""
    echo "安装前端依赖..."
    cd frontend
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 前端依赖安装成功${NC}"
    else
        echo -e "${RED}❌ 前端依赖安装失败${NC}"
        cd ..
        exit 1
    fi
    cd ..
fi

# 创建必要的目录
echo ""
echo "创建必要的目录..."
mkdir -p logs
mkdir -p static
echo -e "${GREEN}✓ 目录创建完成${NC}"

# 检查数据库
echo ""
if [ -f "warehouse.db" ]; then
    echo -e "${GREEN}✓ 数据库文件已存在${NC}"
else
    echo -e "${YELLOW}首次运行，将自动创建数据库${NC}"
fi

echo ""
echo "================================"
echo "  ✅ 安装完成！"
echo "================================"
echo ""
echo -e "${GREEN}下一步：${NC}"
echo ""
echo "开发模式（前后端分离，支持热更新）："
echo "  ./start.sh dev"
echo "  访问: http://localhost:3000"
echo ""
echo "生产模式（构建前端，单一服务）："
echo "  ./start.sh prod"
echo "  访问: http://localhost:8080"
echo ""
echo "查看状态："
echo "  ./status.sh"
echo ""
echo "停止服务："
echo "  ./stop.sh"
echo ""
echo -e "${YELLOW}默认登录账号:${NC}"
echo "  用户名: admin"
echo "  密码: admin123"
echo ""
echo -e "${RED}提示: 首次登录后请立即修改密码${NC}"
echo ""
