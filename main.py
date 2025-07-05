# 这是 main.py (主页) 的代码
import customtkinter as ctk
from data_manager import DataManager

def create_main_frame(parent, dm):
    frame = ctk.CTkFrame(parent)
    frame.configure(fg_color="#FFFFFF")
    frame.pack(fill="both", expand=True)
    
    language = dm.get_config("Language", "English")
    
    # 添加欢迎内容
    welcome_frame = ctk.CTkFrame(frame, fg_color="transparent")
    welcome_frame.place(relx=0.5, rely=0.4, anchor="center")
    
    # 添加应用图标
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