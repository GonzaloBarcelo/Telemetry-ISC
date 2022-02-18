# potentiometer.py

import serial
import datetime
import time
import os
from elasticsearch import helpers, Elasticsearch
import csv
from datetime import datetime
#import Threading
import threading
#import _thread
#ELASTIC
#diccionario con los nombres de los sensores
id_sensor=[100,101,102,110,111,112,130,131,132,133,134,140,141,142,143,144]
variables=["Tension Inversor","Temperatura motor","Temperatura inversor",
        "Temperatura Refri In","Temperatura Refri Out","Presion Aero Refri","Aceleracion Pedal",    
        "Acelerometro X","Acelerometro Y","Acelerometro Z",
        "Presion Frenos", "Temperatura Baterias 1","Temperatura Baterias 2",
        "Temperatura Baterias 3","Temperatura Baterias 4","Temperatura Baterias 5"]
sensores= dict(zip(id_sensor,variables))

def convert(mensaje):   #crear un doc de elastic
    doc={
    "fecha_hora":datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
    "deltas":mensaje[0],
    "can_id": mensaje[1],
    "sensor_name":sensores[mensaje[1]],
    "value":mensaje[2]
    }
    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    return doc
   

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM3', 9800, timeout=1)
time.sleep(2)
canales_utilizados=[]
linea=ser.readline()
es = Elasticsearch(["https://0516a1b9b1d146d68246553b2f420a3f.northeurope.azure.elastic-cloud.com"], port=9243, scheme="https", http_auth=("admin", "comillas")) #llamada al servidor de Elastic

while True:
    line = ser.readline()
    if line:
        try:
            string = line.decode()
            mensaje=string.split(" ")
            mensaje[0]=int(mensaje[0])
            mensaje[1]=int(mensaje[1])
            mensaje[2]=mensaje[2][:-2]
            print(mensaje)
            if mensaje[1]==42:
                print("Mandar mensaje al piloto")

           #pantallaGO()
            if mensaje[1] not in canales_utilizados:
                canales_utilizados.append(mensaje[1])
                with open (str(mensaje[1])+".txt","w") as tt:
                        tt.write("Cominzo de transmisión: "+str(mensaje[1])+"\n")
            else:
                with open(str(mensaje[1])+".txt","a") as tt:
                    tt.write(str(datetime.now().timestamp())+" --- "+str(mensaje[2])+"\n")
                doc=convert(mensaje)
                res = es.index(document=doc,index="if04_telemetry_v1.0",)

        except:
            pass
        
ser.close()