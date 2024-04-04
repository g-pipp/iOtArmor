import tkinter as tk
import subprocess
import signal
import threading
import time

class PacketCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Packet Capture")
        
        self.start_button = tk.Button(root, text="Start Capture", command=self.start_capture)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop Capture", command=self.stop_capture, state=tk.DISABLED)
        self.stop_button.pack()

    def start_capture(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.capture_thread = threading.Thread(target=self.capture_packets)
        self.capture_thread.start()

    def stop_capture(self):
        self.stop_button.config(state=tk.DISABLED)

        self.capture_process.terminate()
        print('Finsihed capture')

    def capture_packets(self):
        self.capture_process = subprocess.Popen(['C:\\Program Files\\Wireshark\\tshark', "-i", "Wi-", "-w", "C:\\Users\\braxm\\OneDrive\\Documents\\captured_packets.pcap"])
        self.capture_process.wait()
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketCaptureApp(root)
    root.mainloop()