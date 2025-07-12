# 这是 menu.py (侧边栏管理器) 的代码
import customtkinter as ctk
import os
from PIL import Image
from data_manager import DataManager

# 按钮样式常量
BUTTON_HEIGHT = 42
BUTTON_FONT = ("Segoe UI", 12)
BUTTON_FG = "transparent"
BUTTON_HOVER = "#EFF6FF"
TEXT_COLOR = "#1E40AF"
SELECTED_COLOR = "#3B82F6"

def create_sidebar(parent, dm, on_button_click):
    """
    创建侧边栏
    :param parent: 父容器
    :param dm: DataManager实例
    :param on_button_click: 按钮点击回调函数
    :return: 侧边栏框架
    """
    language = dm.get_config("Language", "English")
    image_data = os.path.join(os.getenv('LOCALAPPDATA'), "FurinaTB", "image")
    
    # 所有按钮配置
    button_configs = [
        {"id": "login", "text": {"Chinese": "登录", "English": "Login"}, "icon": "character.png", "selected": False},
        {"id": "main", "text": {"Chinese": "主页", "English": "Main"}, "icon": "character.png", "selected": True},
        {"id": "start", "text": {"Chinese": "启动游戏", "English": "Start Game"}, "icon": "weapon.png", "selected": False},
        {"id": "translate", "text": {"Chinese": "翻译", "English": "Translate"}, "icon": "material.png", "selected": False},
        {"id": "settings", "text": {"Chinese": "设置", "English": "Settings"}, "icon": "settings_normal.png", "selected": False, "special": True}
    ]

    # 创建侧边栏框架
    sidebar = ctk.CTkFrame(parent, fg_color="#F8FAFC", corner_radius=0)
    sidebar.pack(side="left", fill="y")
    
    # 标题
    title_text = {"Chinese": "芙宁娜工具箱", "English": "Furina Toolbox"}.get(language, "Furina Toolbox")
    ctk.CTkLabel(
        sidebar,
        text=title_text,
        font=("Segoe UI", 16, "bold"),
        text_color="#1E3A8A"
    ).pack(side="top", fill="x", padx=20, pady=(20, 15))
    
    # 按钮容器
    button_container = ctk.CTkFrame(sidebar, fg_color="transparent")
    button_container.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    
    # 创建所有按钮
    buttons = []
    for config in button_configs:
        btn = create_button(
            button_container,
            config["id"],
            config["text"].get(language, config["text"]["English"]),
            config["icon"],
            config["selected"],
            image_data,
            on_button_click,
            is_settings=config.get("special", False)
        )
        buttons.append(btn)
    
    # 底部版本信息
    bottom_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)
    
    ctk.CTkLabel(
        bottom_frame,
        text="Furina Toolbox v1.0",
        font=("Segoe UI", 10),
        text_color="#4B5563"
    ).pack(side="top", fill="x", pady=5)
    
    return sidebar

def create_button(parent, action, text, icon_name, selected, image_data, on_button_click, is_settings=False):
    """
    创建统一风格的按钮
    :param parent: 父容器
    :param action: 按钮动作标识
    :param text: 按钮文本
    :param icon_name: 图标文件名
    :param selected: 是否选中
    :param image_data: 图片目录
    :param on_button_click: 点击回调
    :param is_settings: 是否为设置按钮
    :return: 创建的按钮对象
    """
    button_frame = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=8)
    button_frame.pack(fill="x", pady=(0, 5))
    
    # 选中指示器
    indicator = ctk.CTkFrame(
        button_frame,
        width=4,
        fg_color=SELECTED_COLOR,
        corner_radius=2
    )
    if selected:
        indicator.place(relx=0, rely=0.5, relheight=0.7, anchor="w")
    else:
        indicator.place_forget()
    
    # 加载图标
    icon_path = os.path.join(image_data, icon_name)
    icon = None
    if os.path.exists(icon_path):
        try:
            icon = ctk.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),
                size=(24, 24)
            )
        except:
            pass
    
    # 创建按钮命令
    if is_settings:
        command = lambda: handle_settings_click(btn, image_data, on_button_click)
    else:
        command = lambda: on_button_click(action)
    
    # 创建按钮
    btn = ctk.CTkButton(
        button_frame,
        text=text,
        image=icon,
        compound="left",
        height=BUTTON_HEIGHT,
        corner_radius=8,
        fg_color=BUTTON_FG,
        hover_color=BUTTON_HOVER,
        text_color=TEXT_COLOR,
        font=BUTTON_FONT,
        anchor="w",
        command=command
    )
    
    # 设置选中样式
    if selected:
        btn.configure(fg_color=BUTTON_HOVER)
    
    btn.pack(side="top", fill="x", pady=(0, 5))
    return btn

def handle_settings_click(btn, image_data, on_button_click):
    """处理设置按钮点击事件"""
    # 更新为点击状态图标
    click_icon_path = os.path.join(image_data, "settings_click.png")
    if os.path.exists(click_icon_path):
        try:
            click_icon = ctk.CTkImage(
                light_image=Image.open(click_icon_path),
                dark_image=Image.open(click_icon_path),
                size=(24, 24)
            )
            btn.configure(image=click_icon)
        except:
            pass
    
    # 触发回调
    on_button_click("settings")
    
    # 500ms后恢复图标
    btn.after(500, lambda: restore_settings_icon(btn, image_data))

def restore_settings_icon(btn, image_data):
    """恢复设置按钮图标"""
    normal_icon_path = os.path.join(image_data, "settings_normal.png")
    if os.path.exists(normal_icon_path):
        try:
            normal_icon = ctk.CTkImage(
                light_image=Image.open(normal_icon_path),
                dark_image=Image.open(normal_icon_path),
                size=(24, 24)
            )
            btn.configure(image=normal_icon)
        except:
            pass