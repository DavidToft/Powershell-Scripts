#from tkinter import *
import json
import datetime

data_file =".\..\json\date_data.json"

with open(data_file, "r") as read_file:
    data = json.load(read_file)
	
def getNextDate(restart):
	if restart['Restart']['Active']:
		dateNow = datetime.datetime.now()
		if "DueDate" in list(restart['Restart'].keys()):
			if restart['Restart']['DueDate']['Year'] == 0:
				dateList = []
				if restart['Restart']['DueDate']['Months'][0] == 0:
					for x in range(len(restart['Restart']['DueDate']['Days'])):
						if datetime.datetime(dateNow.year, dateNow.month, restart['Restart']['DueDate']['Days'][x]) < dateNow:
							if dateNow.month == 12:
								dateList.append(datetime.datetime(dateNow.year+1, 1, restart['Restart']['DueDate']['Days'][x])) 
							else:
								dateList.append(datetime.datetime(dateNow.year, dateNow.month + 1, restart['Restart']['DueDate']['Days'][x]))
						else:
							dateList.append(datetime.datetime(dateNow.year, dateNow.month, restart['Restart']['DueDate']['Days'][x])) 					
				else:
					for x in range(len(restart['Restart']['DueDate']['Months'])):
						if datetime.datetime(dateNow.year, restart['Restart']['DueDate']['Months'][x], restart['Restart']['DueDate']['Days'][x]) < datetime.datetime.now():
							dateList.append(datetime.datetime(dateNow.year+1, restart['Restart']['DueDate']['Months'][x], restart['Restart']['DueDate']['Days'][x])) 
						else:
							dateList.append(datetime.datetime(dateNow.year, restart['Restart']['DueDate']['Months'][x], restart['Restart']['DueDate']['Days'][x])) 
				return min(dateList)
			else:
				oneDate = datetime.datetime(restart['Restart']['DueDate']['Year'], restart['Restart']['DueDate']['Months'][0], restart['Restart']['DueDate']['Days'][0])
				if oneDate < dateNow:
					return None
				return oneDate
		if "Every" in list(restart['Restart'].keys()):
			
			
for x in data['Restarts']:
	print("Next Due Date is " + str(getNextDate(x)))
