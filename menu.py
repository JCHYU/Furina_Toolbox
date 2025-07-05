# 这是 menu.py (侧边栏管理器) 的代码
import customtkinter as ctk
import os
from PIL import Image
import json

def load_language_texts():
    with open('language.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_sidebar(parent, dm, on_button_click):
    language = dm.get_config("Language", "English")
    image_data = os.getenv('LOCALAPPDATA') + "\\FurinaTB\\image\\"
    
    texts = load_language_texts()
    
    sidebar = ctk.CTkFrame(
        parent,
        fg_color="#F8FAFC",
        corner_radius=0,
    )
    sidebar.pack(side="left", fill="y", padx=0, pady=0)
    
    app_title = ctk.CTkLabel(
        sidebar,
        text=texts["title"].get(language, texts["title"]["English"]),
        font=("Segoe UI", 16, "bold"),
        text_color="#1E3A8A",
    )
    app_title.pack(side="top", fill="x", padx=20, pady=(20, 15))
    
    # 添加功能按钮容器
    button_container = ctk.CTkFrame(sidebar, fg_color="transparent")
    button_container.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    
    # 按钮配置
    button_height = 42
    button_font = ("Segoe UI", 12)
    button_fg = "transparent"
    button_hover = "#EFF6FF"
    text_color = "#1E40AF"
    selected_color = "#3B82F6"
    
    # 创建按钮
    buttons = []
    settings_button = None
    
    def on_settings_click():
        """设置按钮点击事件"""
        nonlocal settings_button
        click_icon_path = os.path.join(image_data, "settings_click.png")
        if os.path.exists(click_icon_path):
            try:
                click_icon = ctk.CTkImage(
                    light_image=Image.open(click_icon_path),
                    dark_image=Image.open(click_icon_path),
                    size=(24, 24)
                )
                settings_button.configure(image=click_icon)
                settings_button.after(500, lambda: restore_settings_icon(settings_button))
            except:
                pass
        on_button_click("settings")
    
    def restore_settings_icon(btn):
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

    # 创建各个按钮
    create_button(button_container, texts["login"], "character.png", "login", language, image_data, 
                 button_height, button_font, button_fg, button_hover, text_color, selected_color, 
                 on_button_click, False, buttons)
    
    create_button(button_container, texts["main"], "character.png", "main", language, image_data, 
                 button_height, button_font, button_fg, button_hover, text_color, selected_color, 
                 on_button_click, True, buttons)
    
    create_button(button_container, texts["start_game"], "weapon.png", "start", language, image_data, 
                 button_height, button_font, button_fg, button_hover, text_color, selected_color, 
                 on_button_click, False, buttons)
    
    create_button(button_container, texts["translate"], "material.png", "translate", language, image_data, 
                 button_height, button_font, button_fg, button_hover, text_color, selected_color, 
                 on_button_click, False, buttons)
    
    settings_button = create_settings_button(button_container, texts["settings"], "settings_normal.png", 
                                           language, image_data, button_height, button_font, 
                                           button_fg, button_hover, text_color, on_settings_click, buttons)
    
    # 底部版本信息
    bottom_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)
    
    version_info = ctk.CTkLabel(
        bottom_frame,
        text="Furina Toolbox v1.0",
        font=("Segoe UI", 10),
        text_color="#4B5563",
    )
    version_info.pack(side="top", fill="x", pady=5)
    
    return sidebar


def create_button(parent, text_dict, icon_name, action, language, image_data, 
                 button_height, button_font, button_fg, button_hover, 
                 text_color, selected_color, on_button_click, selected, buttons):
    """创建普通功能按钮"""
    # 获取当前语言的按钮文本
    button_text = text_dict.get(language, text_dict["English"])
    
    # 加载图标
    button_icon = None
    icon_path = os.path.join(image_data, icon_name)
    if os.path.exists(icon_path):
        try:
            button_icon = ctk.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),
                size=(24, 24)
            )
        except:
            button_icon = None
    
    # 创建按钮容器
    button_frame = ctk.CTkFrame(
        parent, 
        fg_color="transparent",
        corner_radius=8
    )
    button_frame.pack(fill="x", pady=(0, 5))
    
    # 创建选中指示器
    selection_indicator = ctk.CTkFrame(
        button_frame,
        width=4,
        fg_color=selected_color,
        corner_radius=2
    )
    selection_indicator.place(relx=0, rely=0.5, relheight=0.7, anchor="w")
    if not selected:
        selection_indicator.place_forget()
    
    # 创建按钮
    btn = ctk.CTkButton(
        button_frame,
        text=button_text,
        image=button_icon,
        compound="left",
        height=button_height,
        corner_radius=8,
        fg_color=button_fg,
        hover_color=button_hover,
        text_color=text_color,
        font=button_font,
        anchor="w",
        command=lambda: on_button_click(action)
    )
    
    # 设置选中样式
    if selected:
        btn.configure(fg_color=button_hover)
    
    buttons.append(btn)
    btn.pack(side="top", fill="x", pady=(0, 5))
    
    return btn

def create_settings_button(parent, text_dict, icon_name, language, image_data, 
                          button_height, button_font, button_fg, 
                          button_hover, text_color, on_settings_click, buttons):
    """创建设置按钮（特殊处理）"""
    # 获取当前语言的按钮文本
    button_text = text_dict.get(language, text_dict["English"])
    
    # 加载图标
    button_icon = None
    icon_path = os.path.join(image_data, icon_name)
    if os.path.exists(icon_path):
        try:
            button_icon = ctk.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),
                size=(24, 24)
            )
        except:
            button_icon = None
    
    # 创建按钮容器
    button_frame = ctk.CTkFrame(
        parent, 
        fg_color="transparent",
        corner_radius=8
    )
    button_frame.pack(fill="x", pady=(0, 5))
    
    # 创建按钮
    btn = ctk.CTkButton(
        button_frame,
        text=button_text,
        image=button_icon,
        compound="left",
        height=button_height,
        corner_radius=8,
        fg_color=button_fg,
        hover_color=button_hover,
        text_color=text_color,
        font=button_font,
        anchor="w",
        command=on_settings_click
    )
    
    buttons.append(btn)
    btn.pack(side="top", fill="x", pady=(0, 5))
    
    return btn