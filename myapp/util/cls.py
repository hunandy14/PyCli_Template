import click

# 自訂 type 類別 ExtPath 範例
class ExtPath(click.Path):
    def __init__(self, my_check=False, **kwargs):
        self.my_check = my_check
        super().__init__(**kwargs)

    def convert(self, value, param, ctx):
        print(f"ExtPath.convert():: 啟動此函數的對象參數是 {param.name} 目前值為 {value}, 自訂參數 my_check={self.my_check}")
        return super().convert(value, param, ctx)

# 自定 Argument 類別 ExtArgument 範例
class ExtArgument(click.Argument):
    def __init__(self, *args, my_option='defalut_value', **kwargs):
        self.my_option = my_option
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        name = self.name
        value = opts.get(name)
        print(f"Argument.handle_parse_result():: 啟動此函數的對象參數是 {name} 目前值為 {value}, 自訂參數 my_option={self.my_option}")
        if isinstance(opts[name], tuple):
            opts[name] = opts[name] + (self.my_option,)
        # (self.my_option)
        return super().handle_parse_result(ctx, opts, args)

# 自定 Option 類別 ExtOption 範例
class ExtOption(click.Option):
    def __init__(self, *args, my_option='defalut_value', **kwargs):
        self.my_option = my_option
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        name = self.name
        value = opts.get(name)
        print(f"Option.handle_parse_result():: 啟動此函數的對象參數是 {name} 目前值為 {value}, 自訂參數 my_option={self.my_option}")
        opts[name] = self.my_option
        return super().handle_parse_result(ctx, opts, args)
