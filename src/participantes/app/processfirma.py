from flask import  request,  redirect, url_for, flash,jsonify

import json

from config import _credential, _configuration
from functions import conexion_data
from bd import BD
from cadena import Cadena
from ips import Ip
from nodo import Nodo
from sendmail import Correo
from titulo import Titulo

def Processfirma_():
    if request.method == 'POST':
        # Obtener la credencial
        database = BD(_credential)
        credential = database.abrir_archivo()
        signhash = request.form['hash']  # Hash del bloque a firmar
        password = request.form['passw']
        data = {'credencial': credential, 'hash': signhash}
        ##############################################
        # Procesamieto de firma
        blockchain = Cadena()
        database = BD(_configuration)
        config = database.abrir_archivo()
        listN = config["nodos"]# Lista de nodos
        solicitud = "SI"
        if len(listN) > 1:
            ip = Ip(listN)
            data['ipenvio'] = ip.ip()
            package ={"data":json.dumps(data)}
            ip_elegido = ip.sort_node_consesous()
            solicitud = conexion_data(ip_elegido, "5000", "consensofirma", "get", package)
            solicitud = solicitud["Respuesta"]
        if solicitud != "SI":
            flash("Ocurr(io un error en el concenso")
            return redirect(url_for('firma'))
            
        node = Nodo(credential)
        block = node.firmar(signhash, password)
        if block[0] is True:
            data = {'addblock': json.dumps(block[1])}
            # Replicar bloque a los nodos participantes y publicos
            cant = 1
            if len(listN) > 1:
                for node in listN:
                    if node['ip'] != ip.ip():
                        response = conexion_data(node['ip'], "5000", "addblock", "get", data)
                        if response['Respuesta'] == 'OK':
                            cant += 1
            if cant == (len(listN)): #Se resta uno porque no se repite la replica del bloque en el mismo nodo
                #Ver si tiene firmas completas para enviar el correo de registro completo en la blockchain
                del blockchain
                blockchain=Cadena() #actualizo instancia
                signhash=block[1]['block']['registro']['Card']
                totalsign=blockchain.firmas_asociadas(signhash)
                mensaje="se firmo correctamente el registro firmas asociadas: "+str(len(totalsign))+str(config["qty"])
                if str(len(totalsign))==config["qty"]:
                    registro=blockchain.consulta_datos(signhash)
                    email=registro['block']['registro']['email']            
                    nombre=registro['block']['registro']["Nombre"]
                    facultad=registro['block']['registro']["Carrera Profesional"]
                    grado=registro['block']['registro']["Grado"]
                    host=config["DNS"]
                    titulo=Titulo(email,nombre,grado,facultad,signhash,host)
                    archivo=titulo.construir1()
                    mail=Correo(email,signhash,archivo)
                    mail.sendEmail()
                    mensaje="se firmo correctamente el registro y se envio el titulo"
                flash(mensaje)
                return redirect(url_for('firma'))
            flash("Ocurrio un error en la replica de bloques")
            return redirect(url_for('firma'))
        else:
            flash("El concenso denego la solicitud porque dio respuesta el nodo concensuador de: "+print(block[1]))
             
            return redirect(url_for('firma'))