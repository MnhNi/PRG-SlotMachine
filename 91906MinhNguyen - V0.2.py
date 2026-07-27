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
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1)
        
        #Top bar
        frame.top_frame = Frame(frame, bg='pink')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')

        #These are just placeholder Labels


        Label(frame.top_frame, font=FONT_DEFAULT, text='Day:').grid(row=0,column=1,padx=(50, 0),pady=10,sticky='nsew')
        Label(frame.top_frame, font=FONT_DEFAULT, text='2').grid(row=0,column=2,padx=10,pady=10,sticky='nsew')

        Label(frame, font=FONT_DEFAULT, text='Action:').grid(row=1,column=1,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='1').grid(row=1,column=2,padx=10,pady=10,sticky='nsw')

        Label(frame, font=FONT_DEFAULT, text='Money:').grid(row=1,column=3,padx=10,pady=10,sticky='nsew')
        Label(frame, font=FONT_DEFAULT, text='230').grid(row=1,column=4,padx=10,pady=10,sticky='nsw')

        #Buttons
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')
        Button(frame, text='<', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine4')).grid(row=1,column=0, padx=10, pady=10, sticky='nsew')
        Button(frame, text='>', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Machine2')).grid(row=1,column=6, padx=10, pady=10, sticky='nsew')


        return frame
    
    def create_machine2_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1)

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
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1)

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
        frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)
        frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1)

        #Top bar
        frame.top_frame = Frame(frame, bg='pink')
        frame.top_frame.grid(row=0, columnspan=7, sticky='ew')
        Button(frame.top_frame, text='Menu', bg='white', font=FONT_HEADING, command=lambda: self.show_frame('Mainframe')).grid(row=0,column=0, padx=(0, 50), pady=10, sticky='nsew')
        
        #Machine
        frame.machine = Frame(frame, bg='red')
        frame.machine.grid(row=3, column=3, rowspan=3, columnspan=4, sticky='nsew')
        frame.machine.rowconfigure(5)
        frame.machine.columnconfigure(3)

        Label(frame.machine, font=FONT_DEFAULT, text='Machine4', background='red').grid(row=0, columnspan=3, sticky='nsew')
        Label(frame.machine, font=FONT_DEFAULT, text='1').grid(row=1, column=0, padx=10,pady=10, sticky='nsew')
        Label(frame.machine, font=FONT_DEFAULT, text='3').grid(row=1, column=1, padx=10,pady=10, sticky='nsew')
        Label(frame.machine, font=FONT_DEFAULT, text='4').grid(row=1, column=2, padx=10,pady=10, sticky='nsew')
        

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