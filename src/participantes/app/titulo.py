from PIL import Image, ImageDraw, ImageFont
import qrcode

class Titulo():
    def __init__(self,codigo,nombre,grado,facultad,hash,host, letra="app/biblioteca/titulos/config/letra.otf"):
        self.alumno=nombre
        self.grado=grado
        self.facultad=facultad
        self.hash=hash
        self.host=host
        self.codigo=codigo
        self.letra=letra

    def qr(self):
        input ="http://"+self.host+":5005/search/"+self.hash
        qr=qrcode.QRCode(version=1,box_size=10,border=1)
        qr.add_data(input)
        qr.make(fit=True)
        img=qr.make_image(fill='black',back_color='white')
        return img
    
    def escritura(self,image_width,constructor,escritura,letra,tamañodeletra,coordenadaY):
        color_texto = (0,137,209)
        tipo_letra = ImageFont.truetype(letra, tamañodeletra)
        text_width, _ = constructor.textsize(escritura, font = tipo_letra)
        coordenadas = ((image_width - text_width)/2, coordenadaY)
        constructor.text(coordenadas,escritura ,fill=color_texto, font=tipo_letra)
        
    def construir1(self):
        certificado = Image.open("app/biblioteca/titulos/config/modelo.jpg", mode ='r') 
        qr=self.qr()
        new_qr = qr.resize((204,204))
        image_width =  certificado.width 
        constructor = ImageDraw.Draw(certificado)
        self.escritura(image_width,constructor,self.grado,self.letra,30,340)
        self.escritura(image_width,constructor,self.alumno,self.letra,45,480)
        self.escritura(image_width,constructor,self.facultad,self.letra,30,660)
        certificado.paste(new_qr,(725,944)) 
        certificado.save("app/biblioteca/titulos/"+self.codigo+".pdf")
        ruta="app/biblioteca/titulos/"+self.codigo+".pdf"
        return ruta