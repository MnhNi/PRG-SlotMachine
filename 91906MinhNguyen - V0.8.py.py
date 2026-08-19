"""          Assessment 91906 (Creating a Game)          """

from tkinter import *
from tkinter import messagebox
import math
import random
import json
from tkinter import PhotoImage

#Constant values
FONT_MAIN_TITLE = "Geomini 20 bold"
FONT_HEADING = "Geomini 12 bold"
FONT_DEFAULT = "Geomini 10"

money_range = {
    "1": {"minimum": 0,
          "maximum": 20},
    "2": {"minimum": 100,
          "maximum": 1000},
    "3": {"minimum": 5000,
          "maximum": 11000},
    "4": {"minimum": 100000,
          "maximum": 999999999},
}

machine_winning = {
    "1": {'x2': 2, 'x3': 3, 'x4': 4, 'x1000': 1000},
    "2": {'Jaiden': 1, 'x2': 2, 'x5': 5, 'x10': 10, 'x2000': 2000},
    "3": {'EvilJaiden': 0.5, 'x5': 5, 'x10': 10, 'GoodJaiden': 2000},
    "4": {'x2': 2, 'x10': 10, 'x50': 50, 'ULTRAJaiden': 1000}
}

machine_odds = {  #1 and 2 is done (in testing)
    "1": {"1": [600, 300, 99, 1],
            "2": [10, 500, 300, 189, 1],
            "3": [199, 400, 400, 1],
            "4": [500, 299, 200, 1]},
    "2": {"1": [200, 600, 199, 1],
            "2": [5, 300, 500, 194, 1], # machine_odds x amountentered x the winning = winratio
            "3": [100, 500, 399, 1],
            "4": [300, 499, 200, 1]},
    "3": {"1": [100, 700, 199, 1],
            "2": [5, 100, 700, 194, 1],
            "3": [99, 400, 500, 1],
            "4": [200, 498, 300, 2]},
    "4": {"1": [40 ,100, 849, 11],
            "2": [1, 6, 793, 195, 5],
            "3": [15, 380, 600, 5],
            "4": [100, 495, 400, 5]}
}

try:
    with open("player_money.txt", "r") as f:
        player_money = f.read()
        if player_money == "":
            player_money = "100"
except FileNotFoundError:
    with open("player_money.txt", "w") as f:
        f.write("100")
    player_money = "100"
# print(player_money)

machines = {}
try:
    with open("machine_level.json", "r") as f:
        machines = json.load(f) 
        if machines == {}:
            machines["1"] = 1
            machines["2"] = 1
            machines["3"] = 1
            machines["4"] = 1
except FileNotFoundError:
    machines["1"] = 1
    machines["2"] = 1
    machines["3"] = 1
    machines["4"] = 1
    with open("machine_level.json", "w") as f:
        json.dump(machines, f, indent=4)

try:
    with open("day.txt", "r") as f:
        day = f.read()
        if day == "":
            day = "1"
except FileNotFoundError:
    with open("day.txt", "w") as f:
        f.write("1")
    day = "1"
# print(day)

try:
    with open("turn.txt", "r") as f:
        turn = f.read()
        if turn == "":
            turn = "10"
except FileNotFoundError:
    with open("turn.txt", "w") as f:
        f.write("10")
    turn = "10"

try:
    with open("debt.txt", "r") as f:
        debt = f.read()
        if debt == "":
            debt = "1000000000"
except FileNotFoundError:
    with open("debt.txt", "w") as f:
        f.write("1000000000")
    debt = "1000000000"

#Logic for the game
class Logic:

    def __init__(self, root):
        self.root = root
        self.day_var = None
        self.turn_var = None
        self.debt_var = None
        self.win_callback = None

    def set_status_variables(self, day_var, turn_var, debt_var):
        self.day_var = day_var
        self.turn_var = turn_var
        self.debt_var = debt_var

    def set_win_callback(self, win_callback):
        self.win_callback = win_callback

    # Making the funtion more convenient to use
    @staticmethod
    def format_money(value):
        value = float(value)
        if value.is_integer():
            return str(int(value))
        return str(value)


    #Variables that can be changed and saved

    #Checking if the entry box is empty
    def get_input(self, entry):
        try:
            entry = int(entry)
            return entry
        except ValueError:
            messagebox.showwarning('Enter something','Please enter the appropriate value(A whole number)')

    #Checking if the amount entered is appropriate 
    def check_input(self, entry, machine_number):
        global player_money
        input = self.get_input(entry)
        player_money = float(player_money)
        if input is not None:
            if input not in range(0, math.floor(player_money) + 1):
                messagebox.showwarning('POOR XD', 'You don\'t have enough money!')
                return False
            elif input in range(0, math.floor(player_money) + 1) and input in range(money_range[machine_number]['minimum'], money_range[machine_number]['maximum'] + 1):
                return True
            else:
                messagebox.showwarning('Out of range', 'Enter a value within the range')
                return False

    # def upgrade(self, currency, machine_number):
    def save_player_money(self):
        with open("player_money.txt", "w") as f:
                f.write(str(player_money))

    def save_debt(self):
        global debt
        with open("debt.txt", "w") as f:
            f.write(str(debt))

    @staticmethod
    def upgrade_cost(machine_number):
        return (100 * int(machine_number) ** 2) * machines[machine_number] ** 3

    def pay_debt(self, entry, currency_var):
        global player_money
        global debt
        payment = self.get_input(entry)
        player_money = float(player_money)
        debt = float(debt)
        if payment is None:
            return
        if payment <= 0:
            messagebox.showwarning('Invalid amount', 'Enter a positive amount')
            return
        if payment > player_money:
            messagebox.showwarning('POOR XD', 'You don\'t have enough money!')
            return
        if payment > debt:
            messagebox.showwarning('Invalid amount', 'You cannot pay more than your debt')
            return
        player_money -= payment
        debt -= payment
        self.save_player_money()
        self.save_debt()
        currency_var.set(self.format_money(player_money))
        self.debt_var.set(self.format_money(debt))
        if debt == 0 and self.win_callback is not None:
            self.win_callback()

    def configure_slots(self, slot1, slot2, slot3, machine_number):
        global machines
        upgrade = str(machines[machine_number])
        random1 = random.choices(list(machine_winning[machine_number].keys()), weights=machine_odds[upgrade][machine_number])[0]
        random2 = random.choices(list(machine_winning[machine_number].keys()), weights=machine_odds[upgrade][machine_number])[0]
        random3 = random.choices(list(machine_winning[machine_number].keys()), weights=machine_odds[upgrade][machine_number])[0]
        slot1.configure(text="")
        slot2.configure(text="")
        slot3.configure(text="")
        self.root.after(500, lambda: slot1.configure(text=random1))
        self.root.after(1000, lambda: slot2.configure(text=random2))
        self.root.after(1500, lambda: slot3.configure(text=random3))

        return random1, random2, random3


    def roll(self, entry, currency_var, machine_number, slot1, slot2, slot3, button):
        global player_money
        global machines

        slot1.configure(bg='white')
        slot2.configure(bg='white')
        slot3.configure(bg='white')
        # Disable button immediately to prevent spam clicks
        button.config(state='disabled')

        status = self.check_input(entry, machine_number)
        if status == True:
            player_money = float(player_money)
            player_money -= int(entry)
            self.save_player_money()
            self.subtract_turn()
            currency_var.set(self.format_money(player_money))
            random1, random2, random3 = self.configure_slots(slot1, slot2, slot3, machine_number)
            if random1 in ['x1000', 'x2000', 'GoodJaiden', 'ULTRAJaiden']:
                player_money += int(entry)*machine_winning[machine_number][random1]
                self.root.after(1500, lambda: currency_var.set(self.format_money(player_money)))
                self.root.after(1500, lambda: slot1.configure(bg='green'))
            elif random2 in ['x1000', 'x2000', 'GoodJaiden', 'ULTRAJaiden']:
                player_money += int(entry)*machine_winning[machine_number][random2]
                self.root.after(1500, lambda: currency_var.set(self.format_money(player_money)))
                self.root.after(1500, lambda: slot2.configure(bg='green'))
            elif random3 in ['x1000', 'x2000', 'GoodJaiden', 'ULTRAJaiden']:
                player_money += int(entry)*machine_winning[machine_number][random3]
                self.root.after(1500, lambda: currency_var.set(self.format_money(player_money)))
                self.root.after(1500, lambda: slot3.configure(bg='green'))
            elif random1 == random2 == random3:
            # Placeholder for testing purposes
                player_money += int(entry)*machine_winning[machine_number][random1]
                self.root.after(1500, lambda: currency_var.set(self.format_money(player_money)))
                self.root.after(1500, lambda: slot1.configure(bg='yellow'))
                self.root.after(1500, lambda: slot2.configure(bg='yellow'))
                self.root.after(1500, lambda: slot3.configure(bg='yellow'))

        # Re-enable button after 2 seconds (2000 milliseconds)
        self.root.after(2000, lambda: button.config(state='normal'))

    def upgrade(self, currency_var, machine_number, odds_label=None, level_label=None, cost_label=None):
        global player_money
        global machines
        player_money = float(player_money)
        if machines[machine_number] < 4:
            cost = self.upgrade_cost(machine_number)
            if player_money >= cost:
                player_money -= cost
                machines[machine_number] += 1
                messagebox.showinfo("LVL Up", f"Level{machines[machine_number]}")
                self.save_player_money()
                with open("machine_level.json", "w") as f:
                    json.dump(machines, f, indent=4)
                currency_var.set(self.format_money(player_money))
                if odds_label is not None:
                    self.odd_lbl_config(odds_label, machine_number)
                if level_label is not None:
                    self.machine_level(level_label, machine_number)
                if cost_label is not None:
                    if machines[machine_number] >= 4:
                        cost_label.configure(text='')
                    else:
                        cost_label.configure(text=f"Cost: {self.upgrade_cost(machine_number)}")
            else:
                messagebox.showwarning('POOR XD', 'You don\'t have enough money!')
        else:
            if level_label is not None:
                level_label.configure(text='MAX')
            if cost_label is not None:
                cost_label.configure(text='')
            messagebox.showwarning('MAX LEVEL', 'Can\'t upgrade anymore!')
    
    def machine_level(self, label, machine_number):
        global machines
        string = 'MAX' if machines[machine_number] >= 4 else f"Level: {machines[machine_number]}"
        label.configure(text=string)
        return label


    def working(self, currency_var):
        global player_money
        player_money = float(player_money)
        earned = random.randint(1, 30)
        player_money += earned
        messagebox.showinfo(random.choice(['Scrolling tiktok...', 'Working...', 'Sleeping...', 'Day dreaming...', 'Working...']), f'You earned {earned} money!')
        self.subtract_turn()
        self.save_player_money()
        currency_var.set(self.format_money(player_money))

        

    def odd_lbl_config(self, label, machine_number):
        global machines
        upgrade = str(machines[machine_number])
        string = ""
        for i in range(len(machine_odds[upgrade][machine_number])):
            string += f"{list(machine_winning[machine_number].keys())[i]} (x{list(machine_winning[machine_number].values())[i]}): {machine_odds[upgrade][machine_number][i] / 1000:.2%}\n"
        label.configure(text=string)
        return label

    def progress_day(self):
        global day
        global turn
        day = int(day)
        turn = int(turn)
        day += 1
        turn = 10  # Reset turn count for the new day
        self.save_day()
        self.save_turn()
        messagebox.showinfo('ANOTHER DAY!', f'Day: {day}')

    def save_day(self):
        global day
        with open("day.txt", "w") as f:
            f.write(str(day))

    def subtract_turn(self):
        global turn
        global day
        turn = int(turn)
        day = int(day)
        turn -= 1
        self.save_turn()
        if turn <= 0:
            self.progress_day()
        self.day_var.set(str(day))
        self.turn_var.set(str(turn))

    def save_turn(self):
        global turn
        with open("turn.txt", "w") as f:
            f.write(str(turn))

    

class GUI:
    def __init__(self, root):
        
        self.logic = Logic(root)
        self.root = root
        self.root.title('Addiction')
        self.container = Frame(self.root)
        self.container.grid(row=0, column=0)
        self.currency_var = StringVar(value=self.logic.format_money(player_money))
        self.day_var = StringVar(value=self.logic.format_money(day))
        self.turn_var = StringVar(value=self.logic.format_money(turn))
        self.debt_var = StringVar(value=self.logic.format_money(debt))
        self.logic.set_status_variables(self.day_var, self.turn_var, self.debt_var)
        self.logic.set_win_callback(self.show_win_frame)
    
        self.frames = {}
        self.frames['Mainframe'] = self.create_main_frame()
        self.frames['Work'] = self.create_work_frame()
        self.frames['Machine1'] = self.create_machine1_frame()
        self.frames['Machine2'] = self.create_machine2_frame()
        self.frames['Machine3'] = self.create_machine3_frame()
        self.frames['Machine4'] = self.create_machine4_frame()
        self.frames['WinMessage'] = self.create_win_message_frame()
        self.frames['WinChoice'] = self.create_win_choice_frame()

        self.show_frame("Mainframe")
    
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def show_win_frame(self):
        self.win_day_label.configure(text=f'After {day} days, idk how, but ig ur free now')
        self.show_frame('WinMessage')

    def create_win_message_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1], minsize=250, weight=1)
        frame.rowconfigure([0, 1, 2], minsize=80, weight=1)

        self.win_image = PhotoImage(file="66b3e5d0c2ab246786ca1d5e_86.png")
        Label(frame, image=self.win_image).grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky='nsew')
        Label(frame, font=FONT_MAIN_TITLE, text='You did it!').grid(row=0, column=1, padx=20, pady=20, sticky='nsew')
        self.win_day_label = Label(frame, font=FONT_HEADING, text='')
        self.win_day_label.grid(row=1, column=1, padx=20, pady=10, sticky='nsew')
        Button(frame, text='Continue', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('WinChoice')).grid(row=2, columnspan=2, padx=20, pady=20, sticky='nsew')

        return frame

    def create_win_choice_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1], minsize=200, weight=1)
        frame.rowconfigure([0, 1], minsize=100, weight=1)
        Label(frame, font=FONT_HEADING, text='Do you wish to continue or quit the game?').grid(row=0, columnspan=2, padx=20, pady=20, sticky='nsew')
        Button(frame, text='Continue', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Work')).grid(row=1, column=0, padx=10, pady=20, sticky='nsew')
        Button(frame, text='Quit', bg='white', font=FONT_HEADING, command=self.root.destroy).grid(row=1, column=1, padx=10, pady=20, sticky='nsew')

        return frame

    def create_odds_panel(self, parent, machine_number):
        odds_frame = Frame(parent, bg='black')
        odds_frame.grid(row=3, column=0, rowspan=3, columnspan=3, sticky='nsew')
        odds_label = self.logic.odd_lbl_config(Label(odds_frame, font=FONT_DEFAULT, text='', fg='white', bg='black'), machine_number)
        odds_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        return odds_label
    
    def create_main_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0,column=0,sticky='nsew')
        frame.columnconfigure([0, 1], minsize=200, weight=1)
        frame.rowconfigure([0, 1], minsize=100, weight=1)
        
        Label(frame, font=FONT_MAIN_TITLE, text='Addiction').grid(row=0,columnspan=2,padx=10,pady=10,sticky='nsew')

        Button(frame, text='PLAY', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine1')).grid(row=1,columnspan=2, padx=10, pady=10, sticky='nsew')

        return frame
    
    def create_work_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0,column=0,sticky='nsew')
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1, uniform='machine')
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1, uniform='machine')

        #Top bar (Day, Menu button)
        frame.top_frame = Frame(frame, bg="#8dfa8d")
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:', background='#8dfa8d').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.day_var, width=12, anchor='w', background='#8dfa8d').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='Debt:', background='#8dfa8d').grid(row=0,column=3,padx=(20, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.debt_var, width=12, anchor='w', background='#8dfa8d').grid(row=0,column=4,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Turn:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.turn_var, width=12, anchor='w').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.currency_var, width=12, anchor='w').grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

         #Machine
        frame.workmachine = Frame(frame, bg='#8dfa8d')
        frame.workmachine.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.workmachine.rowconfigure([0,1,2,3,4,5], minsize=50, weight=1, uniform='machinerow')
        frame.workmachine.columnconfigure([0,1,2], minsize=50,weight=1, uniform='machinecolumn')
        
        Label(frame.workmachine, font=FONT_HEADING, text='Work?', background='#8dfa8d').grid(row=0, column=0, sticky='nsew')
        Button(frame.workmachine, text='Work', bg='white', font=FONT_HEADING, command=lambda: self.logic.working(self.currency_var)).grid(row=3,column=0, padx=10, pady=10, sticky='nsew')
        Label(frame.workmachine, font=FONT_DEFAULT, text='Earn up to 30 money!', background='#8dfa8d').grid(row=4, column=0, sticky='nsew')

        Label(frame.workmachine, font=FONT_DEFAULT, text='Pay Off Debt', background='#8dfa8d').grid(row=0,column=2, sticky='nsew')
        self.debt_entry = Entry(frame.workmachine)
        self.debt_entry.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')
        Button(frame.workmachine, text='Pay', bg='white', font=FONT_HEADING, command=lambda: self.logic.pay_debt(self.debt_entry.get(), self.currency_var)).grid(row=3,column=2, padx=10, pady=10, sticky='nsew')
        Label(frame.workmachine, font=FONT_DEFAULT, text='Pay off your debt! (to win the game)', background='#8dfa8d').grid(row=4, column=2, sticky='nsew')

        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine4')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine1')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')
        
        return frame

    def create_machine1_frame(self):
        # Machine 1 Frame
        global machines
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1, uniform='machine')
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1, uniform='machine')
        
        #Top bar (Day, Menu button)
        frame.top_frame = Frame(frame, bg='#f3a8ff')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:', background='#f3a8ff').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.day_var, width=12, anchor='w', background='#f3a8ff').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='Debt:', background='#f3a8ff').grid(row=0,column=3,padx=(20, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.debt_var, width=12, anchor='w', background='#f3a8ff').grid(row=0,column=4,padx=10,pady=10,sticky='nsew')

        #Machine
        frame.machine1 = Frame(frame, bg='#f3a8ff')
        frame.machine1.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.machine1.rowconfigure([0,1,2,3,4,5], minsize=50, weight=1, uniform='machinerow')
        frame.machine1.columnconfigure([0,1,2], minsize=50,weight=1, uniform='machinecolumn')

        Label(frame.machine1, font=FONT_DEFAULT, text='Machine1', background='#f3a8ff').grid(row=0, columnspan=3, sticky='nsew')

        # Slots
        slot1_1 = Label(frame.machine1, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot1_1.grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        slot2_1 = Label(frame.machine1, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot2_1.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        slot3_1 = Label(frame.machine1, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot3_1.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        # Entry (Enter money)
        Label(frame.machine1, font=FONT_DEFAULT, text=f"Min: {money_range['1']['minimum']}\nMax: {money_range['1']['maximum']}", background='#f3a8ff', width=12, anchor='center').grid(row=3, column=0, sticky='nsew')
        Label(frame.machine1, font=FONT_DEFAULT, text='Enter the bet amount', background='#f3a8ff').grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
        self.machine1_entry = Entry(frame.machine1)
        self.machine1_entry.grid(row=3,column=1, padx=10, pady=10, sticky='nsew')

        # Chances/Odds Table
        chances_lbl = self.create_odds_panel(frame, "1")

        # VALUEs
        Label(frame, font=FONT_DEFAULT, text='Turn:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.turn_var, width=12, anchor='w').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.currency_var, width=12, anchor='w').grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        # Buttons
        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Work')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine2')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')
            # Roll
        self.roll_button1 = Button(frame.machine1, text='Roll', bg='white', font=FONT_DEFAULT, command=lambda: self.logic.roll(self.machine1_entry.get(), self.currency_var, "1", slot1_1, slot2_1, slot3_1, self.roll_button1))
        self.roll_button1.grid(row=3,column=2, padx=10, pady=10, sticky='nsew')
            # Upgrade
        level_lbl = Label(frame.machine1, font=FONT_DEFAULT, text='MAX' if machines['1'] >= 4 else f"Level: {machines['1']}", background='#f3a8ff')
        level_lbl.grid(row=4,column=2, padx=10, pady=10, sticky='nsew')
        cost_lbl = Label(frame.machine1, font=FONT_DEFAULT, text='' if machines['1'] >= 4 else f"Cost: {self.logic.upgrade_cost('1')}", background='#f3a8ff')
        cost_lbl.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        Button(frame.machine1, text='Upgrade', bg='white', font=FONT_HEADING, command=lambda: self.logic.upgrade(self.currency_var, "1", chances_lbl, level_lbl, cost_lbl)).grid(row=4,column=1, padx=10, pady=10, sticky='nsew')

        return frame
    

    # MACHINE 2
    def create_machine2_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1, uniform='machine')
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1, uniform='machine')

        #Top bar
        frame.top_frame = Frame(frame, bg='#9d91fa')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')

        #These are just placeholder Labels
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:', background='#9d91fa').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.day_var, width=12, anchor='w', background='#9d91fa').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='Debt:', background='#9d91fa').grid(row=0,column=3,padx=(20, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.debt_var, width=12, anchor='w', background='#9d91fa').grid(row=0,column=4,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Turn:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.turn_var, width=12, anchor='w').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.currency_var, width=12, anchor='w').grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Chances/Odds
        chances_lbl = self.create_odds_panel(frame, "2")

        #Machine
        frame.machine2 = Frame(frame, bg='#9d91fa')
        frame.machine2.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.machine2.rowconfigure([0,1,2,3,4,5], minsize=50, weight=1, uniform='machinerow')
        frame.machine2.columnconfigure([0,1,2], minsize=50,weight=1, uniform='machinecolumn')

        Label(frame.machine2, font=FONT_DEFAULT, text='Machine2', background='#9d91fa').grid(row=0, columnspan=3, sticky='nsew')

        slot1_2 = Label(frame.machine2, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot1_2.grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        slot2_2 = Label(frame.machine2, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot2_2.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        slot3_2 = Label(frame.machine2, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot3_2.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        Label(frame.machine2, font=FONT_DEFAULT, text=f"Min: {money_range['2']['minimum']}\nMax: {money_range['2']['maximum']}", background='#9d91fa', width=12, anchor='center').grid(row=3, column=0, sticky='nsew')
        Label(frame.machine2, font=FONT_DEFAULT, text='Enter the bet amount', background='#9d91fa').grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
        self.machine2_entry = Entry(frame.machine2)
        self.machine2_entry.grid(row=3,column=1, padx=10, pady=10, sticky='nsew')
        self.roll_button2 = Button(frame.machine2, text='Roll', bg='white', font=FONT_DEFAULT, command=lambda: self.logic.roll(self.machine2_entry.get(), self.currency_var, "2", slot1_2, slot2_2, slot3_2, self.roll_button2))
        self.roll_button2.grid(row=3,column=2, padx=10, pady=10, sticky='nsew')
        level_lbl = Label(frame.machine2, font=FONT_DEFAULT, text='MAX' if machines['2'] >= 4 else f"Level: {machines['2']}", background='#9d91fa')
        level_lbl.grid(row=4,column=2, padx=10, pady=10, sticky='nsew')
        cost_lbl = Label(frame.machine2, font=FONT_DEFAULT, text='' if machines['2'] >= 4 else f"Cost: {self.logic.upgrade_cost('2')}", background='#9d91fa')
        cost_lbl.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        Button(frame.machine2, text='Upgrade', bg='white', font=FONT_HEADING, command=lambda: self.logic.upgrade(self.currency_var, "2", chances_lbl, level_lbl, cost_lbl)).grid(row=4,column=1, padx=10, pady=10, sticky='nsew')

        #Buttons
        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine1')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine3')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')


        return frame
    
    def create_machine3_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1, uniform='machine')
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1, uniform='machine')

        #Top bar
        frame.top_frame = Frame(frame, bg='#a8c7ff')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')

        #These are just placeholder Labels
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:', background='#a8c7ff').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.day_var, width=12, anchor='w', background='#a8c7ff').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='Debt:', background='#a8c7ff').grid(row=0,column=3,padx=(20, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.debt_var, width=12, anchor='w', background='#a8c7ff').grid(row=0,column=4,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Turn:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.turn_var, width=12, anchor='w').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.currency_var, width=12, anchor='w').grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Chances/Odds
        chances_lbl = self.create_odds_panel(frame, "3")

        #Machine
        frame.machine3 = Frame(frame, bg='#a8c7ff')
        frame.machine3.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.machine3.rowconfigure([0,1,2,3,4,5], minsize=50, weight=1, uniform='machinerow')
        frame.machine3.columnconfigure([0,1,2], minsize=50,weight=1, uniform='machinecolumn')

        Label(frame.machine3, font=FONT_DEFAULT, text='Machine3', background='#a8c7ff').grid(row=0, columnspan=3, sticky='nsew')

        slot1_3 = Label(frame.machine3, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot1_3.grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        slot2_3 = Label(frame.machine3, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot2_3.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        slot3_3 = Label(frame.machine3, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot3_3.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        Label(frame.machine3, font=FONT_DEFAULT, text=f"Min: {money_range['3']['minimum']}\nMax: {money_range['3']['maximum']}", background='#a8c7ff', width=12, anchor='center').grid(row=3, column=0, sticky='nsew')
        Label(frame.machine3, font=FONT_DEFAULT, text='Enter the bet amount', background='#a8c7ff').grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
        self.machine3_entry = Entry(frame.machine3)
        self.machine3_entry.grid(row=3,column=1, padx=10, pady=10, sticky='nsew')
        self.roll_button3 = Button(frame.machine3, text='Roll', bg='white', font=FONT_DEFAULT, command=lambda: self.logic.roll(self.machine3_entry.get(), self.currency_var, "3", slot1_3, slot2_3, slot3_3, self.roll_button3))
        self.roll_button3.grid(row=3,column=2, padx=10, pady=10, sticky='nsew')
        level_lbl = Label(frame.machine3, font=FONT_DEFAULT, text='MAX' if machines['3'] >= 4 else f"Level: {machines['3']}", background='#a8c7ff')
        level_lbl.grid(row=4,column=2, padx=10, pady=10, sticky='nsew')
        cost_lbl = Label(frame.machine3, font=FONT_DEFAULT, text='' if machines['3'] >= 4 else f"Cost: {self.logic.upgrade_cost('3')}", background='#a8c7ff')
        cost_lbl.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        Button(frame.machine3, text='Upgrade', bg='white', font=FONT_HEADING, command=lambda: self.logic.upgrade(self.currency_var, "3", chances_lbl, level_lbl, cost_lbl)).grid(row=4,column=1, padx=10, pady=10, sticky='nsew')

        #Buttons
        
        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine2')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine4')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')


        return frame

    def create_machine4_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1, uniform='machine')
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1, uniform='machine')

        #Top bar
        frame.top_frame = Frame(frame, bg='#ff99b1')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')
        
        #Machine
        frame.machine4 = Frame(frame, bg='#ff99b1')
        frame.machine4.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.machine4.rowconfigure([0,1,2,3,4,5], minsize=50, weight=1, uniform='machinerow')
        frame.machine4.columnconfigure([0,1,2], minsize=50,weight=1, uniform='machinecolumn')

        Label(frame.machine4, font=FONT_DEFAULT, text='Machine4', background='#ff99b1').grid(row=0, columnspan=3, sticky='nsew')
        slot1_4 = Label(frame.machine4, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot1_4.grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        slot2_4 = Label(frame.machine4, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot2_4.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        slot3_4 = Label(frame.machine4, font=FONT_DEFAULT, text='', width=12, anchor='center', bg='white')
        slot3_4.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        Label(frame.machine4, font=FONT_DEFAULT, text=f"Min: {money_range['4']['minimum']}\nMax: {money_range['4']['maximum']}", background='#ff99b1', width=12, anchor='center').grid(row=3, column=0, sticky='nsew')
        Label(frame.machine4, font=FONT_DEFAULT, text='Enter the bet amount', background='#ff99b1').grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
        self.machine4_entry = Entry(frame.machine4)
        self.machine4_entry.grid(row=3,column=1, padx=10, pady=10, sticky='nsew')
        self.roll_button4 = Button(frame.machine4, text='Roll', bg='white', font=FONT_DEFAULT, command=lambda: self.logic.roll(self.machine4_entry.get(), self.currency_var, "4", slot1_4, slot2_4, slot3_4, self.roll_button4))
        self.roll_button4.grid(row=3,column=2, padx=10, pady=10, sticky='nsew')
        level_lbl = Label(frame.machine4, font=FONT_DEFAULT, text='MAX' if machines['4'] >= 4 else f"Level: {machines['4']}", background='#ff99b1')
        level_lbl.grid(row=4,column=2, padx=10, pady=10, sticky='nsew')
        cost_lbl = Label(frame.machine4, font=FONT_DEFAULT, text='' if machines['4'] >= 4 else f"Cost: {self.logic.upgrade_cost('4')}", background='#ff99b1')
        cost_lbl.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        Button(frame.machine4, text='Upgrade', bg='white', font=FONT_HEADING, command=lambda: self.logic.upgrade(self.currency_var, "4", chances_lbl, level_lbl, cost_lbl)).grid(row=4,column=1, padx=10, pady=10, sticky='nsew')

        #These are just placeholder Labels
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:', background='#ff99b1').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.day_var, width=12, anchor='w', background='#ff99b1').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='Debt:', background='#ff99b1').grid(row=0,column=3,padx=(20, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, textvariable=self.debt_var, width=12, anchor='w', background='#ff99b1').grid(row=0,column=4,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Turn:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.turn_var, width=12, anchor='w').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, textvariable=self.currency_var, width=12, anchor='w').grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Chances/Odds
        chances_lbl = self.create_odds_panel(frame, "4")

        #Buttons
        
        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine3')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Work')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')


        return frame

root = Tk()
root.resizable(False, False)
app = GUI(root)
root.mainloop()