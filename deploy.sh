#!/bin/bash

# 確認參數 Path 是否已提供，若無則設置預設值
Path=${1:-"./.venv"}

# 定義函數
info() { echo -e "\e[90m$1\e[0m"; }
warning() { echo -e "\e[33mWARNING: $1\e[0m"; }
success() { echo -e "\e[32m$1\e[0m"; }
error() { echo -e "\e[31mERROR: $1\e[0m"; exit 1; }

# 檢查 requirements.txt 是否存在
[[ -f "requirements.txt" ]] || error "requirements.txt not found."

# 檢查是否有 python3
command -v python3 &> /dev/null || error "Python 3 is not installed."

# 檢查虛擬環境是否已存在
if [[ -f "$Path/bin/activate" ]]; then
    warning "Found existing virtual environment at '$Path'. Using it to install dependencies."
else
    info "Creating a new virtual environment at '$Path'."
    python3 -m venv "$Path" || error "Failed to create the virtual environment at '$Path'."
fi

# 啟動虛擬環境
info "Activating the virtual environment at '$Path'..."
source "$Path/bin/activate" || error "Failed to activate the virtual environment at '$Path'."

# 安裝 requirements.txt 中的依賴
info "Installing dependencies from requirements.txt..."
"$Path/bin/pip" install -r requirements.txt || {
    error "Failed to install dependencies from requirements.txt."
    deactivate
}

success "Virtual environment '$Path' successfully created and dependencies installed."

# 離開虛擬環境並恢復原本狀態
deactivate

info "To activate the virtual environment, run the following command:"
info "source '$Path/bin/activate'"
