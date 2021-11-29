import json
from flask import Flask, jsonify, request
import smtplib, ssl
import socket

app = Flask(__name__)

EMAIL = 'paula_pr_lab2@gmail.com'
PASSWORD = 'Moldova1234'
EMAIL_PORT = 465

ssl_context = ssl.create_default_context()

TCP_HOST = '127.0.0.1'
TCP_PORT = 65432

UDP_SERTVER_HOST_PORT = ('127.0.0.1', 4546)

@app.route('/', methods= ['POST', 'GET'])
def index():
    if request.method == 'GET':
        json_data = request.json

        if json_data['type'] == 'send-email':
            receiver_email = json_data['body']['receiver-email']
            email_message = json_data['body']['email-message']

            with smtplib.SMTP_SSL("smtp.gmail.com", EMAIL_PORT, context=ssl_context) as server:
                server.login(EMAIL, PASSWORD)
                server.sendmail(EMAIL, receiver_email, email_message)
        elif json_data['type'] == 'add-remainder':
            tcp_body = json_data['body']
            tcp_body_binary = json.dumps(tcp_body).encode()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((TCP_HOST, TCP_PORT))
                s.sendall(tcp_body_binary)
                data_back = s.recv(1024)
                data_back_json = json.loads(data_back.decode())
                return jsonify(data_back_json)

        elif json_data['type'] == 'add-task':
            udp_body = json_data['body']
            udp_body_binary = json.dumps(udp_body).encode()

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_server:
                udp_server.sendto(udp_body_binary, UDP_SERTVER_HOST_PORT)
                data_back = udp_server.recvfrom(1024)[0]
                data_back_json = json.loads(data_back.decode())
                return jsonify(data_back_json)
    return ''

app.run()
