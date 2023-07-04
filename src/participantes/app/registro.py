from flask import Flask, request, jsonify, redirect, url_for, render_template, flash

import json

from config import _blockchain, _configuration, _credential
from functions import blockchain, credential, conexion_data, ip
from bd import BD
from cadena import Cadena
from nodo import Nodo
from sendmail import Correo

def registro_():
    if not blockchain():
        return redirect(url_for('scb'))
    if not credential():
        return redirect(url_for('newnodo'))

    if request.method == "GET":
        blockchain_ = Cadena()
        Signlist = blockchain_.bd_listfirma()
        return render_template('formregistro.html', datablockr=Signlist[::-1])

    elif request.method == "POST":
        # Registro de los datos del titulado
        register = request.form.to_dict()
        password = register['passw']
        register.pop('passw')
        database = BD(_credential)
        credential_ = database.abrir_archivo()
        nodo = Nodo(credential_)
        requirement = nodo.crear_titulo(register, password)
        # Filtros
        if requirement == "Duplicado":
            flash("No registrado, ya existe un egresado registrado")
            return redirect(request.url)
        if requirement == "No es posible ejecutar proceso":
            flash("No es posible ejecutar proceso")
            return redirect(request.url)
        # Paso los filtros
        email = request.form['email']
        hashU = requirement
        # Envio correo si se activa el evento
        mail = Correo(email, hashU)
        mail.sendEmail()
        del mail
        blockchain_ = Cadena()
        blockchain_data = blockchain_.chain
        lastblock = blockchain_data[-1]
        package = {'addblock': json.dumps(lastblock)}
        # Obtengo la lista de nodos
        database = BD(_configuration)
        config = database.abrir_archivo()  # Lista de nodos ["nodos"]
        # Replicar bloque
        cant = 0
        if len(config["nodos"]) > 1:
            for node in config["nodos"]:
                if node['ip'] != ip():
                    response = conexion_data(
                        node['ip'], "5000", "addblock", "get", package)
                    if response['Respuesta'] == 'OK':
                        cant += 1
        if cant == (len(config["nodos"])-1):
            flash("Egresado registrado con exito y replicado a los nodos")
            return redirect(request.url)
        flash("No se pudo replicar el registro a los nodo")
        return redirect(request.url)
    else:
        return 'Metodos no aceptados'