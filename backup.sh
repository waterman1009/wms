#!/bin/bash
# 仓库管理系统 - 数据备份脚本 (macOS/Linux)

echo "================================"
echo "  数据备份工具"
echo "================================"
echo ""

# 创建备份目录
BACKUP_DIR="backup"
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    echo "✓ 创建备份目录: $BACKUP_DIR"
fi

# 生成时间戳
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# 备份数据库
if [ -f "warehouse.db" ]; then
    cp warehouse.db "$BACKUP_DIR/warehouse_$TIMESTAMP.db"
    echo "✓ 数据库备份: warehouse_$TIMESTAMP.db"
else
    echo "⚠ 数据库文件不存在，跳过"
fi

# 备份Excel文件
if [ -f "20-12月半成品发料.xlsx" ]; then
    cp "20-12月半成品发料.xlsx" "$BACKUP_DIR/20-12月半成品发料_$TIMESTAMP.xlsx"
    echo "✓ Excel备份: 20-12月半成品发料_$TIMESTAMP.xlsx"
fi

# 清理30天前的备份
echo ""
echo "清理旧备份..."
find "$BACKUP_DIR" -name "*.db" -mtime +30 -delete 2>/dev/null
find "$BACKUP_DIR" -name "*.xlsx" -mtime +30 -delete 2>/dev/null
echo "✓ 已清理30天前的备份"

echo ""
echo "================================"
echo "  备份完成！"
echo "================================"
echo "备份位置: $BACKUP_DIR/"
echo ""
