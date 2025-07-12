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

def create_sidebar(parent, dm, on_button_click, image_data):
    """
    创建侧边栏
    :param parent: 父容器
    :param dm: DataManager实例
    :param on_button_click: 按钮点击回调函数
    :param image_data: 图片目录路径
    :return: 侧边栏框架
    """
    language = dm.get_config("Language", "English")
    
    # 所有按钮配置 - 只有设置按钮有图标
    button_configs = [
        {"id": "login", "text": {"Chinese": "登录", "English": "Login"}, "icon": None, "selected": False},
        {"id": "main", "text": {"Chinese": "主页", "English": "Main"}, "icon": None, "selected": True},
        {"id": "start", "text": {"Chinese": "启动游戏", "English": "Start Game"}, "icon": None, "selected": False},
        {"id": "translate", "text": {"Chinese": "翻译", "English": "Translate"}, "icon": None, "selected": False},
        # 设置按钮配置
        {"id": "settings", "text": {"Chinese": "设置", "English": "Settings"}, "icon": "settings/settings_normal.png", 
         "hover_icon": "settings/settings_hover.png", "click_icon": "settings/settings_click.png", 
         "selected": False, "special": True}
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
            config.get("icon", None),  # 正常图标
            config.get("hover_icon", None),  # 悬停图标
            config.get("click_icon", None),  # 点击图标
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

def create_button(parent, action, text, icon_name, hover_icon_name, click_icon_name, 
                 selected, image_data, on_button_click, is_settings=False):
    """
    创建统一风格的按钮
    :param parent: 父容器
    :param action: 按钮动作标识
    :param text: 按钮文本
    :param icon_name: 正常状态图标文件名
    :param hover_icon_name: 悬停状态图标文件名
    :param click_icon_name: 点击状态图标文件名
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
    icons = {}
    if icon_name:  # 正常状态图标
        icon_path = os.path.join(image_data, icon_name)
        if os.path.exists(icon_path):
            try:
                icons["normal"] = ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    dark_image=Image.open(icon_path),
                    size=(24, 24)
                )
            except Exception as e:
                print(f"加载正常图标失败: {e}")
    
    if hover_icon_name:  # 悬停状态图标
        icon_path = os.path.join(image_data, hover_icon_name)
        if os.path.exists(icon_path):
            try:
                icons["hover"] = ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    dark_image=Image.open(icon_path),
                    size=(24, 24)
                )
            except Exception as e:
                print(f"加载悬停图标失败: {e}")
    
    if click_icon_name:  # 点击状态图标
        icon_path = os.path.join(image_data, click_icon_name)
        if os.path.exists(icon_path):
            try:
                icons["click"] = ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    dark_image=Image.open(icon_path),
                    size=(24, 24)
                )
            except Exception as e:
                print(f"加载点击图标失败: {e}")
    
    # 创建按钮命令
    if is_settings:
        command = lambda: handle_settings_click(btn, icons, on_button_click)
    else:
        command = lambda: on_button_click(action)
    
    # 创建按钮
    btn = ctk.CTkButton(
        button_frame,
        text=text,
        image=icons.get("normal", None),  # 默认使用正常图标
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
    
    # 添加悬停效果（仅当有悬停图标时）
    if "hover" in icons:
        btn.bind("<Enter>", lambda event, b=btn, i=icons: on_button_enter(b, i))
        btn.bind("<Leave>", lambda event, b=btn, i=icons: on_button_leave(b, i))
    
    # 设置选中样式
    if selected:
        btn.configure(fg_color=BUTTON_HOVER)
    
    btn.pack(side="top", fill="x", pady=(0, 5))
    
    # 保存图标引用
    btn.icons = icons
    
    return btn

def on_button_enter(btn, icons):
    """鼠标进入按钮时显示悬停图标"""
    if "hover" in icons:
        btn.configure(image=icons["hover"])

def on_button_leave(btn, icons):
    """鼠标离开按钮时显示正常图标"""
    if "normal" in icons:
        btn.configure(image=icons["normal"])

def handle_settings_click(btn, icons, on_button_click):
    """处理设置按钮点击事件"""
    # 更新为点击状态图标
    if "click" in icons:
        btn.configure(image=icons["click"])
    
    # 触发回调
    on_button_click("settings")
    
    # 500ms后恢复图标
    btn.after(500, lambda: restore_settings_icon(btn, icons))

def restore_settings_icon(btn, icons):
    """恢复设置按钮图标"""
    # 根据鼠标位置决定恢复为悬停图标还是正常图标
    x, y = btn.winfo_pointerxy()
    if btn.winfo_containing(x, y) == btn and "hover" in icons:
        # 鼠标仍在按钮上，显示悬停图标
        btn.configure(image=icons["hover"])
    elif "normal" in icons:
        # 鼠标不在按钮上，显示正常图标
        btn.configure(image=icons["normal"])