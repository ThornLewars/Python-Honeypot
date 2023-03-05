# Python-Honeypot
This code defines the ports to listen on, initializes the Flask web server, defines a route for the web server,
logs incoming requests, defines a function to send email alerts, defines a function to handle incoming packets, and starts capturing packets using Scapy.
When a TCP packet is captured on one of the ports, it logs the packet and sends an email alert.
When a request is made to the web server, it logs the request and returns a fake response.

To run this code, you need to install the Scapy and Flask libraries by running pip install scapy flask. 
Then, save the code in a file named honeypot.py and run it using the command python honeypot.py. 
You can then access the web server by visiting http://localhost/ or https://localhost/ in your web
