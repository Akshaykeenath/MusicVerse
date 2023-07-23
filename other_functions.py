import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from database import *

def get_mail_id(uid):
    q = "select * from user where user_id='%s'" % uid
    userdetails = select(q)
    email = userdetails[0]['email']
    return email

def send_email(uid, subject, message):
    subject = subject + ' | MusicVerse'
    recipient_email = get_mail_id(uid)
    sender_email = "akshaykeenath1997@gmail.com"

    # Add a new line in the message
    message += "\n\n\n Regards. \n Admin \n admin@musicverse.com"

    # Create a MIME message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Attach the message body
    msg.attach(MIMEText(message, "plain"))

    # SMTP server configuration
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = 'akshaykeenath1997@gmail.com'
    smtp_password = 'uwsfsixtqoixzhtq'

    # Add an image to the email footer
    with open("static/user/assets/img/musicverse.png", "rb") as f:
        footer_image = MIMEImage(f.read(), name="footer_image.png")
    footer_image.add_header("Content-ID", "<footer_image>")
    msg.attach(footer_image)

    # Create an HTML version of the message with the image embedded in the footer
    html_message = f"""<html>
                        <body>
                            <div style="text-align: left;">
                                <img src="cid:footer_image" alt="Footer Image" width="150" style="max-width: 100%; height: auto;">
                            </div>
                        </body>
                    </html>"""

    msg.attach(MIMEText(html_message, "html"))

    # Create an SMTP session
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        # Start TLS encryption for security
        server.starttls()

        # Login to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Close the SMTP session
        server.quit()
