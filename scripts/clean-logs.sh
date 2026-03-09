#!/bin/bash
# 清理旧日志文件

echo "================================"
echo "  清理旧日志文件"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 默认保留最近7天的日志
DAYS=${1:-7}

echo "保留最近 $DAYS 天的日志文件..."
echo ""

if [ ! -d "logs" ]; then
    echo -e "${YELLOW}logs 目录不存在${NC}"
    exit 0
fi

cd logs

# 统计当前日志文件数量
TOTAL_FILES=$(ls -1 *.log 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh . 2>/dev/null | awk '{print $1}')

echo "当前状态:"
echo "  日志文件数: $TOTAL_FILES"
echo "  总大小: $TOTAL_SIZE"
echo ""

# 查找并删除旧日志
echo "查找 $DAYS 天前的日志文件..."
OLD_FILES=$(find . -name "*.log" -type f -mtime +$DAYS 2>/dev/null)

if [ -z "$OLD_FILES" ]; then
    echo -e "${GREEN}没有需要清理的旧日志${NC}"
else
    echo "将删除以下文件:"
    echo "$OLD_FILES"
    echo ""
    
    read -p "确认删除? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        find . -name "*.log" -type f -mtime +$DAYS -delete
        
        # 统计清理后的状态
        NEW_FILES=$(ls -1 *.log 2>/dev/null | wc -l)
        NEW_SIZE=$(du -sh . 2>/dev/null | awk '{print $1}')
        DELETED=$((TOTAL_FILES - NEW_FILES))
        
        echo ""
        echo -e "${GREEN}清理完成！${NC}"
        echo "  删除文件数: $DELETED"
        echo "  剩余文件数: $NEW_FILES"
        echo "  当前大小: $NEW_SIZE"
    else
        echo "取消清理"
    fi
fi

cd ..
echo ""
