import socket
import threading
import Databasemanager as Database


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
SIZE = 1024
DISCONNECT_MSG = "/DISCONNECT"
FORMAT = "utf-8"
connected_clients = []
logged_users = {}
rooms = {}

def handle_client(conn, addr):
    print(f"[SERVER] {addr} has connected to the server \n")
    connected = True
    while connected:
        try:
            client_message = conn.recv(SIZE).decode(FORMAT)
        except ConnectionResetError:

            try:
                delete_user_from_room(room_code, conn)
            except UnboundLocalError:
                pass

            remove_user(conn)
            print(f"[SERVER] {addr[0]}:{str(addr[1])} has disconnected from the server")
            connected_clients.remove(conn)
            conn.close()
            break

        if not client_message:
            connected_clients.remove(conn)
            print(f"[SERVER] {addr[0]}:{str(addr[1])} has disconnected from the server")
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} ")
            conn.close()
            break

        message_code, message_data = split_message(client_message)
        if message_code == "LOGIN":
            try:
                if Database.login(message_data):
                    if not check_if_user_logged(message_data, conn):
                        conn.send("login successful".encode())
                    else:
                        conn.send("user already logged in".encode())
                else:
                    conn.send("login failed".encode())
            except Exception as e:
                pass


        elif message_code == "REGISTER":
            try:
                conn.send((Database.register(message_data)).encode())
            except Exception as e:
                pass

        elif message_code == "CREATEROOM":
            room_code = message_data
            for k, value in rooms.items():
                if k == room_code:
                    conn.send("room already exists!".encode())
            else:
                try:
                    rooms[room_code].append(conn)
                    conn.send("created room!".encode())
                except KeyError:  # this exception is for the first iteration of the program.
                    rooms[room_code] = [conn]
                    conn.send("created room!".encode())


        elif message_code == "JOINROOM":
            room_code = message_data
            for k, value in rooms.items():
                if k == room_code:
                    rooms[room_code].append(conn)
                    conn.send("success".encode())
                    conn.send(get_all_users_from_room(room_code).encode())

            else:
                conn.send("failed".encode())

        else:
            for client in rooms[room_code]:
                if client != conn:
                    try:
                        client.send(message_data.encode())
                        print(f"[SERVER] {addr[0]}:{str(addr[1])} says {message_data}")
                    except socket.error as e:
                        print(f"[SERVER] Error sending message to client: {e}")


            #for client in connected_clients:
            #    if client is not conn:
            #        client.send(message_code.encode())
            #        print(f"[SERVER] {addr[0]}:{str(addr[1])} says {message_data}")


def split_message(msg):
    try:
        message_code, message_data = msg.split("|")[0], msg.split("|")[1]
        return message_code, message_data
    except Exception:
        pass


def check_if_user_logged(message_data, conn):
    username = message_data.split(":")[0]
    for key, value in logged_users.items():
        if value == username:
            return True

    logged_users[conn] = username
    return False


def remove_user(conn):
    logged_users.pop(conn, None)


def get_all_users_from_room(room_code):
    string_of_users = ""
    for key, value in logged_users.items():
        for socket in rooms[room_code]:
            if socket == key:
                string_of_users += f"{value}|"

    return string_of_users


def delete_room(roomcode):
    rooms.pop(roomcode)


def delete_user_from_room(room_code, conn):
    rooms[room_code].remove(conn)
    if room_code in rooms:
        if conn in rooms[room_code]:
            rooms[room_code].remove(conn)
        if len(rooms[room_code]) == 0:
            del rooms[room_code]
            print("Room deleted as it became empty.")
        else:
            print("User is not in the room.")
    else:
        print("Room does not exist.")


def main():
    print("[SERVER] Server is starting... ")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a new socket object
    server_socket.bind((HOST, PORT))  # bind the SERVER HOST AND PORT
    server_socket.listen()  # starts listening for clients
    print(f"[SERVER] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        connected_clients.append(conn)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")


if __name__ == '__main__':
    main()
