# 这是 settings.py (设置) 的代码
import customtkinter as ctk

text_title = {"Chinese": "设置", "English": "Settings"}

def create_frame(parent, dm, language):
    frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")

    title_frame = ctk.CTkFrame(frame, fg_color="transparent")
    title_frame.pack(side="top", fill="x", padx=20, pady=(20, 15))
    title_label = ctk.CTkLabel(
        title_frame,
        text=text_title [ language ],
        font=("Segoe UI", 24, "bold"),
        text_color="#6CBBE2",
    )
    title_label.pack(side="left")

    return frame