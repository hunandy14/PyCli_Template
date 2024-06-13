#!/bin/bash

# 確認參數 Path 是否已提供，若無則設置預設值
if [ -z "$1" ]; then
    Path="./.venv"
else
    Path="$1"
fi

# 檢查 requirements.txt 是否存在
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found."
    exit 1
fi

# 檢查虛擬環境是否已存在
if [ -f "$Path/bin/activate" ]; then
    echo -e "\e[33mWARNING: Found existing virtual environment at '$Path'. Using it to install dependencies.\e[0m"
else
    echo -e "\e[90mCreating a new virtual environment at '$Path'.\e[0m"
    # 建立虛擬環境
    python3 -m venv $Path
    if [ $? -ne 0 ]; then
        echo -e "\e[31mERROR: Failed to create the virtual environment at '$Path'.\e[0m"
        exit 1
    fi
fi

# 啟動虛擬環境
echo -e "\e[90mActivating the virtual environment at '$Path'...\e[0m"
source "$Path/bin/activate"
if [ $? -ne 0 ]; then
    echo -e "\e[31mERROR: Failed to activate the virtual environment at '$Path'.\e[0m"
    exit 1
fi

# 安裝 requirements.txt 中的依賴
echo -e "\e[90mInstalling dependencies from requirements.txt...\e[0m"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "\e[31mERROR: Failed to install dependencies from requirements.txt.\e[0m"
    deactivate
    exit 1
fi

echo -e "\e[32mVirtual environment '$Path' successfully created and dependencies installed.\e[0m"

# 離開虛擬環境並恢復原本狀態
deactivate

echo -e "\e[90mTo activate the virtual environment, run the following command:\e[0m"
echo -e "\e[90msource '$Path/bin/activate'\e[0m"
