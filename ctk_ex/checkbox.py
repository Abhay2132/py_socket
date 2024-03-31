import customtkinter

app = customtkinter.CTk()
app.geometry("600x400")

def checkbox_event():
    print("checkbox toggled, current value:", check_var.get())

check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(app, text="CTkCheckBox", command=checkbox_event,
                                     checkbox_height=15,
                                     checkbox_width=15,
                                     border_width=1,
                                     corner_radius=5,
                                     variable=check_var, onvalue="on", offvalue="off")
checkbox.pack()
app.mainloop()