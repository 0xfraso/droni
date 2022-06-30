import tkinter as tk
from subprocess import Popen

PADDING=10

def Execute(target):
	Popen(["python", target])

window = tk.Tk()

btn_gateway = tk.Button(master=window, text="gateway", command= lambda: Execute("gateway.py"))
btn_gateway.pack(padx=PADDING, pady=PADDING)

btn_client = tk.Button(master=window, text="client", command= lambda: Execute("client.py"))
btn_client.pack(padx=PADDING, pady=PADDING)

btn_drone1 = tk.Button(master=window, text="drone1", command= lambda: Execute("drone1.py"))
btn_drone1.pack(padx=PADDING, pady=PADDING)

btn_drone2 = tk.Button(master=window, text="drone2", command= lambda: Execute("drone2.py"))
btn_drone2.pack(padx=PADDING, pady=PADDING)

btn_drone3 = tk.Button(master=window, text="drone3", command= lambda: Execute("drone3.py"))
btn_drone3.pack(padx=PADDING, pady=PADDING)

window.mainloop()
