from PyQt6.QtWidgets import *
from PyQt6 import uic
import socket
import sys
import threading

IP, PORT = "127.0.0.1", 65432
SERVERADDR = (IP, PORT)
FORMAT = "utf-8"



class Socket():
    def __init__(self):
        self.connect_to_server()


    def connect_to_server(self):
        """
        Function that initializes a connection with the server.
        """
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(SERVERADDR)



    def receive_message(self):
        try:
            message = self.clientsocket.recv(1024).decode(FORMAT)
            print(f"[Client] received message {message}")
            return message
        except Exception as e:
            print("Err;or receiving message:", str(e))
            return None

    def send_message(self, message):
        try:
            if message:
                print(f"[Client] Sending message {message}")
                self.clientsocket.sendall(message.encode())
        except ConnectionResetError as e:
            print("Error sending message:", str(e))


class LoginPage(QMainWindow):
    def __init__(self):
        super(LoginPage, self).__init__()
        uic.loadUi("LoginPage.ui", self)
        self.show()

        # Actions
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)

    def login(self):
        self.username, self.password = self.loginEntry.text(), self.passwordEntry.text()
        self.passwordEntry.clear()

        if self.username and self.password:
            server_socket.send_message(f"LOGIN|{self.username}:{self.password}")
            received_message = server_socket.receive_message()
            if received_message == "login successful":
                self.alertLabel.setStyleSheet('color: green')
                self.alertLabel.setText("Login Successful")
                self.open_lobby_page()
                return
            elif received_message == "user already logged in":
                self.alertLabel.setText("User already logged in")
                self.alertLabel.setStyleSheet('color: red')
                return
            else:
                self.alertLabel.setText("Login failed")
                self.alertLabel.setStyleSheet('color: red')


    def register(self):
        self.username, self.password = self.loginEntry.text(), self.passwordEntry.text()
        self.passwordEntry.clear()

        if self.username and self.password:
            server_socket.send_message(f"REGISTER|{self.username}:{self.password}")
            if server_socket.receive_message() == "registration successful":
                self.alertLabel.setStyleSheet('color: green')
                self.alertLabel.setText("Register Successful")
            else:
                self.alertLabel.setText("User already exists")
                self.alertLabel.setStyleSheet('color: red')


    def open_lobby_page(self):
        self.hide()
        self.lobby_page = LobbyPage(self.username)
        self.lobby_page.show()


class LobbyPage(QMainWindow):
    def __init__(self, username):
        super(LobbyPage, self).__init__()
        uic.loadUi("chooseRoomPage.ui", self)

        # Variables
        self.username = username
        self.logged_users = None

        # Actions
        self.createRoomButton.clicked.connect(self.create_room)
        self.joinRoomButton.clicked.connect(self.join_room)
        self.nameLabel.setText(f"{self.username}!")

    def join_room(self):
        self.joinRoomAlertLabel.setText("")
        self.room_code = self.joinRoomLabel.text()

        if len(self.room_code) < 3:
            self.joinRoomAlertLabel.setText("Room name must be longer than 3")
            return

        server_socket.send_message(f"JOINROOM|{self.room_code}")
        server_response = server_socket.receive_message()
        if server_response == "success":
            self.logged_users = server_socket.receive_message()
            self.open_chat_page()
        else:
            self.joinRoomAlertLabel.setText("Incorrect room code")

    def create_room(self):
        self.createRoomAlertLabel.setText("")
        self.room_code = self.createRoomLabel.text()

        if len(self.room_code) < 3:
            self.createRoomAlertLabel.setText("Room name must be longer than 3")
            return

        server_socket.send_message(f"CREATEROOM|{self.room_code}")
        server_response = server_socket.receive_message()

        if server_response == "created room!":
            self.open_chat_page()
        else:
            self.createRoomAlertLabel.setText("Room already exists")


    def open_chat_page(self):
        self.hide()
        self.chat_page = ChatPage(self.room_code, self.username, self.logged_users)


class ChatPage(QMainWindow):
    def __init__(self, roomcode, username, logged_users=None):
        super(ChatPage, self).__init__()
        uic.loadUi("ChatPage.ui", self)
        self.show()

        # Variables
        self.room_code = roomcode
        self.username = username
        self.logged_users = logged_users

        # Actions
        self.usersFrame.append(self.username)
        self.RoomLabel.setText(f"Room Id: {self.room_code}")
        socket_thread = threading.Thread(target=self.receive_and_handle_messages)
        socket_thread.start()

        self.sendButton.clicked.connect(self.send_message)
        if logged_users:
            self.append_users()



    def receive_and_handle_messages(self):
        """
        Possible MESSAGES CODES: message, userleave, userjoin

        :return:
        """

        while True:
            print("receiving")
            message = server_socket.receive_message()
            message_code, message_data = message.split("|")[0], message.split("|")[1]
            if message_code == "userjoin":
                self.self.append_user(message_data)
            elif message_code == "userleave":
                continue
            elif message_code == "message":
                pass


    def send_message(self):
        self.message = self.chatLabel.text()
        if self.message:
            server_socket.send_message(self.message)


    def append_users(self):
        ###THIS FUNCTION IS Mainly for the list of the users, created another function just to append a single user.
        try:
            list_of_logged_users = self.logged_users.split("|")
            list_of_logged_users.remove(self.username)
            for user in list_of_logged_users:
                if user:
                    self.usersFrame.append(user)
            self.usersFrame.append(self.username)
        except AttributeError as e:
            print("Error receiving message:", str(e))
            self.usersFrame.append(self.username)


    def append_user(self, user):
        self.usersFrame.append(user)


if __name__ == "__main__":
    server_socket = Socket()
    app = QApplication(sys.argv)
    login_page = LoginPage()
    sys.exit(app.exec())