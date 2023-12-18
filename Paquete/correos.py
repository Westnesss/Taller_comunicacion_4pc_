import smtplib

class AlertasCorreo:
    @staticmethod
    def enviar_alerta_porcentaje_cpu(porcentaje):
        if porcentaje > 40:
            message = 'El porcentaje del CPU es superior al 40%'
            subject = 'Alerta de rendimiento'
            message = 'Subject: {}\n\n{}'.format(subject, message)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('BryanDaviid333@gmail.com', 'ffco lbue izbz ryeh')
            server.sendmail('BryanDavid333@gmail.com', 'davidchalan54@gmail.com', message)
            server.quit()
            print('Correo enviado de manera exitosa')