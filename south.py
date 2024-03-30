import customtkinter as ctk

root = ctk.CTk()
root.geometry("600x400")

frame = ctk.CTkScrollableFrame(root, fg_color="green")
subframe = ctk.CTkFrame(frame, fg_color="blue")

label = ctk.CTkLabel(subframe, text="ABHAY", fg_color="red")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

subframe.grid(row=0, column=0, sticky="se")
frame.grid(row=0, column=0, sticky="nswe")
label.grid(row=0, column=0)

root.mainloop()