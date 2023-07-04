from config import _credential, _configuration, _path
from functions import credential, ip, conexion_data, blockchain

from flask import Flask, redirect, url_for, request,render_template, flash, jsonify
import json

from cadena import Cadena
from bd import BD
from cryptografy import Crypto
from nodo import Nodo


def newnodo_():
    if not blockchain():
        return redirect(url_for('scb'))
    if credential():
        return redirect(url_for('inicio'))
    if request.method=="GET":  
        blockchain_=Cadena()
        node_config=blockchain_.chain[0]
        del blockchain_
        return render_template('newcredencial.html',data=node_config['block']['registro'])
    if request.method=="POST":
        # Verifica que no registre un rol de la blockchain_ en uso
        datas=request.form.to_dict()
        blockchain_= Cadena()
        search_rol= blockchain_.verificar_rol_duplicado(datas)
        del blockchain_
        if search_rol is True:
            flash("No registrado, hay un nodo registrado con el mismo Nodo Peer")
            return redirect(request.url)
        password=datas['password']
        # Se crea la credencial del nodo en un JSON
        database=BD(_credential)
        datas.pop("password")
        datas.pop("password1")
        database.guardar_archivo(datas)
        keys=Crypto(datas["Rol"],password)
        keys.generarkeys()
        del database
        #Se verifica que no se esten registrando datos duplicados antes de registrar el nodo
        blockchain_= Cadena()
        duplicate= blockchain_.verificar_duplicado(datas['DNI'])
        if duplicate:
            flash("No registrado, ya hay un usuario registrado con los datos que ingreso ")
            return redirect(request.url)
        node=Nodo(datas)
        node.registrar_credencial1(password,'Crear credencial de Nuevo nodo')
        del blockchain_
        del node
        #Despues de los filtros, registrar el nodo en la lista de nodos de la configuracion
        database=BD(_configuration)
        config=database.abrir_archivo()#Lista de nodos ["nodos"]
        myip=ip()
        nododata={'hostname':datas["Rol"],'ip':myip}
        config["nodos"].append(nododata)
        database.guardar_archivo(config)
        resp=[]
        #Replica el registro del nodo a los demas nodos de la red
        if len(config["nodos"]) > 1:
            replicas = 1 # Se inicia en 1 porque cuenta el registro del propio nodo
            package = {'nododata': json.dumps(nododata)}
            for node in config["nodos"]:
                if node['ip'] == myip:
                    continue
                response=conexion_data(node['ip'],"5000","addnodo","post",data=package)
                if response['Respuesta'] == "OK":
                    replicas+=1 #contabiliza los nodos que registraron el nodo correctamente
            if replicas == len(config["nodos"]): #Si el total de nodos registraron sin problemas al nuevo nodo
                blockchain_= Cadena()
                block=blockchain_.chain[-1]
                package={'addblock':json.dumps(block)}
                replicas=1
                for node in config["nodos"]:
                    if node['ip']!=ip():
                        response=conexion_data(node['ip'],"5000","addblock","get",package)
                        if response['Respuesta']=='OK':
                            replicas+=1 
                if  replicas==len(config["nodos"]): 
                    with open(_path+"keys/"+request.form['Rol']+"-public.pem", "r") as f:
                        public = f.read()
                    package={'kp':public,'nk':request.form['Rol']} # kp es key public y nk es nodo key
                    #Intercambio de llaves, donde se envia la llave publica y se recepciona las llaves publicas de los nodos
                    for node in config["nodos"]:
                        key_public= conexion_data(node['ip'],"5000","exchangekey","get",package) 
                        with open(_path+"keys/"+key_public['name']+"-public.pem", "w") as f:
                            f.write(key_public['public'])
                    return redirect(url_for("inicio"))
                return "Se replico el registro del nodo, pero hubo un problema con la replica del bloque del registro"
            if replicas<len(config["nodos"]):
                return "algunos nodos no recibieron la informacion"
            return "ningun nodo recibio informacion"
        return redirect(url_for("inicio"))

