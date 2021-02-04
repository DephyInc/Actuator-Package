"""
This script can be used to send an email with an IP address when your RPi boots

This is a convenient tool for headless applications

Gmail uses 2FA (2 Factor Authentication). To enable RPi4 email via Gmail, I
reduced its security at the following location:
Google Appls > Account > # Security > Less secure app access
	> Turn-on access (not recommended).
Lowered security + plain-text password: use a dedicated, throwaway Gmail account!

To send-out an email at RPi4 bootup, follow these steps:
1] Make sure ssmtp is installed:
	sudo apt list --installed | grep ssmtp
	If needed, install it:
	sudo apt-get ssmtp
2] Place this file at: /home/pi/Documents
3] sudo crontab -e
4] Add following command to the file:
	@reboot python3 /home/yourUserName/Documents/startup_email.py &
NOTE: For this script, it seems critical to delay for 15s+ before connecting
to socket.  This gives enough time for the OS to bootup.
"""
import socket
import smtplib
import time
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Update this section:
SENDER = "senderEmail@gmail.com"  # Your throaway account
SENDER_PLAIN_TEXT_PW = "securityLevel0Password"  # and its non-critical, unique password
RECIPIENTS = "recipientEmail@theirDomain.com"  # Your "real" email account

# Get IP address:
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
# A 15s delay might be critical to running this scripts successfully at startup
time.sleep(15)
s.connect(("8.8.8.8", 80))
IPAddr = s.getsockname()[0]
s.close()
userid = getpass.getuser()

# Terminal output:
print("User: ", userid)
print("Hostname: ", hostname)
print("IP Address: ", IPAddr)

# Generate and send email:
body = (
	"This is an automated message from RPi4.\nUser: "
	+ userid
	+ "\nHostname: "
	+ hostname
	+ "\nIP address: "
	+ IPAddr
)
msg = MIMEMultipart()

msg["From"] = SENDER
msg["To"] = RECIPIENTS
msg["Subject"] = "RPi4 bootup message"

msg.attach(MIMEText(body, "plain"))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()  # Say hello to server
server.starttls()  # Start TLS encryption
server.ehlo()  # Say hello to server
server.login(SENDER, SENDER_PLAIN_TEXT_PW)
server.sendmail(SENDER, RECIPIENTS.split(","), msg.as_string())
server.quit()
