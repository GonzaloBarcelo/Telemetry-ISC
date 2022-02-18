
#diccionario con los nombres de los sensores
id_sensor=[100,101,102,110,111,112,130,131,132,133,134,140,141,142,143,144]
variables=["Tension Inversor","Temperatura motor","Temperatura inversor",
        "Temperatura Refri In","Temperatura Refri Out","Presion Aero Refri","Aceleracion Pedal",    
        "Acelerometro X","Acelerometro Y","Acelerometro Z",
        "Presion Frenos", "Temperatura Baterias 1","Temperatura Baterias 2",
        "Temperatura Baterias 3","Temperatura Baterias 4","Temperatura Baterias 5"]
sensores= dict(zip(id_sensor,variables))


from elasticsearch import helpers, Elasticsearch
import csv
from datetime import datetime


#ejemplo de documento
# doc={
#     "fecha_hora": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
#     "can_id": 0x100,
#     "sensor_name":"Tensión Inversor (DC_BUS)",
#     "value":330.35
# }

def convert(dato):
	doc={
    "fecha_hora": dato[0].strftime('%d/%m/%Y %H:%M:%S'),
    "can_id": dato[1],
    "sensor_name":sensores[dato[1]],
    "value":dato[2]
	}
	return doc

#llamada al servidor elastic
es = Elasticsearch(["https://0516a1b9b1d146d68246553b2f420a3f.northeurope.azure.elastic-cloud.com"], port=9243, scheme="https", http_auth=("admin", "comillas"))

#postear un dato en el indice
res = es.index(document=doc,index="if04_telemetry_v1.0",)

