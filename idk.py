import customtkinter

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

        self.onlineusers = customtkinter.CTkLabel(master=root2, text=f"hey", text_color="#EA6A47",font=("arial", 18))
        self.onlineusers.place(x=15, y=70)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(root2, width=500, height=600)
        self.scrollable_frame.place(x=160, y=50)

        self.blankLabel = customtkinter.CTkLabel(master=self.scrollable_frame, text=" ", width=20)
        self.blankLabel.grid(row = 0, column=0)

        self.blankLabel2 = customtkinter.CTkLabel(master=self.scrollable_frame, text=" ", width=30)
        self.blankLabel2.grid(row=0, column=1)

        self.blankLabel3 = customtkinter.CTkLabel(master=self.scrollable_frame, text=" ", width=30)
        self.blankLabel3.grid(row=0, column=2)

        self.textbox = customtkinter.CTkTextbox(master=self.scrollable_frame, width=500, height=500, bg_color="red")
        self.textbox.place(x=800, y=800)

        self.timeLabel = customtkinter.CTkLabel(master=self.scrollable_frame, text="TIME: 12:34", text_color="black", font=("arial", 19))
        self.timeLabel.grid(row=0, column=3)

        self.timeLabel2 = customtkinter.CTkLabel(master=self.scrollable_frame, text="X joined the chat", text_color="blue",bg_color="#CBC3E3", font=("arial", 19))
        self.timeLabel2.grid(row=1, column=0)
    



        root2.mainloop()





ChatroomPage()