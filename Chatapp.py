
from PyQt6.QtWidgets import *
from PyQt6 import uic
import socket, time

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

            if self.receive_msg() == "login successful":

                self.alertLabel.setStyleSheet('color: green')
                self.alertLabel.setText("Login Successful")
                loadpage("Chatscreen")

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

            self.alertLabel.setText("Register Failed")
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
            return clientsocket.recv(1024).decode(FORMAT)
        except Exception:
            return

    def send_msg(self, message):
        clientsocket = self.clientsocket
        try:
            clientsocket.send(message.encode())
        except ConnectionResetError:
            return



class ChatPage(QMainWindow):

    def __init__(self):
        super(ChatPage, self).__init__()
        uic.loadUi("LoginPage.ui", self)
        self.show()

        ##Variables
        self.username = MyGui.username


        ##Actions



def loadpage(page):

    if page == "Loginscreen":
        app = QApplication([])
        window = Loginpage()
        app.exec()
    elif page == "Chatscreen":
        app = QApplication([])
        window = ChatPage()
        app.exec()
    else:
        pass



if __name__ == "__main__":
    app = QApplication([])
    window = Loginpage()
    app.exec()
