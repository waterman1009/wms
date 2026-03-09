#!/bin/bash
# 仓库管理系统 - 日志查看脚本 (macOS/Linux)

if [ ! -d "logs" ]; then
    echo "❌ 日志目录不存在"
    exit 1
fi

# 获取最新的日志文件
LATEST_LOG=$(ls -t logs/app_*.log 2>/dev/null | head -1)

if [ -z "$LATEST_LOG" ]; then
    echo "❌ 没有找到日志文件"
    exit 1
fi

echo "================================"
echo "  查看日志: $LATEST_LOG"
echo "================================"
echo "按 Ctrl+C 退出"
echo ""

# 实时查看日志
tail -f "$LATEST_LOG"
