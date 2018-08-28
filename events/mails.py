from simple_mail.mailer import BaseSimpleMail, simple_mailer


class WelcomeMail(BaseSimpleMail):
    email_key = 'welcome'


simple_mailer.register(WelcomeMail)
