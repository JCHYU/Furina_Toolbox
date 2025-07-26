# 这是 click.py (连点器) 的代码
import customtkinter as ctk
from data_manager import DataManager

def create_frame(parent, dm):
    """创建连点器页面"""
    frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
    
    # 添加标题
    text_title = {"Chinese": "连点器", "English": "Continuous Clicker"}
    language = dm.get_config("Language", "English")
    title = ctk.CTkLabel(
        frame,
        text=text_title.get(language, "Continuous Clicker"),
        font=("Segoe UI", 24, "bold"),
        text_color="#6CBBE2"
    )
    title.pack(side="left")
    
    return frame