import customtkinter as ctk
import tkinter as tk

family = "Roboto Medium"
font_size = -16


class Editor(ctk.CTkFrame):
    """Нижний фрейм"""

    def __init__(self, master=None):
        self.master = master
        super().__init__(master, corner_radius=0, fg_color='grey20')
        font_textbox = ctk.CTkFont(family=f"{family}", size=font_size)
        self.st = ctk.CTkTextbox(self, font=font_textbox, corner_radius=0,
                                 height=115, fg_color="transparent",
                                 # fg_color=bg_color,  text_color='white'
                                 )
        self.st.focus_set()
        self.st.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.st.delete("0.0", "end")

    def set_text_to_edit(self, msg: str) -> None:
        """Вывести текст в редактор"""
        self.st.configure(state="normal")
        self.st.insert("0.0", f"{msg}")
        self.st.configure(state="disabled")
