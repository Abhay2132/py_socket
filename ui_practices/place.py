import customtkinter as ctk
import tkinter as tk

window = ctk.CTk()
window.geometry("800x400")

rc = ctk.CTkFrame(window)

label1 = tk.Label(window, text="MY NAME IS ...", )
# label1.anchor("center")
label1.place(relx=0.5, rely=0.5, relwidth=0.5, height=200, anchor="center")

window.mainloop()