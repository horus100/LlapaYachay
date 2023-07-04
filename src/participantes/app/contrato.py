import cadena
import datetime
class Contrato():
    def __init__(self,credencial):
        self.card=credencial
    def smartcontract(self):
        Cadena=cadena.Cadena()
        req1= Cadena.verificar_credencial(self.card)
        req2= Cadena.verificar_cadena()
        if req1 and req2:
            return True,self.generar_contrato(self.card,'Titulo generado')
        else:
            return False,self.cancelar_proceso()

    # Funcion generar contrato
    def generar_contrato(self,a1,escritura):
        smartcontract= {
                'timesello':str(datetime.datetime.now()),
                'actor principal':str(a1['Nombre']+" "+a1['Apellido']),
                'rol actor':str(a1['Rol']),
                'escritura':escritura}
        return smartcontract
    # Funcion cancelar proceso
    def cancelar_proceso(self):
        return "No es posible ejecutar proceso"

 