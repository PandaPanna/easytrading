from tkinter import *
from loginpage import *


def main():
    """Create the main function """
    root = Tk()
    root.title('Easy Trading')
    root.wm_iconbitmap('stock.ico')
    LoginPage(root)
    root.mainloop()

main()