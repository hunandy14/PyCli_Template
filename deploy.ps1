<#
.SYNOPSIS
建立並啟動 Python 虛擬環境並安裝 requirements.txt 中的依賴

.PARAMETER Path
指定虛擬環境的安裝路徑

.EXAMPLE
.\deploy.ps1 -Path .venv
#>

[CmdletBinding()]
param (
    [string]$Path = "$PSScriptRoot\.venv"
)

# 檢查 requirements.txt 是否存在
if (-Not (Test-Path -Path "requirements.txt")) {
    Write-Host "requirements.txt not found."
    exit 1
}

# 檢查虛擬環境是否已存在
if (Test-Path -Path "$Path\Scripts\Activate.ps1") {
    Write-Host "WARNING: Found existing virtual environment at '$Path'. Using it to install dependencies." -ForegroundColor Yellow
} else {
    Write-Host "Creating a new virtual environment at '$Path'." -ForegroundColor DarkGray
    # 建立虛擬環境
    python -m venv $Path
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create the virtual environment at '$Path'." -ForegroundColor Red
        exit 1
    }
}

# 啟動虛擬環境
Write-Host "Activating the virtual environment at '$Path'..." -ForegroundColor DarkGray
& "$Path\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate the virtual environment at '$Path'." -ForegroundColor Red
    exit 1
}

# 更新 pip
Write-Host "Updating pip to the latest version..." -ForegroundColor DarkGray
& "$Path\Scripts\python.exe" -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to update pip." -ForegroundColor Red
    deactivate
    exit 1
}

# 安裝 requirements.txt 中的依賴
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor DarkGray
& "$Path\Scripts\python.exe" -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies from requirements.txt." -ForegroundColor Red
    deactivate
    exit 1
}

Write-Host "Virtual environment '$Path' successfully created and dependencies installed." -ForegroundColor DarkGreen

# 刪除不必要的檔案
Write-Host "Cleaning up unnecessary files..." -ForegroundColor DarkGray
python setup.py clean --all

# 離開虛擬環境並恢復原本狀態
deactivate

Write-Host "To activate the virtual environment, run the following command:" -ForegroundColor DarkGray
Write-Host "& '$Path\Scripts\Activate.ps1'" -ForegroundColor DarkGray
