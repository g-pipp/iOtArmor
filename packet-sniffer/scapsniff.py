#Please note that you have to run this script with root privileges (aka sudo python3 packet-sniffer.py)
from scapy.all import sniff

def packet_callback(packet):
    print(packet.show())

def main():
    sniff(prn=packet_callback, count=20)

if __name__ == '__main__':
    main()
