# SSL-Cert-Expiration-Email-Notifier
Python CLI Script to check SSL certificates for their expriration date.

This script runs from the command line and takes 3 arguments.

--hotname     example: google.com
--port        example: 443 which is also the default
--threshold   example: 5 (If the expiration date is within the threshold, an email notification email will be sent.)

The script utilizes a .env file to store the following values:
SMTP_SERVER   example: smtp.google.com
SENDER_EMAIL  The email address where the notification will originate.
SENDER_PASSWORD The password for the SENDER_EMAIL (This is stored locally in plain text.  More secure options can be added later.)
