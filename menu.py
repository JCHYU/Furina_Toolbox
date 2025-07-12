import customtkinter as ctk
import os
from PIL import Image
from data_manager import DataManager

BUTTON_HEIGHT = 42
BUTTON_FONT = ("Segoe UI", 12)
BUTTON_FG = "transparent"
BUTTON_HOVER = "#EFF6FF"
TEXT_COLOR = "#1E40AF"
SELECTED_COLOR = "#3B82F6"

Button_Login = {"Chinese": "登录", "English": "Login"}
Button_Main = {"Chinese": "主页", "English": "Main"}
Button_Start = {"Chinese": "启动游戏", "English": "Start Game"}
Button_Translate = {"Chinese": "翻译", "English": "Translate"}
Button_Click = {"Chinese": "连点器", "English": "Continuous Clicker"}
Button_Settings = {"Chinese": "设置", "English": "Settings"}

def create_sidebar(parent, dm, on_button_click, image_data):
    language = dm.get_config("Language", "English")
    
    button_configs = [
        {
            "id": "login", 
            "text": Button_Login, 
            "icons": {
                "normal": None,
                "hover": None,
                "click": None
            },
            "selected": False
        },
        {
            "id": "main", 
            "text": Button_Main, 
            "icons": {
                "normal": None,
                "hover": None,
                "click": None
            },
            "selected": True
        },
        {
            "id": "start", 
            "text": Button_Start, 
            "icons": {
                "normal": None,
                "hover": None,
                "click": None
            },
            "selected": False
        },
        {
            "id": "translate", 
            "text": Button_Translate, 
            "icons": {
                "normal": None,
                "hover": None,
                "click": None
            },
            "selected": False
        },
        {
            "id": "Click", 
            "text": Button_Click, 
            "icons": {
                "normal": None,
                "hover": None,
                "click": None
            },
            "selected": False
        },
        {
            "id": "settings", 
            "text": Button_Settings, 
            "icons": {
                "normal": "settings\\settings_normal.png",
                "hover": "settings\\settings_hover.png",
                "click": "settings\\settings_click.png"
            },
            "selected": False,
            "special": True
        }
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
            config.get("icons", {}),
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

def create_button(parent, action, text, icons_config, selected, image_data, on_button_click, is_settings=False):
    """
    创建统一风格的按钮
    :param parent: 父容器
    :param action: 按钮动作标识
    :param text: 按钮文本
    :param icons_config: 图标配置字典，包含normal、hover、click三种状态的图标路径
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
    
    # 加载所有图标状态
    icons = {}
    for state, icon_path in icons_config.items():
        if icon_path is None:
            continue  # 跳过None值
            
        full_path = os.path.join(image_data, icon_path)
        if os.path.exists(full_path):
            try:
                icons[state] = ctk.CTkImage(
                    light_image=Image.open(full_path),
                    dark_image=Image.open(full_path),
                    size=(24, 24)
                )
                print(f"成功加载 {state} 状态图标: {full_path}")
            except Exception as e:
                print(f"加载 {state} 状态图标失败: {e}")
        else:
            print(f"{state} 状态图标文件不存在: {full_path}")
    
    # 创建按钮命令
    if is_settings:
        command = lambda: handle_settings_click(btn, icons, on_button_click)
    else:
        command = lambda: on_button_click(action)
    
    # 创建按钮
    btn = ctk.CTkButton(
        button_frame,
        text=text,
        image=icons.get("normal", None),  # 默认使用正常状态图标
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
    
    # 保存图标引用
    btn.icons = icons
    
    # 添加鼠标事件绑定
    btn.bind("<Enter>", lambda event, b=btn: on_button_enter(b))
    btn.bind("<Leave>", lambda event, b=btn: on_button_leave(b))
    btn.bind("<ButtonPress-1>", lambda event, b=btn: on_button_press(b))
    btn.bind("<ButtonRelease-1>", lambda event, b=btn: on_button_release(b))
    
    # 设置选中样式
    if selected:
        btn.configure(fg_color=BUTTON_HOVER)
    
    btn.pack(side="top", fill="x", pady=(0, 5))
    return btn

def on_button_enter(btn):
    """鼠标进入按钮时显示悬停图标"""
    if "hover" in btn.icons:
        btn.configure(image=btn.icons["hover"])

def on_button_leave(btn):
    """鼠标离开按钮时显示正常图标"""
    if "normal" in btn.icons:
        btn.configure(image=btn.icons["normal"])

def on_button_press(btn):
    """鼠标按下按钮时显示点击图标"""
    if "click" in btn.icons:
        btn.configure(image=btn.icons["click"])

def on_button_release(btn):
    """鼠标释放按钮时显示悬停图标（如果鼠标仍在按钮上）"""
    # 获取当前鼠标位置
    x, y = btn.winfo_pointerxy()
    relative_widget = btn.winfo_containing(x, y)
    
    if relative_widget == btn and "hover" in btn.icons:
        # 鼠标仍在按钮上，显示悬停图标
        btn.configure(image=btn.icons["hover"])
    elif "normal" in btn.icons:
        # 鼠标不在按钮上，显示正常图标
        btn.configure(image=btn.icons["normal"])

def handle_settings_click(btn, icons, on_button_click):
    """处理设置按钮点击事件"""
    # 更新为点击状态图标（如果存在）
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
    relative_widget = btn.winfo_containing(x, y)
    
    if relative_widget == btn and "hover" in icons:
        # 鼠标仍在按钮上，显示悬停图标
        btn.configure(image=icons["hover"])
    elif "normal" in icons:
        # 鼠标不在按钮上，显示正常图标
        btn.configure(image=icons["normal"])