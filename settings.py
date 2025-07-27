# 这是 settings.py (设置) 的代码
import customtkinter as ctk
from tkinter.messagebox import showinfo, showwarning
import os
from tkinter import filedialog

# 设置文本字典
text_title = {"Chinese": "设置", "English": "Settings"}
button_texts = {
    "Language": {"Chinese": "语言", "English": "Language"},
    "About": {"Chinese": "关于", "English": "About"},
    "GamePath": {"Chinese": "游戏路径", "English": "Game Path"},
    "Appearance": {"Chinese": "外观", "English": "Appearance"},
    "Updates": {"Chinese": "更新", "English": "Updates"},
    "Notifications": {"Chinese": "通知", "English": "Notifications"},
    "Privacy": {"Chinese": "隐私", "English": "Privacy"},
    "Advanced": {"Chinese": "高级设置", "English": "Advanced"}
}

text_language_finish_title = {"Chinese": "提示", "English": "Tip"}
text_language_finish_text = {"Chinese": "语言已修改，需要重启工具箱以生效。", "English": "The language has been modified and requires a restart of the kit to take effect."}
button_browse_text = {"Chinese": "更改", "English": "Change"}
window_file_title = {"Chinese": "选择游戏可执行文件","English": "Select Game Executable"}
type_game_path_exe = {"Chinese": "游戏路径", "English": "Game Path"}
type_game_path_all = {"Chinese": "所有文件", "English": "All File"}
button_test_text = {"Chinese": "测试路径", "English": "Test Path"}
text_ok_path_title = {"Chinese": "提示", "English": "Tip"}
text_ok_path_text = {"Chinese": "此路径有效。", "English": "This path is valid."}
text_none_path_title = {"Chinese": "警告", "English": "Warning"}
text_none_path_text = {"Chinese": "游戏路径未设置", "English": "Game path not set"}
text_no_path_title = {"Chinese": "警告", "English": "Warning"}
text_no_path_text = {"Chinese": "此路径无效。", "Engish": "This path is invalid."}

default_path = r"C:\Program Files\HoYoPlay\games\Genshin Impact game"

settings_list = list(button_texts.keys())

def create_frame(parent, dm, language):
    frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
    frame.pack_propagate(False)  # 防止内容改变框架大小
    
    # 创建页面容器 - 用于切换主页面和详情页
    pages_container = ctk.CTkFrame(frame, fg_color="transparent")
    pages_container.pack(fill="both", expand=True)
    
    # 存储页面容器和页面字典的引用
    frame.pages_container = pages_container
    frame.detail_pages = {}
    
    # 创建主页面
    main_page = create_main_page(pages_container, dm, language, frame)
    main_page.pack(fill="both", expand=True)
    
    # 创建详情页面
    for setting in settings_list:
        page = create_detail_page(pages_container, setting, dm, language, frame)
        frame.detail_pages[setting] = page
    
    # 存储主页面
    frame.main_page = main_page
    
    return frame

def create_main_page(parent, dm, language, frame_ref):
    frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
    
    # 标题框架
    title_frame = ctk.CTkFrame(frame, fg_color="transparent")
    title_frame.pack(side="top", fill="x", padx=20, pady=(20, 15))
    
    title_label = ctk.CTkLabel(
        title_frame,
        text=text_title[language],
        font=("Segoe UI", 24, "bold"),
        text_color="#6CBBE2",
    )
    title_label.pack(side="left")
    
    # 添加搜索区域
    search_frame = ctk.CTkFrame(frame, fg_color="transparent")
    search_frame.pack(side="top", fill="x", padx=20, pady=(0, 20))
    
    # 搜索框
    search_text = {"Chinese": "搜索设置...", "English": "Search settings..."}
    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text=search_text[language],
        height=40,
        corner_radius=8,
        border_width=1,
        border_color="#D1D5DB",
        fg_color="#F9FAFB"
    )
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    # 搜索按钮
    search_button_text = {"Chinese": "搜索", "English": "Search"}
    search_button = ctk.CTkButton(
        search_frame,
        text=search_button_text[language],
        width=100,
        height=40,
        fg_color="#4B5563",
        hover_color="#374151",
        corner_radius=8,
        font=("Segoe UI", 12, "bold")
    )
    search_button.pack(side="right")
    
    # 创建按钮容器 - 使用网格布局
    buttons_container = ctk.CTkFrame(frame, fg_color="transparent")
    buttons_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # 计算每行按钮数量（响应式布局）
    buttons_per_row = 4  # 默认每行4个按钮
    
    # 创建按钮
    buttons = []
    # 基础字体大小和最小字体大小
    base_font_size = 14
    min_font_size = 10
    
    for i, setting in enumerate(settings_list):
        row = i // buttons_per_row
        col = i % buttons_per_row
        
        # 创建按钮框架（包含按钮和间距）
        btn_frame = ctk.CTkFrame(buttons_container, fg_color="transparent")
        btn_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # 创建按钮 - 使用基础字体大小
        btn = ctk.CTkButton(
            btn_frame,
            text=button_texts[setting][language],
            height=80,  # 固定高度
            fg_color="#3B82F6",
            hover_color="#2563EB",
            corner_radius=10,
            font=("Segoe UI", base_font_size, "bold"),  # 初始字体大小
            anchor="center"
        )
        btn.pack(fill="both", expand=True)
        btn.setting = setting  # 存储设置项标识
        
        # 绑定按钮点击事件 - 切换到详情页
        btn.configure(command=lambda s=setting: show_detail_page(frame_ref, s))
        buttons.append(btn)
    
    # 确保网格布局均匀分布
    for i in range(buttons_per_row):
        buttons_container.grid_columnconfigure(i, weight=1)
    
    rows_needed = (len(settings_list) // buttons_per_row + 1)
    for i in range(rows_needed):
        buttons_container.grid_rowconfigure(i, weight=1)
    
    # 响应窗口大小变化
    def update_buttons(event=None):
        container_width = buttons_container.winfo_width()
        if container_width > 0:
            # 动态计算按钮宽度（占1/4宽度减去间距）
            btn_width = max(100, (container_width / buttons_per_row) - 20)
            
            # 根据按钮宽度动态调整字体大小
            # 基础宽度为150px时使用14px字体
            # 字体大小随宽度线性变化，但有最小限制
            font_size = max(
                min_font_size,
                int(base_font_size * (btn_width / 150))
            )
            for btn in buttons:
                # 更新按钮宽度
                btn.configure(width=btn_width)
                
                # 更新按钮字体大小
                current_font = btn.cget("font")
                new_font = (current_font[0], font_size, current_font[2])
                btn.configure(font=new_font)
    
    # 初始更新
    buttons_container.after(100, update_buttons)
    # 绑定尺寸变化事件
    buttons_container.bind("<Configure>", lambda e: update_buttons())
    
    # 添加搜索功能
    def perform_search():
        query = search_entry.get().lower()
        if not query:
            # 显示所有按钮
            for btn_frame in buttons_container.winfo_children():
                btn_frame.grid()
            return
        
        # 过滤按钮
        for btn in buttons:
            btn_text = btn.cget("text").lower()
            setting_name = button_texts[btn.setting]["English"].lower()
            
            # 检查是否匹配
            if query in btn_text or query in setting_name:
                btn.master.grid()  # 显示匹配项
            else:
                btn.master.grid_remove()  # 隐藏不匹配项
    
    # 绑定搜索按钮和回车键
    search_button.configure(command=perform_search)
    search_entry.bind("<Return>", lambda e: perform_search())
    
    return frame

def create_detail_page(parent, setting, dm, language, frame_ref):
    frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
    
    # 标题框架 - 包含返回按钮
    title_frame = ctk.CTkFrame(frame, fg_color="transparent")
    title_frame.pack(side="top", fill="x", padx=20, pady=(20, 15))
    
    # 返回按钮
    back_text = {"Chinese": "← 返回", "English": "← Back"}
    back_button = ctk.CTkButton(
        title_frame,
        text=back_text[language],
        font=("Segoe UI", 14),
        fg_color="transparent",
        hover_color="#F3F4F6",
        text_color="#3B82F6",
        width=80,
        height=30,
        anchor="w",
        command=lambda: show_main_page(frame_ref)
    )
    back_button.pack(side="left", padx=(0, 20))
    
    # 页面标题
    title_label = ctk.CTkLabel(
        title_frame,
        text=button_texts[setting][language],
        font=("Segoe UI", 24, "bold"),
        text_color="#6CBBE2",
    )
    title_label.pack(side="left")
    
    # 添加内容区域
    content_frame = ctk.CTkFrame(frame, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 根据设置项创建不同的内容
    if setting == "Language":
        create_language_page(content_frame, dm, language)
    elif setting == "GamePath":
        create_gamepath_page(content_frame, dm, language)
    elif setting == "Appearance":
        create_appearance_page(content_frame, dm, language)
    elif setting == "Updates":
        create_updates_page(content_frame, dm, language)
    elif setting == "Notifications":
        create_notifications_page(content_frame, dm, language)
    elif setting == "Privacy":
        create_privacy_page(content_frame, dm, language)
    elif setting == "Advanced":
        create_advanced_page(content_frame, dm, language)
    else:  # About
        create_about_page(content_frame, dm, language)
    
    return frame

def show_main_page(frame_ref):
    # 隐藏所有详情页
    for setting in settings_list:
        frame_ref.detail_pages[setting].pack_forget()
    
    # 显示主页面
    frame_ref.main_page.pack(fill="both", expand=True)

def show_detail_page(frame_ref, setting):
    # 隐藏主页面
    frame_ref.main_page.pack_forget()
    
    # 显示选中的详情页
    frame_ref.detail_pages[setting].pack(fill="both", expand=True)

# ====== 各个设置项的详情页面创建函数 ======

def create_language_page(parent, dm, language):
    content_frame = ctk.CTkFrame(parent, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 语言选择标签
    lang_text = {"Chinese": "选择工具箱语言：", "English": "Choose the language of the kit:"}
    lang_label = ctk.CTkLabel(
        content_frame,
        text=lang_text[language],
        font=("Segoe UI", 16),
        text_color="#4B5563"
    )
    lang_label.pack(side="top", anchor="w", pady=(0, 10))
    
    # 语言选择下拉框 - 设置为只读
    lang_var = ctk.StringVar(value=dm.get_config("Language", "English"))
    lang_combo = ctk.CTkComboBox(
        content_frame,
        values=["Chinese", "English"],
        variable=lang_var,
        width=200,
        height=40,
        font=("Segoe UI", 14),
        border_color="#3498db",
        button_color="#3498db",
        button_hover_color="#2980b9",
        fg_color="#FFFFFF",
        text_color="#2c3e50",
        dropdown_fg_color="#FFFFFF",
        dropdown_hover_color="#e3f2fd",
        state="readonly"  # 设置为只读模式
    )
    lang_combo.pack(side="top", anchor="w", pady=(0, 20))
    
    save_text = {"Chinese": "保存设置", "English": "Save Settings"}
    save_button = ctk.CTkButton(
        content_frame,
        text=save_text[language],
        command=lambda: save_language(dm, lang_var.get()),
        width=150,
        height=40,
        fg_color="#3B82F6",
        hover_color="#2563EB",
        font=("Segoe UI", 14, "bold")
    )
    save_button.pack(side="top", anchor="w", pady=20)
def save_language(dm, language):
    dm.set_config("Language", language)
    showinfo ( title=text_language_finish_title [ language ], message=text_language_finish_text [ language ] )

def create_gamepath_page(parent, dm, language):
    # 游戏路径设置页面
    content_frame = ctk.CTkFrame(parent, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 当前路径显示 - 使用只读文本框支持自动换行
    path_text = {"Chinese": "当前游戏路径:", "English": "Current game path:"}
    path_label = ctk.CTkLabel(
        content_frame,
        text=path_text[language],
        font=("Segoe UI", 14),
        text_color="#4B5563",
        anchor="w"
    )
    path_label.pack(side="top", fill="x", pady=(0, 5))
    
    # 创建只读文本框来显示路径
    current_path = dm.get_config("GamePath", "")
    path_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    path_frame.pack(side="top", fill="x", pady=(0, 20))
    
    # 滚动文本框
    path_textbox = ctk.CTkTextbox(
        path_frame,
        height=60,  # 固定高度
        wrap="word",  # 自动换行
        font=("Segoe UI", 12),
        fg_color="#F9FAFB",
        border_color="#D1D5DB",
        border_width=1,
        corner_radius=4
    )
    path_textbox.pack(side="left", fill="x", expand=True)
    path_textbox.insert("1.0", current_path if current_path else "未设置")
    path_textbox.configure(state="disabled")  # 设置为只读
    
    # 存储文本框引用以便更新
    path_frame.path_textbox = path_textbox
    
    # 直接使用字典获取文本
    browse_button = ctk.CTkButton(
        content_frame,
        text=button_browse_text[language],
        width=120,
        height=40,
        command=lambda: browse_game_path(dm, path_frame, language),
        font=("Segoe UI", 14)
    )
    browse_button.pack(side="top", anchor="w", pady=10)
    
    test_button = ctk.CTkButton(
        content_frame,
        text=button_test_text[language],
        width=120,
        height=40,
        command=lambda: test_game_path(dm, language),
        font=("Segoe UI", 14)
    )
    test_button.pack(side="top", anchor="w", pady=10)

def browse_game_path(dm, path_frame, language):
    initialdir = default_path if os.path.exists(default_path) else None
    
    selected_file = filedialog.askopenfilename(
        title=window_file_title[language],
        filetypes=[(type_game_path_exe [ language ], "*.exe"), (type_game_path_all [ language ], "*.*")],
        initialdir=initialdir
    )
    
    if selected_file and selected_file.lower().endswith('.exe'):
        normalized_path = os.path.normpath(selected_file)
        
        dm.set_config("GamePath", normalized_path)
        
        path_frame.path_textbox.configure(state="normal")  # 启用编辑以更新内容
        path_frame.path_textbox.delete("1.0", "end")  # 清空内容
        path_frame.path_textbox.insert("1.0", normalized_path)  # 插入新路径
        path_frame.path_textbox.configure(state="disabled")  # 恢复只读状态
    else:
        # 如果用户取消选择或选择了无效文件
        warning_title = {"Chinese": "警告", "English": "Warning"}
        warning_message = {
            "Chinese": "未选择有效的游戏可执行文件(.exe)",
            "English": "No valid game executable (.exe) selected"
        }
        showwarning(
            title=warning_title[language],
            message=warning_message[language]
        )

def test_game_path(dm, language):
    path = dm.get_config("GamePath", "")
    if path:
        if os.path.exists(path):
            showinfo( title=text_ok_path_title[language], message=text_ok_path_text[language] )
        else:
            showwarning( title=text_no_path_title[language], message=text_no_path_text[language] )
    else:
        showwarning ( title=text_none_path_title [ language ], message=text_none_path_text [ language ] )
        

# 其他设置项页面的创建函数（占位）
def create_appearance_page(parent, dm, language):
    content_frame = ctk.CTkFrame(parent, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 外观设置内容
    text = {"Chinese": "外观设置", "English": "Appearance Settings"}
    label = ctk.CTkLabel(
        content_frame,
        text=text[language],
        font=("Segoe UI", 24),
        text_color="#6CBBE2"
    )
    label.pack(pady=50)

def create_updates_page(parent, dm, language):
    content_frame = ctk.CTkFrame(parent, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 更新设置内容
    text = {"Chinese": "更新设置", "English": "Update Settings"}
    label = ctk.CTkLabel(
        content_frame,
        text=text[language],
        font=("Segoe UI", 24),
        text_color="#6CBBE2"
    )
    label.pack(pady=50)

def create_notifications_page(parent, dm, language):
    content_frame = ctk.CTkFrame(parent, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 通知设置内容
    text = {"Chinese": "通知设置", "English": "Notification Settings"}
    label = ctk.CTkLabel(
        content_frame,
        text=text[language],
        font=("Segoe UI", 24),
        text_color="#6CBBE2"
    )
    label.pack(pady=50)

def create_privacy_page(parent, dm, language):
    content_frame = ctk.CTkFrame(parent, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 隐私设置内容
    text = {"Chinese": "隐私设置", "English": "Privacy Settings"}
    label = ctk.CTkLabel(
        content_frame,
        text=text[language],
        font=("Segoe UI", 24),
        text_color="#6CBBE2"
    )
    label.pack(pady=50)

def create_advanced_page(parent, dm, language):
    content_frame = ctk.CTkFrame(parent, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 高级设置内容
    text = {"Chinese": "高级设置", "English": "Advanced Settings"}
    label = ctk.CTkLabel(
        content_frame,
        text=text[language],
        font=("Segoe UI", 24),
        text_color="#6CBBE2"
    )
    label.pack(pady=50)

def create_about_page(parent, dm, language):
    content_frame = ctk.CTkFrame(parent, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 关于页面内容
    text = {"Chinese": "关于芙宁娜工具箱", "English": "About Furina Kit"}
    label = ctk.CTkLabel(
        content_frame,
        text=text[language],
        font=("Segoe UI", 24, "bold"),
        text_color="#6CBBE2"
    )
    label.pack(pady=20)
    
    # 版本信息
    version_text = {"Chinese": "版本: 1.0.0", "English": "Version: 1.0.0"}
    version_label = ctk.CTkLabel(
        content_frame,
        text=version_text[language],
        font=("Segoe UI", 16),
        text_color="#4B5563"
    )
    version_label.pack(pady=10)
    
    # 版权信息
    copyright_text = {
        "Chinese": "© 2023 芙宁娜工具箱 - 保留所有权利",
        "English": "© 2023 Furina Kit - All Rights Reserved"
    }
    copyright_label = ctk.CTkLabel(
        content_frame,
        text=copyright_text[language],
        font=("Segoe UI", 14),
        text_color="#6B7280"
    )
    copyright_label.pack(pady=20)
    
    # 开发者信息
    developer_text = {"Chinese": "开发者: Your Name", "English": "Developer: Your Name"}
    developer_label = ctk.CTkLabel(
        content_frame,
        text=developer_text[language],
        font=("Segoe UI", 14),
        text_color="#3B82F6"
    )
    developer_label.pack(pady=10)