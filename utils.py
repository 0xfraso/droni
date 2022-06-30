#!/usr/bin/env python
HOST = '127.0.0.1'

# tupla [IP, PORT]
GATEWAY_UDP = ['192.168.1.15' , 1329] 
GATEWAY_TCP = ['10.10.10.1' , 1328 ]

CLIENT_IP = '192.168.1.12'

BUFFER_SIZE=1024

# uso un dizionario per associare ad ogni id una tupla contenente l'indirizzo ip e la porta di ogni drone
DRONES = { 
    'drone_1': ['192.168.1.5', 4040],
    'drone_2': ['192.168.1.6', 4041],
    'drone_3': ['192.168.1.7', 4042]
    }
