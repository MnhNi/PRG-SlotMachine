"""          Assessment 91906 (Creating a Game)          """
from tkinter import *
from tkinter import messagebox
import math
import random
import json

#Constant values
FONT_MAIN_TITLE = "Geomini 20 bold"
FONT_HEADING = "Geomini 12 bold"
FONT_DEFAULT = "Geomini 12"

money_range = {
    "1": {"minimum": 0,
          "maximum": 20},
    "2": {"minimum": 100,
          "maximum": 1000},
    "3": {"minimum": 5000,
          "maximum": 11000},
    "4": {"minimum": 100000,
          "maximum": 250000},
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
            "4": [499, 500, 1]},
    "3": {"1": [100, 700, 199, 1],
            "2": [5, 100, 700, 194, 1],
            "3": [500, 400, 99, 1],
            "4": [498, 501, 1]},
    "4": {"1": [40 ,100, 849, 11],
            "2": [1, 1, 793, 90, 11],
            "3": [600, 399, 1],
            "4": [490, 505, 5]}
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
print(player_money)

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


#Logic for the game
class Logic:

    def __init__(self, root):
        self.root = root

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
        print(player_money)
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

    def configure_slots(self, slot1, slot2, slot3, machine_number):
        upgrade = "1"  #str(machines[machine_number])
        random1 = random.choices(list(machine_winning[machine_number].keys()), weights=machine_odds[upgrade][machine_number])  # The machine upgrades will be implemented later on
        random2 = random.choices(list(machine_winning[machine_number].keys()), weights=machine_odds[upgrade][machine_number])
        random3 = random.choices(list(machine_winning[machine_number].keys()), weights=machine_odds[upgrade][machine_number])
        slot1.configure(text="")
        slot2.configure(text="")
        slot3.configure(text="")
        # for t in range(1, 40):
        #     if t <= 10:
        #         self.root.after(100, lambda: slot1.configure(text=random.choices(list(machine_winning[machine_number].keys()))))
        #     if t > 10:
        #         self.root.after(100, lambda: slot1.configure(text=random1))
        #     if t <= 20:
        #         self.root.after(100, lambda: slot2.configure(text=random.choices(list(machine_winning[machine_number].keys()))))
        #     if t > 20:
        #         self.root.after(100, lambda: slot2.configure(text=random2))
        #     if t <= 30:
        #         self.root.after(100, lambda: slot3.configure(text=random.choices(list(machine_winning[machine_number].keys()))))
        #     if t > 30:
        #         self.root.after(100, lambda: slot3.configure(text=random3))
        #     self.root.update()
        self.root.after(500, lambda: slot1.configure(text=random1))
        self.root.after(1000, lambda: slot2.configure(text=random2))
        self.root.after(1500, lambda: slot3.configure(text=random3))

        return random1, random2, random3


    def roll(self, entry, currency, machine_number, slot1, slot2, slot3, button):
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
            currency.configure(text=player_money)
            random1, random2, random3 = self.configure_slots(slot1, slot2, slot3, machine_number)
            if random1[0] in ['x1000', 'x2000', 'GoodJaiden', 'ULTRAJaiden']:
                player_money += int(entry)*machine_winning[machine_number][random1[0]]
                self.root.after(1500, lambda: currency.configure(text=player_money))
                self.root.after(1500, lambda: slot1.configure(bg='green'))
            elif random2[0] in ['x1000', 'x2000', 'GoodJaiden', 'ULTRAJaiden']:
                player_money += int(entry)*machine_winning[machine_number][random2[0]]
                self.root.after(1500, lambda: currency.configure(text=player_money))
                self.root.after(1500, lambda: slot2.configure(bg='green'))
            elif random3[0] in ['x1000', 'x2000', 'GoodJaiden', 'ULTRAJaiden']:
                player_money += int(entry)*machine_winning[machine_number][random3[0]]
                self.root.after(1500, lambda: currency.configure(text=player_money))
                self.root.after(1500, lambda: slot3.configure(bg='green'))
            elif random1[0] == random2[0] and random1[0] == random3[0]:
                print('win')  # Placeholder for testing purposes
                player_money += int(entry)*machine_winning[machine_number][random1[0]]
                self.root.after(1500, lambda: currency.configure(text=player_money))
                self.root.after(1500, lambda: slot1.configure(bg='yellow'))
                self.root.after(1500, lambda: slot2.configure(bg='yellow'))
                self.root.after(1500, lambda: slot3.configure(bg='yellow'))

        # Re-enable button after 2 seconds (2000 milliseconds)
        self.root.after(2000, lambda: button.config(state='normal'))

    def upgrade(self, currency, machine_number):
        global player_money
        global machines
        player_money = float(player_money)
        if machines[machine_number] <= 4:
            if player_money >= (100 * int(machine_number)**2) * machines[machine_number]:
                player_money -= (100 * int(machine_number)**2) * machines[machine_number]
                machines[machine_number] += 1
                self.save_player_money()
                with open("machine_level.json", "w") as f:
                    json.dump(machines, f, indent=4)
                currency.configure(text=player_money)
            else:
                messagebox.showwarning('POOR XD', 'You don\'t have enough money!')
        else:
            messagebox.showwarning('MAX LEVEL', 'Can\'t upgrade anymore!')
    
    def working(self, currency):
        global player_money
        player_money = float(player_money)
        player_money += 100
        self.save_player_money()
        currency.configure(text=player_money)

    # def load_chance(self, label, machine_number):
    #     for i in machine_winning:
    #         string
#The User interface (only for look and not very functional)

class GUI:
    def __init__(self, root):
        
        self.logic = Logic(root)
        self.root = root
        self.root.title('Addiction')
        self.container = Frame(self.root)
        self.container.grid(row=0, column=0)
        

        self.frames = {}
        self.frames['Mainframe'] = self.create_main_frame()
        self.frames['Machine1'] = self.create_machine1_frame()
        self.frames['Machine2'] = self.create_machine2_frame()
        self.frames['Machine3'] = self.create_machine3_frame()
        self.frames['Machine4'] = self.create_machine4_frame()


        self.show_frame("Mainframe")
    
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
    
    def create_main_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0,column=0,sticky='nsew')
        frame.columnconfigure([0, 1], minsize=200, weight=1)
        frame.rowconfigure([0, 1], minsize=100, weight=1)
        
        Label(frame, font=FONT_MAIN_TITLE, text='Addiction').grid(row=0,columnspan=2,padx=10,pady=10,sticky='nsew')

        Button(frame, text='PLAY', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine1')).grid(row=1,columnspan=2, padx=10, pady=10, sticky='nsew')

        return frame
    
    def create_machine1_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1, uniform='machine')
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1, uniform='machine')
        
        #Top bar
        frame.top_frame = Frame(frame, bg='pink')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')
        
        #Machine
        frame.machine1 = Frame(frame, bg='pink')
        frame.machine1.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.machine1.rowconfigure([0,1,2,3,4,5], minsize=50, weight=1, uniform='machinerow')
        frame.machine1.columnconfigure([0,1,2], minsize=50,weight=1, uniform='machinecolumn')

        Label(frame.machine1, font=FONT_DEFAULT, text='Machine1', background='pink').grid(row=0, columnspan=3, sticky='nsew')

        # These 3 Label will be changed to something more configurable in the next session

        slot1_1 = Label(frame.machine1, font=FONT_DEFAULT, text='')
        slot1_1.grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        slot2_1 = Label(frame.machine1, font=FONT_DEFAULT, text='')
        slot2_1.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        slot3_1 = Label(frame.machine1, font=FONT_DEFAULT, text='')
        slot3_1.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        Label(frame.machine1, font=FONT_DEFAULT, text='Max:$20', background='pink').grid(row=3, column=0, sticky='nsew')
        self.machine1_entry = Entry(frame.machine1)
        self.machine1_entry.grid(row=3,column=1, padx=10, pady=10, sticky='nsew')
        # Subject to change below
        self.roll_button1 = Button(frame.machine1, text='Roll', bg='white', font=FONT_DEFAULT, command=lambda: self.logic.roll(self.machine1_entry.get(), self.currency1_lbl, "1", slot1_1, slot2_1, slot3_1, self.roll_button1))
        self.roll_button1.grid(row=3,column=2, padx=10, pady=10, sticky='nsew')

        #Chances/Odds
        frame.odd = Frame(frame, bg='black')
        frame.odd.grid(row=3, column=0, rowspan=3, columnspan=3, sticky='nsew')
        # chances_lbl = Label(frame.odd, font=FONT_DEFAULT, text='', bg='black')

        #These are just placeholder Labels
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='2').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Action:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='1').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        self.currency1_lbl = Label(frame, font=FONT_DEFAULT, text=player_money)
        self.currency1_lbl.grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Buttons
        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine4')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine2')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')
        Button(frame.machine1, text='Work(+$100)', bg='white', font=FONT_HEADING, command=lambda: self.logic.working(self.currency1_lbl)).grid(row=4,column=0, padx=10, pady=10, sticky='nsew')


        return frame
    
    def create_machine2_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1, uniform='machine')
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1, uniform='machine')

        #Top bar
        frame.top_frame = Frame(frame, bg='pink')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')

        #These are just placeholder Labels
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='2').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Action:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='2').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        self.currency2_lbl = Label(frame, font=FONT_DEFAULT, text=player_money)
        self.currency2_lbl.grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Machine
        frame.machine2 = Frame(frame, bg='blue')
        frame.machine2.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.machine2.rowconfigure([0,1,2,3,4,5], minsize=50, weight=1, uniform='machinerow')
        frame.machine2.columnconfigure([0,1,2], minsize=50,weight=1, uniform='machinecolumn')

        Label(frame.machine2, font=FONT_DEFAULT, text='Machine2', background='blue').grid(row=0, columnspan=3, sticky='nsew')

        slot1_2 = Label(frame.machine2, font=FONT_DEFAULT, text='')
        slot1_2.grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        slot2_2 = Label(frame.machine2, font=FONT_DEFAULT, text='')
        slot2_2.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        slot3_2 = Label(frame.machine2, font=FONT_DEFAULT, text='')
        slot3_2.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        Label(frame.machine2, font=FONT_DEFAULT, text='Max:$1000', background='blue').grid(row=3, column=0, sticky='nsew')
        self.machine2_entry = Entry(frame.machine2)
        self.machine2_entry.grid(row=3,column=1, padx=10, pady=10, sticky='nsew')
        self.roll_button2 = Button(frame.machine2, text='Roll', bg='white', font=FONT_DEFAULT, command=lambda: self.logic.roll(self.machine2_entry.get(), self.currency2_lbl, "2", slot1_2, slot2_2, slot3_2, self.roll_button2))
        self.roll_button2.grid(row=3,column=2, padx=10, pady=10, sticky='nsew')
        Button(frame.machine2, text='Work(+$100)', bg='white', font=FONT_HEADING, command=lambda: self.logic.working(self.currency2_lbl)).grid(row=4,column=0, padx=10, pady=10, sticky='nsew')

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
        frame.top_frame = Frame(frame, bg='pink')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')

        #These are just placeholder Labels
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='2').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Action:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='3').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        self.currency3_lbl = Label(frame, font=FONT_DEFAULT, text=player_money)
        self.currency3_lbl.grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Machine
        frame.machine3 = Frame(frame, bg='green')
        frame.machine3.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.machine3.rowconfigure([0,1,2,3,4,5], minsize=50, weight=1, uniform='machinerow')
        frame.machine3.columnconfigure([0,1,2], minsize=50,weight=1, uniform='machinecolumn')

        Label(frame.machine3, font=FONT_DEFAULT, text='Machine3', background='green').grid(row=0, columnspan=3, sticky='nsew')

        slot1_3 = Label(frame.machine3, font=FONT_DEFAULT, text='')
        slot1_3.grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        slot2_3 = Label(frame.machine3, font=FONT_DEFAULT, text='')
        slot2_3.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        slot3_3 = Label(frame.machine3, font=FONT_DEFAULT, text='')
        slot3_3.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        Label(frame.machine3, font=FONT_DEFAULT, text='Max:$11000', background='green').grid(row=3, column=0, sticky='nsew')
        self.machine3_entry = Entry(frame.machine3)
        self.machine3_entry.grid(row=3,column=1, padx=10, pady=10, sticky='nsew')
        self.roll_button3 = Button(frame.machine3, text='Roll', bg='white', font=FONT_DEFAULT, command=lambda: self.logic.roll(self.machine3_entry.get(), self.currency3_lbl, "3", slot1_3, slot2_3, slot3_3, self.roll_button3))
        self.roll_button3.grid(row=3,column=2, padx=10, pady=10, sticky='nsew')
        Button(frame.machine3, text='Work(+$100)', bg='white', font=FONT_HEADING, command=lambda: self.logic.working(self.currency3_lbl)).grid(row=4,column=0, padx=10, pady=10, sticky='nsew')

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
        frame.top_frame = Frame(frame, bg='pink')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')
        
        #Machine
        frame.machine4 = Frame(frame, bg='red')
        frame.machine4.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.machine4.rowconfigure([0,1,2,3,4,5], minsize=50, weight=1, uniform='machinerow')
        frame.machine4.columnconfigure([0,1,2], minsize=50,weight=1, uniform='machinecolumn')

        Label(frame.machine4, font=FONT_DEFAULT, text='Machine4', background='red').grid(row=0, columnspan=3, sticky='nsew')
        Label(frame.machine4, font=FONT_DEFAULT, text='1').grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        Label(frame.machine4, font=FONT_DEFAULT, text='3').grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        Label(frame.machine4, font=FONT_DEFAULT, text='4').grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        Label(frame.machine4, font=FONT_DEFAULT, text='Max:$250000', background='red').grid(row=3, column=0, sticky='nsew')
        self.machine4_entry = Entry(frame.machine4)
        self.machine4_entry.grid(row=3,column=1, padx=10, pady=10, sticky='nsew')
        self.roll_button4 = Button(frame.machine4, text='Roll', bg='white', font=FONT_DEFAULT, command=lambda: self.logic.roll(self.machine4_entry.get(), self.currency4_lbl, "4", Label(frame.machine4), Label(frame.machine4), Label(frame.machine4), self.roll_button4))
        self.roll_button4.grid(row=3,column=2, padx=10, pady=10, sticky='nsew')
        Button(frame.machine4, text='Work(+$100)', bg='white', font=FONT_HEADING, command=lambda: self.logic.working(self.currency4_lbl)).grid(row=4,column=0, padx=10, pady=10, sticky='nsew')

        #These are just placeholder Labels
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='2').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Action:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='4').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        self.currency4_lbl = Label(frame, font=FONT_DEFAULT, text=player_money)
        self.currency4_lbl.grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Buttons
        
        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine3')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine1')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')


        return frame

root = Tk()
app = GUI(root)
root.mainloop()
