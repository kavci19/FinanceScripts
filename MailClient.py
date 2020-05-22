import smtplib, ssl

def send_mail(stockName):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = #insert sender email address
    receiver_email = #insert recepient email address
    password = #insert sender email password
    message = "Invest in " + stockName + "!"


    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
