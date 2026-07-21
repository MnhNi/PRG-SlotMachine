"""THE SLOTMACHINE"""
from tkinter import *


FONT_MAIN_TITLE = "Geomini 20 bold"
FONT_HEADING = "Geomini 12 bold"
FONT_DEFAULT = "Geomini 12"
#class Logic:
    

class GUI:
    def __init__(self, root):
        
        #self.logic = Logic()
        self.root = root
        self.root.title('Main menu')
        self.container = Frame(self.root)
        self.container.grid(row=0, column=0, sticky='nsew')
        

        self.frames = {}
        self.frames['Mainframe'] = self.create_main_frame()
        self.frames['Machine1'] = self.create_machine1_frame()
        # self.frames['Machine2'] = self.create_machine2_frame()
        # self.frames['Machine3'] = self.create_machine3_frame()
        # self.frames['Machine4'] = self.create_machine4_frame()


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

        Button(frame, text='PLAY', bg='white', font=FONT_HEADING, command=lambda:self.show_frame('Machine1')).grid(row=1,columnspan=2, padx=10, pady=10, sticky='nsew')

        return frame
    
    def create_machine1_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1)

        Label(frame, font=FONT_DEFAULT, text='Action:').grid(row=0,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='5').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')



root = Tk()
app = GUI(root)
root.mainloop()