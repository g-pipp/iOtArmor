import os
import subprocess
import customtkinter as ctk
import tkinter.messagebox as tkmb
from tkinter import Tk, filedialog
import re
import time
import threading as thread
import tkinter as tk
from joblib import load
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Replace 'path/to/your/model.joblib' with the actual path to your model file
#from CTkListbox import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


##if you get stuck on the signin page press alt+f4

# class for the home page gui
class TopLevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        self.ip_addresses = []
        self.ip_labels = []

        super().__init__(*args, **kwargs)
        # temporary solution to fix the main screen not popping up on top
        self.focus()
        self.lift()
        self.grab_set()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        #self.attributes('-fullscreen', True)
        self.title("IoT Armor Portal")
        # setting cosmetic stuff

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.title_label = ctk.CTkLabel(self, text_color="gainsboro",
                                        text="Welcome to IOTArmor, the all-in-one hotspot for managing your own network")
        self.title_label.place(x=115, y=0)

        self.title_label.configure(font=('Rog Fonts', 20))

        # self.label = ctk.CTkLabel(self, text="Active IP Addresses", width=120, height=25, corner_radius=10)
        self.ml_button = ctk.CTkButton(self, fg_color="cadetblue4", command=self.start_machine_learning,
                                       text="Start Network Shield")
        self.ml_button.place(x=0, y=650)
        self.ml_button.configure(font=('Nirmala UI', 30), height=100, width=400)

        self.active_button = ctk.CTkButton(self, fg_color="cadetblue4", command=self.button_activate,
                                           text="Start Monitoring")
        self.active_button.place(x=0, y=100)
        self.active_button.configure(font=('Nirmala UI', 30), height=100, width=400)

        self.no_active_button = ctk.CTkButton(self, fg_color="cadetblue4", command=self.no_button_activate,
                                              text="Stop Monitoring")
        self.no_active_button.place(x=0, y=250)
        self.no_active_button.configure(font=('Nirmala UI', 30), height=100, width=400)

        self.start_button = ctk.CTkButton(self, fg_color="cadetblue4", command=self.start_capture,
                                          text="Start Capture")  # for packetsniffing
        self.start_button.place(x=0, y=380)
        self.start_button.configure(font=('Nirmala UI', 30), height=100, width=400)

        self.stop_button = ctk.CTkButton(self, fg_color="cadetblue4", command=self.stop_capture,
                                         text="Stop Capture")  # for packetsniffing
        self.stop_button.place(x=0, y=500)
        self.stop_button.configure(font=('Nirmala UI', 30), height=100, width=400)

        self.close_button = ctk.CTkButton(self, fg_color="cadetblue4" ,command=self.close, text="Exit")
        self.close_button.place(x=530, y=250)
        self.close_button.configure(font=('Nirmala UI', 30), height = 100, width = 400)

        # self.textbox = ctk.CTkTextbox(self, width=350, height=520)
        # self.textbox.place(x=1000, y=100)
        self.notelabel = ctk.CTkLabel(self, text="Active IP Addresses", width=120, height=25, corner_radius=20,
                                      font=('Nirmala UI', 30))
        self.notelabel.place(x=1000, y=30)
        # self.add_button = ctk.CTkButton(self, fg_color="cadetblue4" ,command=self.button_add, text="Update IP Address")
        # self.add_button.place(x=530, y=150)
        # self.add_button.configure(font=('Nirmala UI', 30), height = 100, width = 400)

        self.my_frame = ctk.CTkScrollableFrame(self, orientation="vertical",
                                                       width=350, height=420, label_text="Active IP Addresses")
        self.my_frame.place(x=1000, y=100)

        #for x in range(20):
            #ctk.CTkLabel(self.my_frame, text="IP Address!").pack(pady=10)

        '''
        self.listbox = CTkListbox(self, width=350, height=520)
        self.listbox.place(x=1000, y=100)

        self.listbox.insert(1, "IP 1")
        self.listbox.insert(2, "IP 2")
        self.listbox.insert(3, "IP 3")
        self.listbox.insert(4, "IP 4")
        self.listbox.insert(5, "IP 5")
        self.listbox.insert(6, "IP 6")
        '''

        self.void = ctk.CTkLabel(self, text="STATUS", font=('Consolas', 70))
        self.void.place(x=610, y=400)
        self.status_label = ctk.CTkLabel(self, text=" ", font=('Terminal', 32))
        self.status_label.place(x=500, y=530)
        '''self.void1 = ctk.CTkLabel(self, text="and trusting us to keep", font=('Nirmala UI', 32))
        self.void1.place(x=580, y=480)
        self.void2 = ctk.CTkLabel(self, text="your network safe", font=('Nirmala UI', 32))
        self.void2.place(x=610, y=530)'''

        # this is the part you are looking for with the user input
        self.iplabel = ctk.CTkLabel(self, text="Please enter your IP addresses here Ex: 123.123.123.0/24", width=120,
                                    height=25, corner_radius=20, font=('Nirmala UI', 20))
        self.iplabel.place(x=500, y=30)

        self.enterip = ctk.CTkEntry(self, width=450, text_color="deepskyblue2", placeholder_text="IP Address")
        self.enterip.place(x=500, y=100)
        self.enterip.configure(font=('Nirmala UI', 30))

        self.progressbar = ctk.CTkProgressBar(self, width=800, height=100, orientation="horizontal")
        self.progressbar.place(x=530, y=650)
        self.progressbar.set(0)

    # monitoring functionality for the button when pro
    # what happens when the activate monitoring button is pressed
    def clear_ip_labels(self):
        # Destroy all children widgets in my_frame, which are the IP address labels
        for widget in self.my_frame.winfo_children():
            widget.destroy()

    # only does it when button pressed...must change to where button doesnt need to be pressed and stops when pressed again
    def monitor(self, subnet_to_scan, stop_event):
        while not stop_event.is_set():
            self.status_label.configure(text="Scanning for IP's...")
            print("STARTING SCAN\n.....................")
            command = ["nmap", "-sn", "n", subnet_to_scan]
            try:
                result = subprocess.run(command, check=True, capture_output=True, text=True)
                self.ip_addresses = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', result.stdout)
                # ip_addresses var holds the IPs. Use this for a for loop to assign IPs to
                # labels for color manpiulation
                if self.ip_addresses:
                    print("Discovered IP Addresses")
                    self.clear_ip_labels()
                    for ip in self.ip_addresses:
                        iplabel = ctk.CTkLabel(self.my_frame, text=ip)
                        iplabel.pack(pady=10)
                        self.ip_labels.append(iplabel)

            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                print(f"Commend output: {e.output}")
            time.sleep(1)

    # Packet capture function goes here
    def capture(self):
        self.status_label.configure(text="Starting Wireshark Scan...")
        app_PATH = 'C:\\Program Files\\Wireshark\\tshark'
        interface = 'Wi-Fi'
        wrTo_File_PATH = "C:\\iotArmor\\captured_packets.pcap"
        self.capture_process = subprocess.Popen([app_PATH, "-i", interface, "-w", wrTo_File_PATH])
        self.capture_process.wait()
        self.start_button.configure(state=tk.NORMAL)

    # Start capture fucntion goes here
    def start_capture(self):
        self.status_label.configure(text="Starting Capture...")
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.capture_thread = thread.Thread(target=self.capture)
        self.capture_thread.start()

    # Stop capture function goes here
    def stop_capture(self):
        self.status_label.configure(text="Capture Finished")
        self.stop_button.configure(state=tk.DISABLED)
        self.capture_process.terminate()
        print('Finished capture')

    # machine learning function goes here
    def start_machine_learning(self):
        root = Tk()
        root.withdraw()
        root.title('Select a CSV File')

        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])

        if file_path:
            try:
                dfdemo = pd.read_csv(file_path)
                print("CSV file loaded successfully.")
            except Exception as e:
                print(f"Error reading the CSV file: {e}")
        else:
            print("No file selected or the file selected is not a CSV file.")
        print(dfdemo)

        SRC_encoder = LabelEncoder()
        DEST_encoder = LabelEncoder()
        self.status_label.configure(text="machine learning!!")
        dfdemo = self.preprocessData(dfdemo, SRC_encoder, DEST_encoder)
        print(dfdemo)
        self.prediction(dfdemo, SRC_encoder)


    def preprocessData(self,df,ipSRC_encoder,ipDEST_encoder):

        dict = {'HTTP/XML': 0, 'UDP': 0, 'TPLINK-SMARTHOME/JSON': 0, 'DNS': 0, 'MDNS': 0, 'HTTP': 0, 'RCL': 0,
                'TLS': 0, 'TLSv1.2': 0, 'TLSv1.3': 0, 'AJP13': 0, 'SSDP': 0, 'ICMP': 0, 'ICMPv6': 0,
                'LLMNR': 0, 'BROWSER': 0, 'NTP': 0, 'IGMPv3': 0,'QUIC': 0,'DHCP': 0, 'RSL': 0,
                'SSH': 2, 'SSHv2': 2, 'TCP': 1}

        df['Protocol'] = df['Protocol'].map(dict)

        j = 0
        limit = 0
        for j, row in df.iterrows():
                if ('RST' in df['Info'][j] or 'Retransmission' in df['Info'][j] or 'TCP Port numbers reused' in
                        df['Info'][j]):
                    df.loc[j, 'Info'] = '1'  # anomaly
                elif ((df['Info'][j] == "Client: New Keys")):
                    df.loc[j, 'Info'] = '0'  # benign
                    limit += 1
                elif (limit == 3 and (df["Info"][j] == "Client: " or df["Info"][j] == "Server: ")):
                    df.loc[j, 'Info'] = '1'  # anomaly
                else:
                    df.loc[j, 'Info'] = '0'  # benign
        df['Info'].astype(int)


        # classifier
        df['Classifier'] = df['Info']

        # mode column
        # groups unique IP addresses together
        grouped = df.groupby('Source')

        # counts 1s and 0s based on classifier column using unique IPs stored in group
        goodSrc_count = grouped['Classifier'].apply(lambda x: (x == 0).sum())
        badSrc_count = grouped['Classifier'].apply(lambda x: (x != 0).sum())

        # assign value for final
        final_value = (goodSrc_count <= badSrc_count).astype(int)

        # map final to rows for proper addresses
        df['Final'] = df['Source'].map(final_value)

        # IP address conversion

        df['Source'] = ipSRC_encoder.fit_transform(df['Source'])
        df['Destination'] = ipDEST_encoder.fit_transform(df['Destination'])
        return df
    # ^ these are the last things along with the list of IPs on the screen to implement!
    def prediction(self, df, ipSRC_encoder):
        ben_IPs = set()
        sus_IPs = set()
        features = ['Source', 'Destination', 'Info', 'Protocol', 'Classifier']
        model = load("C:\\iotArmor\\officialModel.joblib")
        # Loop through each row in the DataFrame
        for a, row in df.iterrows():
            # Extract the features for prediction
            yyy = df.loc[a, features]
            res = pd.DataFrame([yyy])
            X = model.predict(res)
            current_ip = row['Source']
            # Decode the IP address
            decoded_ip = ipSRC_encoder.inverse_transform([current_ip])[0]

            # Categorize the IP based on the model's prediction
            if X == 1:
                # If the prediction is 1, add to sus_IPs
                sus_IPs.add(decoded_ip)
            else:
                # Otherwise, add to ben_IPs only if it hasn't been flagged as suspicious before
                if decoded_ip not in sus_IPs:
                    ben_IPs.add(decoded_ip)

        # Convert the sets to lists
        sus_IPs_list = list(sus_IPs)
        ben_IPs_list = list(ben_IPs)
        print("Benign IPs:", ben_IPs_list)
        print("Suspicious IPs:", sus_IPs_list)
        print(type(self.iplabel))
        self.do_colors(ben_IPs_list, sus_IPs_list)


    def do_colors(self, safe_ips, bad_ips):
        for label in self.ip_labels:
            ip = label.cget("text")
            if ip in safe_ips:
                label.configure(text_color="green")  # Safe IPs in green
            elif ip in bad_ips:
                label.configure(text_color="red")  # Unsafe IPs in red
            else:
                label.configure(text_color="Yellow")  # IPs that are neutral


        '''
        for self.iplabel in self.ip_addresses:
            print(self.iplabel.cget("text"))
            if item == self.iplabel.cget("text"):
                self.iplabel.configure(text_color='green')
            else:
                self.iplabel.configure(text_color='red')
                return
        '''

    def button_activate(self):
        self.status_label.configure(text="Activating Something")
        print("Congrats you clicked a button")
        # green means it has been investigated and it has been determined to be good
        subnet_to_scan = self.enterip.get()

        # Create an Event object to signal when to stop monitoring (thank you Dr. Humphries...)
        self.stop_event = thread.Event()
        self.monitor_thread = thread.Thread(target=self.monitor, args=(subnet_to_scan, self.stop_event))
        self.monitor_thread.start()
        self.progressbar.start()

    # what happens when the active monitoring is turned off
    def no_button_activate(self):
        self.status_label.configure(text="Scanning done")
        self.stop_event.set()
        self.progressbar.stop()
        print("thank you for scanning!")

    def close(self):
        # will close the program
        app.destroy()

    def button_add(self):
        # displays user input in the list of active ip's...in the future I will add the ability to input more
        # than one ip address and do case checking but this is good enough for the moment to demo our idea

        print(self.enterip.get())
        self.string = self.enterip.get()
        ipNum = self.string
        self.enterip.delete(0, 'end')
        self.ip_label22.configure(text=self.string)


# main app/sign in screen
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.attributes('-fullscreen', True)
        self.title("IoT Armor")
        self.label = ctk.CTkLabel(self, text_color="gainsboro",
                                  text="Welcome to IOTArmor, the all-in-one hotspot for managing your own network")
        self.label.pack(pady=20)
        self.label.configure(font=('Rog Fonts', 20))

        self.frame = ctk.CTkFrame(self, width=200, height=200, corner_radius=40, border_color="white")
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.label_1 = ctk.CTkLabel(master=self.frame, text_color="cyan", text='Please enter your credentials')
        self.label_1.pack(pady=12, padx=10)
        self.label_1.configure(font=('Rog Fonts', 40))

        self.user_entry = ctk.CTkEntry(master=self.frame, width=150, placeholder_text="Username")
        self.user_entry.pack(pady=12, padx=10)
        self.user_entry.configure(font=('Nirmala UI', 30))

        self.user_pass = ctk.CTkEntry(master=self.frame, width=150, placeholder_text="Password", show="*")
        self.user_pass.pack(pady=12, padx=10)
        self.user_pass.configure(font=('Nirmala UI', 30))

        self.button = ctk.CTkButton(master=self.frame, text='Login', command=self.login)
        self.button.pack(pady=12, padx=10)
        self.button.configure(font=('Nirmala UI', 20))

        self.toplevel_window = None

    def login(self):
        self.username = "123"
        self.password = "123"
        # if login info is correct, opens the home page
        if self.user_entry.get() == self.username and self.user_pass.get() == self.password:
            self.toplevel_window = TopLevelWindow(self)
        else:
            tkmb.showerror(title="Login Failed", message="Invalid Username or password")


if __name__ == "__main__":
    app = App()
    app.mainloop()

'''
COLORS BELOW
		self.ip_label.configure(text_color="green")
		#red means it is has been investigated and has been determined to be bad
		self.ip_label2.configure(text_color="red")
		#yellow means it is being investigated
		self.ip_label1.configure(text_color="yellow")
		self.progressbar.start()
'''