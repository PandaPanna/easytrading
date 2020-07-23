from tkinter import *
from tkinter.messagebox import *
import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

style.use('ggplot')


class AnalysisFrame(Frame):
    """Build the analysis frame"""

    def __init__(self, master=None):
        """Initialise analysis frame"""
        Frame.__init__(self, master)
        self.root = master
        self.createPage()

    def createPage(self):
        """Create entry and button"""
        Label(self).grid(row=0, stick=W, pady=10)
        Label(self, text='Start date: (eg.01/01/2019)').grid(row=1, stick=W, pady=10)
        self.start_entry = Entry(self)
        self.start_entry.insert(0, "01/01/2019")
        self.start_entry.grid(row=1, column=1, stick=E)
        Label(self, text='End date: (eg.25/05/2019)').grid(row=2, stick=W, pady=10)
        self.end_entry = Entry(self)
        self.end_entry.insert(0, "25/05/2019")
        self.end_entry.grid(row=2, column=1, stick=E)
        Label(self, text='Stock code: (eg.GOOGL)').grid(row=3, stick=W, pady=10)
        self.stock_code_entry = Entry(self)
        self.stock_code_entry.insert(0, "GOOGL")
        self.stock_code_entry.grid(row=3, column=1, stick=E)
        Label(self, text='Show data in shell').grid(row=12, stick=N, pady=10)
        show_button = Button(self, text='Go', command=self.show_summary)
        show_button.grid(row=12, column=1, stick=E, pady=10)
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        self.addmov = 0
        self.addchange = 0
        self.percentage_change = 0
        self.volatility = 0
        self.move_average_check = Checkbutton(self, text="100 days moving average"
                                              , variable=self.var1, command=self.add_mov)
        self.move_average_check.grid(row=8, column=1, stick=W)
        self.daily_differ_check = Checkbutton(self, text="Daily difference", variable=self.var2
                                              , command=self.add_change)
        self.daily_differ_check.grid(row=9, column=1, stick=W)
        self.percentage_check = Checkbutton(self, text="Percentage change", variable=self.var3
                                            , command=self.add_percentage)
        self.percentage_check.grid(row=10, column=1, stick=W)
        self.volatility_check = Checkbutton(self, text="Volatility", variable=self.var4
                                            , command=self.add_volatility)
        self.volatility_check.grid(row=11, column=1, stick=W)
        Label(self, text='Show graph').grid(row=13, stick=N, pady=10)
        show_button = Button(self, text='Go', command=self.show_graph)
        show_button.grid(row=13, column=1, stick=E, pady=10)
        self.choices()

    def choices(self):
        """Create buttons for choices"""
        Label(self, text='Monte Carlo Simulator').grid(row=14, stick=N, pady=10)
        self.mont50_button = Button(self, text='50 days', command=self.mont_carlo50)
        self.mont50_button.grid(row=15, column=0, stick=E, pady=10)
        self.mont100_button = Button(self, text='100 days', command=self.mont_carlo100)
        self.mont100_button.grid(row=15, column=1, stick=E, pady=10)
        Label(self, text='Resample data').grid(row=16, stick=N, pady=10)
        self.resample5_button = Button(self, text='Weekly', command=self.resample5)
        self.resample5_button.grid(row=17, column=0, stick=E, pady=10)
        self.resample20_button = Button(self, text='Monthly', command=self.resample30)
        self.resample20_button.grid(row=17, column=1, stick=E, pady=10)
        Label(self, text='Moving average graph').grid(row=18, stick=N, pady=10)
        self.resample5_button = Button(self, text='50 days'
                                       , command=self.moving_graph50)
        self.resample5_button.grid(row=19, column=0, stick=E, pady=10)
        self.resample5_button = Button(self, text='100 days'
                                       , command=self.moving_graph100)
        self.resample5_button.grid(row=19, column=1, stick=E, pady=10)  
        

    def mont_carlo50(self):
        """Pass parameter '50' into mont_carlo()"""
        self.mont_carlo(50)

    def mont_carlo100(self):
        """Pass parameter '100' into mont_carlo()"""
        self.mont_carlo(100)

    def mont_carlo(self, days):
        """Build monte carlo simulator"""
        df = self.get_data()
        prices = df['Close']
        stock_code = self.stock_code_entry.get()
        returns = prices.pct_change()
        last_price = prices[-1]
        num_simulations = 100
        num_days = days
        simulation_df = pd.DataFrame()
        for x in range(num_simulations):
            count = 0
            daily_vol = returns.std()
            price_series = []
            price = last_price * (1 + np.random.normal(0, daily_vol))
            price_series.append(price)

            for y in range(num_days):
                if count == num_days - 1:
                    break
                else:
                    price = price_series[count] * (1 + np.random.normal(0, daily_vol))
                    price_series.append(price)
                    count += 1
            simulation_df[x] = price_series

        fig = plt.figure()
        fig.suptitle('Monte Carlo Simulation: {}'.format(stock_code))
        plt.plot(simulation_df)
        plt.axhline(y=last_price, color='r', linestyle='-')
        plt.xlabel('Day')
        plt.ylabel('Price')
        plt.show()
        
    def moving_graph100(self):
        """Pass '100' to moving_graph function"""
        self.moving_graph(100)
        
    def moving_graph50(self):
        """Pass '50' to moving_graph function"""
        self.moving_graph(50)
        
    def moving_graph(self, days):
        """Show moving average graph"""
        df = self.get_data()
        self.days = days
        df["Mov"] = df["Adj Close"].rolling(window=self.days, min_periods=0).mean()
        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)        
        ax1.plot(df.index, df['Adj Close'])
        ax1.plot(df.index, df['Mov'])
        ax2.bar(df.index, df['Volume'])  
        plt.show()
        
    def add_mov(self):
        """Add moving average to dataframe"""
        self.addmov = 1

    def add_change(self):
        """Add daily change to dataframe"""
        self.addchange = 1

    def add_percentage(self):
        """Add percentage to dataframe"""
        self.percentage_change = 1

    def add_volatility(self):
        """Add volatility column to dataframe"""
        self.volatility = 1

    def get_data(self):
        """Get data frame"""
        start_date = dt.datetime.strptime(self.start_entry.get(), "%d/%m/%Y")
        end_date = dt.datetime.strptime(self.end_entry.get(), "%d/%m/%Y")
        stock_code = self.stock_code_entry.get()
        df = web.get_data_yahoo(stock_code, start_date, end_date)
        if self.addmov == 1:
            print("yes")
            df["100Mov"] = df["Adj Close"].rolling(window=100, min_periods=0).mean()
        if self.addchange == 1:
            df["Daily change"] = df["Adj Close"] - df["Adj Close"].shift(1)
        if self.percentage_change == 1:
            df["Percentage"] = df['Close'].pct_change()
        if self.volatility == 1:
            df["Volatility"] = df['Close'].pct_change().std()

        return df

    def show_summary(self):
        """Get data and show data frame in shell"""
        df = self.get_data()
        stock_code = self.stock_code_entry.get()
        print("*" * 40)
        print("Here is the result: \n", df)
        save_window = Tk()
        SavePage(save_window, df, stock_code)
        save_window.mainloop()

    def show_graph(self):
        """Get data and show in a graph"""
        df = self.get_data()
        plt.plot(df)
        plt.show()

    def resample5(self):
        """Pass '5D' into resample function"""
        self.resample('5D')

    def resample30(self):
        self.resample('20D')
        """Pass '20D' into resample function"""

    def resample(self, sp_size):
        """Get data and do resample"""
        df = self.get_data()
        stock_code = self.stock_code_entry.get()
        df_ohlc = df['Adj Close'].resample(sp_size).ohlc()
        df_volume = df["Volume"].resample(sp_size).sum()
        df_ohlc.reset_index(inplace=True)
        df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
        ax1.xaxis_date()
        candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup="g")
        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
        plt.show()


class SavePage():
    """Create save page"""

    def __init__(self, save_window, df, stock_code):
        """Initialise save page"""
        self.df = df
        self.stock_code = stock_code
        Label(save_window).grid(row=0, stick=W)
        Label(save_window, text='Do you want to save the result? ').grid(row=1, stick=W, pady=10)
        Button(save_window, text='Yes', command=self.save_result).grid(row=3, stick=W, pady=10)
        Button(save_window, text='No', command=save_window.destroy).grid(row=3, column=1, stick=E)
        self.buttom_label = Label(save_window, text=' '.format(self.stock_code))
        self.buttom_label.grid(row=4, stick=W, pady=10)

    def save_result(self):
        """Save result to csv"""
        self.df.to_csv("{}.csv".format(self.stock_code), sep=',', index=False)
        self.buttom_label["text"] = "Saved successfully to '{}.csv'".format(self.stock_code)


class CalculatorFrame(Frame):
    """Build calculator frame"""

    def __init__(self, master=None):
        """Initialise calculator frame"""
        Frame.__init__(self, master)
        self.root = master
        self.itemName = StringVar()
        self.createPage()

    def createPage(self):
        """Create label/button/entry in calculator frame"""
        Label(self, text='Calculator').grid(row=0, stick=W, pady=10)
        Label(self, text='Number of shares: ').grid(row=1, stick=W, pady=10)
        self.share_entry = Entry(self)
        self.share_entry.grid(row=1, column=1, stick=E)
        self.share_entry.insert(0, "1")
        Label(self, text='Purchase price($): ').grid(row=2, stick=W, pady=10)
        self.purchase_entry = Entry(self)
        self.purchase_entry.grid(row=2, column=1, stick=E)
        self.purchase_entry.insert(0, "1")
        Label(self, text='Sell price($): ').grid(row=3, stick=W, pady=10)
        self.sell_entry = Entry(self)
        self.sell_entry.grid(row=3, column=1, stick=E)
        self.sell_entry.insert(0, "0")
        Label(self, text='Buy commission rate(%): ').grid(row=4, stick=W, pady=10)
        self.buy_rate_entry = Entry(self)
        self.buy_rate_entry.grid(row=4, column=1, stick=E)
        self.buy_rate_entry.insert(0, "0")
        Label(self, text='Sell commission rate(%): ').grid(row=5, stick=W, pady=10)
        self.sell_rate_entry = Entry(self)
        self.sell_rate_entry.grid(row=5, column=1, stick=E)
        Label(self, text='GST rate(%): ').grid(row=6, stick=W, pady=10)
        self.sell_rate_entry.insert(0, "0")
        self.gst_entry = Entry(self)
        self.gst_entry.grid(row=6, column=1, stick=E)
        self.gst_entry.insert(0, "0")
        self.confirm_button = Button(self, text='Calculate', command=self.calculate)
        self.confirm_button.grid(row=8, column=1, stick=E, pady=10)
        # Below will be calculated
        self.net_buy_label = Label(self, text='Net Buy Price: ')
        self.net_buy_label.grid(row=9, stick=W, pady=10)
        self.buy_com_label = Label(self, text='Buy Commission: ')
        self.buy_com_label.grid(row=10, stick=W, pady=10)
        self.net_sell_label = Label(self, text='Net Sell Price: ')
        self.net_sell_label.grid(row=11, stick=W, pady=10)
        self.sell_com_label = Label(self, text='Sell Commission: ')
        self.sell_com_label.grid(row=12, stick=W, pady=10)
        self.profit_label = Label(self, text='Profit / Loss: ')
        self.profit_label.grid(row=13, stick=W, pady=10)
        self.return_label = Label(self, text='Return On Investment: ')
        self.return_label.grid(row=14, stick=W, pady=10)

    def calculate(self):
        """Get numbers from input and calculate"""
        self.net_buy = float(self.share_entry.get()) * float(self.purchase_entry.get())
        self.buy_com = self.net_buy * float(self.buy_rate_entry.get()) / 100
        self.net_sell = float(self.share_entry.get()) * float(self.sell_entry.get())
        self.sell_com = self.net_buy * float(self.sell_rate_entry.get()) / 100
        self.profit = self.net_sell - self.net_buy
        self.return_rate = self.profit / self.net_buy *100
        self.net_buy_label["text"] = 'Net Buy Price: {:.2f}'.format(self.net_buy)
        self.buy_com_label["text"] = 'Buy Commission: {:.2f}'.format(self.buy_com)
        self.net_sell_label["text"] = 'Net Sell Price: {:.2f}'.format(self.net_sell)
        self.sell_com_label["text"] = 'Sell Commission: {:.2f}'.format(self.sell_com)
        self.profit_label["text"] = 'Profit / Loss: {:.2f}'.format(self.profit)
        self.return_label["text"] = 'Return On Investment: {:.2f}%'.format(self.return_rate)


class AdminFrame(Frame):
    """Build admin frame"""

    def __init__(self, master=None):
        """Initialise admin frame"""
        Frame.__init__(self, master)
        self.root = master
        self.createPage()

    def createPage(self):
        """Get input and create a new user"""
        Label(self, text='Create new account').grid(row=0, stick=W, pady=10)
        Label(self, text='User ID: ').grid(row=1, stick=W, pady=10)
        self.id_entry = Entry(self)
        self.id_entry.grid(row=1, column=1, stick=E)
        Label(self, text='Password: ').grid(row=2, stick=W, pady=10)
        self.pw_entry = Entry(self, show='*')
        self.pw_entry.grid(row=2, column=1, stick=E)
        Label(self, text='Email: ').grid(row=3, stick=W, pady=10)
        self.email_entry = Entry(self)
        self.email_entry.grid(row=3, column=1, stick=E)
        self.confirm_button = Button(self, text='OK', command=self.register_check)
        self.confirm_button.grid(row=8, column=1, stick=E, pady=10)

    def register_check(self):
        """Check the user name is valid or not"""
        infile = open("users.txt")
        lines = infile.readlines()
        infile.close()
        userids = []
        for line in lines:
            line = line.split(",")
            userids.append(line[0].strip(","))
        print(userids)
        if self.id_entry.get() in userids:
            showerror(title='Error', message='User ID already registered!')
        elif self.pw_entry.get() == "":
            print("no")
            showerror(title='Error', message='Password can not be empty')
        else:
            self.save_user()

    def save_user(self):
        """Save new user information in user.txt"""
        outfile = open("users.txt", 'a')
        id = self.id_entry.get()
        pw = self.pw_entry.get()
        email = self.email_entry.get()
        line = "{},{},{}\n".format(id, pw, email)
        outfile.writelines("{}\n".format(line))
        outfile.close()
        showinfo(title='âˆš', message='Registered successfully!')


class User:
    """The user class"""

    def __init__(self, user_id, password, email):
        """Initialise the user class"""
        self.user_id = user_id
        self.password = password
        self.email = email


class AboutFrame(Frame):
    """Build about page"""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master
        self.createPage()

    def createPage(self):
        information = "This is a python project.\n" \
                      "Created by Na Pan.\n" \
                      "Any problem please contact npa95@uclive.ac.nz"
        Label(self, text=information).pack()


class QuitFrame(Frame):
    """Build quit frame"""

    def __init__(self, master=None):
        """Initialise the quit page"""
        Frame.__init__(self, master)
        self.root = master


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

def main():
    """Create the main function """
    root = Tk()
    root.title('Easy Trading')
    root.wm_iconbitmap('stock.ico')
    LoginPage(root)
    root.mainloop()

main()
