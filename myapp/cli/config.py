import click
from .. import cli
from .. import util
from .. import command

# 宣告選項群
@click.group()
def entry():
    """群組指令介面進入點"""

# 群組命令1:: democmd
@entry.command(cls=cli.AddWithExtraArgsCheck)
@click.option('--path', '-p', type=str, callback=cli.auto_fill_argument(required=True), help="指定文件路徑")
@click.option('--identity', '-id', type=str, callback=cli.auto_fill_argument(required=False), help="指定ID")
@click.option('--type', '-t', type=click.Choice(['any', 'folder', 'file'], case_sensitive=False), default='any', help="指定路徑類型: any (預設), folder, file")
@click.argument('args', nargs=-1)
@command.forward
def demo(path, identity, type, args):
    """範例命令"""

# 群組命令2:: info
@entry.command()
@command.forward
def info():
    """獲取從cli設置的初始化信息"""

# 群組命令3:: demo2
@entry.command()
@click.argument('name', required=True, nargs=1, type=util.cls.ExtPath())
@click.argument('path', required=True, nargs=-1, type=util.cls.ExtPath(my_check=True, exists=True))
def demo2(name, path):
    cli.echo_inf_message(f"[\n    name: {name}\n    path: {path}\n]")
    """獲取從cli設置的初始化信息"""

# 群組命令4:: demo3
@entry.command()
@click.argument('name', required=True, nargs=1, type=util.cls.ExtPath(), cls=util.cls.ExtArgument, my_option=True)
@click.argument('path', required=True, nargs=-1, type=util.cls.ExtPath(my_check=True, exists=True), cls=util.cls.ExtArgument, my_option='deploy.ps1')
@click.option('--identity', '-id', type=str, required=False, help="指定ID", cls=util.cls.ExtOption, my_option=-1)
def demo3(name, path, identity):
    cli.echo_inf_message(f"[\n    name: {name}\n    path: {path}\n    identity: {identity}\n]")
    """獲取從cli設置的初始化信息"""
