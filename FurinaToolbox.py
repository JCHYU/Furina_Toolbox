# 这是 FurinaToolbox.py (主程序) 的代码
import customtkinter as ctk
import os
from tkinter.messagebox import showerror
from screeninfo import get_monitors
import sys
import ctypes
from data_manager import DataManager
from initialization import create_initialization_frame
from main import create_main_frame
from menu import create_sidebar
import json

is_debug = not ( getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') )
def outlog(log):
    if is_debug:
        print("[控制台Console]" + log)

if is_debug:
    print("程序运行于 Python 中。您将会看到控制台中的调试日志。")
else:
    print("程序运行模式为 可执行程序。您将不会看到控制台中的调试日志。")

data = os.getenv('LOCALAPPDATA') + "\\FurinaTB\\"
image_data = data + "image\\"

# 初始化数据管理器
dm = DataManager()
dm.load(data)

# 获取主显示器信息
primary_monitor = get_monitors()[0]
screen_width, screen_height = primary_monitor.width, primary_monitor.height

# 获取系统DPI缩放比例
def get_dpi():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    hdc = ctypes.windll.user32.GetDC(0)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
    ctypes.windll.user32.ReleaseDC(0, hdc)
    return dpi / 96.0

DPI_SCALING = get_dpi()

# 窗口尺寸
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

# 目录检查函数
def check_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except:
            return False
    return True

def check_settings_file():
    settings_path = os.path.join(data, 'settings.json')
    if not os.path.isfile(settings_path):
        default_settings = {
            "Version": 1.0,
            "Initialization": False,
            "Language": "English",
            "GamePath": ""
        }
        try:
            dm.savejson("settings.json", default_settings)
            return True
        except:
            return False
    return True

# 检查目录和配置文件
if not check_dir(data) or not check_settings_file() or not check_dir(image_data):
    showerror(title="We are sorry.", 
              message="Initialization failed.\nYou can tell the developer.")
    sys.exit(1)

# 设置主题
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def load_language_texts():
    """从当前目录的language.json加载多语言文本"""
    try:
        with open('language.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # 如果文件不存在或读取失败，返回默认文本
        return {
            "window_title": {"Chinese": "芙宁娜工具箱", "English": "Furina Toolbox"},
            "sidebar_title": {"Chinese": "芙宁娜工具箱", "English": "Furina Toolbox"},
            "login": {"Chinese": "登录", "English": "Login"},
            "main": {"Chinese": "主页", "English": "Main"},
            "start_game": {"Chinese": "启动游戏", "English": "Start Game"},
            "translate": {"Chinese": "翻译", "English": "Translate"},
            "settings": {"Chinese": "设置", "English": "Settings"},
            "welcome": {"Chinese": "欢迎使用 Furina Toolbox", "English": "Welcome to Furina Toolbox"},
            "description": {"Chinese": "请从左侧菜单中选择功能", "English": "Select a function from the sidebar"}
        }

# 创建主窗口
win = ctk.CTk()

# 设置窗口标题
language = dm.get_config("Language", "English")
texts = load_language_texts()
win.title(texts["window_title"].get(language, texts["window_title"]["English"]))

win.configure(fg_color="#E6F2FF")

# 计算居中位置
x_pos = int((screen_width - WINDOW_WIDTH * DPI_SCALING) / 2)
y_pos = int((screen_height - WINDOW_HEIGHT * DPI_SCALING) / 2)
win.geometry(f"{int(WINDOW_WIDTH)}x{int(WINDOW_HEIGHT)}+{int(x_pos)}+{int(y_pos)}")

# 检查是否需要初始化
settings = dm.loadjson("settings.json")
needs_initialization = not settings.get('Initialization', False) if settings else True

# 全局变量
init_frame = None  # 添加全局变量定义

def on_button_click(action):
    """处理侧边栏按钮点击事件"""
    print(f"按钮点击: {action}")
    # 这里可以添加切换页面等逻辑

def show_main():
    # 创建主容器
    main_container = ctk.CTkFrame(win, fg_color="transparent")
    main_container.pack(fill="both", expand=True)
    
    # 创建侧边栏 (使用函数式版本)
    sidebar_frame = create_sidebar(main_container, dm, on_button_click)
    
    # 创建右侧内容区域
    content_frame = ctk.CTkFrame(
        main_container,
        fg_color="#FFFFFF",
        corner_radius=0,
        border_width=0
    )
    content_frame.pack(side="right", fill="both", expand=True)
    
    # 创建主页内容
    main_frame = create_main_frame(content_frame, dm)
    main_frame.pack(fill="both", expand=True)

# 初始化完成回调
def on_initialization_complete():
    show_main()

# 显示界面
if needs_initialization:
    outlog("即将进行初始化操作。About to initialize.")
    init_frame = create_initialization_frame(win, dm, on_initialization_complete)
    init_frame.pack(fill="both", expand=True)
else:
    outlog("加载主页。Load the main page.")
    show_main()

win.mainloop()