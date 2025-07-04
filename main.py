import customtkinter as ctk
import os
from PIL import Image, ImageDraw
from math import radians, sin, cos
from data_manager import DataManager
from initialization import create_initialization_frame

# 路径配置
data = os.getenv('LOCALAPPDATA') + "\\FurinaTB\\"
image_data = os.getenv('LOCALAPPDATA') + "\\FurinaTB\\image\\"
exec_path = os.path.dirname(os.path.abspath(__file__))

buttons_text_login = {"Chinese": "登录", "English": "Login"}
buttons_text_main = {"Chinese": "主页", "English": "Main"}
buttons_text_start = {"Chinese": "启动游戏", "English": "Start Game"}
buttons_text_translate = {"Chinese": "翻译", "English": "Translate"}
buttons_text_settings = {"Chinese": "设置", "English": "Settings"}

# 初始化数据管理器
dm = DataManager()
dm.load(data)

language = dm.get_config("Language", "English")

# 打开设置的回调函数
def Settings_Open():
    pass

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
        "icon": "settings.png",
        "command": Settings_Open
    }
]

# 创建设置图标函数
def create_settings_icon(icon_path):
    """动态生成设置图标"""
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
        
        img.save(icon_path)
        return True
    except Exception as e:
        print(f"无法创建设置图标: {e}")
        return False

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
        width=200,           # 宽度
    )
    # 放置侧边栏 - 左侧，高度占100%，宽度占15%
    sidebar.place(relx=0.0, rely=0.0, relwidth=0.15, relheight=1.0)
    
    # 添加应用标题
    app_title = ctk.CTkLabel(
        sidebar,
        text="Furina Toolbox",
        font=("Segoe UI", 16, "bold"),
        text_color="#1E3A8A",  # 深蓝色
    )
    app_title.pack(side="top", fill="x", padx=20, pady=(20, 15))
    
    # 添加功能按钮容器
    button_container = ctk.CTkFrame(sidebar, fg_color="transparent")
    button_container.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    
    # 按钮高度和样式
    button_height = 42
    button_font = ("Segoe UI", 12)
    button_fg = "transparent"
    button_hover = "#EFF6FF"  # 非常淡的蓝色
    text_color = "#1E40AF"    # 蓝色
    
    # 确保设置图标存在
    settings_icon_path = os.path.join(image_data, "settings.png")
    if not os.path.exists(settings_icon_path):
        create_settings_icon(settings_icon_path)
    
    # 添加功能按钮
    for button_info in function_buttons:
        # 获取当前语言的按钮文本
        if isinstance(button_info["text"], dict):
            button_text = button_info["text"].get(language, button_info["text"]["English"])
        else:
            button_text = button_info["text"]
        
        # 加载图标
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
                except:
                    button_icon = None
        
        # 创建按钮
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
    
    # 创建右侧内容区域
    content_frame = ctk.CTkFrame(
        main_container,
        fg_color="#FFFFFF",
        corner_radius=0,
        border_width=0
    )
    content_frame.place(relx=0.15, rely=0, relwidth=0.85, relheight=1.0)
    
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