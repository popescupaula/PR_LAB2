import socket
import json
from db_manager import DataBaseManager

HOST = '127.0.0.1'
PORT = 4546

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_server:
    udp_server.bind((HOST, PORT))

    while True:
        data = udp_server.recvfrom(1024)

        if data:
            message = data[0].decode()
            json_data = json.loads(message)

            task_name = json_data["task-name"]
            task_body = json_data["task-body"]
            task_due_date = json_data["task-due-date"]

            database_manager = DataBaseManager('database.db')
            database_manager.add_task(task_name, task_body, task_due_date)
            database_manager.close()

            message = {"status" : "done"}
            message_binary = json.dumps(message).encode()

            udp_server.sendto(message_binary, data[1])
