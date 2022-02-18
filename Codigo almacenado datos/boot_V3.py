import can
import os
import time
import RPi.GPIO as GPIO
import time
from can import Message
import tkinter as tk
import Thread
from tkinter import * 
from tkinter.ttk import *
import time
from threading import Thread
from PIL import ImageTk, Image




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


####### Difinicion de pantallas temporales


class PantallaDeInicio(tk.Tk):
    def __init__(self):
        ventana=tk.Tk()
        style=Style()

        style.configure('W.TButton', font =
               ('calibri', 10, 'bold', 'underline'),
                foreground = 'red')

        label=tk.Label(ventana, text="Preparando el coche...", font=("Helvetica",40),anchor="center")
        label.pack()
        
        img = Image.open("ICAI_Speed_Club.jpg")
        img = img.resize((600, 400), Image.ANTIALIAS)
        imgdef= ImageTk.PhotoImage(img)
        panel = Label(ventana, image = imgdef)

        panel.pack(side="top",fill="both",expand=True)
        
        ventana.resizable(200,200)
        ventana.title("Pagina de prueba")
        ventana.geometry('600x500')
        ventana.mainloop()

    def quitScreen():
        ventana.destroy

class PantallaIntermedia(tk.Tk):
    def __init__(self):
        ventana=tk.Tk()
        style=Style()


########Configurar el estilo de la pantalla intermedia ---> 

        style.configure('W.TButton', font =
               ('calibri', 10, 'bold', 'underline'),
                foreground = 'blue')

        btn1 = Button(ventana, text = 'Quit !',
                style = 'W.TButton',
             command = ventana.destroy)
        btn1.grid(row = 0, column = 3, padx = 100)

        ventana.resizable(0,0)
        ventana.title("Pagina de prueba")
        ventana.geometry('680x430')
        ventana.mainloop()

    def quitScreen():
        ventana.destroy


def start_pantalla1():
    screen1 = PantallaDeInicio()
    screen1.start()


def start_pantalla2():
    screen1 = PantallaIntermedia()
    screen1.start()

thread1 = Thread(target=start_pantalla1)
thread2= Thread(target= start_pantalla2)


###########################################

    

canales_utilizados=[]
os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()
    
#Configurar pin control led RTS
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, False)

temp=[]
id_ok=[10,20,30,40]
a=0
b=0
#############
screen1 = Pantalla()
screen1.start()

class Pantalla(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Webpage Download')
        self.geometry('680x430')
        self.resizable(0, 0)

#############


### Poner bien la secuancia de arranque --> mas intuitiva
try:
    thread1.start()
    while a<1:
        
        mensaje=leerCan(bus)
        mensaje_id=mensaje[1]
        if mensaje_id in id_ok:
            a=a+1
            id_ok.remove(mensaje_id)
    print("Ok recibidos")
    enviarBus(bus,0x51,[0])
    print("Coche RTS")
    GPIO.output(7, True)
    thread2.start()
    ##Poner a la espera a la raspberry para el rts
    while b==0:
        mensaje=leerCan(bus)
        mensaje_id=mensaje[1]
        if mensaje_id==41:
            b=1
    ##Mandar a la pantalla READY TO START
    enviarBus(bus,0x52,[0])
    ##Mandamos el ACK para que los sensores empiecen a mandar la telemetria
    canales_utilizados=[]
    while True:
        mensaje=leerCan(bus)
        if mensaje[1]==42:
           print("Mandar mensaje al piloto")
        if mensaje[1] not in canales_utilizados:
            canales_utilizados.append(mensaje[1])
            with open (str(mensaje[1])+".txt","w") as tt:
                    tt.write("Cominzo de transmisión: "+str(mensaje[1])+"\n")
        else:
            with open(str(mensaje[1])+".txt","a") as tt:
                    tt.write(str(mensaje[2]))
except KeyboardInterrupt:
    print("Fin")
    





#### Alternativa a los archivos txt ---> archivos CSV organizados por columnas (ID) y filas por tiempo 
#### EJ:
####     ID|010|020|030|040|
#### valor | Ok| Ok| Wt| Ok|
#### ...


#### Introducir leyenda de canales utilizados y su significados. 

### --- Secuencia de arranque ---

### Todos los canales de dos digitos (10,20,30,...) son utilizados unicamente como medida de control de todos los sistemas utilizados 
### y conectados al bus CAN. Los ID's se especifican a continuacion:

### ID --- 0x10 = GPS ECU 	 		--> Ok
### ID --- 0x20 = BMS ECU	 		--> Ok
### ID --- 0x30 = BackSensor 		--> Ok
### ID --- 0x40 = ArduinoFront		--> Ok

### ID --- 0x1000 = INV Volatge 	--> Ok

### Cuando se reciben todos los oks + la medicion del voltaje del inversor, mandamos un ack (medida de control) al arduino para confirmar que tambien nos escucha desde el bus:

### ID --- 0x51 = Rts (Raspberry)	--> Ok (al arduino)

### Una vez confirmada todas las conexiones, mandamos el ok a la raspberry para que comience con el arranque

### ID --- 0x41 = ArduinoFront 		--> Ready to start

### Despues de recibirse el ready to start el coche manda el ready to telemetry a los sensores para que comiencen a mandar datos

### ID --- 0x52 = ACK OK (Raspberry)--> Start telemetry



### Todo esto ocurrirá en la secuencia de arranque sin que el piloto toque nada --> Se le mostrará al piloto que se está ejecutando la secuencia de arranque en el dashboard (SCREEN 1)
### Una vez finalizada, la pantalla cambiará a otra que muestre al piloto que el coche está listo para arrancar (SCREEN 2).
### Finalmente cuando el piloto pulse el boton de start, la pantalla cambiará a la definitiva y mostrará la telemtría :Nivel de batería, voltaje, temperatura, velocidad y errores (Screen 3). 


def guardarCsv(tiempo,id, mensaje):
	
