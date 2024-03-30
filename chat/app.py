import customtkinter as ctk

root = ctk.CTk()
root.title("Chat")
root.geometry("600x400")

boxFrame = ctk.CTkFrame(master=root, fg_color="blue", width=600)
messagesFrame = ctk.CTkFrame(master=boxFrame, fg_color="red", width=600)
inputFrame = ctk.CTkFrame(master=boxFrame, fg_color="green", height=40, width=600)


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

boxFrame.grid_rowconfigure(0, weight=1)
boxFrame.grid_columnconfigure(0, weight=1)

boxFrame.grid(row=0, column=0, sticky='ns')

messagesFrame.grid(row=0, column=0, sticky='nswe')
inputFrame.grid(row=1, column=0, sticky='ew')

print(boxFrame.winfo_width())

if __name__ == "__main__":
    root.mainloop()