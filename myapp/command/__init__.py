import os
import importlib
import inspect
from functools import wraps

# 設定警告訊息和資訊訊息的控制變數
print_warnings = False
print_info = False

# 強制只轉同名的函式或類別
force_promote = True

# 獲取當前目錄
module_dir = os.path.dirname(__file__)

# 獲取當前模組的包名
current_package = __package__

# 動態導入同層資料夾中的所有模組
for module_name in os.listdir(module_dir):
    if module_name.endswith('.py') and module_name != '__init__.py':
        module_name = module_name[:-3]
        try:
            # 若 globals 中已有相同名稱的模組且 print_warnings 為 True，則打印警告訊息
            if module_name in globals() and print_warnings:
                print(f"Warning: '{module_name}' already exists in globals and will be overridden.")

            # 動態導入模組
            module = importlib.import_module(f'.{module_name}', package=current_package)
            globals()[module_name] = module

            # 獲取模組中的屬性，排除內建屬性和非該模組定義的屬性
            module_attrs = [
                attr for attr in module.__dict__
                if not attr.startswith('__')
                and inspect.getmodule(getattr(module, attr)) == module
            ]
            # 找到與模組同名的屬性
            same_name_attr = [attr for attr in module_attrs if attr == module_name]

            # 強制只轉同名的函式或類別
            if force_promote:
                if same_name_attr:
                    # 若 globals 中已有相同名稱的屬性且 print_warnings 為 True，則打印警告訊息
                    if module_name in globals() and print_warnings:
                        print(f"Warning: '{module_name}' in globals will be overridden by '{module.__name__}.{same_name_attr[0]}'.")
                    globals()[module_name] = getattr(module, same_name_attr[0])
                else:
                    if print_warnings:
                        print(f"Warning: No attribute with the same name '{module_name}' found in module '{module.__name__}'.")
            else:
                # 當模組中只有一個與檔名同名的函式或類別時將其提升到父級命名空間
                if len(module_attrs) == 1 and module_attrs[0] == module_name:
                    # 若 globals 中已有相同名稱的屬性且 print_warnings 為 True，則打印警告訊息
                    if module_name in globals() and print_warnings:
                        print(f"Warning: '{module_name}' in globals will be overridden by '{module.__name__}.{module_attrs[0]}'.")
                    globals()[module_name] = getattr(module, module_attrs[0])

            # 若 print_info 為 True，則打印導入的模組及其屬性
            if print_info:
                imported_items = ", ".join(module_attrs)
                print(f"Module '{module_name}' imported with items: \n  [ {imported_items} ]")
        except Exception as e:
            # 打印導入模組時的錯誤訊息
            print(f"Error importing module '{module_name}': {e}")

# 動態轉發與檔案名稱相同的函式或類別
def forward(target):
    # 裝飾器應用於函式時
    if callable(target):
        @wraps(target)
        def wrapper(*args, **kwargs):
            func_name = target.__name__
            try:
                # 動態導入目標模組
                parent_module = importlib.import_module(f'.{func_name}', package=current_package)
                # 獲取同名的函數
                target_func = getattr(parent_module, func_name, None)
                if target_func is None:
                    raise AttributeError(f"'{parent_module.__name__}' module has no attribute '{func_name}'")
                # 轉送參數並調用函數
                return target_func(*args, **kwargs)
            except ImportError as e:
                raise ImportError(f"Failed to import module for function '{func_name}': {e}")
            except AttributeError as e:
                raise AttributeError(f"Function '{func_name}' not found in the module '{parent_module.__name__}': {e}")
        return wrapper
    # 裝飾器應用於類別時
    elif isinstance(target, type):
        for attr_name, attr_value in target.__dict__.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                decorated_method = forward(attr_value)
                setattr(target, attr_name, decorated_method)
        return target
    else:
        raise TypeError("The @forward decorator can only be applied to functions or classes")
