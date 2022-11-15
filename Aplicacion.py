import csv
import json
import os
import smtplib
import ssl
import numpy as np
import pandas as pd

#Leo el CSV, pero como no tiene header, hay que agregarlo, para esto:
#df = pd.read_csv("user_manager - user_manager.csv",header=None)
#agrego el Header a las columnas del CSV
#df.to_csv("user_manager - user_manager.csv",header=["row_id", "user_id", "user_state", "user_manager"],index=False)
#Como ya se agergo el header, la lectura del CSV seria asi:
#df = pd.read_csv("user_manager - user_manager.csv",header=["row_id", "user_id", "user_state", "user_manager"])


#Configuracion para el envio del mail automatico
EMAIL_ADDRESS = "noreplychallengedatasec@gmail.com"
EMAIL_PASSWORD= "" #Se borra la contraseña para no exponer datos, pero sera necesaria para la correcta ejecucion del programa
#Creo la conexion
context=ssl.create_default_context()

#jsonToPython = json.loads(db_list)

with open('db_list.json') as file:
    data = json.load(file) #Se carga la informacion del archivo json en una variable que se llama data
#print(data[ "db_list" ]) Para ver los datos que estan en db_list

for registro in data ["db_list"]:
   #Verifico los campos del archivo json para saber si poseen infromacion
    if registro["dn_name"] == "":
        print("\nNombre de la Base de Datos: --")
    else:
        print("\nNombre de la Data Base: {}".format(registro["dn_name"]))

    print("Nombre del Usuario: {}".format(registro["owner"]["name"])) #\n es un enter    
    if "email" in registro["owner"]:
        if registro["owner"]["email"] == "":
            print("Email del Usuario: --")
        else:
            print("Email del Usuario: {}".format(registro["owner"]["email"]))
    elif "email" in registro:
        if registro["email"] == "":
            print("Email del Usuario: --")
        else:
            print("Email del Usuario: {}".format(registro["email"]))
    else:
        print("No hay email en la base de datos para el usuario")

#ENVIO DE CORREO ELECTRONICO SEGUN CRITICIDAD
path ="user_manager - user_manager.csv"
content_dict = [] #Imprimo el contenido del CSV como una lista

#Leo el contenido del CSV, en caso de que este vacio el archivo, se indica que no existe. En caso de que exista, genero tuplas
#Output: [{'header1':'a','header2':'b','header3':'c'},{'header1':'d','header2':'e','header3':'f'},...]
if os.path.exists(path):
    with open(path,'r') as open_file:
        csvreader = csv.reader(open_file)
        headers = next(csvreader)
        content = []
        for row in csvreader:
            content.append(row)
else:
    print("No existe el archivo indicado: " + path)
    sys.exit(1) #genero un error
for line in content:
    content_dict.append(dict(zip(headers,line)))

 #Para cada elemento en elCSV, usando la info del json, verifico Si alguna base de datos es high, buscamos el manager y enviamos mail a manager
    for elemento in content_dict:
        for registro in data ["db_list"]:
            if registro["classification"]["confidentiality"]=="high" or registro["classification"]["integrity"]=="high" or registro["classification"]["availability"]=="high":
                if elemento ["user_id"] == registro["owner"]["uid"] and elemento["user_state"] == "activo": #Verificamos la info y si el usuario esta activo
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465,context=context) as smtp:
                            baseDeDatos=(registro["dn_name"])
                            confidencialidad = (registro["classification"]["confidentiality"])
                            integridad = (registro["classification"]["integrity"])
                            disponibilidad=(registro["classification"]["availability"])
                            subject=("IMPORTANTE: Consulta criticidad Base de datos: {baseDeDatos}".format(baseDeDatos=baseDeDatos))
                            body=("""
                            Hola, que tal?
                            Nos contactamos desde el area de data security para que nos puedas validar la criticdad de la sigueinte base de datos: {baseDeDatos}
                            Con la siguiente clasificacion:
                            Confidencialidad: {confidencialidad}
                            Integridad: {integridad}                              
                            Disponibilidad: {disponibilidad}
                            Considera que la clasificacion es correcta?
                            Desde ya muchas gracias,
                            Saludos coridales.""").format(baseDeDatos=baseDeDatos,confidencialidad = confidencialidad,integridad = integridad,disponibilidad=disponibilidad)
                            msg = f"Subject: {subject}\n\n{body}"
                            smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                            smtp.sendmail(EMAIL_ADDRESS,elemento["user_manager"],msg) #(sender, receivers, message)
                else:
                    print("El usuario no esta activo, por favor validar")
