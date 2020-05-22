import smtplib, ssl

def send_mail(stockName):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "avci.investments@gmail.com"
    receiver_email = "avci.investment@gmail.com"
    password = "orhans311"
    message = "Invest in " + stockName + "!"


    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
