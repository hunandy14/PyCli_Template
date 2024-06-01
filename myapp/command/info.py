from ..cli import echo_std_message
from .. import util

def info():
    """獲取從cli設置的初始化信息"""
    echo_std_message(f"專案主目錄位於: {util.get_project_dir()}")
