import smtplib
import scapy.all as scapy
from flask import Flask, request
from scapy.layers.inet import TCP as TCP

# Define the ports to listen on
PORTS = [22, 80, 443]

# Define the email parameters
EMAIL_FROM = "example.com"
EMAIL_TO = "example.com"
EMAIL_SUBJECT = "Honeypot Alert"
EMAIL_SMTP_SERVER = "smtp-mail"
EMAIL_SMTP_PORT = 587
EMAIL_SMTP_USERNAME = "Username"
EMAIL_SMTP_PASSWORD = "Password"

# Initialize the Flask web server
app = Flask(__name__)


# Define the route for the web server
@app.route("/", methods=["GET", "POST"])
def index():
    # Log the request
    log_request(request)
    # Return a fake response
    return "OK"


# Define the function to log the request
def log_request(request):
    with open("honeypot.log", "a") as logfile:
        logfile.write(f"{request.method} {request.path} {request.headers}\n")


# Define the function to send an email alert
def send_email_alert(message):
    with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_SMTP_USERNAME, EMAIL_SMTP_PASSWORD)
        smtp.sendmail(EMAIL_FROM, EMAIL_TO, f"Subject: {EMAIL_SUBJECT}\n\n{message}")


# Define the function to handle incoming packets
def handle_packet(packet):
    # Check if the packet is a TCP packet
    if scapy.TCP in packet:
        # Check if the packet is on one of the ports we are listening on
        if packet[TCP].dport in PORTS:
            # Log the packet
            with open("honeypot.pcap", "ab") as pcapFile:
                pcapFile.write(bytes(packet))
            # Send an email alert
            send_email_alert(f"TCP packet captured on port {packet[TCP].dport}")


# Start capturing packets
scapy.sniff(prn=handle_packet)

# Start the Flask web server
app.run(host="0.0.0.0", port=80)
app.run(host="0.0.0.0", port=443, ssl_context="adhoc")
