@echo off
chcp 65001 >nul
echo ==================================================
echo 投资学 Agent - 智能投资组合优化系统
echo ==================================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.9+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/2] 检查依赖...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo [完成] 依赖检查通过

echo.
echo [2/2] 启动投资学 Agent...
echo.
python src/investment_agent.py

echo.
echo ==================================================
echo 程序运行完成
echo ==================================================
pause
