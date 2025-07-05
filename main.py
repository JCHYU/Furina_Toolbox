# 这是 main.py (主页) 的代码
import customtkinter as ctk
import os
from PIL import Image, ImageDraw
from math import radians, sin, cos
from data_manager import DataManager
from initialization import create_initialization_frame

# 路径配置
data = os.getenv('LOCALAPPDATA') + "\\FurinaTB\\"
image_data = data + "image\\"
exec_path = os.path.dirname(os.path.abspath(__file__))  
dm = DataManager()
dm.load(data)

# 图标状态路径
icon_settings_normal = "settings\\settings_normal.png"
icon_settings_click = "settings\\settings_click.png"

# 多语言
language = dm.get_config("Language", "English")
text_title = {"Chinese": "芙宁娜工具箱", "English": "Furina Toolbox"}
buttons_text_login = {"Chinese": "登录", "English": "Login"}
buttons_text_main = {"Chinese": "主页", "English": "Main"}
buttons_text_start = {"Chinese": "启动游戏", "English": "Start Game"}
buttons_text_translate = {"Chinese": "翻译", "English": "Translate"}
buttons_text_settings = {"Chinese": "设置", "English": "Settings"}

# 布局
weight = 0.2  # 侧边栏与总窗口宽度之比

def Settings_Open(btn):
    """设置按钮点击事件，更改图标为点击状态"""
    try:
        # 获取点击状态图标路径
        icon_path = os.path.join(image_data, icon_settings_click)
        
        # 如果图标文件存在，则更新按钮图标
        if os.path.exists(icon_path):
            click_icon = ctk.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),
                size=(24, 24)
            )
            btn.configure(image=click_icon)
            
            # 设置定时器，500ms后恢复为正常图标
            btn.after(500, lambda: restore_settings_icon(btn))
            
            # 这里添加实际打开设置窗口的代码
            # open_settings_window()
    except Exception as e:
        print(f"设置按钮点击事件错误: {e}")

def restore_settings_icon(btn):
    """恢复设置按钮为正常状态图标"""
    try:
        icon_path = os.path.join(image_data, icon_settings_normal)
        if os.path.exists(icon_path):
            normal_icon = ctk.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),
                size=(24, 24)
            )
            btn.configure(image=normal_icon)
    except Exception as e:
        print(f"恢复设置图标错误: {e}")

def Login_Open():
    pass

def Start_Open():
    pass

def Fanyi_Open():
    pass

function_buttons = [
    {
        "text": buttons_text_login, 
        "icon": "character.png",
        "command": Login_Open
    },
    {
        "text": buttons_text_main, 
        "icon": "character.png",
        "command": None
    },
    {
        "text": buttons_text_start,
        "icon": "weapon.png",
        "command": Start_Open
    },
    {
        "text": buttons_text_translate,
        "icon": "material.png",
        "command": Fanyi_Open
    },
    {
        "text": buttons_text_settings,
        "icon": icon_settings_normal,
        "command": None  # 这里设置为None，因为我们将在创建按钮时单独处理
    }
]

def create_main_frame(parent, dm, on_initialization_complete):
    """
    创建主界面框架 - 简洁现代风格
    
    :param parent: 父容器
    :param dm: DataManager实例
    :param on_initialization_complete: 初始化完成回调函数
    """
    
    # 创建主框架
    frame = ctk.CTkFrame(parent)
    frame.configure(fg_color="#FFFFFF")  # 白色背景
    frame.pack(fill="both", expand=True)
    
    # 创建主容器
    main_container = ctk.CTkFrame(frame, fg_color="transparent")
    main_container.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # 创建左侧功能区 - 简洁现代风格
    sidebar = ctk.CTkFrame(
        main_container,
        fg_color="#F8FAFC",  # 浅灰蓝色背景
        corner_radius=0,     # 直角
    )
    # 放置侧边栏 - 左侧，高度占100%，宽度为weight
    sidebar.place(relx=0.0, rely=0.0, relwidth=weight, relheight=1.0)
    
    # 添加应用标题
    app_title = ctk.CTkLabel(
        sidebar,
        text=text_title[language],
        font=("Segoe UI", 16, "bold"),
        text_color="#1E3A8A",  # 深蓝色
    )
    app_title.pack(side="top", fill="x", padx=20, pady=(20, 15))
    
    # 添加功能按钮容器 - 使用fill="both"确保宽度填满侧边栏
    button_container = ctk.CTkFrame(sidebar, fg_color="transparent")
    button_container.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    
    # 按钮高度和样式
    button_height = 42
    button_font = ("Segoe UI", 12)
    button_fg = "transparent"
    button_hover = "#EFF6FF"  # 非常淡的蓝色
    text_color = "#1E40AF"    # 蓝色
    
    # 保存设置按钮的引用
    settings_button = None
    
    # 添加功能按钮 - 宽度填满容器
    buttons = []  # 存储所有按钮的列表
    
    for button_info in function_buttons:
        # 获取当前语言的按钮文本
        if isinstance(button_info["text"], dict):
            button_text = button_info["text"].get(language, button_info["text"]["English"])
        else:
            button_text = button_text = button_info["text"]
        
        # 加载图标（仅当图片存在时）
        button_icon = None
        if button_info["icon"]:
            icon_path = os.path.join(image_data, button_info["icon"])
            if os.path.exists(icon_path):
                try:
                    button_icon = ctk.CTkImage(
                        light_image=Image.open(icon_path),
                        dark_image=Image.open(icon_path),
                        size=(24, 24)
                    )
                except Exception as e:
                    print(f"加载图标失败: {e}")
                    button_icon = None
            else:
                # 图片不存在，不创建也不报错
                button_icon = None
        
        # 创建按钮 - 使用fill="x"确保宽度填满容器
        if button_info["text"] == buttons_text_settings:
            # 设置按钮特殊处理
            btn = ctk.CTkButton(
                button_container,
                text=button_text,
                image=button_icon,
                compound="left",
                height=button_height,
                corner_radius=8,  # 轻微圆角
                fg_color=button_fg,
                hover_color=button_hover,
                text_color=text_color,
                font=button_font,
                anchor="w",  # 左对齐
                command=None  # 稍后设置
            )
            # 设置按钮的特殊命令
            btn.configure(command=lambda b=btn: Settings_Open(b))
            settings_button = btn  # 保存设置按钮的引用
        else:
            # 其他按钮正常创建
            btn = ctk.CTkButton(
                button_container,
                text=button_text,
                image=button_icon,
                compound="left",
                height=button_height,
                corner_radius=8,  # 轻微圆角
                fg_color=button_fg,
                hover_color=button_hover,
                text_color=text_color,
                font=button_font,
                anchor="w",  # 左对齐
                command=button_info["command"]
            )
        
        buttons.append(btn)  # 添加到按钮列表
        btn.pack(side="top", fill="x", pady=(0, 5))
    
    # 添加底部版本信息
    bottom_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)
    
    # 添加版本信息
    version_info = ctk.CTkLabel(
        bottom_frame,
        text="Furina Toolbox v1.0",
        font=("Segoe UI", 10),
        text_color="#4B5563",  # 灰色
    )
    version_info.pack(side="top", fill="x", pady=5)
    
    content_frame = ctk.CTkFrame(
        main_container,
        fg_color="#FFFFFF",
        corner_radius=0,
        border_width=0
    )
    content_frame.place(relx=weight, rely=0, relwidth=1-weight, relheight=1.0)
    
    # 添加欢迎内容
    welcome_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    welcome_frame.place(relx=0.5, rely=0.4, anchor="center")
    
    # 添加应用图标（占位）
    app_icon = ctk.CTkLabel(
        welcome_frame,
        text="🎮",  # 使用emoji作为占位符
        font=("Segoe UI", 64),
        text_color="#3B82F6",  # 蓝色
    )
    app_icon.pack(side="top", pady=(0, 20))
    
    welcome_label = ctk.CTkLabel(
        welcome_frame,
        text="欢迎使用 Furina Toolbox" if language == "Chinese" else "Welcome to Furina Toolbox",
        font=("Segoe UI", 24, "bold"),
        text_color="#1E3A8A",  # 深蓝色
    )
    welcome_label.pack(side="top", pady=(0, 10))
    
    description_text = "请从左侧菜单中选择功能" if language == "Chinese" else "Select a function from the sidebar"
    description_label = ctk.CTkLabel(
        welcome_frame,
        text=description_text,
        font=("Segoe UI", 14),
        text_color="#4B5563",  # 灰色
    )
    description_label.pack(side="top")
    
    return frame