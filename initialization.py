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

class InitializationFrame(ctk.CTkFrame):
    """初始化界面框架"""
    def __init__(self, parent, dm, on_complete_callback):
        super().__init__(parent)
        self.parent = parent
        self.top_level = parent.winfo_toplevel()  # 保存顶层窗口引用
        self.dm = dm
        self.on_complete_callback = on_complete_callback
        self.selected_language = None
        self.selected_path = None
        
        # 框架设置
        self.pack(fill="both", expand=True)
        self.configure(fg_color="#E6F2FF")
        
        # 创建容器
        self.language_container = ctk.CTkFrame(self, fg_color="transparent")
        self.path_container = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_container = ctk.CTkFrame(self, fg_color="transparent")
        
        # 创建初始界面
        self.create_language_selection()
        
    def create_language_selection(self):
        """创建语言选择界面"""
        self.language_container.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # 欢迎标签
        ctk.CTkLabel(
            self.language_container,
            text="Welcome to Furina Toolbox!",
            font=("Arial", 24, "bold"),
            text_color="#1a56db"
        ).place(relx=0.5, rely=0.1, anchor="center")
        
        # 标题标签
        ctk.CTkLabel(
            self.language_container,
            text="Set language first.\nOK?",
            font=("楷体", 30, "bold"),
            text_color="#1a56db",
            corner_radius=10,
            padx=20,
            pady=10
        ).place(relx=0.5, rely=0.25, anchor="center")
        
        # 中文选项
        chinese_frame = ctk.CTkFrame(
            self.language_container, 
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
        
        chinese_frame.bind("<Button-1>", lambda e: self.select_language("Chinese"))
        chinese_label.bind("<Button-1>", lambda e: self.select_language("Chinese"))
        
        # 英语选项
        english_frame = ctk.CTkFrame(
            self.language_container, 
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
        
        english_frame.bind("<Button-1>", lambda e: self.select_language("English"))
        english_label.bind("<Button-1>", lambda e: self.select_language("English"))
        
        # 初始化状态标签
        self.status_label = ctk.CTkLabel(
            self.progress_container,
            text="正在初始化...",
            font=("微软雅黑", 14),
            text_color="#4b5563",
            justify="center"
        )
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def create_path_selection(self):
        """创建路径选择界面"""
        self.path_container.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # 路径标题
        self.path_title_label = ctk.CTkLabel(
            self.path_container,
            text=gamepath_Tip [ language ],
            font=("楷体", 24, "bold") if self.selected_language == "Chinese" else ("Arial", 24, "bold"),
            text_color="#1a56db"
        )
        self.path_title_label.place(relx=0.5, rely=0.15, anchor="center")
        
        # 路径框架
        path_frame = ctk.CTkFrame(self.path_container, fg_color="transparent", height=50)
        path_frame.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8)
        
        # 路径输入框
        self.path_entry = ctk.CTkEntry(
            path_frame,
            placeholder_text="",
            width=400,
            height=40,
            corner_radius=10,
            fg_color="#F0F0F0",
            text_color="#1a56db",
            font=("微软雅黑", 12) if self.selected_language == "Chinese" else ("Arial", 12),
            state="readonly"
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # 浏览按钮
        self.browse_btn = ctk.CTkButton(
            path_frame,
            text=browse_Text [ language ],
            width=100,
            height=40,
            corner_radius=10,
            fg_color="#E6F2FF",
            hover_color="#C4D9F0",
            text_color="#1a56db",
            font=("微软雅黑", 12) if self.selected_language == "Chinese" else ("Arial", 12),
            command=self.browse_directory
        )
        self.browse_btn.pack(side="right")
        
        # 按钮容器
        button_container = ctk.CTkFrame(self.path_container, fg_color="transparent")
        button_container.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.6)
        
        # 确认按钮
        self.confirm_btn = ctk.CTkButton(
            button_container,
            text=ok_Text [ language ],
            width=200,  # 设置最小宽度为200像素
            height=50,
            corner_radius=10,
            fg_color="#E6F2FF",
            hover_color="#C4D9F0",
            text_color="#1a56db",
            font=("微软雅黑", 14) if self.selected_language == "Chinese" else ("Arial", 14),
            command=self.confirm_path
        )
        self.confirm_btn.pack(side="left", padx=(0, 20), expand=True)
        
        # 跳过按钮 - 添加了相同的宽度设置
        self.skip_btn = ctk.CTkButton(
            button_container,
            text=skip_Text [ language ],
            width=200,  # 添加宽度设置，与确认按钮保持一致
            height=50,
            corner_radius=10,
            fg_color="#F0F0F0",
            hover_color="#D0D0D0",
            text_color="#4b5563",
            font=("微软雅黑", 14) if self.selected_language == "Chinese" else ("Arial", 14),
            command=self.skip_path
        )
        self.skip_btn.pack(side="right", expand=True)
        
        # 返回按钮
        self.back_btn = ctk.CTkButton(
            self.path_container,
            text="←返回" if self.selected_language == "Chinese" else "←Back",
            width=100,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#D0E0F0",
            text_color="#1a56db",
            font=("微软雅黑", 10) if self.selected_language == "Chinese" else ("Arial", 10),
            command=self.back_to_language
        )
        self.back_btn.place(relx=0.05, rely=0.05, anchor="nw")

    def browse_directory(self):
        """浏览文件选择游戏路径"""
        file_types = [("游戏路径", "*.exe"), ("所有文件", "*.*")]
        default_path = r"C:\Program Files\HoYoPlay\games\Genshin Impact game"
        initialdir = default_path if os.path.exists(default_path) else None
        
        title = "选择游戏可执行文件" if self.selected_language == "Chinese" else "Select Game Executable"
        selected_file = filedialog.askopenfilename(title=title, filetypes=file_types, initialdir=initialdir)
        
        if selected_file and selected_file.lower().endswith('.exe'):
            normalized_path = os.path.normpath(selected_file)
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, normalized_path)
            self.path_entry.configure(state="readonly")
    
    def skip_path(self):
        """跳过路径选择步骤"""
        self.selected_path = ""  # 设置为空路径
        
        # 切换到进度界面
        self.path_container.place_forget()
        self.progress_container.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # 初始化提示
        self.status_label.configure(text=init_Text [ language ] )
        
        # 开始初始化过程
        run_initialization(self.top_level, self.dm, self.on_complete_callback, self.selected_language, self.selected_path)
    
    def confirm_path(self):
        """确认选择的路径"""
        self.selected_path = self.path_entry.get().strip()
        if not self.selected_path:
            if self.selected_language == "Chinese":
                showerror("错误", "请选择游戏可执行文件。")
            else:
                showerror("Error", "Please select game executable file.")
            return
        
        # 切换到进度界面
        self.path_container.place_forget()
        self.progress_container.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # 更新状态文本
        if self.selected_language == "Chinese":
            self.status_label.configure(text="正在初始化应用程序，请稍候...")
        else:
            self.status_label.configure(text="Initializing application, please wait...")
        
        # 开始初始化过程
        run_initialization(self.top_level, self.dm, self.on_complete_callback, self.selected_language, self.selected_path)
    
    def back_to_language(self):
        """返回语言选择界面"""
        self.path_container.place_forget()
        self.language_container.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    def select_language(self, language):
        """选择语言并切换到路径选择界面"""
        self.selected_language = language
        self.language_container.place_forget()
        self.create_path_selection()
        self.path_container.place(relx=0, rely=0, relwidth=1, relheight=1)