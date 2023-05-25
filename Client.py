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


class Chatapp(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.IP,self.PORT = "127.0.0.1", 65432
        self.SERVERADDR = (self.IP, self.PORT)

        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()

        self.x_co = int((screen_width / 2) - (550 / 2))
        self.y_co = int((screen_height / 2) - (400 / 2)) - 80

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.root = customtkinter.CTk()
        self.title("Chat Room")
        self.root.geometry(f"550x400+{self.x_co}+{self.y_co}")


        self.connect_to_server()

        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.loginSystemLabel = customtkinter.CTkLabel(master=self.frame, text="login system")
        self.loginSystemLabel.pack(pady=12, padx=10)

        self.username_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username")
        self.username_entry.pack(pady=12, padx=10)

        self.password_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.label = customtkinter.CTkEntry(master=self.frame, placeholder_text="placeholder") # button is meant to avoid Errors with the authentication function

        self.login_button = customtkinter.CTkButton(master=self.frame, command=lambda: self.Authentication("LOGIN"), text="Login")
        self.login_button.pack(pady=12, padx=10)

        register_button = customtkinter.CTkButton(master=self.frame, command=lambda: self.Authentication("REGISTER"),
                                                  text="Sign Up")
        register_button.pack(pady=12, padx=10)

        self.root.mainloop()



    def Authentication(self, action):
        self.label.destroy()
        global username
        username, password = self.username_entry.get(), self.password_entry.get()

        if len(username) > 0 and len(password) > 0:
            self.send_msg(f"{action}|{username}:{password}")
            if self.receive_msg() == "True":
                if action == "REGISTER":
                    self.label = customtkinter.CTkLabel(master=self.frame, text=f"{action} Sucessful, Please log in")
                    self.label.pack(pady=12, padx=10)
                    return
                else:
                    self.username = username
                    self.root.destroy()
                    ChatroomPage()

            else:
                self.label = customtkinter.CTkLabel(master=self.frame, text=f"{action} Failed, Please try again")
                self.label.pack(pady=12, padx=10)
                return

        self.label = customtkinter.CTkLabel(master=self.frame, text="Username and Password length must be over 0 ")
        self.label.pack(pady=12, padx=10)



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






class ChatroomPage(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        root2 = customtkinter.CTk()
        root2.title("Chatroom")
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()

        self.x_co = int((screen_width / 2) - (550 / 2))
        self.y_co = int((screen_height / 2) - (400 / 2)) - 80

        root2.geometry(f"800x768+{self.x_co}+{self.y_co}")

        self.roomnumberlabel = customtkinter.CTkLabel(master=root2, text= "Room Number: 183209" , text_color="black", font=("arial", 20))
        self.roomnumberlabel.place(x=290, y=0)

        self.onlineusers = customtkinter.CTkLabel(master=root2, text="Online Users:", text_color="#EA6A47",font=("arial", 18))
        self.onlineusers.place(x=15, y=50)

        self.onlineusers = customtkinter.CTkLabel(master=root2, text=f"{username}", text_color="#EA6A47",font=("arial", 18))
        self.onlineusers.place(x=15, y=70)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(root2, width=500, height=600)
        self.scrollable_frame.place(x=160, y=50)

        self.blankLabel = customtkinter.CTkLabel(master=self.scrollable_frame, text=" ", width=20)
        self.blankLabel.grid(row = 0, column=0)

        self.blankLabel2 = customtkinter.CTkLabel(master=self.scrollable_frame, text=" ", width=30)
        self.blankLabel2.grid(row=0, column=1)

        self.blankLabel3 = customtkinter.CTkLabel(master=self.scrollable_frame, text=" ", width=30)
        self.blankLabel3.grid(row=0, column=2)

        self.timeLabel = customtkinter.CTkLabel(master=self.scrollable_frame, text="TIME: 12:34", text_color="black", font=("arial", 19))
        self.timeLabel.grid(row=0, column=3)

        self.timeLabel2 = customtkinter.CTkLabel(master=self.scrollable_frame, text="X joined the chat", text_color="blue",bg_color="#CBC3E3", font=("arial", 19))
        self.timeLabel2.grid(row=1, column=0)

        textbox = customtkinter.CTkTextbox(master=self.scrollable_frame, width=500)
        textbox.place(x=600, y=400)





        root2.mainloop()



NewChatter = Chatapp()


