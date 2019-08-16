## Created by David Toft

from tkinter import *
import json
import datetime

data_file ="data.json"


with open(data_file, "r") as read_file:
    data = json.load(read_file)
    
    
def boarderFrame(frame, d, color, sides="udlr"):
    if "u" in sides:
        topBumper = Frame(frame, height=d, bg=color)
        topBumper.pack(side=TOP, fill=X)
    if "l" in sides:
        leftBumper = Frame(frame, width=d, bg=color)
        leftBumper.pack(side=LEFT, fill=Y)
    if "r" in sides:
        rightBumper = Frame(frame, width=d, bg=color)
        rightBumper.pack(side=RIGHT, fill=Y)
    if "d" in sides:
        bottomBumper = Frame(frame, height=d, bg=color)
        bottomBumper.pack(side=BOTTOM, fill=X)

def menuCreation(frame, lineColor, BackGround):
    MenuButtonF = Frame(frame, bg=lineColor)
    boarderFrame(MenuButtonF, 3, BackGround, "udlr")
    boarderFrame(MenuButtonF, 3, lineColor, "ud")
    boarderFrame(MenuButtonF, 1, BackGround, "ud")
    boarderFrame(MenuButtonF, 1, lineColor, "ud")
    widenFrame = Frame(MenuButtonF, width=9, bg="blue")
    widenFrame.pack()
    MenuButtonF.grid(column=0)
    

## Window Creation
master = Tk()
master.minsize(width=100, height=200)
boarderFrame(master, 2, "black")
boarderFrame(master, 5, "light blue")

#Main Frames declaration
headerFrame = Frame(master)
boarderFrame(headerFrame, 5, "light blue", "d")
headerFrame.pack(side=TOP, fill=X)
#headerFrame.grid(row=0, column=0)
topFrame = Frame(master)
topFrame.pack(side=TOP, fill=X)
#topFrame.grid(row=1, column=0)
#boarderFrame(topFrame, 1, "black")
bottomFrame = Frame(master)
bottomFrame.pack(side=BOTTOM)
#bottomFrame.grid(row=2, column=0)

Header = Label(headerFrame, text="Reminder++", fg="blue", bg="grey", font=("Times New Roman",18))

Header.pack(side=TOP, fill=X)
#Header.grid(row=0, column=0)
menuCreation(topFrame, "blue", "grey")

mainloop()




# How to:
#label_1 = Label(<Frame>, text="<Label Text>", fg="blue", bg="grey", font=("Times New Roman",18))
#button_1 = Button(<Frame>, text="<Button Text>", fg="green")
