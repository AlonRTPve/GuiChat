import tkinter
import socket
import customtkinter


MSG_FORMAT = "CODE|MSGDATA"

FORMAT = "utf-8"

"""
MSG CODES:
REGISTER
LOGIN
LOGOUT
MESSAGE


"""



class Chatapp():
    def __init__(self):
        self.username = None
        self.password = None
        self.username_entry = None
        self.password_entry = None
        self.IP,self.PORT = "127.0.0.1", 65432
        self.SERVERADDR = (self.IP, self.PORT)



    def first_window(self):
        """
        Authentication Window | Sign up + login options

        """

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        root = customtkinter.CTk()
        root.geometry("500x350")

        frame = customtkinter.CTkFrame(master=root)
        self.frame = frame
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text = "login system")
        label.pack(pady=12, padx=10)

        username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
        self.username_entry = username_entry
        username_entry.pack(pady=12, padx = 10)

        password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
        self.password_entry = password_entry
        password_entry.pack(pady=12, padx=10)

        login_button = customtkinter.CTkButton(master=frame, command=self.Login, text="Login")
        login_button.pack(pady=12, padx=10)

        register_button = customtkinter.CTkButton(master=frame, command=self.Signup, text="Sign Up")
        register_button.pack(pady=12, padx=10)

        self.connect_to_server()
        root.mainloop()


    def Login(self): ## Handle login info
        Username,Password = self.username_entry.get(), self.password_entry.get()
        if len(Username) > 0 and len(Password) > 0:
            self.send_msg(f"LOGIN|{Username}:{Password}")
            server_response = self.receive_msg()
            print(server_response)
            return
        label = customtkinter.CTkLabel(master=self.frame, text="Username/Password length Must over 0")
        label.pack(pady=12, padx=10)




    def Signup(self):
        Username, Password = self.username_entry.get(), self.password_entry.get()

        if len(Username) > 0 and len(Password) > 0:
            self.send_msg(f"REGISTER|{Username}:{Password}")
            server_response = self.receive_msg()
            return

        label = customtkinter.CTkLabel(master=self.frame, text="Username/Password length Must over 0")
        label.pack(pady=12, padx=10)





    def receive_msg(self):
        clientsocket = self.clientsocket
        try:
            return clientsocket.recv(1024).decode(FORMAT)
        except Exception:
            label = customtkinter.CTkLabel(master=self.frame, text="unknown error")
            label.pack(pady=12, padx=10)
            return




    def send_msg(self, message):
        clientsocket = self.clientsocket
        try:
            clientsocket.send(message.encode())
        except ConnectionResetError:
            label = customtkinter.CTkLabel(master=self.frame, text="Server has closed the connection")
            label.pack(pady=12, padx=10)
            return


    def connect_to_server(self):
        """
        Function that initializes a connection with the server.

        """

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.SERVERADDR)
        self.clientsocket = client






NewChatter = Chatapp()
NewChatter.first_window()

