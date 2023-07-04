import json
import subprocess
 
def almacenar (archivo,nombre):
  with open('config/'+nombre+'.json', 'w') as f:
    jblock=json.dump(archivo,f)
  return jblock

def ip():
    output = subprocess.check_output("hostname -i", shell=True)
    output=output.splitlines()
    output=output[0].decode("utf-8")
    return output