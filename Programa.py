#coding:utf-8
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import time
import pyodbc
from os import getcwd
#print("ingrese url completa: ")
#url=input()
temp=""
temp2=""
temp3=""
temp4=""
DRIVER_NAME = "Microsoft Access Driver (*.mdb, *.accdb)"
DB_PATH ="M:/PanelControlFR_db.accdb"
try:
    #conexion con la base de datos
    conn = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH))
    cursor = conn.cursor()

    ######################################################################################
    #################################--NAVE A--###########################################
    ######################################################################################
    
    #consulta para leer el ultimo estado de la maquina (asi no genere dos registros iguales)
    cursor.execute("SELECT Tipo FROM Midato WHERE Linea = 'NB' ORDER BY id DESC")
    dato=cursor.fetchall()
    u=list(dato[0])
    if(u[0] == 'A'):
        temp="contando"
    else:
        temp="parado"

    #consulta para leer el ultimo estado de la maquina (asi no genere dos registros iguales)
    cursor.execute("SELECT Tipo FROM Midato WHERE Linea = 'CB' ORDER BY id DESC")
    dato=cursor.fetchall()
    u=list(dato[0])
    if(u[0] == 'A'):
        temp2="contando"
    else:
        temp2="parado"

    ######################################################################################
    #################################--NAVE B--###########################################
    ######################################################################################

    #consulta para leer el ultimo estado de la maquina (asi no genere dos registros iguales)
    cursor.execute("SELECT Tipo FROM Midato WHERE Linea = 'LB' ORDER BY id DESC")
    dato=cursor.fetchall()
    u=list(dato[0])
    if(u[0] == 'A'):
        temp3="contando"
    else:
        temp3="parado"

    #consulta para leer el ultimo estado de la maquina (asi no genere dos registros iguales)
    cursor.execute("SELECT Tipo FROM Midato WHERE Linea = 'CC' ORDER BY id DESC")
    dato=cursor.fetchall()
    u=list(dato[0])
    if(u[0] == 'A'):
        temp4="contando"
    else:
        temp4="parado"


    cursor.close()
    conn.close()
except:
    now = datetime.now()
    fecha = now.strftime('%d-%m-%Y')
    hora = now.strftime('%H:%M')
    print("Error de Conexion con la BDD, Tabla Nave A, Fecha: "+fecha+" Hora: "+hora)


print("Programa de registro automatico de parada de lineas, Usted esta ejecutando la version 3.1.1")

while(1):

    ######################################################################################
    #################################--NAVE A--###########################################
    ######################################################################################

    try:
        
        response = requests.get("http://10.0.0.28")
    
        response.encoding = "utf-8"
    
        response = requests.get("http://10.0.0.28")
    
        soup=BeautifulSoup(response.text,'html.parser')
        hola=soup.find_all("p")


        now = datetime.now()
        hora = now.strftime('%H')
        minutos = now.strftime('%M')

        if(hora == "06" and minutos == "00"): #verifico condicion de hora

        ########################################################################################
        ########################--creo registro de parada a las 6--#############################
        ########################################################################################

            conn = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH)) #me conecto con la BDD
            cursor = conn.cursor()
            cursor.execute("SELECT Tipo FROM Midato WHERE Linea = 'NB' ORDER BY id DESC") #verifico el ultimo estado de  NB (si estaba andando creo registro falso de parada, si no no hago nada)
            dato=cursor.fetchall()
            lestado=list(dato[0])
            if(lestado[0] == 'A' or lestado[0] == 'AD'):
                linea = "NB"  # si estaba andando genero registo de parada
                now = datetime.now()
                fecha = now.strftime('%d-%m-%Y')
                hora = now.strftime('%H:%M')
                estado="PD"
                cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
                u"horaE, horomtro) VALUES (?, ?, "
                "?, ?, ?)",
                linea, estado, fecha, hora, hola[1].contents[0])
                cursor.commit()

            cursor.execute("SELECT Tipo FROM Midato WHERE Linea = 'CB' ORDER BY id DESC") #verifico el ultimo estado de  CB (si estaba andando creo registro falso de parada, si no no hago nada)
            dato=cursor.fetchall()
            lestado1=list(dato[0])
            if(lestado1[0] == 'A' or lestado1[0] == 'AD'):
                linea = "CB"  # si estaba andando genero registo de parada
                now = datetime.now()
                fecha = now.strftime('%d-%m-%Y')
                hora = now.strftime('%H:%M')
                estado="PD"
                cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
                u"horaE, horomtro) VALUES (?, ?, "
                "?, ?, ?)",
                linea, estado, fecha, hora, hola[5].contents[0])
                cursor.commit()

        ########################################################################################
        ########################--creo registro de Arranque a las 6--###########################
        ########################################################################################

            if(lestado[0] == 'A' or lestado[0] == 'AD'): #verifico el estado de NB con el dato de la consulta de arriba para generar registro falso de arranque o, si estaba parada, no hacer nada
                linea = "NB"  # Nombre
                now = datetime.now()
                fecha = now.strftime('%d-%m-%Y')
                hora = now.strftime('%H:%M')
                estado="AD"
                cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
                u"horaE, horomtro) VALUES (?, ?, "
                "?, ?, ?)",
                linea, estado, fecha, hora, hola[1].contents[0])
                cursor.commit()

            if(lestado1[0] == 'A' or lestado1[0] == 'AD'): #idem con CB
                linea = "CB"  # Nombre
                now = datetime.now()
                fecha = now.strftime('%d-%m-%Y')
                hora = now.strftime('%H:%M')
                estado="AD"
                cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
                u"horaE, horomtro) VALUES (?, ?, "
                "?, ?, ?)",
                linea, estado, fecha, hora, hola[5].contents[0])
                cursor.commit()

            cursor.close()
            conn.close()


        ########################################################################################
        ###############################--Verifico estado de lineas--############################
        ########################################################################################



        if(hola[2].contents[0] != temp):
            temp=hola[2].contents[0]
            conn = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH))
            cursor = conn.cursor()

            linea = "NB"  # Nombre
            now = datetime.now()
            fecha = now.strftime('%d-%m-%Y')
            hora = now.strftime('%H:%M')

            if(hola[2].contents[0]=="contando"):
                estado="A"
            else:
                estado="P"

            cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
            u"horaE, horomtro) VALUES (?, ?, "
            "?, ?, ?)",
            linea, estado, fecha, hora, hola[1].contents[0])
            cursor.commit()
            cursor.close()
            conn.close()


        if(hola[6].contents[0] != temp2):
            temp2=hola[6].contents[0]

            conn = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH))
            cursor = conn.cursor()

            linea = "CB"  # Nombre
            now = datetime.now()
            fecha = now.strftime('%d-%m-%Y')
            hora = now.strftime('%H:%M')

            if(hola[6].contents[0]=="contando"):
                estado="A"
            else:
                estado="P"

            cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
            u"horaE, horomtro) VALUES (?, ?, "
            "?, ?, ?)",
            linea, estado, fecha, hora, hola[5].contents[0])
            cursor.commit()
            cursor.close()
            conn.close()

        
    except:
        now = datetime.now()
        fecha = now.strftime('%d-%m-%Y')
        hora = now.strftime('%H:%M')
        print("Error de Conexion con el Sistema de la Nave A, Revisar en la Linea, PIN0 NB, PIN2 CB, Fecha: " +fecha+ " ,Hora: "+hora)

    
    ######################################################################################
    #################################--NAVE B--###########################################
    ######################################################################################

    try:
        
        response = requests.get("http://10.0.0.27")
    
        response.encoding = "utf-8"
    
        response = requests.get("http://10.0.0.27")
    
        soup=BeautifulSoup(response.text,'html.parser')
        hola=soup.find_all("p")


        now = datetime.now()
        hora = now.strftime('%H')
        minutos = now.strftime('%M')

        if(hora == "06" and minutos == "00"): #verifico condicion de hora

        ########################################################################################
        ########################--creo registro de parada a las 6--#############################
        ########################################################################################

            conn = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH)) #me conecto con la BDD
            cursor = conn.cursor()
            cursor.execute("SELECT Tipo FROM Midato WHERE Linea = 'LB' ORDER BY id DESC") #verifico el ultimo estado de  NB (si estaba andando creo registro falso de parada, si no no hago nada)
            dato=cursor.fetchall()
            lestado=list(dato[0])
            if(lestado[0] == 'A' or lestado[0] == 'AD'):
                linea = "LB"  # si estaba andando genero registo de parada
                now = datetime.now()
                fecha = now.strftime('%d-%m-%Y')
                hora = now.strftime('%H:%M')
                estado="PD"
                cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
                u"horaE, horomtro) VALUES (?, ?, "
                "?, ?, ?)",
                linea, estado, fecha, hora, hola[1].contents[0])
                cursor.commit()

            cursor.execute("SELECT Tipo FROM Midato WHERE Linea = 'CC' ORDER BY id DESC") #verifico el ultimo estado de  CB (si estaba andando creo registro falso de parada, si no no hago nada)
            dato=cursor.fetchall()
            lestado1=list(dato[0])
            if(lestado1[0] == 'A' or lestado1[0] == 'AD'):
                linea = "CC"  # si estaba andando genero registo de parada
                now = datetime.now()
                fecha = now.strftime('%d-%m-%Y')
                hora = now.strftime('%H:%M')
                estado="PD"
                cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
                u"horaE, horomtro) VALUES (?, ?, "
                "?, ?, ?)",
                linea, estado, fecha, hora, hola[5].contents[0])
                cursor.commit()

        ########################################################################################
        ########################--creo registro de Arranque a las 6--###########################
        ########################################################################################

            if(lestado[0] == 'A' or lestado[0] == 'AD'): #verifico el estado de NB con el dato de la consulta de arriba para generar registro falso de arranque o, si estaba parada, no hacer nada
                linea = "LB"  # Nombre
                now = datetime.now()
                fecha = now.strftime('%d-%m-%Y')
                hora = now.strftime('%H:%M')
                estado="AD"
                cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
                u"horaE, horomtro) VALUES (?, ?, "
                "?, ?, ?)",
                linea, estado, fecha, hora, hola[1].contents[0])
                cursor.commit()

            if(lestado1[0] == 'A' or lestado1[0] == 'AD'): #idem con CB
                linea = "CC"  # Nombre
                now = datetime.now()
                fecha = now.strftime('%d-%m-%Y')
                hora = now.strftime('%H:%M')
                estado="AD"
                cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
                u"horaE, horomtro) VALUES (?, ?, "
                "?, ?, ?)",
                linea, estado, fecha, hora, hola[5].contents[0])
                cursor.commit()

            cursor.close()
            conn.close()

        ########################################################################################
        ###############################--Verifico estado de lineas--############################
        ########################################################################################

        if(hola[2].contents[0] != temp3):
            temp3=hola[2].contents[0]
            conn = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH))
            cursor = conn.cursor()

            linea = "LB"  # Nombre
            now = datetime.now()
            fecha = now.strftime('%d-%m-%Y')
            hora = now.strftime('%H:%M')

            if(hola[2].contents[0]=="contando"):
                estado="A"
            else:
                estado="P"

            cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
            u"horaE, horomtro) VALUES (?, ?, "
            "?, ?, ?)",
            linea, estado, fecha, hora, hola[1].contents[0])
            cursor.commit()
            cursor.close()
            conn.close()


        if(hola[6].contents[0] != temp4):
            temp4=hola[6].contents[0]

            conn = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH))
            cursor = conn.cursor()

            linea = "CC"  # Nombre
            now = datetime.now()
            fecha = now.strftime('%d-%m-%Y')
            hora = now.strftime('%H:%M')

            if(hola[6].contents[0]=="contando"):
                estado="A"
            else:
                estado="P"

            cursor.execute(u"INSERT INTO Midato (Linea, Tipo, FechaE, "
            u"horaE, horomtro) VALUES (?, ?, "
            "?, ?, ?)",
            linea, estado, fecha, hora, hola[5].contents[0])
            cursor.commit()
            cursor.close()
            conn.close()

        
    except:
        now = datetime.now()
        fecha = now.strftime('%d-%m-%Y')
        hora = now.strftime('%H:%M')
        print("Error de Conexion con el Sistema de la Nave B, Revisar en la Linea, PIN0 LB, PIN2 CC, Fecha: " +fecha+ " ,Hora: "+hora)
        
    


    time.sleep(60)  






