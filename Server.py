import socket
import threading
import Databasemanager as Database


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to en on (non-privileged ports are > 1023)
SIZE = 1024
DISCONNECT_MSG = "/DISCONNECT"
FORMAT = "utf-8"


####TO FIX



class ChatServer:
    def __init__(self):
        self.logged_users = {}
        self.rooms = {}
        self.room_code = None

        self.start_server_socket()


    def start_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a new socket object
        self.server_socket.bind((HOST, PORT))  # bind the SERVER HOST AND PORT
        self.server_socket.listen()  # starts listening for clients
        print(f"[SERVER] Server is listening on {HOST}:{PORT}")

        while True:
            conn, addr = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")

    def receive_message(self, conn):
        try:
            client_message = conn.recv(SIZE).decode(FORMAT)
            if client_message:
                print(f"[SERVER] Received message: {client_message}")
                return client_message

        except (ConnectionResetError, OSError, TypeError):
            self.remove_client()


    def handle_client(self, conn, addr):
        self.conn, self.addr = conn, addr
        print(f"[SERVER] {self.addr} has connected to the server \n")
        self.connected = True

        while self.connected:
            self.client_message = self.receive_message(self.conn)
            self.message_code, self.message_data = self.split_message()
            if self.message_code and self.message_data:
                self.handle_message_codes()


    def split_message(self):
        try:
            if "|" in self.client_message:
                message_code, message_data = self.client_message.split("|", 1)
                return message_code, message_data
            return None, None
        except Exception:
            self.remove_user()
            return None, None


    def check_if_user_logged(self):
        self.username = self.message_data.split(":")[0]
        for value in self.logged_users.values():
            if value == self.username:
                return True

        self.logged_users[self.conn] = self.username
        return False


    def remove_user(self):
        self.logged_users.pop(self.conn, None)


    def get_all_users_from_room(self):
        string_of_users = ""
        for key, value in self.logged_users.items():
            for socket in self.rooms[self.room_code]:
                if socket == key:
                    string_of_users += f"{value}|"
        return string_of_users


    def delete_user_from_room(self):
        if self.room_code in self.rooms:
            if self.conn in self.rooms[self.room_code]:
                self.rooms[self.room_code].remove(self.conn)
            if len(self.rooms[self.room_code]) == 0:
                del self.rooms[self.room_code]
                print("Room deleted as it became empty.")
            else:
                print("User is not in the room.")
        else:
            print("Room does not exist.")


    def send_message(self, message):
        try:
            print(f"[SERVER] Sending message: {message}")
            self.conn.send(message.encode())
        except ConnectionResetError:
            print("[ERROR] Connection reset by peer")
            self.remove_client()
        except socket.error as e:
            print(f"[ERROR] Failed to send message: {e}")
            self.remove_client()
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while sending message: {e}")
            self.remove_client()


    def handle_message_codes(self):
        if self.message_code == "LOGIN":
            if Database.login(self.message_data):
                if not self.check_if_user_logged():
                    self.send_message("login successful")
                else:
                    self.send_message("user already logged in")
            else:
                self.send_message("login failed")

        elif self.message_code == "REGISTER":
            self.send_message((Database.register(self.message_data)))

        elif self.message_code == "CREATEROOM":
            self.room_code = self.message_data
            for k, value in self.rooms.items():
                if k == self.room_code:
                    self.send_message("room already exists!")
            else:
                self.rooms.setdefault(self.room_code, []).append(self.conn)
                self.send_message("created room!")

        elif self.message_code == "JOINROOM":
            for k, value in self.rooms.items():
                if k == self.message_data:
                    self.rooms[self.message_data].append(self.conn)
                    self.send_message("success")
                    self.room_code = self.message_data
                    self.send_message(self.get_all_users_from_room())
                    self.send_message(f"userjoin|{self.username}")

            else:
                self.send_message("failed")

        elif self.message_code == "MESSAGE":
            self.broadcast()

    def remove_client(self):
        self.connected = False
        print(f"[SERVER] USER {self.addr[0]}:{self.addr[1]} disconnected")
        self.remove_user()
        if self.username in self.logged_users:
            self.logged_users.pop(self.username)
        if self.room_code:
            self.delete_user_from_room()
        self.conn.close()

    def broadcast(self):
        for client in self.rooms[self.room_code]:
            if client != self.conn:
                try:
                    self.send_message(self.message_data)
                    print(f"[SERVER] {self.addr[0]}:{str(self.addr[1])} says {self.message_data}")
                except socket.error as e:
                    print(f"[SERVER] Error sending message to client: {e}")

def main():
    print("[SERVER] Server is starting... ")
    server = ChatServer()  # Create an instance of ChatServer



if __name__ == '__main__':
    main()
