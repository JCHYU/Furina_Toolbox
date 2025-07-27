# 这是 start.py (启动游戏) 的代码
import customtkinter as ctk
from tkinter.messagebox import askyesno, showerror
from tkinter import filedialog
from subprocess import Popen, CREATE_NEW_PROCESS_GROUP
from sys import platform
import ctypes
import os
import psutil  # 用于检查进程是否存在

text_title = {"Chinese": "启动游戏", "English": "Start Game"}
button_start_text = {"Chinese": "原神，启动！", "English": "Boot Up Genshin Impact!"}
button_running_text = {"Chinese": "游戏运行中", "English": "Game is Running"}
text_gamepath_tip_title = {"Chinese": "提示", "English": "Tip"}
text_gamepath_tip_text = {"Chinese": "您没有设置游戏路径，是否立即设置？", "English": "You haven't set the game path, do you want to set it now?"}
window_file_title = {"Chinese": "选择游戏可执行文件","English": "Select Game Executable"}
type_game_path_exe = {"Chinese": "游戏路径", "English": "Game Path"}
type_game_path_all = {"Chinese": "所有文件", "English": "All File"}
text_admin_error_title = {"Chinese": "权限错误", "English": "Permission Error"}
text_admin_error_text = {"Chinese": "无法以管理员权限启动游戏。请尝试以管理员身份运行工具箱。", "English": "Failed to start game with admin privileges. Please try running the kit as administrator."}


default_path = r"C:\Program Files\HoYoPlay\games\Genshin Impact game"

Game_Path = ""
Language = "English"
start_button = None  # 全局引用启动按钮

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(exe_path):
    try:
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", exe_path, None, None, 1
        )
        if result <= 32:
            print(f"[管理员启动失败] 错误代码: {result}"    )
            return False
        print("[管理员启动成功] 已请求管理员权限")
        return True
    except Exception as e:
        print(f"[管理员启动异常] {str(e)}")
        return False

def is_game_running(game_path):
    """检查游戏进程是否正在运行"""
    if not game_path or not os.path.exists(game_path):
        return False
    
    # 获取游戏进程名
    process_name = os.path.basename(game_path)
    
    # 检查所有进程
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == process_name.lower():
            return True
    
    return False

def disable_start_button():
    global start_button, Language
    if start_button:
        start_button.configure(
            text=button_running_text[Language],
            state="disabled",
            fg_color="#6B7280",
            hover_color="#6B7280"
        )

def enable_start_button( string ):
    global start_button, Language
    if start_button:
        start_button.configure(
            text=string,
            state="normal",
            fg_color="#3B82F6",
            hover_color="#2563EB"
        )

def start_game( dm ):
    global Game_Path, Language
    if not Game_Path or not os.path.exists(Game_Path):
        response = askyesno(
            title=text_gamepath_tip_title[Language], 
            message=text_gamepath_tip_text[Language]
        )
        if response:
            initialdir = default_path if os.path.exists(default_path) else None
            selected_file = filedialog.askopenfilename(
                title=window_file_title [ Language ],
                filetypes=[(type_game_path_exe [ Language ], "*.exe"), (type_game_path_all [ Language ], "*.*")],
                initialdir=initialdir
            )
            if selected_file and selected_file.lower().endswith('.exe'):
                normalized_path = os.path.normpath(selected_file)
                dm.set_config("GamePath", normalized_path)
                Game_Path = normalized_path 
                if is_game_running(Game_Path):
                    disable_start_button()
                else:
                    enable_start_button(button_start_text[Language])
        else:
            print("[启动失败] 游戏路径未设置，用户取消设置")
        return response
    else:
        try:
            # 在尝试启动前禁用按钮
            disable_start_button()
            
            if platform == "win32":
                if is_admin():
                    print("[管理员检测] 当前已以管理员身份运行")
                    Popen(
                        [Game_Path],
                        creationflags=CREATE_NEW_PROCESS_GROUP,
                        close_fds=True
                    )
                    print("[游戏启动] 成功启动游戏 (管理员权限)")
                else:
                    print("[管理员检测] 当前非管理员身份，尝试请求权限")
                    if run_as_admin(Game_Path):
                        print("[游戏启动] 已请求管理员权限启动游戏")
                        # 假设管理员启动请求成功，禁用按钮
                        disable_start_button()
                    else:
                        print("[游戏启动失败] 用户取消或管理员权限请求失败")
                        # 启动失败，重新启用按钮
                        enable_start_button( button_start_text[Language] )
                        showerror(
                            title=text_admin_error_title[Language],
                            message=text_admin_error_text[Language]
                        )
            else:
                Popen(
                    [Game_Path],
                    start_new_session=True,
                    close_fds=True
                )
                print("[游戏启动] 成功启动游戏 (非Windows系统)")
                # 成功启动，禁用按钮
                disable_start_button()
            return False
        except Exception as e:
            print(f"[游戏启动异常] {str(e)}")
            # 启动失败，重新启用按钮
            enable_start_button( button_start_text[Language] )
            showerror(
                title=text_admin_error_title[Language],
                message=f"{text_admin_error_text[Language]} ({str(e)})"
            )
            return False

def create_frame(parent, dm, language, gamepath, on_settings_requested=None):
    global Game_Path, Language, start_button
    Game_Path = gamepath
    Language = language
    
    frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
    frame.is_start_frame = True
    
    title_frame = ctk.CTkFrame(frame, fg_color="transparent")
    title_frame.pack(side="top", fill="x", padx=20, pady=(20, 15))
    
    title_label = ctk.CTkLabel(
        title_frame,
        text=text_title[language],
        font=("Segoe UI", 24, "bold"),
        text_color="#6CBBE2",
    )
    title_label.pack(side="left")
    
    button_frame = ctk.CTkFrame(frame, fg_color="transparent")
    button_frame.pack(side="top", fill="x", padx=20, pady=30)
    
    # 保存按钮引用到全局变量
    start_button = ctk.CTkButton(
        button_frame,
        text=button_start_text[language],
        font=("Segoe UI", 16, "bold"),
        fg_color="#3B82F6",
        hover_color="#2563EB",
        text_color="#FFFFFF",
        height=50,
        width=200,
        corner_radius=8,
        command=lambda: handle_start_click(on_settings_requested, dm)
    )
    start_button.pack()
    
    # 切换到页面时检查游戏是否在运行
    if is_game_running(Game_Path):
        disable_start_button()
        print("[页面切换] 检测到游戏正在运行，禁用启动按钮")
    else:
        enable_start_button( button_start_text[Language] )
        print("[页面切换] 游戏未运行，启用启动按钮")
    
    return frame

def handle_start_click(on_settings_requested, dm):
    need_settings = start_game( dm )
    if need_settings and callable(on_settings_requested):
        print("[用户操作] 用户选择跳转到设置页面")
        enable_start_button( button_start_text[Language] )
        on_settings_requested()