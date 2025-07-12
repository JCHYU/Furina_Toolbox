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
from menu import create_sidebar  # 导入 create_sidebar 函数
from click import create_click_frame  # 导入连点器页面

def error ( log ):
    outlog ( log )
    showerror(title="We are sorry.", 
              message="Booting failed.\nYou can tell the developer.")
    sys.exit(1)
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
dm = DataManager()
dm.load(data)

primary_monitor = get_monitors()[0]
screen_width, screen_height = primary_monitor.width, primary_monitor.height
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

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

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

def check_icon_files():
    required_icons = [
        "settings/settings_normal.png",
        "settings/settings_hover.png",
        "settings/settings_click.png"
    ]
    
    missing_icons = []
    for icon in required_icons:
        icon_path = os.path.join(image_data, icon)
        if not os.path.exists(icon_path):
            missing_icons.append(icon)
    
    return missing_icons

if not check_dir(data) or not check_settings_file() or not check_dir(image_data):
    error ( "无法创建数据文件。" )
missing_icons = check_icon_files()
if missing_icons:
    error ( f"缺失一些文件: {', '.join(missing_icons)}." )

# 设置主题
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# 创建主窗口
win = ctk.CTk()

# 设置窗口标题多语言支持
text_title = {"Chinese": "芙宁娜工具箱", "English": "Furina Toolbox"}
language = dm.get_config("Language", "English")
win.title(text_title.get(language, text_title["English"]))

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
content_frame = None  # 存储内容框架引用

def on_button_click(action):
    """处理侧边栏按钮点击事件"""
    global content_frame
    
    print(f"按钮点击: {action}")
    
    if content_frame is None:
        return
    
    # 隐藏当前页面
    if hasattr(content_frame, 'current_page') and content_frame.current_page in content_frame.pages:
        content_frame.pages[content_frame.current_page].pack_forget()
    
    # 显示新页面
    if action in content_frame.pages:
        content_frame.pages[action].pack(fill="both", expand=True)
        content_frame.current_page = action
        print(f"已切换到 {action} 页面")
    else:
        print(f"找不到 {action} 页面")

def show_main():
    global content_frame
    
    main_container = ctk.CTkFrame(win, fg_color="transparent")
    main_container.pack(fill="both", expand=True)
    
    # 创建侧边栏 (传递正确的 image_data 路径)
    sidebar_frame = create_sidebar(main_container, dm, on_button_click, image_data)
    sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
    
    # 创建右侧内容区域
    content_frame = ctk.CTkFrame(
        main_container,
        fg_color="#FFFFFF",
        corner_radius=0,
        border_width=0
    )
    content_frame.pack(side="right", fill="both", expand=True)
    
    # 创建多个页面（堆叠在一起）
    content_frame.pages = {
        "main": create_main_frame(content_frame, dm),
        "click": create_click_frame(content_frame, dm),
        # 添加其他页面...
    }
    
    # 设置当前页面为主页
    content_frame.current_page = "main"
    content_frame.pages["main"].pack(fill="both", expand=True)
    
    # 存储内容框架引用
    win.content_frame = content_frame

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