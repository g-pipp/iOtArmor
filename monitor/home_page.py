import customtkinter as ctk 
import tkinter.messagebox as tkmb 
import time

ctk.set_appearance_mode("dark") 

ctk.set_default_color_theme("blue") 

class App(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.geometry("1200x680")
        self.title("IoTArmor")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.label = ctk.CTkLabel(master=self, text="Active IP Addresses", width=120, height=25, corner_radius=10)
        self.label.place(x=0, y=0)
        #self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,0), sticky="ew")

        self.ip_label = ctk.CTkLabel(master=self, text="192.0.1.1", width=120, height=25, corner_radius=20)
        self.ip_label.place(x=0, y=50)

        self.ip_label1 = ctk.CTkLabel(master=self, text="192.0.1.2", width=120, height=25, corner_radius=20)
        self.ip_label1.place(x=0, y=100)

        self.ip_label2 = ctk.CTkLabel(master=self, text="192.0.0.1", width=120, height=25, corner_radius=20)
        self.ip_label2.place(x=0, y=150)

        self.active_button = ctk.CTkButton(master=self, command=self.button_callback, text="Activate")
        self.active_button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.active_button.configure(height = 90, width = 30)

        self.button = ctk.CTkButton(master=self, command=self.button_callback, text="Review Log")
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.button.configure(height = 90, width = 30)

        self.textbox = ctk.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def button_callback(self):
        print("Congrats you clicked a button")
        self.ip_label.configure(text_color="green")
        self.ip_label2.configure(text_color="red")

if __name__ == "__main__":
    app = App()
    app.mainloop()