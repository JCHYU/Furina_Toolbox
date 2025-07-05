# 这是 start.py (启动游戏) 的代码
import customtkinter as ctk
from data_manager import DataManager

def create_start_frame(parent, dm, language):
    """创建启动游戏页面框架"""
    frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
    
    # 添加一个标志，表示这是启动游戏页面
    frame.is_start_frame = True
    
    # 添加启动游戏标题
    title_frame = ctk.CTkFrame(frame, fg_color="transparent")
    title_frame.pack(side="top", fill="x", padx=20, pady=(20, 15))
    
    title_label = ctk.CTkLabel(
        title_frame,
        text="启动游戏" if language == "Chinese" else "Start Game",
        font=("Segoe UI", 24, "bold"),
        text_color="#1E3A8A",  # 深蓝色
    )
    title_label.pack(side="left")
    
    # 添加游戏选择区域
    game_select_frame = ctk.CTkFrame(frame, fg_color="transparent")
    game_select_frame.pack(side="top", fill="x", padx=20, pady=10)
    
    game_label = ctk.CTkLabel(
        game_select_frame,
        text="选择游戏:" if language == "Chinese" else "Select Game:",
        font=("Segoe UI", 14),
        text_color="#1E3A8A",  # 深蓝色
    )
    game_label.pack(side="left", padx=(0, 10))
    
    game_options = ["原神", "崩坏：星穹铁道"] if language == "Chinese" else ["Genshin Impact", "Honkai: Star Rail"]
    game_combobox = ctk.CTkComboBox(
        game_select_frame,
        values=game_options,
        font=("Segoe UI", 14),
        dropdown_font=("Segoe UI", 14),
        width=200
    )
    game_combobox.pack(side="left")
    game_combobox.set(game_options[0])
    
    # 添加账号选择区域
    account_frame = ctk.CTkFrame(frame, fg_color="transparent")
    account_frame.pack(side="top", fill="x", padx=20, pady=10)
    
    account_label = ctk.CTkLabel(
        account_frame,
        text="选择账号:" if language == "Chinese" else "Select Account:",
        font=("Segoe UI", 14),
        text_color="#1E3A8A",  # 深蓝色
    )
    account_label.pack(side="left", padx=(0, 10))
    
    account_options = ["账号1", "账号2", "账号3"] if language == "Chinese" else ["Account 1", "Account 2", "Account 3"]
    account_combobox = ctk.CTkComboBox(
        account_frame,
        values=account_options,
        font=("Segoe UI", 14),
        dropdown_font=("Segoe UI", 14),
        width=200
    )
    account_combobox.pack(side="left")
    account_combobox.set(account_options[0])
    
    # 添加启动按钮
    button_frame = ctk.CTkFrame(frame, fg_color="transparent")
    button_frame.pack(side="top", fill="x", padx=20, pady=30)
    
    start_button = ctk.CTkButton(
        button_frame,
        text="启动游戏" if language == "Chinese" else "Start Game",
        font=("Segoe UI", 16, "bold"),
        fg_color="#3B82F6",  # 蓝色
        hover_color="#2563EB",  # 深蓝色
        text_color="#FFFFFF",  # 白色
        height=50,
        width=200,
        corner_radius=8
    )
    start_button.pack()
    
    # 添加状态区域
    status_frame = ctk.CTkFrame(frame, fg_color="transparent")
    status_frame.pack(side="top", fill="x", padx=20, pady=20)
    
    status_label = ctk.CTkLabel(
        status_frame,
        text="状态: 就绪" if language == "Chinese" else "Status: Ready",
        font=("Segoe UI", 14),
        text_color="#4B5563",  # 灰色
    )
    status_label.pack(side="left")
    
    return frame