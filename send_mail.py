import smtplib
from email.mime.text import MIMEText


def send_mail(customer, customer_email, consultant_name, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '455d90cbcf3d60'
    password = 'ba8378a606ecfb'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Consultant: {consultant_name}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    # sender_email = 'email1@example.com'
    sender_email = customer_email
    receiver_email = f'{consultant_name.split()[0]}.{consultant_name.split()[1]}@whitlockis.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = f'Feedback - {consultant_name}'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
