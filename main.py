# 这是 main.py (主页) 的代码
import customtkinter as ctk
import json
from data_manager import DataManager

def load_language_texts():
    """从当前目录的language.json加载多语言文本"""
    try:
        with open('language.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # 如果文件不存在或读取失败，返回默认文本
        return {
            "window_title": {"Chinese": "芙宁娜工具箱", "English": "Furina Toolbox"},
            "sidebar_title": {"Chinese": "芙宁娜工具箱", "English": "Furina Toolbox"},
            "login": {"Chinese": "登录", "English": "Login"},
            "main": {"Chinese": "主页", "English": "Main"},
            "start_game": {"Chinese": "启动游戏", "English": "Start Game"},
            "translate": {"Chinese": "翻译", "English": "Translate"},
            "settings": {"Chinese": "设置", "English": "Settings"},
            "welcome": {"Chinese": "欢迎使用 Furina Toolbox", "English": "Welcome to Furina Toolbox"},
            "description": {"Chinese": "请从左侧菜单中选择功能", "English": "Select a function from the sidebar"}
        }

def create_main_frame(parent, dm):
    frame = ctk.CTkFrame(parent)
    frame.configure(fg_color="#FFFFFF")
    frame.pack(fill="both", expand=True)
    
    # 获取语言设置
    language = dm.get_config("Language", "English")
    texts = load_language_texts()
    
    # 添加欢迎内容
    welcome_frame = ctk.CTkFrame(frame, fg_color="transparent")
    welcome_frame.place(relx=0.5, rely=0.4, anchor="center")
    
    # 添加应用图标
    app_icon = ctk.CTkLabel(
        welcome_frame,
        text="🎮",
        font=("Segoe UI", 64),
        text_color="#3B82F6",
    )
    app_icon.pack(side="top", pady=(0, 20))
    
    welcome_label = ctk.CTkLabel(
        welcome_frame,
        text=texts["welcome"].get(language, texts["welcome"]["English"]),
        font=("Segoe UI", 24, "bold"),
        text_color="#1E3A8A",
    )
    welcome_label.pack(side="top", pady=(0, 10))
    
    description_label = ctk.CTkLabel(
        welcome_frame,
        text=texts["description"].get(language, texts["description"]["English"]),
        font=("Segoe UI", 14),
        text_color="#4B5563",
    )
    description_label.pack(side="top")
    
    return frame