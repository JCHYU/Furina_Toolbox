# 这是 start.py (启动游戏) 的代码
import customtkinter as ctk
from tkinter.messagebox import askyesno

text_title = {"Chinese": "启动游戏", "English": "Start Game"}
button_start_text = {"Chinese": "原神，启动！", "English": "Boot Up Genshin Impact!"}
text_gamepath_tip_title = {"Chinese": "提示", "English": "Tip"}
text_gamepath_tip_text = {"Chinese": "您没有设置游戏路径，是否立即设置？", "English": "You haven't set the game path, do you want to set it now?"}
Game_Path = ""
Language = "English"
def start_game () :
    if Game_Path == "":
        askyesno(title=text_gamepath_tip_title [ Language ], message=text_gamepath_tip_text [ Language ])
    else:
        pass
def create_frame(parent, language, gamepath):
    global Game_Path, Language
    Game_Path = gamepath
    Language = language
    frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
    
    frame.is_start_frame = True
    
    title_frame = ctk.CTkFrame(frame, fg_color="transparent")
    title_frame.pack(side="top", fill="x", padx=20, pady=(20, 15))
    
    title_label = ctk.CTkLabel(
        title_frame,
        text=text_title [ language ],
        font=("Segoe UI", 24, "bold"),
        text_color="#6CBBE2",
    )
    title_label.pack(side="left")
    
    button_frame = ctk.CTkFrame(frame, fg_color="transparent")
    button_frame.pack(side="top", fill="x", padx=20, pady=30)
    
    start_button = ctk.CTkButton(
        button_frame,
        text=button_start_text [ language ],
        font=("Segoe UI", 16, "bold"),
        fg_color="#3B82F6",
        hover_color="#2563EB",
        text_color="#FFFFFF",
        height=50,
        width=200,
        corner_radius=8,
        command=start_game
    )
    start_button.pack()
    
    return frame