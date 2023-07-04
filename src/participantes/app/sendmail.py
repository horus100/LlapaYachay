import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os

correo_Asunto = "Creacion Hash del Titulo Profesional"

class Correo():
    def __init__(self,dest,hash,archivo=None,asunto=correo_Asunto):
        self.smtpHost="smtp.gmail.com"
        self.smtpPort=587
        self.mailUname = 'bcproject2022@gmail.com'
        self.mailPwd = 'bpgkcjeukdbrcfya'
        self.fromEmail = 'bcproject2022@gmail.com'
        self.asunto=asunto
        self.hash=hash
        self.msgtexto="En este mensaje, enviamo el codigo hash <br/>  <b>"+hash+"</b> , con el podra consultar su Titulo a partir hoy y su progreso de firmado"
        self.destinatario=dest
        self.archivo=archivo

    def sendEmail(self):
        # create message object
        msg = MIMEMultipart()
        msg['From'] = self.fromEmail
        msg['To'] = self.destinatario
        msg['Subject'] = self.asunto
        # msg.attach(MIMEText(mailContentText, 'plain'))
        msg.attach(MIMEText(self.msgtexto, 'html'))

        # create file attachments
        if not self.archivo is None:
            # check if file exists
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(self.archivo, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{0}"'.format(os.path.basename(self.archivo)))
            msg.attach(part)

        # Send message object as email using smptplib
        s = smtplib.SMTP(self.smtpHost, self.smtpPort)
        s.starttls()
        s.login(self.mailUname, self.mailPwd)
        msgText = msg.as_string()
        sendErrs = s.sendmail(self.fromEmail, self.destinatario, msgText)
        s.quit()

        # check if errors occured and handle them accordingly
        if not len(sendErrs.keys()) == 0:
            raise Exception("Errors occurred while sending email", sendErrs)
        return