#!/usr/bin/env python
import socket, time, sys

#Import gateway address and port.
from utils import *
import tkinter as tk
from tkinter import ttk

def close_socket():
    clientSocket.close()
    sys.exit()

def send_to_gateway():
    dest = my_msg.get()
    dest_drone = combo.get()
    ip, port = DRONES[dest_drone]
    msg_list.insert(tk.END, f'dispositivo selezionato: {dest_drone}, ip: {ip}, port: {port}')
    ip, port = DRONES[dest_drone]
    msg_list.insert(tk.END, f'dispositivo selezionato: {dest_drone}, ip: {ip}, port: {port}')
    msg_list.insert(tk.END, f'richiesta inviata a => {dest_drone}')

    packet = dest + ',' + dest_drone 

    ## invia pacchetto al gateway e calcola tempo trascorso
    t0 = time.time()
    clientSocket.send(packet.encode('utf8'))
    t1 = time.time() -t0
    msg_list.insert(tk.END, f'tempo trascorso per inviare pacchetto: {t1}')

window = tk.Tk()
window.title("Client")
 
messages_frame = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=5)
messages_frame.pack()

scrollbar = tk.Scrollbar(messages_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# La parte seguente contiene i messaggi.
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()

my_msg = tk.StringVar()
my_msg.set("Inserisci qui l'indirizzo")

entry_field = tk.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send_to_gateway)
entry_field.pack()

buttons_frame = tk.Frame(master=window, height=25)
buttons_frame.pack(fill=tk.X)

drones_list = []
for d in DRONES:
    drones_list.append(d)

combo = ttk.Combobox(buttons_frame, values = drones_list)

# lo setto direttamente al primo drone come valore di default
combo.set("drone_1")
combo.pack(padx = 5, pady = 5)

btn_send = tk.Button(buttons_frame, text="send", command= lambda: send_to_gateway())
btn_send.pack()

btn_connect = tk.Button(buttons_frame, text="riconnetti", command= lambda: connect_to_gateway())
btn_connect.pack()

btn_disconnect = tk.Button(buttons_frame, text="chiudi socket", command= lambda: clientSocket.close())
btn_disconnect.pack()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def connect_to_gateway():
    # tenta la connessione al gateway, se non riesce riprova ogni 2 secondi
    try:
        clientSocket.connect((HOST, GATEWAY_TCP[1]))
    except Exception as e:
        msg_list.insert(tk.END, e)

if __name__ == "__main__":
    msg_list.insert(tk.END, f'Client online, IP: {CLIENT_IP}')
    connect_to_gateway()

window.mainloop()
