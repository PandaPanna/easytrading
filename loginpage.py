from tkinter import *
from mainpage import *
from tkinter.messagebox import *

"""Create login page and check user id and password"""
class LoginPage(object):
    """Crete the login page"""

    def __init__(self, master=None):
        """Initialise the login page"""
        self.root = master
        self.root.geometry('%dx%d' % (300, 200))  # Window size
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        """Create frame/ID/password entry and buttons"""
        self.page = Frame(self.root)
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='ID: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text='Password: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)
        Button(self.page, text='Login', command=self.check_login).grid(row=3, stick=W, pady=10)
        Button(self.page, text='Quit', command=self.page.quit).grid(row=3, column=1, stick=E)
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='Test password: "0000" ').grid(row=4, stick=W)

    def check_login(self):
        """Check if id matches the inut"""
        name = self.username.get()
        password = self.password.get()
        users = {"Panna": "1234", "Test": "1111"}
        infile = open("users.txt")
        lines = infile.readlines()
        for line in lines:
            line = line.split(",")
            user = User(line[0], line[1], line[2])
            users[user.user_id] = user.password
        if password == '0000':
            self.page.destroy()
            MainPage(self.root)
        elif name in users:
            if password == users[name]:
                self.page.destroy()
                MainPage(self.root)
        else:
            showerror(title='Error', message='Invalid password')