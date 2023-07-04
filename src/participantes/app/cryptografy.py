import io
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from hashlib import sha256
import json

class Crypto():
    def __init__(self,nombre,clave=None,data=None):
        self.nombre=nombre
        self.clave=clave
        self.data=data
        
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return sha256(encoded_block).hexdigest()
        
    ###############################################
    ## CREAR LLAVES ###############################
    ###############################################

    def generarkeys( self):
        key = RSA.generate(2048)
        private_key = key.export_key(passphrase=self.clave)
        with open("/home/nodo/keys/"+self.nombre+"-private.pem", "wb") as f:
            f.write(private_key)
        public_key = key.publickey().export_key()
        with open("/home/nodo/keys/"+self.nombre+"-public.pem", "wb") as f:
            f.write(public_key)


    ###############################################
    ## CIFRADO ####################################
    ###############################################

    def encriptar (self):
        bin_data = self.data.encode("utf-8")
        with open("/home/nodo/keys/"+self.nombre+"-public.pem", "rb") as f:
            recipient_key = f.read()
            key = RSA.importKey(recipient_key)   
        cipher_rsa = PKCS1_OAEP.new(key)
        aes_key = get_random_bytes(16)
        enc_aes_key = cipher_rsa.encrypt(aes_key)
        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(bin_data)
        enc_data = b"".join((enc_aes_key, cipher_aes.nonce, tag, ciphertext))
        return enc_data

    def decifrar(self):
        data_file = io.BytesIO(self.data)
        with open("/home/nodo/keys/"+self.nombre+"-private.pem", "rb") as f:
            recipient_key = f.read()
        key = RSA.importKey(recipient_key,  passphrase=self.clave)
        cipher_rsa = PKCS1_OAEP.new(key)
        enc_aes_key, nonce, tag, ciphertext =\
            (data_file.read(c) for c in (key.size_in_bytes(), 16, 16, -1))
        aes_key = cipher_rsa.decrypt(enc_aes_key)
        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        cadena = data.decode("utf-8")
        print(cadena)

    #############################################
    ## FIRMA ####################################
    #############################################

    def firmar(self,data_firmar):
        with open("/home/nodo/keys/"+self.nombre+"-private.pem", "rb") as f:
            recipient_key = f.read()
        key = RSA.importKey(recipient_key,passphrase=self.clave)
        msg=data_firmar.encode('utf-8') 
        hash = int.from_bytes(sha256(msg).digest(), byteorder='big')
        firma = pow(hash, key.d, key.n)
        return firma

    def autenticar(self,aut_block):
        with open("/home/nodo/keys/"+self.nombre+"-public.pem", "rb") as f:
            recipient_key = f.read()
        keyp = RSA.importKey(recipient_key) 
        block=aut_block.encode('utf-8')
        hash = int.from_bytes(sha256(block).digest(), byteorder='big')
        hashFromSignature = pow(self.data, keyp.e, keyp.n)
        return hash == hashFromSignature