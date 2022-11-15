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
#ENVIO DE CORREO ELECTRONICO PARA CONSULTAR INFO 
for registro in data ["db_list"]:
   #Verifico los campos del archivo json para saber si poseen infromacion, si les falta, la consulto
    if registro["dn_name"] == "":
        with smtplib.SMTP_SSL("smtp.gmail.com", 465,context=context) as smtp:
                integridad = (registro["classification"]["integrity"])
                disponibilidad=(registro["classification"]["availability"])
                confidencialidad = (registro["classification"]["confidentiality"])
                owner=(registro["owner"]["name"])
                baseDeDatos=(registro["dn_name"])
                subject=("IMPORTANTE: Falta de informacion sobre Base de datos")
                body=("""
Hola, que tal?
Identificamos una base de datos perteneciente a {owner}, sin embargo no poseemos el nombre de la misma, a continuacion se detalla mas infromacion:
Nombre de la Base de datos: --
Owner: {owner}
Clasificacion:
    Confidencialidad: {confidencialidad}
    Integridad: {integridad}                              
    Disponibilidad: {disponibilidad}
Por favor, nos podria indicar el nombre de la base de datos?
En caso de presentarse algun inconveniente, contactarse con el equipo de Data Security.

Desde ya muchas gracias,
Saludos
                """).format(owner=owner,baseDeDatos=baseDeDatos,confidencialidad = confidencialidad,integridad = integridad,disponibilidad=disponibilidad)
                msg3 = f"Subject: {subject}\n\n{body}"
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.sendmail(EMAIL_ADDRESS,registro["owner"]["email"],msg3) #(sender, receivers, message)
    else:
        print("\nNombre de la Data Base: {}".format(registro["dn_name"]))

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
                if registro["owner"]["email"]==""or registro["email"]=="":
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465,context=context) as smtp:
                        integridad = (registro["classification"]["integrity"])
                        disponibilidad=(registro["classification"]["availability"])
                        confidencialidad = (registro["classification"]["confidentiality"])
                        owner=(registro["owner"]["name"])
                        baseDeDatos=(registro["dn_name"])
                        subject=("IMPORTANTE: Falta de informacion sobre Base de datos")
                        body=("""
Hola, que tal?
Identificamos una base de datos perteneciente a {owner}, sin embargo no encontramos el correo electronico del usuario, a continuacion le brindamos infromacion sobre la base de datos:
Nombre de la Base de datos:{baseDeDatos}
Owner: {owner}
Clasificacion:
    Confidencialidad: {confidencialidad}
    Integridad: {integridad}                              
    Disponibilidad: {disponibilidad}
Por favor, nos podria indicar el correo del colaborador?
En caso de presentarse algun inconveniente, contactarse con el equipo de Data Security.

Desde ya muchas gracias,
Saludos
                    """).format(owner=owner,baseDeDatos=baseDeDatos,confidencialidad = confidencialidad,integridad = integridad,disponibilidad=disponibilidad)
                        msg4 = f"Subject: {subject}\n\n{body}"
                        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                        smtp.sendmail(EMAIL_ADDRESS,elemento["user_manager"],msg4) #(sender, receivers, message)
           
                if registro["classification"]["confidentiality"]=="" or registro["classification"]["integrity"]=="" or registro["classification"]["availability"]=="":
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465,context=context) as smtp:
                        integridad = (registro["classification"]["integrity"])
                        disponibilidad=(registro["classification"]["availability"])
                        confidencialidad = (registro["classification"]["confidentiality"])
                        owner=(registro["owner"]["name"])
                        baseDeDatos=(registro["dn_name"])
                        subject=("IMPORTANTE: Falta de informacion sobre Base de datos")
                        body=("""
Hola, que tal?
Identificamos una base de datos perteneciente a {owner}, sin embargo nos faltan datos sobre la clasificacion de la misma, a continuacion se detalla mas infromacion:
Nombre de la Base de datos:{baseDeDatos}
Owner: {owner}
Clasificacion:
    Confidencialidad: {confidencialidad}
    Integridad: {integridad}                              
    Disponibilidad: {disponibilidad}
Por favor, nos podria indicar la clasificacion faltantes?
En caso de presentarse algun inconveniente, contactarse con el equipo de Data Security.

Desde ya muchas gracias,
Saludos
                    """).format(owner=owner,baseDeDatos=baseDeDatos,confidencialidad = confidencialidad,integridad = integridad,disponibilidad=disponibilidad)
                        msg1 = f"Subject: {subject}\n\n{body}"
                        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                        smtp.sendmail(EMAIL_ADDRESS,registro["owner"]["email"],msg1) #(sender, receivers, message)
        
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