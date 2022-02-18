import random
import datetime
import time

idm=[100,101,102,103,104,105,110,111,112,130,131,132,133,134,140,141,142,143,144]

variables=["Tension Inversor","Temperatura motor","Temperatura inversor","Temperatura Refri In","Temperatura Refri Out","Presion Aero Refri","Acelerometro X","Acelerometro Y","Acelerometro Z","Aceleracion Pedal","Presion Frenos", "Temperatura Baterias 1","Temperatura Baterias 2","Temperatura Baterias 3","Temperatura Baterias 4","Temperatura Baterias 5"]
while True:
	for i in idm:
		with open(str(i)+".txt","a") as file:
			for j in range(1):
				tiempo=datetime.datetime.now().timestamp()
				mesageInt=random.randrange(0,100)
				messageFloat=random.randrange(0,100)
				escribir=str(tiempo)+" --- "+str(mesageInt)+"."+str(messageFloat)+"\n"
				print(escribir,end="")
				file.write(str(escribir))
				time.sleep(0.001)
	time.sleep(0.1)
			