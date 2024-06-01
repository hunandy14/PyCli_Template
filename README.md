Python Comand Line Interface Framework
===

基於 click 的一個 python 命令列框架，實現了類於 powershell 中自動填入的參數的功能  

舉例來說對於這個命令 `myapp` 中的選項 'demo' 參數 `path` 與參數 `identity` 設置為  

 - 自動填入(要求輸入) `callback=cli.auto_fill_argument(required=True)`  
 - 自動填入(可選輸入) `callback=cli.auto_fill_argument(required=False)`  

就可以像這樣使用

```ps1
# 顯示指定所有參數名
myapp demo --path "C:\path\to\your\file.txt" --identity 0 --type=file

# 隱式輸入 path 參數
myapp demo "C:\path\to\your\file.txt" --identity 0 --type=file

# 隱式輸入 path, identity 參數
myapp demo "C:\path\to\your\file.txt" 0 --type=file

# 隱式輸入 path 參數名, 不輸入 identity 參數
myapp demo "C:\path\to\your\file.txt" --type=file

# 隱式輸入 path, identity 參數 (任意調換參數)
myapp demo "C:\path\to\your\file.txt" 0 --type=file
myapp demo "C:\path\to\your\file.txt" --type=file 0
myapp demo --type=file "C:\path\to\your\file.txt" 0
```



## 參數多樣化輸入

對於參數的輸入會有四種形式都是可被接受的，這是 click 預設的功能

```ps1
myapp demo --path='Text.txt'
myapp demo --path 'Text.txt'
myapp demo -p 'Text.txt'
myapp demo -p'Text.txt'
```



## 環境變數路徑
對於環境的設置寫了一個批次檔放在 bin 資料夾中，可以直接這樣使用

```ps1
.\bin\myapp.cmd demo --path "C:\path\to\your\file.txt" --identity 0 --type=file
```

或者是將 bin 加入環境變數後就可以直接使用了
