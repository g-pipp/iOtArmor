import os
import subprocess
import customtkinter as ctk 
import tkinter.messagebox as tkmb 

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

class TopLevelWindow(ctk.CTkToplevel):
	def __init__(self, master = None):
		super().__init__(master = master)
		self.geometry("800x800")
		self.title("IoT Armor Portal")
		self.master = master
		
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure((0,1), weight=1)
		
		self.label = ctk.CTkLabel(self, text="Active IP Addresses", width=120, height=25, corner_radius=10)
		self.label.place(x=0, y=0)
		
		self.ip_label = ctk.CTkLabel(self, text="192.0.1.1", width=120, height=25, corner_radius=20)
		self.ip_label.place(x=0, y=50)
		
		self.ip_label1 = ctk.CTkLabel(self, text="192.0.1.2", width=120, height=25, corner_radius=20)
		self.ip_label1.place(x=0, y=100)
		
		self.ip_label2 = ctk.CTkLabel(self, text="192.0.0.1", width=120, height=25, corner_radius=20)
		self.ip_label2.place(x=0, y=150)
		
		self.active_button = ctk.CTkButton(self, command=self.button_callback, text="Activate")
		self.active_button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
		self.active_button.configure(height = 90, width = 30)
		
		self.button = ctk.CTkButton(self, command=self.button_callback, text="Review Log")
		self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
		self.button.configure(height = 90, width = 30)

		self.textbox = ctk.CTkTextbox(self)
		self.textbox.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
		
	def button_callback(self):
		print("Congrats you clicked a button")
		self.ip_label.configure(text_color="green")
		self.ip_label2.configure(text_color="red")


class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.geometry("800x800")
		self.title("IoT Armor")
		self.label = ctk.CTkLabel(self,text="Welcome to IOTArmor, the all-in-one hotspot for managing your own network.") 
		self.label.pack(pady=20) 
		
		self.frame = ctk.CTkFrame(self) 
		self.frame.pack(pady=20,padx=40,fill='both',expand=True) 
		
		self.label1 = ctk.CTkLabel(self,text='Please enter your credentials') 
		self.label1.pack(pady=12,padx=10) 
		
		self.user_entry= ctk.CTkEntry(self,placeholder_text="Username") 
		self.user_entry.pack(pady=12,padx=10) 
		
		self.user_pass= ctk.CTkEntry(self,placeholder_text="Password",show="*") 
		self.user_pass.pack(pady=12,padx=10) 
		
		self.button = ctk.CTkButton(self,text='Login',command=self.login) 
		self.button.pack(pady=12,padx=10)
		
		self.toplevel_window = None
		
	def login(self):
		self.username = "test"
		self.password = "12345"
		
		if self.user_entry.get() == self.username and self.user_pass.get() == self.password:  
		    self.toplevel_window = TopLevelWindow(self)
		#elif self.user_entry.get() == self.username and self.user_pass.get() != self.password: 
		    #tkmb.showwarning(title='Wrong password',message='Please check your password') 
		#elif self.user_entry.get() != self.username and self.user_pass.get() == self.password: 
		 #   tkmb.showwarning(title='Wrong username',message='Please check your username')
		#else: 
		 #   tkmb.showerror(title="Login Failed",message="Invalid Username and password") 


if __name__ == "__main__":
	app = App()
	app.mainloop()
