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

Settings_Text = {"Chinese": "设置", "English": "Settings"}

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
    
    # 创建设置按钮 - 使用淡蓝色背景
    # 图片路径
    settings_image = image_data + "settings.png"
    
    # 加载设置图片
    settings_img = ctk.CTkImage(
        light_image=Image.open(settings_image),
        dark_image=Image.open(settings_image),
        size=(24, 24)
    )
    
    # 按钮高度
    button_height = 40
    
    # 计算圆角半径 - 高度的一半，确保始终为椭圆形
    corner_radius = button_height // 2
        
    settings_btn = ctk.CTkButton(
        sidebar,  # 放在功能区白条内
        text=Settings_Text[language],
        image=settings_img,
        compound="left",
        height=button_height,
        corner_radius=corner_radius,  # 高度的一半，确保椭圆形
        fg_color="#E6F2FF",  # 淡蓝色背景
        hover_color="#C4D9F0",  # 悬停时稍深的蓝色
        font=("Segoe UI", 12),
        text_color="#1a56db",  # 深蓝色文本
        command=open_settings_callback   
    )
        
    # 将按钮放置在功能区白条的左下角
    settings_btn.place(relx=0.5, rely=1.0, anchor="s", y=-10, relwidth=0.9)
    
    # 定义调整按钮形状的函数
    def adjust_button_shape(event):
        """动态调整按钮形状以保持椭圆形"""
        # 获取按钮当前宽度
        button_width = settings_btn.winfo_width()
        
        # 计算理想宽度（高度的3倍）
        ideal_width = button_height * 3
        
        # 计算圆角半径（高度的一半）
        corner_radius = button_height // 2
        
        # 如果按钮宽度小于理想宽度，调整宽度
        if button_width < ideal_width:
            settings_btn.configure(width=ideal_width)
        # 否则，使用当前宽度，但保持圆角半径
        else:
            settings_btn.configure(corner_radius=corner_radius)
    
    # 绑定窗口大小变化事件
    parent.bind("<Configure>", adjust_button_shape)
    
    return frame