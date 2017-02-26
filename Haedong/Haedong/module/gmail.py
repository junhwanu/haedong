# -*- coding: utf-8 -*-
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText

def send_email(subject, contents):  
    from_addr = 'haedong2017@gmail.com'
    to_addr = 'junhwanu@gmail.com'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()

    server.login(from_addr, 'goehddl00')

    body = MIMEMultipart()
    body['subject'] = subject
    body['From'] = from_addr
    body['To'] = to_addr

    html = ("<div>%s</div>" % contents)
    msg = MIMEText(html, 'html')
    body.attach(msg)

    server.sendmail(from_addr=from_addr,
                    to_addrs=[to_addr],  # list, str 둘 다 가능
                    msg=body.as_string())

    server.quit()