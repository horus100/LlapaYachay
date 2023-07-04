from config import _configuration,_blockchain,_credential
from functions import blockchain, credential

from flask import Flask, redirect, url_for, request,render_template
import os
import json

from bd import BD
from cadena import Cadena


def setup_():
    if blockchain():
        if credential():
            return redirect(url_for('inicio'))
        return redirect(url_for('newnodo'))
    if request.method=="GET":
        return render_template('crearbc.html')
    if request.method=="POST":
        data=request.form.to_dict()
        #crea un json con los datos de la red blockchain
        database=BD(_configuration)
        config={}
        config['DNS']=data['DNS']
        config['Nombre']=data['Nombre de red']
        config['estado']="1"
        config['qty']=data["qtynodos"]
        config['nodos']=[]
        database.guardar_archivo(config)
        del database
        # Crear el bloque genesis y añadirlo
        database=BD(_blockchain)
        contract={
                'actor principal':'ninguno',
                'rol actor':'ninguno',
                'escritura':'es un bloque genesis'
            }
        card={'Nombres':'Genesis','Apellidos':'System', 'DNI':'ninguno','Rol':'System'}
        register=data
        cadena=Cadena()
        block = cadena.crear_bloque('0',contract,register,card,0)
        cadena.añadir_bloque(block)
        database.guardar_archivo(cadena.chain)
        return redirect(url_for('newnodo'))

    