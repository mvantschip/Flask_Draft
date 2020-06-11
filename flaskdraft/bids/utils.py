from flask import render_template
from flaskdraft import mail
from flask_mail import Message

def send_mail(form_bids, recipient, recipient_email):
    msg = Message("[Gorro FM Draft] Hoger bod geplaatst!",
    sender = ("Gorro FM Draft Commissie" ,"gorrofmdraft@mailbox.org"),
    recipients = [recipient_email])
    msg.html = render_template('email.html', form_bids = form_bids, recipient = recipient)
    mail.send(msg)
