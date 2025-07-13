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
from click import create_click_frame
import datetime

text_title = {"Chinese": "芙宁娜工具箱", "English": "Furina Toolbox"}

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
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        default_settings = {
            "Version": 1.0,
            "Initialization": False,
            "Language": "English",
            "GamePath": "",
            "LastDate": current_date,  
            "Time": 0 
        }
        try:
            dm.savejson("settings.json", default_settings)
            return True
        except:
            return False
    return True
settings = dm.loadjson("settings.json")
needs_initialization = not settings.get('Initialization', False) if settings else True
if not needs_initialization:
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    last_date = settings.get('LastDate', '0000-00-00')
    time_count = settings.get('Time', 0)
    if last_date != current_date:
        time_count += 1
    settings['LastDate'] = current_date
    settings['Time'] = time_count
    dm.savejson("settings.json", settings)


win = ctk.CTk()
language = dm.get_config("Language", "English")
win.title(text_title.get(language, text_title["English"]))
win.configure(fg_color="#E6F2FF")

x_pos = int((screen_width - WINDOW_WIDTH * DPI_SCALING) / 2)
y_pos = int((screen_height - WINDOW_HEIGHT * DPI_SCALING) / 2)
win.geometry(f"{int(WINDOW_WIDTH)}x{int(WINDOW_HEIGHT)}+{int(x_pos)}+{int(y_pos)}")

settings = dm.loadjson("settings.json")
needs_initialization = not settings.get('Initialization', False) if settings else True

init_frame = None
content_frame = None

def press_button(action):
    global content_frame
    if content_frame is None:
        return
    if hasattr(content_frame, 'current_page') and content_frame.current_page in content_frame.pages:
        content_frame.pages[content_frame.current_page].pack_forget()
    if action in content_frame.pages:
        content_frame.pages[action].pack(fill="both", expand=True)
        content_frame.current_page = action

def show_main():
    global content_frame
    
    main_container = ctk.CTkFrame(win, fg_color="transparent")
    main_container.pack(fill="both", expand=True)
    
    main_container.grid_columnconfigure(0, weight=10)  # 侧边栏占10%
    main_container.grid_columnconfigure(1, weight=90)
    main_container.grid_rowconfigure(0, weight=1)
    
    sidebar_frame = create_sidebar(main_container, dm, press_button, image_data)
    sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    
    content_frame = ctk.CTkFrame(
        main_container,
        fg_color="#FFFFFF",
        corner_radius=0,
        border_width=0
    )
    content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
    
    content_frame.pages = {
        "main": create_main_frame(content_frame, dm),
        "click": create_click_frame(content_frame, dm),
    }
    
    content_frame.current_page = "main"
    content_frame.pages["main"].pack(fill="both", expand=True)
    
    win.content_frame = content_frame

def on_initialization_complete():
    show_main()

if needs_initialization:
    outlog("即将进行初始化操作。About to initialize.")
    init_frame = create_initialization_frame(win, dm, on_initialization_complete)
    init_frame.pack(fill="both", expand=True)
else:
    outlog("加载主页。Load the main page.")
    show_main()

win.mainloop()