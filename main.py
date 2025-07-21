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
        #text= if language == "Chinese" else "Furina has been with you for",
        text="芙宁娜已经陪伴你了" + str ( time_count ) + "天",
        font=("Segoe UI", 24, "bold"),
        text_color="#6CBBE2", 
    )
    welcome_label.pack(side="top", pady=(0, 10))

    
    return frame