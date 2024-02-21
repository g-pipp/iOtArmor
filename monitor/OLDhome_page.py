import customtkinter as ctk 
import tkinter.messagebox as tkmb 

ctk.set_appearance_mode("dark") 

ctk.set_default_color_theme("blue") 

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("IoTArmor")
        self.geometry("1200x680")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox_frame_1 = MainFrame(self, values=["value 1", "value 2", "value 3"])
        self.checkbox_frame_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.checkbox_frame_2 = MainFrame(self, values=["option 1", "option 2"])
        self.checkbox_frame_2.grid(row=0, column=2, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        print("checkbox_frame_1:", self.checkbox_frame_1.get())
        print("checkbox_frame_2:", self.checkbox_frame_2.get())


app = App()
app.mainloop()