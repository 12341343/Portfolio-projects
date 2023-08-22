import smtplib
MY_EMAIL = "YOUR EMAIL"
PASSWORD = "YOUR PASSWORD"

class Mail_sender:
    def __init__(self):
        self.email = MY_EMAIL
        self.password = PASSWORD
    def send_mail(self, name, mail, phone, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(
                from_addr=self.email,
                to_addrs=self.email,
                msg=f"Subject:New user reached you\n\nName: {name}\nMail: {mail}\nPhone: {phone}\nMessage: {message}"
            )
