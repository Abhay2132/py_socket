from typing import Any, Tuple
import customtkinter as ctk
import sys

HEIGHT = 400
WIDTH = 600
def scroll_to_bottom(frame):
  frame.after(10, frame._parent_canvas.yview_moveto, 1.0)

class Message(ctk.CTkFrame):
    def __init__(self, master, text="", user="YOU"):
        width = 200
        super().__init__(master, fg_color="#2156ac")

        text_limit = 80
        if len(text) > text_limit:
            text = text[:text_limit] + " ..."

        self.width = width
        self.user = ctk.CTkLabel(master=self, text=user, font=("sans", 10), height=10)
        self.text = ctk.CTkLabel(master=self,width=100, anchor="w", text=text, font=("Roboto", 12), fg_color="transparent")  

    def showContent(self):
        self.user.grid(row=0, column=0, sticky='w', padx=5, pady=(3,0))
        self.text.grid(row=1, column=0, sticky='nswe',  padx=10, pady=2)

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=WIDTH)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self.messageFrame = MessageFrame(self)
        self.inputFrame = InputFrame(self)
    
    def show(self):
        self.messageFrame.show()
        self.inputFrame.show()
        self.grid(row=0, column=0, sticky='ns')

class MessageFrame(ctk.CTkScrollableFrame):
    messages = list()
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        # ctk.CTkLabel(self, text="", height=10, fg_color="red").grid(row=0, column=0, sticky="we")


    def addMessage(self, text="", user="YOU", isMe = True):
        message = Message(self, text, user)
        
        message.showContent()
        self.grid_rowconfigure(len(self.messages), weight=1)

        message.grid(row=len(self.messages), column=0, sticky= ('se' if isMe else 'sw'), padx=5, pady=(0,10))
        self.messages.append(message)
    
    def show(self):
        self.grid(row=0, column=0, sticky='nswe')

class InputFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=50)
        self.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(master=self, font=("roboto", 15))
        self.entry.insert(0, "HELLO")
        self.sendButton = ctk.CTkButton(master=self, text="SEND", width=60)
    
    def show(self):
        self.entry.grid(row=0, column=0, sticky="we", padx=10, pady=4)
        self.sendButton.grid(row=0, column=1, sticky="ns", padx=(0,10), pady=4)
        self.grid(row=1, column=0, sticky='we')

class APP(ctk.CTk):

    pendingMessages = list()
    username="YOU"

    def __init__(self, title="", username="YOU"):
        super().__init__()

        self.username = username
        
        self.title(title)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.mainFrame = MainFrame(self)

        self.mainFrame.inputFrame.sendButton.configure(command=self.sendMessage)

    def sendMessage(self,):
        text = self.mainFrame.inputFrame.entry.get()
        if not bool(text.strip()): return
        self.mainFrame.messageFrame.addMessage(text, self.username)
        scroll_to_bottom(self.mainFrame.messageFrame)

        self.mainFrame.inputFrame.entry.delete(0, ctk.END) # clear input
        self.pendingMessages.append(text) 
        self.postMessage()

    def receiveMessage(self, message, user="USER0"):
        self.mainFrame.messageFrame.addMessage(message, user, isMe=False)
        scroll_to_bottom(self.mainFrame.messageFrame)
        pass

    # sends message to server
    def postMessage(self):
        # implement by child class
        pass

    def show(self):
        self.mainFrame.show()
        self.mainloop()

if __name__ == "__main__":
    # username = input("USERNAME : ")
    app = APP("Server")
    try:
        app.show()
    except KeyboardInterrupt:
        print("Exiting due to KEYBOARD INTERUPT")
        sys.exit(1)

