#!/bin/bash
# 打包脚本 - 创建部署压缩包

echo "================================"
echo "  创建部署包"
echo "================================"
echo ""

# 设置打包文件名（使用英文避免乱码）
PACKAGE_NAME="warehouse-system-macos-$(date +%Y%m%d).zip"

# 需要打包的文件和目录
FILES=(
    "app.py"
    "database.py"
    "models.py"
    "main.py"
    "requirements.txt"
    "README.md"
    "DEPLOY.md"
    "快速开始.txt"
    "使用说明.txt"
    "成品发货功能说明.md"
    "交易取消功能说明.md"
    "时间筛选功能说明.md"
    "部署检查清单.md"
    "install.sh"
    "start.sh"
    "stop.sh"
    "status.sh"
    "logs.sh"
    "backup.sh"
    "templates"
    "20-12月半成品发料.xlsx"
)

# 可选文件（如果存在则打包）
OPTIONAL_FILES=(
    "warehouse.db"
)

echo "准备打包以下文件："
for file in "${FILES[@]}"; do
    if [ -e "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (不存在)"
    fi
done

echo ""
echo "可选文件："
for file in "${OPTIONAL_FILES[@]}"; do
    if [ -e "$file" ]; then
        echo "  ✓ $file (将包含)"
        FILES+=("$file")
    else
        echo "  - $file (不存在，跳过)"
    fi
done

echo ""
echo "创建压缩包..."

# 创建临时目录（使用英文避免乱码）
TEMP_DIR="warehouse-system"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# 复制文件
for file in "${FILES[@]}"; do
    if [ -e "$file" ]; then
        if [ -d "$file" ]; then
            # 复制目录，保持结构
            cp -r "$file" "$TEMP_DIR/"
        else
            cp "$file" "$TEMP_DIR/"
        fi
    fi
done

# 确保脚本有执行权限
chmod +x "$TEMP_DIR"/*.sh

# 创建压缩包
zip -r "$PACKAGE_NAME" "$TEMP_DIR" > /dev/null 2>&1

# 清理临时目录
rm -rf "$TEMP_DIR"

if [ -f "$PACKAGE_NAME" ]; then
    SIZE=$(du -h "$PACKAGE_NAME" | awk '{print $1}')
    echo "✓ 打包完成！"
    echo ""
    echo "================================"
    echo "  部署包信息"
    echo "================================"
    echo "文件名: $PACKAGE_NAME"
    echo "大小: $SIZE"
    echo "位置: $(pwd)/$PACKAGE_NAME"
    echo ""
    echo "下一步："
    echo "1. 将 $PACKAGE_NAME 复制到目标Mac"
    echo "2. 解压文件"
    echo "3. 运行 ./install.sh"
    echo "4. 运行 ./start.sh"
    echo ""
else
    echo "❌ 打包失败"
    exit 1
fi
