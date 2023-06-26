
from PyQt6.QtWidgets import *
from PyQt6 import uic
import socket, sys, threading

IP, PORT = "127.0.0.1", 65432
SERVERADDR = (IP, PORT)
FORMAT = "utf-8"


class Loginpage(QMainWindow):

    def __init__(self):
        super(Loginpage, self).__init__()
        uic.loadUi("LoginPage.ui", self)
        self.show()

        ##Variables


        ##Actions
        self.connect_to_server()
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)


    def login(self):

        self.username, self.password = self.loginEntry.text(), self.passwordEntry.text()
        self.passwordEntry.clear()

        if self.username and self.password:

            self.send_msg(f"LOGIN|{self.username}:{self.password}")
            received_message = self.receive_msg()
            if received_message == "login successful":

                self.alertLabel.setStyleSheet('color: green')
                self.alertLabel.setText("Login Successful")
                self.open_second_screen()
                return

            elif received_message == "user already logged in":

                self.alertLabel.setText("user already logged in")
                self.alertLabel.setStyleSheet('color: red')
                return
            else:
                self.alertLabel.setText("Login failed")
                self.alertLabel.setStyleSheet('color: red')


    def register(self):

        self.username, self.password = self.loginEntry.text(), self.passwordEntry.text()
        self.passwordEntry.clear()

        if self.username and self.password:

            self.send_msg(f"REGISTER|{self.username}:{self.password}")

            if self.receive_msg() == "registration successful":

                self.alertLabel.setStyleSheet('color: green')
                self.alertLabel.setText("Register Successful")
                return

            self.alertLabel.setText("user already exists ")
            self.alertLabel.setStyleSheet('color: red')


    def connect_to_server(self):
        """
        Function that initializes a connection with the server.

        """

        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(SERVERADDR)


    def receive_msg(self):
        clientsocket = self.clientsocket
        try:
            message = clientsocket.recv(1024).decode(FORMAT)
            return message
        except Exception:
            return


    def send_msg(self, message):
        clientsocket = self.clientsocket
        try:
            if message:
                clientsocket.sendall(message.encode())
        except ConnectionResetError:
            return


    def open_second_screen(self):
        self.hide()
        self.lobbypage = LobbyPage()
        self.lobbypage.show()


class LobbyPage(Loginpage, QMainWindow):

    def __init__(self):
        super(LobbyPage, self).__init__()
        uic.loadUi("chooseRoomPage.ui", self)

        ##Variables
        username = login_window.username
        self.clientsocket = login_window.clientsocket

        ##Actions
        self.createRoomButton.clicked.connect(self.create_room)
        self.joinRoomButton.clicked.connect(self.join_room)
        self.nameLabel.setText(f"{username}!")




    def join_room(self):
        """
              Steps:
              1. Once button is pressed get the room code entry
              2. Send entry to server to check if room exists
              3. join room
              return

              """

        self.joinRoomAlertLabel.setText("")
        self.room_code = self.joinRoomLabel.text()

        if len(self.room_code) < 3:
            self.joinRoomAlertLabel.setText("Room name must be longer than 3")
            return

        self.send_msg(f"JOINROOM|{self.room_code}")
        server_response = self.receive_msg()
        if server_response == "success":
            self.logged_users = self.receive_msg()
            self.open_chat_window()
        else:
            self.joinRoomAlertLabel.setText("incorrect room code")





    def create_room(self):
        """
        Steps:
        1. Once button is pressed get the room code entry
        2. Send entry to server to check if room exists
        3. if room doesn't exist create room
        return

        """

        self.createRoomAlertLabel.setText("")
        self.room_code = self.createRoomLabel.text()

        if len(self.room_code) < 3:
            self.createRoomAlertLabel.setText("Room name must be longer than 3")
            return

        self.send_msg(f"CREATEROOM|{self.room_code}")
        server_response = self.receive_msg()

        if server_response == "created room!":
            self.open_chat_window()
        else:
            self.createRoomAlertLabel.setText("Room already exists")


    def open_chat_window(self):
        self.hide()
        self.Chatpage = ChatPage()
        self.Chatpage.show()



class ChatPage(Loginpage, QMainWindow):

    def __init__(self):
        super(ChatPage, self).__init__()
        uic.loadUi("ChatPage.ui", self)

        ##Variables
        room_code = login_window.lobbypage.room_code


        ##Actions
        self.sendButton.clicked.connect(self.send_message)
        self.RoomLabel.setText(f"Room Id# {room_code}")
        self.append_users()
        socket_thread = threading.Thread(target=self.handle_socket)
        socket_thread.start()



    def handle_socket(self):
        while True:
            print("in the thread: ")
            try:
                message = self.clientsocket.recv(1024).decode()
                print("in the thread: " + message)
                if not message:
                    pass
            except ConnectionError:
                pass

    def send_message(self):
        login_window.send_msg("MESSAGE|hey")

    def append_users(self):
        username = login_window.username
        try:
            logged_users = login_window.lobbypage.logged_users
            list_of_logged_users = logged_users.split("|")
            list_of_logged_users.remove(username)
            for user in list_of_logged_users:
                if user:
                    self.usersFrame.append(user)
            self.usersFrame.append(username)
        except AttributeError:
            self.usersFrame.append(username)















if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = Loginpage()
    sys.exit(app.exec())
