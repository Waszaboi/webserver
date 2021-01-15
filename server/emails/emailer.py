import smtplib
from .models import Email

from . import url

base_url = url.base_url

def send_verification(email):
    gmail_user = 'szabi.heal@gmail.com'
    gmail_password = 'healgmailjelszo'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail("szabi.heal@gmail.com", email, bytes("Subject:Sikeres regisztráció\nSikeresen feliratkoztál a teszt szerver hírlevelére.\nLeiratkozás: " + base_url + "/unsubscribe/?email=" + email, "iso8859_2"))
    server.close()

def send_to_everyone():
    emails = map(lambda x: x["email"], Email.objects.values())

    gmail_user = 'szabi.heal@gmail.com'
    gmail_password = 'healgmailjelszo'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login(gmail_user, gmail_password)
    for email in emails:
        server.sendmail("szabi.heal@gmail.com", email, bytes("Subject:Email mindenkinek\nEz az email minden feljegyzett email címre el lett küldve\nLeiratkozás: " + base_url + "/unsubscribe/?email=" + email, "iso8859_2"))
    server.close()
