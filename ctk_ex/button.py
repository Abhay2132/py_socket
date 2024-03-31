import customtkinter as ctk

window = ctk.CTk()
window.geometry("600x400")

def button_event():
    print("button pressed")

button = ctk.CTkButton(window, text="CTkButton", command=button_event)
button.pack()

window.mainloop()