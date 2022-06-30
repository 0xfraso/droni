#!/usr/bin/env python
#Import all modules from socket.
import socket, random, time, sys
from utils import *
import tkinter as tk
from threading import Thread

id = 'drone_1'
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
udpSocket.bind((HOST,DRONES[id][1]))

window = tk.Tk()
window.title("Drone 1")
 
messages_frame = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=5)
messages_frame.pack()

scrollbar = tk.Scrollbar(messages_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# La parte seguente contiene i messaggi.
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()

buttons_frame = tk.Frame(master=window, height=25)
buttons_frame.pack(fill=tk.X)

btn_disconnect = tk.Button(buttons_frame, text="chiudi socket", command= lambda: close_socket())
btn_disconnect.pack()

def close_socket():
    udpSocket.close()
    sys.exit()

def listen_from_gateway():
    while True:
        # drone si rende disponibile mandando un messaggio UDP al client
        udpSocket.sendto((f'{id} <disponibile>').encode('utf8'),(HOST, GATEWAY_UDP[1]))
        msg_list.insert(tk.END, f'{id} pronto a ricevere richieste..')
        inData, gatewayAddr = udpSocket.recvfrom(BUFFER_SIZE)
        msg_list.insert(tk.END, f"ricevuta richiesta da {gatewayAddr}")
        msg_list.insert(tk.END, f"indirizzo: {inData.decode()} spedizione in corso..")
        randSeconds = random.randint(2,6)
        time.sleep(randSeconds)
        msg_list.insert(tk.END, f'<consegna effettuata in {randSeconds} secondi>')
        udpSocket.sendto((f'consegna all\'indirizzo => "{inData.decode()}" effettuata').encode('utf8'), (HOST, GATEWAY_UDP[1]))

if __name__ == "__main__":
    listen_from_gateway_thread = Thread(target=listen_from_gateway)
    listen_from_gateway_thread .start()

window.mainloop()
