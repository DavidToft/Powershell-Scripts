## Created by David Toft

from tkinter import *
import json
import datetime

data_file ="data.json"


with open(data_file, "r") as read_file:
    data = json.load(read_file)
    
def categoryFrameCreation(catName, catData):
    categoryFrame = Frame(topFrame, bg="light yellow")
    categoryFrame.pack(side=TOP, fill=X)
    categoryButton = Button(categoryFrame, text=catName)
    categoryButton.pack(side=TOP, fill=X)
    indentFrame = Frame(categoryFrame, width=15, bg="dark grey")
    indentFrame.pack(side=LEFT, fill=Y)
    for reminder in catData:
        date = datetime.datetime.now().date()
        if 'By' in list(reminder['Restart'].keys()):
            date = datetime.datetime("YYYY","MM","DD").date()
        reminderFrameCreation(categoryFrame, reminder['Name'], )

def reminderFrameCreation(catFrame, name, index, due):
    reminderFrame = Frame(catFrame, bg="white")
    reminderFrame.pack(side=TOP, fill=X)
    boarderFrame(reminderFrame, 1, "black")

    voteFrame = Frame(reminderFrame, width=15)
    voteFrame.pack(side=RIGHT, fill=Y)
    boarderFrame(voteFrame, 2, "black", "l")
    upDoot = Frame(voteFrame, bg="orange", width=14, height=12)
    upDoot.pack(side=TOP, fill=X)
    downDoot = Frame(voteFrame, bg="blue", width=14, height=12)
    downDoot.pack(side=BOTTOM, fill=X)

    reminder = Label(reminderFrame, text=index+': '+name, fg="green", bg="white")
    reminder.pack(side=LEFT, fill=X)
    dateLabel = Label(reminderFrame, text=due, fg="black", bg="white")
    dateLabel.pack(side=RIGHT)

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


## Window Creation
master = Tk()
master.minsize(width=100, height=200)
boarderFrame(master, 2, "black")
boarderFrame(master, 5, "light blue")

#Main Frames declaration
headerFrame = Frame(master)
headerFrame.pack(side=TOP, fill=X)
midBumper = Frame(master, height=5, bg="light blue")
midBumper.pack(side=TOP, fill=X)
topFrame = Frame(master)
topFrame.pack(side=TOP, fill=X)
boarderFrame(topFrame, 1, "black")
bottomFrame = Frame(master)
bottomFrame.pack(side=BOTTOM)

header1 = Label(headerFrame, text="Reminder++", fg="blue", bg="grey", font=("Times New Roman",18))
button1 = Button(bottomFrame, text="Button 1", fg="green")
button2 = Button(bottomFrame, text="Button 2", fg="blue")

#Display creation
for category in data['Reminders']:
    catName = list(category.keys())[0] #Key name of category
    categoryFrameCreation(catName, category[catName]) 

#    for y in range(len(data['Reminders'][x])):
#        reminderFrameCreation(data['Reminders'][x][y]['Name'], str(x+1), date)

header1.pack(side=TOP, fill=X)
button1.pack(side=LEFT)
button2.pack(side=RIGHT)

#w = Label(master, text=reminder_name)
#w.pack() #organizes widgets in blocks before placing them in the parent. (packs it in)

mainloop()



for x in data['Reminders']:
    catName = list(x.keys())[0]
    print(catName)
    for y in x[catName]:
        print('    ' + y['Name'])





#~ Desired Features:
    #~ Easy task Addition
    #~ Optional Date/Repeat Preferences
    #~ Special Category Tag for Sub-Selection/Label
    #~ Task Selected Sub-Items:
        #~ Highlighed
        #~ Directly Under Parent task:
            #~ Complete Button
            #~ Move to Top Option
            #~ Tags show/hide
        #~ Sub-Tasks
    #~ Menu Items:
        #~ Tags Library:
            #~ Sorted List of all tags with links to that sub selection
        #~ Cleanup feature of old tasks
        #~ Multi-Delete
        #~ View Completed Sub-Tasks Checkbox


































