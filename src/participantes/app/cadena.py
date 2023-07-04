import json
import cryptografy
from pathlib import Path
import bloque
import bd
import contrato
import json
import datetime
from config import _blockchain, _credential


class Cadena():
    def __init__(self):
        if self.okchain() is True:
            url = str(_blockchain)
            with open(url) as f:
                jblock = json.load(f)
            self.chain = jblock
        else:
            self.chain = []

    def okchain(self):
        url = _blockchain
        if (Path(url).is_file()):
            return True
        else:
            return False

    def okcredencial(self):
        url = '/home/nodo/BD/Blockchain/credencial.json'
        if (Path(url).is_file()):
            return True
        else:
            return False

    def cadena(self):
        return self.chain

    def crear_bloque(self, hash_anterior, contract, registro, credencial, totalbloques, clave=None):
        # se puede agregar las caracteristicas que se quiera en el bloque
        Crypto = cryptografy.Crypto(credencial['Rol'], clave)
        metadata = {'index': totalbloques+1,
                    'estado': str(1),
                    'timestamp': str(datetime.datetime.now()),
                    'CA': Crypto.hash(credencial),
                    'previous_hash': hash_anterior,
                    'hash_Dato': Crypto.hash(registro)}  # HASH
        block = {
            'metadata': metadata,
            'smartcontract': contract,
            'registro': registro
        }
        hashblock = Crypto.hash(block)
        if credencial['Rol'] != "System":
            firmahash = Crypto.firmar(hashblock)  
        else:
            firmahash = "system"
        metablock = {
            'hash0': firmahash,
            'hash1': hashblock,
            'actor': credencial['Rol'],
            'block': {  
                'metadata': metadata,
                'smartcontract': contract,
                'registro': registro}
        }
        return metablock

    def crear_genesis(self, config):
        BD = bd.BD(_blockchain)
        contrato = {
            'actor principal': 'ninguno',
            'rol actor': 'ninguno',
            'escritura': 'es un bloque genesis'
        }
        credencial = {'Nombres': 'Genesis', 'Apellidos': 'System',
                      'DNI': 'ninguno', 'Rol': 'System'}
        registro = config
        block = bloque.Bloque('0', contrato, registro, credencial, 0)
        self.añadir_bloque(block.crear_bloque())
        return BD.guardar_archivo(self.chain)

    def previo_bloque(self):
        block = self.chain[-1]
        return block['block']

    def anterior_hash(self):
        block = self.chain[-1]
        return block['hash1']

    def añadir_bloque(self, block):
        BD = bd.BD(_blockchain)
        self.chain.append(block)
        BD.guardar_archivo(self.chain)

    def verificar_cadena(self):
        chain = self.chain
        previous_block = chain[0]
        previous_block = previous_block['block']
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            nombre = block['actor']
            firma = block['hash0']
            hashb = block['hash1']
            Crypto = cryptografy.Crypto(nombre, None, firma)
            if Crypto.autenticar(hashb) is True:
                if block['block']['metadata']['previous_hash'] != Crypto.hash(previous_block):
                    return False
            else:
                return False
            previous_block = block['block']
            block_index += 1
        return True

    def verificar_credencial(self, a1):
        try:
            verify = False
            blocks = len(self.chain)
            cadenatemporal = self.chain
            for i in range(blocks):
                leer = cadenatemporal[i]
                data = leer['block']['registro']
                if 'DNI' in data and 'Rol' in data:
                    if (leer['block']['registro']['DNI'] == a1['DNI'] and leer['block']['registro']['Rol'] == a1['Rol']):
                        verify = True
                        break
            return verify
        except Exception as e:
            return {'Respuesta': 'No', 'Mensaje': str(e)+" ccp"}

    def verificar_duplicado(self, DNI):
        chain = self.chain
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            data = block['block']['registro']
            if "DNI" in data:
                if block['block']['registro']['DNI'] == DNI:
                    return True
            block_index += 1
        return False

    def verificar_rol_duplicado(self, registro):
        chain = self.chain
        block_index = 0
        while block_index < len(chain):
            block = chain[block_index]
            data = block['block']['registro']
            if "Rol" in data:
                if block['block']['registro']['Rol'] == registro['Rol']:
                    return True
            block_index += 1
        return False

    def firmas_asociadas(self, hashdato, role=""):
        chain = self.chain
        firmas = []
        block_index = 0
        firma=False
        while block_index < len(chain):
            block = chain[block_index]
            data = block['block']['registro']
            if "Card" in data:
                if block['block']['registro']['Card'] == hashdato:
                    firmas.append(block)
                    firma = role == block['block']['registro']['RolFirma']
            block_index += 1
        if role != "":
            return firmas, firma
        return firmas

    def verificar_firma(self, credencial, hashdato):
        is_valid_credential = self.verificar_credencial(credencial)
        is_valid_chain = self.verificar_cadena()
        existe_tarjeta = self.consulta(hashdato)
        if is_valid_chain and is_valid_credential and existe_tarjeta:
            return True
        return False

    def consulta(self, hashdato):
        chain = self.chain
        block_index = 1
        result = False
        for block_index in range(len(chain)):
            block = chain[block_index]
            if block['block']['metadata']['hash_Dato'] == hashdato:
                result = True
                break
        return result

    def consulta_datos(self, hashdato):
        chain = self.chain
        block_index = 1
        result = False
        for block_index in range(len(chain)):
            block = chain[block_index]
            if block['block']['metadata']['hash_Dato'] == hashdato:
                result = block
                break
        return result

    def bd_listfirma(self):
        bc = self.cadena()
        bd_lf = []
        block_index = 0
        while block_index < len(bc):
            block = bc[block_index]
            data = block['block']['registro']
            if "Rol" in data:

                if block['block']['registro']['Rol'] == "Egresado":
                    #   sign=self.firmas_asociadas(block['block']['metadata']['hash_Dato'])
                    dbase = bd.BD(_credential)
                    nodo = dbase.abrir_archivo()
                    del dbase
                    sign = self.firmas_asociadas(
                        block['block']['metadata']['hash_Dato'], nodo["Rol"])
                    fbd = {
                        'index': block['block']['metadata']['index'],
                        'Nombre': block['block']['registro']['Nombre'],
                        'DNI': block['block']['registro']['DNI'],
                        'CP': block['block']['registro']['Carrera Profesional'],
                        'Grado': block['block']['registro']['Grado'],
                        'YearE': block['block']['registro']['Year de egreso'],
                        'hash_Dato': block['block']['metadata']['hash_Dato'],
                        'cantf': str(len(sign[0])),
                        'firma': sign[1],
                    }
                    bd_lf.append(fbd)
            block_index += 1
        return bd_lf
