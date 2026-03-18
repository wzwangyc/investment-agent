#!/bin/bash

echo "=================================================="
echo "投资学 Agent - 智能投资组合优化系统"
echo "=================================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.9+"
    echo "下载地址：https://www.python.org/downloads/"
    exit 1
fi

echo "[1/2] 检查依赖..."
pip3 install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "[错误] 依赖安装失败"
    exit 1
fi
echo "[完成] 依赖检查通过"

echo ""
echo "[2/2] 启动投资学 Agent..."
echo ""
python3 src/investment_agent.py

echo ""
echo "=================================================="
echo "程序运行完成"
echo "=================================================="
