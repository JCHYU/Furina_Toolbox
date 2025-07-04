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
    创建主界面框架
    
    :param parent: 父容器
    :param dm: DataManager实例
    :param on_initialization_complete: 初始化完成回调函数
    """
    # 创建主框架
    frame = ctk.CTkFrame(parent)
    frame.configure(fg_color="#E6F2FF")
    frame.pack(fill="both", expand=True)
    
    # 创建主容器
    main_container = ctk.CTkFrame(frame, fg_color="transparent")
    main_container.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # 创建左侧功能区白条
    sidebar = ctk.CTkFrame(
        main_container,
        fg_color="#FFFFFF",  # 白色背景
        corner_radius=0,     # 直角
        width=100,           # 初始宽度
        height=600           # 初始高度
    )
    # 放置白条 - 左侧，高度占100%，宽度占15%
    sidebar.place(relx=0.0, rely=0.0, relwidth=0.15, relheight=1.0)
    
    # 按钮高度和间距
    button_height = 40
    corner_radius = button_height // 2  # 椭圆形按钮
    
    # 创建功能按钮列表
    buttons = []
    
    # 计算按钮间距 - 使用固定间距实现紧凑布局
    button_spacing = 5  # 按钮之间的垂直间距（像素）
    top_margin = 10     # 顶部边距（像素）
    
    # 确保设置图标存在
    settings_icon_path = os.path.join(image_data, "settings.png")
    if not os.path.exists(settings_icon_path):
        create_settings_icon(settings_icon_path)
    
    # 创建按钮容器 - 用于实现紧凑布局
    button_container = ctk.CTkFrame(sidebar, fg_color="transparent")
    button_container.pack(side="top", fill="both", expand=True, padx=5, pady=top_margin)
    
    # 添加功能按钮
    for i, button_info in enumerate(function_buttons):
        # 获取当前语言的按钮文本
        # 确保button_info["text"]是一个字典
        if isinstance(button_info["text"], dict):
            # 使用当前语言获取文本，如果不存在则使用英语
            button_text = button_info["text"].get(language, button_info["text"]["English"])
        else:
            # 如果不是字典，直接使用文本值
            button_text = button_info["text"]
        
        # 加载图标（如果有）
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
        
        # 创建按钮 - 直接使用按钮配置中的command
        btn = ctk.CTkButton(
            button_container,
            text=button_text,
            image=button_icon,
            compound="left",
            height=button_height,
            corner_radius=corner_radius,
            fg_color="#E6F2FF",
            hover_color="#C4D9F0",
            text_color="#1a56db",
            font=("Segoe UI", 12),
            command=button_info["command"]  # 直接使用配置中的命令
        )
        
        # 使用pack放置按钮，实现紧凑排列
        btn.pack(side="top", fill="x", padx=5, pady=(0, button_spacing))
        buttons.append(btn)
    
    # 定义调整按钮形状的函数
    def adjust_button_shape(event=None):
        """动态调整按钮形状以保持椭圆形"""
        # 获取容器宽度
        container_width = button_container.winfo_width()
        
        # 计算理想宽度（容器宽度的100%）
        ideal_width = container_width - 10  # 减去左右边距
        
        # 计算圆角半径（高度的一半）
        corner_radius = button_height // 2
        
        # 更新所有按钮的宽度和圆角
        for btn in buttons:
            btn.configure(width=ideal_width, corner_radius=corner_radius)
    
    # 初始调整一次
    adjust_button_shape()
    
    # 绑定窗口大小变化事件
    button_container.bind("<Configure>", lambda e: adjust_button_shape())
    
    return frame