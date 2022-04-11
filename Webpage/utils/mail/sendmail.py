from utils.mail.createMails import createMail
import smtplib
from email.message import EmailMessage
import os

def sendMail(TO:str, mail: str):

    host        = os.environ["MAIL_Host"]
    FROM        = os.environ["MAIL_Username"]

    try:
        em = EmailMessage()
        em.set_content(mail)
        em['To'] = TO
        em['From'] = FROM
        em['Subject'] = "Neue Website für den ASV Aachen"

        server = smtplib.SMTP(host, 25)
        server.send_message(em)

        server.quit()
    except Exception as e:
        print(e)
        print("Error: unable to send email")

    return
