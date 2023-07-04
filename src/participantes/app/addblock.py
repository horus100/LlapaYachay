from flask import Flask, request, jsonify
import json

from cadena import Cadena

def addblock_():
    try:
        block = json.loads(request.form['addblock'])
        blockchain = Cadena()
        blockchain.añadir_bloque(block)
        return jsonify({'Respuesta':'OK'})
    except Exception as e:
        return jsonify({'Respuesta':'No','Mensaje': str(e)})