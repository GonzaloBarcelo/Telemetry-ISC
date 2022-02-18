# potentiometer.py

import serial
import datetime
import time
import os

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM3', 9800, timeout=1)
time.sleep(2)
canales_utilizados=[]
linea=ser.readline()
while True:
    line = ser.readline()
    if line:
        try:
            string = line.decode()
            mensaje=string.split(" ")
            mensaje[0]=int(mensaje[0])
            mensaje[1]=mensaje[1][:-2]
            print(mensaje)
            if mensaje[0]==42:
                print("Mandar mensaje al piloto")

           #pantallaGO()
            if mensaje[0] not in canales_utilizados:
                canales_utilizados.append(mensaje[0])
                with open (str(mensaje[0])+".txt","w") as tt:
                        tt.write("Cominzo de transmisión: "+str(mensaje[0])+"\n")
            else:
                with open(str(mensaje[0])+".txt","a") as tt:
                        tt.write(str(datetime.datetime.now().timestamp())+" --- "+str(mensaje[1])+"\n")

        except:
            pass
        
ser.close()