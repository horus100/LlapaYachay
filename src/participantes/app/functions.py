from pathlib import Path
import subprocess
import json
import requests

from config import _blockchain,_credential, _configuration


def blockchain():
    if (Path(_blockchain).is_file()):
        return True
    else:
        return False
    
def credential():
    if (Path(_credential).is_file()):
        return True
    else:
        return False
    
def ip():
    output = subprocess.check_output("hostname -i", shell=True)
    output=output.splitlines()
    output=output[0].decode("utf-8")
    return output


def conexion_data(to_ip, puerto, enlace, metodo, data=None):
    # Construir la URL para la solicitud HTTP
    url = f"http://{to_ip}:{puerto}/{enlace}"
    
    # Enviar solicitud HTTP GET
    if metodo == "get":
        try:
            res = requests.get(url, data=data)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.HTTPError as e:
            return {"Respuesta": "No", "Error": str(e)}
        except requests.exceptions.Timeout:
            return {"Respuesta": "No", "Error": "Timeout"}
        except requests.exceptions.RequestException as e:
            return {"Respuesta": "No", "Error": str(e)}
    
    # Enviar solicitud HTTP POST
    elif metodo == "post":
        try:
            res = requests.post(url, data=data)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.HTTPError as e:
            return {"Respuesta": "No", "Error": str(e)}
        except requests.exceptions.Timeout:
            return {"Respuesta": "No", "Error": "Timeout"}
        except requests.exceptions.RequestException as e:
            return {"Respuesta": "No", "Error": str(e)}
    
    # Manejar errores de método HTTP no reconocidos
    else:
        return {"Error": f"Método HTTP '{metodo}' no es válido."}


