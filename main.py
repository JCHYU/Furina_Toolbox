# 这是 main.py (主页) 的代码
import customtkinter as ctk
import os
from PIL import Image
from data_manager import DataManager

# 路径配置
data = os.getenv('LOCALAPPDATA') + "\\FurinaTB\\"
image_data = os.getenv('LOCALAPPDATA') + "\\FurinaTB\\image\\"
exec_path = os.path.dirname(os.path.abspath(__file__))

# 初始化数据管理器
dm = DataManager()
dm.load(data)

language = dm.get_config("Language", "English")

# 功能按钮配置（包括设置按钮）
function_buttons = [
    {
        "text": {"Chinese": "角色管理", "English": "Character Management"},
        "icon": "character.png",
        "command": lambda: print("角色管理功能")
    },
    {
        "text": {"Chinese": "武器管理", "English": "Weapon Management"},
        "icon": "weapon.png",
        "command": lambda: print("武器管理功能")
    },
    {
        "text": {"Chinese": "材料计算", "English": "Material Calculator"},
        "icon": "material.png",
        "command": lambda: print("材料计算功能")
    },
    {
        "text": {"Chinese": "任务追踪", "English": "Quest Tracker"},
        "icon": "quest.png",
        "command": lambda: print("任务追踪功能")
    },
    {
        "text": {"Chinese": "地图工具", "English": "Map Tools"},
        "icon": "map.png",
        "command": lambda: print("地图工具功能")
    },
    {
        "text": {"Chinese": "设置", "English": "Settings"},
        "icon": "settings.png",
        "command": None  # 将由参数传入
    }
]

def create_main_frame(parent, dm, open_settings_callback):
    """
    创建主界面框架
    
    :param parent: 父容器
    :param dm: DataManager实例
    :param open_settings_callback: 打开设置的回调函数
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
    
    # 计算按钮间距
    total_buttons = len(function_buttons)
    top_margin = 0.05  # 顶部边距
    bottom_margin = 0.05  # 底部边距
    available_space = 1.0 - top_margin - bottom_margin
    button_spacing = available_space / total_buttons
    
    # 添加功能按钮（包括设置按钮）
    for i, button_info in enumerate(function_buttons):
        # 获取当前语言的按钮文本
        button_text = button_info["text"].get(language, button_info["text"]["English"])
        
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
        
        # 如果是设置按钮，使用传入的回调函数
        if button_text in ["设置", "Settings"]:
            command = open_settings_callback
        else:
            command = button_info["command"]
        
        # 创建按钮
        btn = ctk.CTkButton(
            sidebar,
            text=button_text,
            image=button_icon,
            compound="left",
            height=button_height,
            corner_radius=corner_radius,
            fg_color="#E6F2FF",
            hover_color="#C4D9F0",
            text_color="#1a56db",
            font=("Segoe UI", 12),
            command=command
        )
        
        # 计算按钮位置
        rely_position = top_margin + (i * button_spacing) + (button_spacing / 2)
        
        # 放置按钮
        btn.place(relx=0.5, rely=rely_position, anchor="center", relwidth=0.9)
        buttons.append(btn)
    
    # 定义调整按钮形状的函数
    def adjust_button_shape(event=None):
        """动态调整按钮形状以保持椭圆形"""
        # 获取边栏宽度
        sidebar_width = sidebar.winfo_width()
        
        # 计算理想宽度（边栏宽度的90%）
        ideal_width = sidebar_width * 0.9
        
        # 计算圆角半径（高度的一半）
        corner_radius = button_height // 2
        
        # 更新所有按钮的宽度和圆角
        for btn in buttons:
            # 如果按钮宽度小于理想宽度，调整宽度
            if btn.winfo_width() < ideal_width:
                btn.configure(width=ideal_width)
            # 否则，使用当前宽度，但保持圆角半径
            else:
                btn.configure(corner_radius=corner_radius)
    
    # 初始调整一次
    adjust_button_shape()
    
    # 绑定窗口大小变化事件
    parent.bind("<Configure>", lambda e: adjust_button_shape())
    
    return frame