import click

# 自定義命令類以實現多餘參數檢查
class AddWithExtraArgsCheck(click.Command):
    def invoke(self, ctx):
        # 在所有選項處理後執行多餘參數檢查
        if 'args' in ctx.params and ctx.params['args']:
            # 打印目前已經被判定的變數和值
            params_info = ", ".join(f"{param}: {value if value is not None else ''}" for param, value in ctx.params.items() if param != 'args')
            extra_args = " ".join(ctx.params['args'])
            raise click.UsageError(
                f"Got unexpected extra arguments ({extra_args})"
                f", already assigned ({params_info})",
                ctx=ctx
            )
        return super().invoke(ctx)

# 自動填入剩餘參數的函數閉包
def auto_fill_argument(required=False):
    def callback(ctx, param, value):
        # 檢查 args 是否存在於 ctx.params 中
        if 'args' not in ctx.params:
            ctx.params['args'] = ()
        # 將 args 轉換為 list
        args = list(ctx.params['args'])
        # 檢查是否需要動態填充參數
        if value is None:
            if args:
                value = args.pop(0)
                ctx.params['args'] = tuple(args)
            elif required:
                raise click.MissingParameter(param_hint=[f"--{param.name}", f"-{param.opts[1]}"])
        # 更新 ctx.params 中的 args
        ctx.params['args'] = tuple(args)
        return value
    return callback

# 撤除 click 自動 glob 展開變數路徑中的萬用字元
def disable_expand_args():
    from click import core
    def _no_expand_args(args): return args
    core._expand_args = _no_expand_args



import click
def echo_inf_message(message):
    click.echo(click.style(message, fg='blue', bold=True))
def echo_std_message(message):
    click.echo(message, err=False)
def echo_err_message(message, exit_code=None):
    click.echo(message, err=True)
    if exit_code: sys.exit(exit_code)

import sys, os
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.append(PROJECT_DIR)
