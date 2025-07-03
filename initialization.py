# 这是 initialization.py (初始化页面) 的代码
import threading
from data_manager import DataManager
import customtkinter as ctk
from tkinter.messagebox import showerror, showinfo
import os
from tkinter import filedialog
import sys

# 路径配置
data = os.path.join(os.getenv('LOCALAPPDATA'), "FurinaTB")
dm = DataManager()
dm.load(data)

# 获取语言配置
language = dm.get_config("Language", "English")

# 完成消息配置
gamepath_Tip = {"Chinese": "选择游戏路径(GenshinImpact.exe,而不是启动器)", 
                 "English": "Select game path (GenshinImpact.exe, not launcher)"}
ok_Text = {"Chinese": "确认", 
           "English": "Confirm"}
browse_Text = {"Chinese": "浏览", 
               "English": "Browse"}
skip_Text = {"Chinese": "跳过",
             "English": "Skip"}
done_Title = {"Chinese": "完成", "English": "Finish"}
done_Text = {"Chinese": "初始化操作顺利完成，即将退出应用程序。如需使用，请重新启动它。", 
             "English": "The initialization operation has been successfully completed and the application is about to exit. If needed, please start it."}
init_Text = {"Chinese": "正在初始化应用程序，请稍候...", "English": "Initializing application, please wait..."}

def done():
    """退出应用程序"""
    sys.exit(0)

def run_initialization(top_level, dm, on_complete_callback, language, install_path):
    """启动初始化线程"""
    threading.Thread(
        target=initialization_process, 
        args=(top_level, dm, on_complete_callback, language, install_path),
        daemon=True
    ).start()

def initialization_process(top_level, dm, on_complete_callback, language, install_path):
    """初始化过程主函数"""
    try:
        # 设置语言和安装路径
        dm.set_config('Language', language)
        dm.set_config('GamePath', install_path)
        dm.set_config('Initialization', True)
        
        # 获取当前语言设置
        current_language = dm.get_config('Language', 'English')
        
        # 在主线程中显示完成消息
        top_level.after(0, lambda: show_done_message(top_level, current_language))
        
    except Exception as e:
        # 显示错误信息
        top_level.after(0, lambda: showerror("We are Sorry.", f"This is the error code: {str(e)}\nYou can tell the developer."))

def show_done_message(top_level, current_language):
    """显示完成消息并退出程序"""
    showinfo(
        title=done_Title.get(current_language, "Finish"),
        message=done_Text.get(current_language, "Initialization completed successfully."),
        parent=top_level
    )
    # 延迟1秒后退出
    top_level.after(1000, done)

def create_initialization_frame(parent, dm, on_complete_callback):
    """创建初始化界面框架的函数式实现"""
    # 创建主框架
    frame = ctk.CTkFrame(parent)
    frame.configure(fg_color="#E6F2FF")
    frame.pack(fill="both", expand=True)
    
    # 获取顶层窗口
    top_level = parent.winfo_toplevel()
    
    # 状态变量
    selected_language = None
    selected_path = None
    
    # 创建容器
    language_container = ctk.CTkFrame(frame, fg_color="transparent")
    path_container = ctk.CTkFrame(frame, fg_color="transparent")
    progress_container = ctk.CTkFrame(frame, fg_color="transparent")
    
    # 创建语言选择界面并获取控件字典
    language_controls = create_language_selection(
        language_container, 
        path_container, 
        progress_container, 
        top_level, 
        dm, 
        on_complete_callback, 
        selected_language, 
        selected_path
    )
    
    # 保存状态标签引用
    status_label = language_controls["status_label"]
    
    language_container.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # 返回框架和状态标签
    return frame, status_label

def create_language_selection(language_container, path_container, progress_container, top_level, dm, on_complete_callback, selected_language, selected_path):
    """创建语言选择界面"""
    # 欢迎标签
    ctk.CTkLabel(
        language_container,
        text="Welcome to Furina Toolbox!",
        font=("Arial", 24, "bold"),
        text_color="#1a56db"
    ).place(relx=0.5, rely=0.1, anchor="center")
    
    # 标题标签
    ctk.CTkLabel(
        language_container,
        text="Set language first.\nOK?",
        font=("楷体", 30, "bold"),
        text_color="#1a56db",
        corner_radius=10,
        padx=20,
        pady=10
    ).place(relx=0.5, rely=0.25, anchor="center")
    
    # 中文选项
    chinese_frame = ctk.CTkFrame(
        language_container, 
        width=300, 
        height=60, 
        corner_radius=10, 
        fg_color="#FFFFFF",
        border_width=2, 
        border_color="#1a56db"
    )
    chinese_frame.place(relx=0.5, rely=0.45, anchor="center")
    
    chinese_label = ctk.CTkLabel(
        chinese_frame,
        text="简体中文",
        font=("微软雅黑", 16),
        text_color="#1a56db"
    )
    chinese_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # 绑定事件时传递状态标签
    chinese_frame.bind("<Button-1>", lambda e: select_language(
        "Chinese", 
        language_container, 
        path_container, 
        progress_container, 
        top_level, 
        dm, 
        on_complete_callback, 
        selected_language, 
        selected_path,
        status_label  # 添加状态标签参数
    ))
    
    chinese_label.bind("<Button-1>", lambda e: select_language(
        "Chinese", 
        language_container, 
        path_container, 
        progress_container, 
        top_level, 
        dm, 
        on_complete_callback, 
        selected_language, 
        selected_path,
        status_label  # 添加状态标签参数
    ))
    
    # 英语选项
    english_frame = ctk.CTkFrame(
        language_container, 
        width=300, 
        height=60, 
        corner_radius=10, 
        fg_color="#FFFFFF",
        border_width=2, 
        border_color="#1a56db"
    )
    english_frame.place(relx=0.5, rely=0.60, anchor="center")
    
    english_label = ctk.CTkLabel(
        english_frame,
        text="English",
        font=("Arial", 16, "bold"),
        text_color="#1a56db"
    )
    english_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # 绑定事件时传递状态标签
    english_frame.bind("<Button-1>", lambda e: select_language(
        "English", 
        language_container, 
        path_container, 
        progress_container, 
        top_level, 
        dm, 
        on_complete_callback, 
        selected_language, 
        selected_path,
        status_label  # 添加状态标签参数
    ))
    
    english_label.bind("<Button-1>", lambda e: select_language(
        "English", 
        language_container, 
        path_container, 
        progress_container, 
        top_level, 
        dm, 
        on_complete_callback, 
        selected_language, 
        selected_path,
        status_label  # 添加状态标签参数
    ))
    
    # 初始化状态标签
    status_label = ctk.CTkLabel(
        progress_container,
        text="正在初始化...",
        font=("微软雅黑", 14),
        text_color="#4b5563",
        justify="center"
    )
    status_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # 返回所有创建的控件，以便后续操作
    return {
        "status_label": status_label,
        "language_container": language_container,
        "path_container": path_container,
        "progress_container": progress_container
    }

def create_path_selection(path_container, selected_language, language_container, progress_container, top_level, dm, on_complete_callback, selected_path, status_label):
    """创建路径选择界面"""
    # 路径标题
    path_title_label = ctk.CTkLabel(
        path_container,
        text=gamepath_Tip.get(selected_language, gamepath_Tip["English"]),
        font=("楷体", 24, "bold") if selected_language == "Chinese" else ("Arial", 24, "bold"),
        text_color="#1a56db"
    )
    path_title_label.place(relx=0.5, rely=0.15, anchor="center")
    
    # 路径框架
    path_frame = ctk.CTkFrame(path_container, fg_color="transparent", height=50)
    path_frame.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8)
    
    # 路径输入框
    path_entry = ctk.CTkEntry(
        path_frame,
        placeholder_text="",
        width=400,
        height=40,
        corner_radius=10,
        fg_color="#F0F0F0",
        text_color="#1a56db",
        font=("微软雅黑", 12) if selected_language == "Chinese" else ("Arial", 12),
        state="readonly"
    )
    path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    # 浏览按钮
    browse_btn = ctk.CTkButton(
        path_frame,
        text=browse_Text.get(selected_language, browse_Text["English"]),
        width=100,
        height=40,
        corner_radius=10,
        fg_color="#E6F2FF",
        hover_color="#C4D9F0",
        text_color="#1a56db",
        font=("微软雅黑", 12) if selected_language == "Chinese" else ("Arial", 12),
        command=lambda: browse_directory(path_entry, selected_language)
    )
    browse_btn.pack(side="right")
    
    # 按钮容器
    button_container = ctk.CTkFrame(path_container, fg_color="transparent")
    button_container.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.6)
    
    # 确认按钮
    confirm_btn = ctk.CTkButton(
        button_container,
        text=ok_Text.get(selected_language, ok_Text["English"]),
        width=200,
        height=50,
        corner_radius=10,
        fg_color="#E6F2FF",
        hover_color="#C4D9F0",
        text_color="#1a56db",
        font=("微软雅黑", 14) if selected_language == "Chinese" else ("Arial", 14),
        command=lambda: confirm_path(path_entry, selected_language, language_container, path_container, progress_container, top_level, dm, on_complete_callback, selected_path, status_label)
    )
    confirm_btn.pack(side="left", padx=(0, 20), expand=True)
    
    # 跳过按钮
    skip_btn = ctk.CTkButton(
        button_container,
        text=skip_Text.get(selected_language, skip_Text["English"]),
        width=200,
        height=50,
        corner_radius=10,
        fg_color="#F0F0F0",
        hover_color="#D0D0D0",
        text_color="#4b5563",
        font=("微软雅黑", 14) if selected_language == "Chinese" else ("Arial", 14),
        command=lambda: skip_path(selected_language, language_container, path_container, progress_container, top_level, dm, on_complete_callback, selected_path, status_label)
    )
    skip_btn.pack(side="right", expand=True)
    
    # 返回按钮
    back_btn = ctk.CTkButton(
        path_container,
        text="←返回" if selected_language == "Chinese" else "←Back",
        width=100,
        height=30,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#D0E0F0",
        text_color="#1a56db",
        font=("微软雅黑", 10) if selected_language == "Chinese" else ("Arial", 10),
        command=lambda: back_to_language(language_container, path_container)
    )
    back_btn.place(relx=0.05, rely=0.05, anchor="nw")
    
    # 返回创建的控件
    return {
        "path_title_label": path_title_label,
        "path_entry": path_entry,
        "browse_btn": browse_btn,
        "confirm_btn": confirm_btn,
        "skip_btn": skip_btn,
        "back_btn": back_btn
    }

def browse_directory(path_entry, selected_language):
    """浏览文件选择游戏路径"""
    file_types = [("游戏路径", "*.exe"), ("所有文件", "*.*")]
    default_path = r"C:\Program Files\HoYoPlay\games\Genshin Impact game"
    initialdir = default_path if os.path.exists(default_path) else None
    
    title = "选择游戏可执行文件" if selected_language == "Chinese" else "Select Game Executable"
    selected_file = filedialog.askopenfilename(title=title, filetypes=file_types, initialdir=initialdir)
    
    if selected_file and selected_file.lower().endswith('.exe'):
        normalized_path = os.path.normpath(selected_file)
        path_entry.configure(state="normal")
        path_entry.delete(0, "end")
        path_entry.insert(0, normalized_path)
        path_entry.configure(state="readonly")

def skip_path(selected_language, language_container, path_container, progress_container, top_level, dm, on_complete_callback, selected_path, status_label):
    """跳过路径选择步骤"""
    selected_path = ""  # 设置为空路径
    
    # 切换到进度界面
    path_container.place_forget()
    progress_container.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # 初始化提示
    status_label.configure(text=init_Text.get(selected_language, init_Text["English"]))
    
    # 开始初始化过程
    run_initialization(top_level, dm, on_complete_callback, selected_language, selected_path)

def confirm_path(path_entry, selected_language, language_container, path_container, progress_container, top_level, dm, on_complete_callback, selected_path, status_label):
    """确认选择的路径"""
    selected_path = path_entry.get().strip()
    if not selected_path:
        if selected_language == "Chinese":
            showerror("错误", "请选择游戏可执行文件。")
        else:
            showerror("Error", "Please select game executable file.")
        return
    
    # 切换到进度界面
    path_container.place_forget()
    progress_container.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # 更新状态文本
    if selected_language == "Chinese":
        status_label.configure(text="正在初始化应用程序，请稍候...")
    else:
        status_label.configure(text="Initializing application, please wait...")
    
    # 开始初始化过程
    run_initialization(top_level, dm, on_complete_callback, selected_language, selected_path)

def back_to_language(language_container, path_container):
    """返回语言选择界面"""
    path_container.place_forget()
    language_container.place(relx=0, rely=0, relwidth=1, relheight=1)

def select_language(language, language_container, path_container, progress_container, top_level, dm, on_complete_callback, selected_language, selected_path, status_label):
    """选择语言并切换到路径选择界面"""
    selected_language = language
    language_container.place_forget()
    
    # 创建路径选择界面
    create_path_selection(path_container, selected_language, language_container, progress_container, top_level, dm, on_complete_callback, selected_path, status_label)
    path_container.place(relx=0, rely=0, relwidth=1, relheight=1)