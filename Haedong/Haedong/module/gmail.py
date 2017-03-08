# -*- coding: utf-8 -*-
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText

def send_email(subject, contents , account=None):  
    from_addr = 'haedong2017@gmail.com'
    
    if account == None:
        to_addr = 'genioustar@gmail.com,hayden4143@gmail,junhwanu@gmail.com'
    elif account == '5107243872' or account == '7003919272':
        to_addr = 'hayden4143@gmail'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()

    server.login(from_addr, 'goehddl00')

    body = MIMEMultipart()
    body['subject'] = subject
    body['From'] = from_addr
    body['To'] = to_addr

    html = ("<div>%s</div>" % contents)
    msg = MIMEText(html, '')
    body.attach(msg)

    server.sendmail(from_addr=from_addr,
                    to_addrs=[to_addr],  # list, str 둘 다 가능
                    msg=body.as_string())

    server.quit()