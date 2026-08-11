"""          Assessment 91906 (Creating a Game)          """
from tkinter import *
from tkinter import messagebox
import math
import random

#Constant values
FONT_MAIN_TITLE = "Geomini 20 bold"
FONT_HEADING = "Geomini 12 bold"
FONT_DEFAULT = "Geomini 12"

money_range = {
    "1": {"minimum": 0,
          "maximum": 20},
    "2": {"minimum": 100,
          "maximum": 1000},
    "3": {"minimum": 5500,
          "maximum": 11000},
    "4": {"minimum": 100000,
          "maximum": 250000},
}

machine_winning = {
    "1": {'x1.5': 1.5, 'x2': 2, 'x3': 3, 'x10': 10},
    "2": {'Jaiden': 1, 'x2': 2, 'x5': 5, 'x100': 100, 'x2000': 2000},
    "3": {'EvilJaiden': 0.5, 'x5': 5, 'x100': 100, 'GoodJaiden': 2000},
    "4": {'x100': 100, 'x500': 500, 'ULTRAJaiden': 1000}
}

machine_odds = {
    "upgrade0": {"1": [250, 40, 8, 2],
                 "2": [10, 200, 79, 10, 1], # All chances are based on .../300
                 "3": [20, 220, 50, 10],
                 "4": [200, 80, 20]}

}


#Logic for the game
class Logic:

    #Variables that can be changed and saved
    def __init__(self):
        self.player_money = 50

    #Checking if the entry box is empty
    def get_input(self, entry):
        try:
            entry = int(entry)
            return entry
        except ValueError:
            messagebox.showwarning('Enter something','Please enter the appropriate value(A whole number)')

    #Checking if the amount entered is appropriate 
    def check_input(self, entry):
        input = self.get_input(entry)

        if input is not None:
            if input not in range(0, math.floor(self.player_money + 1)):
                messagebox.showwarning('POOR XD', 'You don\'t have enough money!')
                return False
            elif input in range(0, math.floor(self.player_money + 1)) and input in range(money_range['1']['minimum'], money_range['1']['maximum'] + 1):
                return True
            else:
                messagebox.showwarning('Out of range', 'Enter a value within the range')
                return False

    def roll(self, entry, currency, machine_number, slot1, slot2, slot3):
        status = self.check_input(entry)
        if status == True:
            self.player_money -= int(entry)
            currency.configure(text=self.player_money)
            random1 = random.choices(list(machine_winning[machine_number].keys()), weights=machine_odds['upgrade0'][machine_number])  # The machine upgrades will be implemented later on
            random2 = random.choices(list(machine_winning[machine_number].keys()), weights=machine_odds['upgrade0'][machine_number])
            random3 = random.choices(list(machine_winning[machine_number].keys()), weights=machine_odds['upgrade0'][machine_number])
            slot1.configure(text=random1)
            slot2.configure(text=random2)
            slot3.configure(text=random3)
            winning = random1[0]
            if random1 == random2 and random1 == random3:
                print('win')  # Placeholder for testing purposes
                self.player_money += int(entry)*machine_winning[machine_number][winning]
                currency.configure(text=self.player_money)
        

#The User interface (only for look and not very functional)

class GUI:
    def __init__(self, root):
        
        self.logic = Logic()
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

        slot1_1 = Label(frame.machine1, font=FONT_DEFAULT, text='1')
        slot1_1.grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        slot2_1 = Label(frame.machine1, font=FONT_DEFAULT, text='3')
        slot2_1.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        slot3_1 = Label(frame.machine1, font=FONT_DEFAULT, text='4')
        slot3_1.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

        Label(frame.machine1, font=FONT_DEFAULT, text='Max:$20', background='pink').grid(row=3, column=0, sticky='nsew')
        self.machine1_entry = Entry(frame.machine1)
        self.machine1_entry.grid(row=3,column=1, padx=10, pady=10, sticky='nsew')
        # Subject to change below
        Button(frame.machine1, text='Roll', bg='white', font=FONT_DEFAULT, command=lambda: self.logic.roll(self.machine1_entry.get(), self.currency1_lbl, "1", slot1_1, slot2_1, slot3_1)).grid(row=3,column=2, padx=10, pady=10, sticky='nsew')

        #Chances/Odds
        frame.odd = Frame(frame, bg='black')
        frame.odd.grid(row=3, column=0, rowspan=3, columnspan=3, sticky='nsew')

        #These are just placeholder Labels
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='2').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Action:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='1').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        self.currency1_lbl = Label(frame, font=FONT_DEFAULT, text=self.logic.player_money)
        self.currency1_lbl.grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Buttons
        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine4')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine2')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')


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
        Label(frame, font=FONT_DEFAULT, text='230').grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

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
        Label(frame, font=FONT_DEFAULT, text='230').grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

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

        Label(frame.machine4, font=FONT_DEFAULT, text='Max:$20', background='red').grid(row=3, column=0, sticky='nsew')
        self.machine4_entry = Entry(frame.machine4)
        self.machine4_entry.grid(row=3,column=1, padx=10)

        #These are just placeholder Labels
        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='2').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Action:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='4').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='230').grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Buttons
        
        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine3')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine1')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')


        return frame

root = Tk()
app = GUI(root)
root.mainloop()