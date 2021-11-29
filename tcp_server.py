import socket
import json
from db_manager import DataBaseManager

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    s.listen()

    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            if data:
                string_data = data.decode()
                json_data = json.loads(string_data)

                remainder_name = json_data["remainder-name"]
                remainder_body = json_data["remainder-body"]
                remainder_time = json_data["remainder-time"]

                database_manager = DataBaseManager('database.db')
                database_manager.add_remainder(remainder_name, remainder_body, remainder_time)
                database_manager.close()

                message = {"status" : "done"}
                message_binary = json.dumps(message).encode()

                conn.sendall(message_binary)
