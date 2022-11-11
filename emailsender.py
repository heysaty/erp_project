#
# from email.message import EmailMessage
# import ssl
# import smtplib
# from config import settings
#
#
# def send_the_mail(email_receiver, msg):
#     email_sender = "kumarsatyam035@gmail.com"
#     password = settings.EMAIL_TOKEN
#
#     cc = "satyam@gkmit.co"
#
#     subject = "Email Sender Testing"
#
#     if msg == 'approved':
#         body = """
#                 Hello there, Your leave request has been approved"""
#     else:
#         body = """
#                 Hello there, Your leave request has been rejected"""
#
#     send_email = EmailMessage()
#
#     send_email['From'] = email_sender
#     send_email['To'] = email_receiver
#     send_email['Cc'] = cc
#     send_email['Subject'] = subject
#     send_email.set_content(body)
#
#     context = ssl.create_default_context()
#
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
#         smtp.login(email_sender, password)
#         smtp.sendmail(email_sender, email_receiver, send_email.as_string())
