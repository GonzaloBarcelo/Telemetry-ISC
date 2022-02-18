import can
import os
import time
import tkinter as tk #Librería para mostrar los mensajes al piloto
import datetime
import time

def createWindow():
    window =tk.Tk() #crea la ventana
    window.attributes('-fullscreen', True) #Configuración de la ventana
    window.title("IFS03")
    
    label=tk.Label(window, text="Preparando el coche...", font=("Helvetica",40),anchor="center")
    label.pack()
    
    window.mainloop()
    return window

def toInt(string):
    temp=["1","2","3","4","5","6","7","8","9","0"]
    s=''
    for i in string:
        if i in temp:
            s+=i
    return int(s)
#El mensaje a enviar debe ser una lista de numeros
def enviarBus(bus,mensaje_id,mensaje):
    
    msg=can.Message(arbitration_id=mensaje_id, data=mensaje, is_extended_id=False)
    bus.send(msg)
    
def leerCan(bus):
    tt=[]
    #print("hola")
    message = bus.recv()
    
    c = '{0:f} {1:x} {2:x} '.format(message.timestamp, message.arbitration_id, message.dlc)
    s=''
    for i in range(message.dlc ):
        s +=  '{0:x} '.format(message.data[i])
    mensaje_id=' {}'.format(c+s)
    tiempo=mensaje_id[:15]
    canal=int(mensaje_id[19:22])
    #print(str(canal)+": "+s)
    
    mensaje=toInt(mensaje_id[24:])
    tt.append(tiempo)
    tt.append(canal)
    tt.append(mensaje)
    return tt
    

#Crear ventana
window=createWindow()

#Inicializar CAN
canales_utilizados=[]
os.system("sudo /sbin/ip link set can0 up type can bitrate 125000")
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()
    
temp=[]
id_ok=[10,20,30,40]
a=0
b=0
try:
    while a<4:
        mensaje=leerCan(bus)
        mensaje_id=mensaje[1]
        if mensaje_id in id_ok:
            a=a+1
            id_ok.remove(mensaje_id)
    print("Ok recibidos")
    enviarBus(bus,0x51,[0])
    print("Mensaje enviado")
    
    while b==0:
        mensaje=leerCan(bus)
        mensaje_id=mensaje[1]
        if mensaje_id==41:
            b=1
    
    enviarBus(bus,0x52,[0])
    
    canales_utilizados=[]
    while True:
        mensaje=leerCan(bus)
        if mensaje[1]==42:
           print("Mandar mensaje al piloto")
           #pantallaGO()
        if mensaje[1] not in canales_utilizados:
            canales_utilizados.append(mensaje[1])
            with open (str(mensaje[1])+".txt","w") as tt:
                    tt.write("Cominzo de transmisión: "+str(mensaje[1])+"\n")
        else:
            with open(str(mensaje[1])+".txt","a") as tt:
                    tt.write(str(datetime.datetime.now().timestamp())+" --- "+str(mensaje[2]))
except KeyboardInterrupt:
    print("Fin")
    