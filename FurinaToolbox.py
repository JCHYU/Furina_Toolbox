# 这是 FurinaToolbox.py (主程序) 的化简版
import customtkinter as ctk
import os
from tkinter.messagebox import showerror
from screeninfo import get_monitors
import sys
import ctypes
from PIL import Image, ImageDraw
from math import radians, sin, cos
from data_manager import DataManager
from initialization import InitializationFrame
from main import MainFrame

# 设置背景颜色
BACKGROUND_COLOR = "#E6F2FF"

# 检查是否在调试模式
is_debug = not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'))

# 日志函数
def outlog(log):
    if is_debug:    
        print("[控制台Console]" + log)

if is_debug:
    print("程序运行于 Python 中。您将会看到控制台中的调试日志。")
else:
    print("程序运行模式为 可执行程序。您将不会看到控制台中的调试日志。")

# 路径配置
data = os.getenv('LOCALAPPDATA') + "\\FurinaTB\\"
image_data = os.getenv('LOCALAPPDATA') + "\\FurinaTB\\image\\"

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

# 创建主窗口
win = ctk.CTk()
win.title("Furina Toolbox")
win.configure(fg_color=BACKGROUND_COLOR)

# 计算居中位置
x_pos = int((screen_width - WINDOW_WIDTH * DPI_SCALING) / 2)
y_pos = int((screen_height - WINDOW_HEIGHT * DPI_SCALING) / 2)
win.geometry(f"{int(WINDOW_WIDTH)}x{int(WINDOW_HEIGHT)}+{int(x_pos)}+{int(y_pos)}")

# 检查是否需要初始化
settings = dm.loadjson("settings.json")
needs_initialization = not settings.get('Initialization', False) if settings else True

# 全局变量
init_frame = None  # 添加全局变量定义

# 显示主界面
def show_main():
    global init_frame  # 声明使用全局变量
    
    # 移除初始化框架
    if init_frame:
        init_frame.destroy()
        init_frame = None  # 重置为None
    
    # 创建主界面框架
    main_frame = MainFrame(win, dm, open_settings)

# 初始化完成回调
def on_initialization_complete():
    show_main()

# 设置按钮功能
def open_settings():
    print("Settings button clicked")

# 创建设置图标
settings_image = os.path.join(image_data, "settings.png")
if not os.path.exists(settings_image):
    try:
        img_size = (32, 32)
        img = Image.new('RGBA', img_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        center = (img_size[0] // 2, img_size[1] // 2)
        radius = 12
        
        # 绘制齿轮
        draw.ellipse([(center[0]-radius, center[1]-radius), 
                     (center[0]+radius, center[1]+radius)], 
                     outline="#1a56db", width=2)
        
        # 绘制齿轮齿
        for i in range(8):
            angle = i * 45
            rad_angle = radians(angle)
            cos_val, sin_val = cos(rad_angle), sin(rad_angle)
            
            x1 = center[0] + int(radius * 0.7 * cos_val)
            y1 = center[1] + int(radius * 0.7 * sin_val)
            x2 = center[0] + int(radius * 1.3 * cos_val)
            y2 = center[1] + int(radius * 1.3 * sin_val)
            draw.line([(x1, y1), (x2, y2)], fill="#1a56db", width=2)
        
        img.save(settings_image)
    except Exception as e:
        print(f"无法创建设置图标: {e}")

# 显示界面
if needs_initialization:
    outlog("即将进行初始化操作。About to initialize.")
    init_frame = InitializationFrame(win, dm, on_initialization_complete)
else:
    outlog("加载主页。Load the main page.")
    show_main()

win.mainloop()