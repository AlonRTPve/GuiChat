import socket
import threading
import Databasemanager as Database


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
SIZE = 1024
DISCONNECT_MSG = "/DISCONNECT"
FORMAT = "utf-8"
connected_clients = []


def handle_client(conn, addr):
    print(f"[SERVER] {addr} has connected to the server \n")
    connected = True
    while connected:
        client_message = conn.recv(SIZE).decode(FORMAT)

        if not client_message:
            connected_clients.remove(conn)
            print(f"[SERVER] {addr[0]}:{str(addr[1])} has disconnected from the server")
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} ")

        message_code, message_data = split_message(client_message)

        #if message_code == "LOGIN":
          #  conn.send(str(Database.login(message_data)).encode())  # TRUE if login successful / False if not
        #elif message_code == "REGISTER":
         #   conn.send(str(Database.login(message_data)).encode())  # TRUE if register successful / False if not

        for client in connected_clients:
            if client is not conn:
                print(f"[SERVER] {addr[0]}:{str(addr[1])} says {message_data}")





def split_message(msg):
    message_code, message_data = msg.split("|")[0], msg.split("|")[1]
    return message_code, message_data


def main():
    print("[SERVER] Server is starting... ")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a new socket object
    server_socket.bind((HOST, PORT)) #bind the SERVER HOST AND PORT
    server_socket.listen() # starts listening for clients
    print(f"[SERVER] Server is listening on {HOST}:{PORT}")



    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        connected_clients.append(conn)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")

if __name__ == '__main__':
  main()




