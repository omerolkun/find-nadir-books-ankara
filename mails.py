import smtplib, ssl
from info import info

def mailahmet(mesaz):
    sender_email = info()[1][0]
    receiver_email = info()[1][1]
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    password = "ekax nbuc iqpo ttvm"
    message = mesaz

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
