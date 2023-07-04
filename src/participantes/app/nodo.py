import cadena
import ips
import bloque
import cryptografy
import bd
import contrato
import datetime

class Nodo():
    def __init__(self,credencial):
        self.clase_ip=ips.Ip()
        self.credencial=credencial
        self.private_ip=self.clase_ip.ip()
        self.rol=self.credencial['Rol']
        
    def registrar_credencial0(self,pw):
        Cadena=cadena.Cadena()
        duplicado= Cadena.verificar_duplicado(self.credencial['DNI'])
        if duplicado is False:
            self.registrar_credencial1(pw,'Crear credencial de Nuevo nodo')
            return True
        else:
            return False
        
    def registrar_credencial1(self,pw,escritura):
        Cadena=cadena.Cadena()
        hash_anterior=Cadena.anterior_hash()
        contract={
              'timesello':str(datetime.datetime.now()),
              'actor principal':str(self.credencial['Nombre']+" "+self.credencial['Apellido']),
              'rol actor':str(self.credencial['Rol']),
              'escritura':str(escritura)
          }
        block=bloque.Bloque()
        Cadena.añadir_bloque(block.crear_bloque(hash_anterior,contract,self.credencial,self.credencial,len(Cadena.cadena()),pw))


    def crear_titulo(self,registro,pw):
        Cadena=cadena.Cadena()
        contract=contrato.Contrato(self.credencial)
        accion=contract.smartcontract()
        duplicado= Cadena.verificar_duplicado(registro['DNI'])
        if accion[0] is True and duplicado is False:
            sc=accion[1]
            hash_anterior=Cadena.anterior_hash()
            block=bloque.Bloque()
            block=block.crear_bloque(hash_anterior,sc,registro,self.credencial,len(Cadena.cadena()),pw)
            Cadena.añadir_bloque(block)
            return block['block']['metadata']['hash_Dato']
        elif duplicado is True:
            return "Duplicado"
        else:
            return accion[1]
    
    def firmar(self,hashdato,passw):
        Cadena=cadena.Cadena()
        crypto=cryptografy.Crypto(None)
        contract=contrato.Contrato(self.credencial)
        accion=contract.smartcontract()
        existe_tarjeta=Cadena.consulta(hashdato)
        if accion[0] is True and existe_tarjeta is True:
            sc=accion[1]
            hash_anterior=Cadena.anterior_hash()
            registro={'Card':hashdato,'Firma':crypto.hash(self.credencial),'RolFirma':self.credencial['Rol']}
            block=bloque.Bloque()
            block=block.crear_bloque(hash_anterior,sc,registro,self.credencial,len(Cadena.cadena()),passw)
            Cadena.añadir_bloque(block)
            #print('operacion exitosa')
            return True,block
        else:
            return False,"No existe la tarjeta o algo ocurrio mal"

    def crear_llaves(self,pw):
        bdatos=bd.BD(None)
        bdatos.crear_carpeta("keys")
        crypto=cryptografy.Crypto(self.credencial['Rol'],pw)
        crypto.generarkeys()
    
