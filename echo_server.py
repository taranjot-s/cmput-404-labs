#!/usr/bin/env python3
import socket
import time

# define address & buffer size
MY_HOST = ""
MY_PORT = 8001
BUFFER_SIZE = 1024

# define address of server to connect to
SERVER_HOST = "www.google.com"
SERVER_PORT = 80


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as read_clients_socket:

        read_clients_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind socket to address
        read_clients_socket.bind(("", MY_PORT))
        # set to listening mode
        read_clients_socket.listen(10)

        # continuously listen for connections
        while True:
            client_conn, client_addr = read_clients_socket.accept()
            print("Connected by client: ", client_addr)

            # recieve data, wait a bit, then send it back
            request_full_data = client_conn.recv(BUFFER_SIZE)
            print("Full data: ", request_full_data)
            time.sleep(0.5)

            server_write_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            server_ip = socket.gethostbyname(SERVER_HOST)
            server_write_socket.connect((server_ip, SERVER_PORT))
            print(f'Socket Connected to {SERVER_HOST} on ip {server_ip}')

            # send the data and shutdown
            server_write_socket.sendall(request_full_data)
            server_write_socket.shutdown(socket.SHUT_WR)

            # continue accepting data until no more left
            response_full_data = b""
            while True:
                data = server_write_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                response_full_data += data
            print(response_full_data)

            server_write_socket.close()

            client_conn.sendall(response_full_data)
            client_conn.close()


if __name__ == "__main__":
    main()
