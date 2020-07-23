from tkinter import *
from view import *

class MainPage(object):
    """Build main page frames"""
    def __init__(self, master=None):
        """Initialise main page"""
        self.root = master
        self.root.geometry('%dx%d' % (600, 800))
        self.create_page()

    def create_page(self):
        """Create menu and the frame"""
        self.analysisPage = AnalysisFrame(self.root)
        self.calculatorPage = CalculatorFrame(self.root)
        self.adminPage = AdminFrame(self.root)
        self.aboutPage = AboutFrame(self.root)
        self.quitPage = QuitFrame(self.root)
        self.analysisPage.pack()
        menubar = Menu(self.root)
        menubar.add_command(label='Data Analysis', command=self.pack_analysis)
        menubar.add_command(label='Calculator', command=self.pack_calculator)
        menubar.add_command(label='New account', command=self.pack_admin)
        menubar.add_command(label='About', command=self.pack_about)
        menubar.add_command(label='Quit', command=self.quitPage.quit)
        self.root['menu'] = menubar

    def pack_analysis(self):
        """Pack analysis frame into window"""
        self.analysisPage.pack()
        self.calculatorPage.pack_forget()
        self.adminPage.pack_forget()
        self.aboutPage.pack_forget()

    def pack_calculator(self):
        """Pack calculator frame into window"""
        self.analysisPage.pack_forget()
        self.calculatorPage.pack()
        self.adminPage.pack_forget()
        self.aboutPage.pack_forget()

    def pack_admin(self):
        """Pack admin frame into window"""
        self.analysisPage.pack_forget()
        self.calculatorPage.pack_forget()
        self.adminPage.pack()
        self.aboutPage.pack_forget()

    def pack_about(self):
        """Pack about frame into window"""
        self.analysisPage.pack_forget()
        self.calculatorPage.pack_forget()
        self.adminPage.pack_forget()
        self.aboutPage.pack()