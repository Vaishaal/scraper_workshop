import smtplib
def send_email(body, toaddrs, subject):
    fromaddr = ''
    username = ''
    password = ''

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    headers = ["from: " + fromaddr,
            "subject: " + subject,
            "to: " + toaddrs,
            "mime-version: 1.0",
            "content-type: text/html"]
    headers = "\r\n".join(headers)
    server.sendmail(fromaddr, toaddrs, headers + "\r\n\r\n" + body)
    server.quit()
