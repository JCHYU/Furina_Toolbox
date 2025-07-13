# 这是 main.py (主页) 的代码
import customtkinter as ctk
from data_manager import DataManager

def create_main_frame(parent, dm):
    frame = ctk.CTkFrame(parent)
    frame.configure(fg_color="#FFFFFF")
    frame.pack(fill="both", expand=True)
    
    language = dm.get_config("Language", "English")
    
    # 获取已启动天数
    time_count = dm.get_config("Time", 0)
    
    # 添加欢迎内容
    welcome_frame = ctk.CTkFrame(frame, fg_color="transparent")
    welcome_frame.place(relx=0.5, rely=0.4, anchor="center")
    
    # 欢迎标签
    welcome_label = ctk.CTkLabel(
        welcome_frame,
        text="芙宁娜已经陪伴你了" if language == "Chinese" else "Furina has been with you for",
        font=("Segoe UI", 24, "bold"),
        text_color="#6CBBE2", 
    )
    welcome_label.pack(side="top", pady=(0, 10))
    
    # 天数显示
    days_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
    days_frame.pack(side="top", pady=(0, 10))
    
    days_label = ctk.CTkLabel(
        days_frame,
        text=str(time_count),
        font=("Segoe UI", 36, "bold"),
        text_color="#3B82F6",  # 蓝色
    )
    days_label.pack(side="left", padx=5)
    
    days_text = ctk.CTkLabel(
        days_frame,
        text="天" if language == "Chinese" else "days",
        font=("Segoe UI", 24, "bold"),
        text_color="#1E3A8A",  # 深蓝色
    )
    days_text.pack(side="left", padx=5)
    
    # 描述文本
    description_text = "请从左侧菜单中选择功能" if language == "Chinese" else "Select a function from the sidebar"
    description_label = ctk.CTkLabel(
        welcome_frame,
        text=description_text,
        font=("Segoe UI", 14),
        text_color="#4B5563",  # 灰色
    )
    description_label.pack(side="top")
    
    return frame