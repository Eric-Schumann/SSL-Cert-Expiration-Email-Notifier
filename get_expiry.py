import os
import click
import ssl
import smtplib
import socket
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER=os.getenv('SMTP_SERVER')
SENDER_EMAIL=os.getenv('SENDER_EMAIL')
SENDER_PASSWORD=os.getenv('SENDER_PASSWORD')


@click.command()
@click.option('--hostname', prompt="Enter the hostname to check", help="A valid hostname is required to locate an SSL Certificate.")
@click.option('--port', prompt="Please enter a port number. Deafult=", help="443: HTTPS, 22: SSH, etc..", default=443)
@click.option('--threshold', prompt="Expiration threshold", default=5, help="An email notification will be sent if the expiration date is within the threshold number of days.")
def get_ssl_expiry_date(hostname, port, threshold):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert_info = ssock.getpeercert()
    
    timestamp = cert_info['notAfter']
    datetime_object = datetime.strptime(timestamp, "%b %d %H:%M:%S %Y %Z")

    time_left = datetime_object - datetime.today()

    if time_left.days < threshold:
        send_expiry_notification_email(cert_info, time_left.days)
    else:
        print(f"This cert will expire in {time_left.days} days on {datetime_object.strftime('%a %b, %d %Y %I:%M%p')}.")
    

def send_expiry_notification_email(cert_info, days):
    email_context = ssl.create_default_context()
    message = f"""
        SUBJECT: {cert_info['subject']}\n
        ISSUER: {cert_info['issuer']}\n
        Your certificate will expire in {days} days.
        """
    try:
        server = smtplib.SMTP(SMTP_SERVER)
        server.starttls(context=email_context)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, SENDER_EMAIL, message)
    except Exception as e:
        print(f'Email Exception: {e}')
    finally:
        server.quit()

if __name__ == '__main__':
    get_ssl_expiry_date()
