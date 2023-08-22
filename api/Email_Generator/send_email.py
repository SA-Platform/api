from email.message import EmailMessage
import ssl 
import smtplib

"""Function for sending email to reset the password when the user forgert it"""

"""email_token_password : Not your gmail password, It's a password you generate from your gmail settings"""

def email_sender_for_pass_reset(email_sender, email_token_password, email_receiver):
    subject = "Reseting Password"
    
    # Read the HTML content from the template file
    with open('index.html', 'r') as html_file:
        body = html_file.read()


    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
        smtp.login(email_sender, email_token_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
