@echo off
REM Project3 虚拟环境启动脚本 (批处理版本)
REM 使用方法: start_project3.bat

echo =====================================
echo   Learning Activity System - Project3
echo =====================================
echo.

REM 检查虚拟环境是否存在
if not exist ".\Project3\" (
    echo [ERROR] 虚拟环境 Project3 不存在!
    echo 请先运行: python -m venv Project3
    pause
    exit /b 1
)

echo [OK] 虚拟环境 Project3 已找到

REM 检查依赖是否已安装
.\Project3\Scripts\python.exe -m pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [INFO] 正在安装依赖包...
    .\Project3\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] 依赖安装失败!
        pause
        exit /b 1
    )
    echo [OK] 依赖安装完成
) else (
    echo [OK] 依赖包已安装
)

REM 检查 .env 文件
if not exist ".\.env" (
    echo [WARNING] .env 文件不存在
    echo [ERROR] 请先配置 .env 文件中的 API 密钥!
    pause
    exit /b 1
)

echo [OK] .env 文件已配置
echo.

REM 提示信息
echo =====================================
echo 提示: 如果是首次运行，请先执行:
echo   .\Project3\Scripts\python.exe init_db.py
echo.
echo 正在启动应用...
echo   虚拟环境: Project3
echo   访问地址: http://localhost:5000
echo   管理员账号: admin / admin123
echo.
echo 按 Ctrl+C 停止服务器
echo =====================================
echo.

REM 启动 Flask 应用
.\Project3\Scripts\python.exe app.py

pause
