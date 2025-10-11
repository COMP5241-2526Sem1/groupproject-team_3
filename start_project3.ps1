# Project3 虚拟环境启动脚本
# 使用方法: .\start_project3.ps1

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Learning Activity System - Project3" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 检查虚拟环境是否存在
if (-Not (Test-Path ".\Project3")) {
    Write-Host "❌ 虚拟环境 Project3 不存在!" -ForegroundColor Red
    Write-Host "请先运行: python -m venv Project3" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ 虚拟环境 Project3 已找到" -ForegroundColor Green

# 检查依赖是否已安装
$pipList = & .\Project3\Scripts\python.exe -m pip list
if ($pipList -notmatch "Flask") {
    Write-Host "⚠️  正在安装依赖包..." -ForegroundColor Yellow
    & .\Project3\Scripts\python.exe -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 依赖安装失败!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "✅ 依赖包已安装" -ForegroundColor Green
}

# 检查 .env 文件
if (-Not (Test-Path ".\.env")) {
    Write-Host "⚠️  .env 文件不存在，使用 .env.example 创建..." -ForegroundColor Yellow
    Copy-Item ".\.env.example" ".\.env"
    Write-Host "❌ 请先配置 .env 文件中的 API 密钥!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ .env 文件已配置" -ForegroundColor Green
Write-Host ""

# 检查是否需要初始化数据库
Write-Host "💡 提示: 如果是首次运行，请先执行数据库初始化:" -ForegroundColor Yellow
Write-Host "   .\Project3\Scripts\python.exe init_db.py" -ForegroundColor Cyan
Write-Host ""

# 启动应用
Write-Host "🚀 正在启动应用..." -ForegroundColor Green
Write-Host "   使用虚拟环境: Project3" -ForegroundColor Gray
Write-Host "   访问地址: http://localhost:5000" -ForegroundColor Gray
Write-Host "   管理员账号: admin / admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 启动 Flask 应用
& .\Project3\Scripts\python.exe app.py
