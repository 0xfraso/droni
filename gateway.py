#!/usr/bin/env python
import time, socket, sys
import tkinter as tk
from utils import *
from threading import Thread

def close_sockets():
    gatewaySocket_tcp.close()
    gatewaySocket_udp.close()
    sys.exit()

window = tk.Tk()
window.title("Gateway")

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

btn_disconnect = tk.Button(buttons_frame, text="chiudi socket", command= lambda: close_sockets())
btn_disconnect.pack()

drones_available = {
    'drone_1': False,
    'drone_2': False,
    'drone_3': False
    }

gatewaySocket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
gatewaySocket_udp.bind((HOST, GATEWAY_UDP[1]))

gatewaySocket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
gatewaySocket_tcp.bind((HOST,GATEWAY_TCP[1]))

msg_list.insert(tk.END, "Gateway Online!")

def send_to_drones(indirizzo, drone):
    # attendo finche il drone non torna disponibile 
    while not drones_available[drone.decode()]:
        msg_list.insert(tk.END, f'{drone} non disponibile, attendo..')
        time.sleep(2)
        
    msg_list.insert(tk.END, f'{drone.decode()} disponibile, inoltro la richiesta..')

    #accedo al dizionario presente nel file utils.py per risalire alla porta del drone a cui inoltrare la richiesta
    t0 = time.time()
    gatewaySocket_udp.sendto(indirizzo, (HOST,DRONES[drone.decode()][1]))
    t1 = time.time() -t0
    msg_list.insert(tk.END, f'tempo trascorso per inviare pacchetto: {t1}')
    drones_available[drone.decode()] = False

def listen_from_drones():
    while True:
            inPacket, fromAddr = gatewaySocket_udp.recvfrom(BUFFER_SIZE)
            packet = inPacket.decode().split()
            # se il pacchetto contiene il pattern <disponibile> tiene traccia dello stato del drone
            if inPacket.decode().find('<disponibile>') != -1:
                msg_list.insert(tk.END, f'{packet[0]} {packet[1]}, IP: {DRONES[packet[0]][0]}, PORT: {DRONES[packet[0]][1]}')
                drones_available[packet[0]] = True
            # altrimenti lo tratta come un messaggio di notifica
            else:
                msg_list.insert(tk.END, f'ricevuto messaggio da {fromAddr}: {inPacket.decode()}')

def listen_from_client():
    msg_list.insert(tk.END, f'TCP in attesa di connessione, IP:{GATEWAY_TCP[0]}, porta: {GATEWAY_TCP[1]}')
    gatewaySocket_tcp.listen(1)
    conn, fromAddr = gatewaySocket_tcp.accept()
    msg_list.insert(tk.END, f'connesso a {fromAddr}')
    while True:
        inPacket = conn.recv(BUFFER_SIZE)
        msg = inPacket.decode()
        indirizzo, drone = msg.split(',')
        msg_list.insert(tk.END, f'ricevuta richiesta di invio pacchetto => {indirizzo} al dispositivo: {drone}')
        send_to_drones_thread = Thread(target=send_to_drones, args=(indirizzo.encode('utf8'),drone.encode('utf8')))
        send_to_drones_thread.start()

if __name__ == "__main__":
    listen_from_client_thread = Thread(target=listen_from_client)
    listen_from_client_thread.start()
    listen_from_drones_thread = Thread(target=listen_from_drones)
    listen_from_drones_thread.start()

window.mainloop()
