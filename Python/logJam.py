#Version 1.1
#          Created by:   Brian Roosevelt
#    Last Modified by:   David Toft

import gzip, shelve
from os import listdir
from os.path import isfile, join

#-----------------------------------Checks for/Opens data file "LogJamShelf.dat"--------------------------------------
try:
	if 'LogJamShelf.dat.dat'  not in listdir('.\\'):
		print('Saved settings and queries file not found.  New file will be created')
	ss = shelve.open('LogJamShelf.dat', flag='c',writeback=True)
except:
	print('ERROR: Default settings and queries file could not be created.')
	if input('Continue anyway[Y/N]').upper() != 'Y':
		exit()

#------------------------------------One time creation of pickle on shelf---------------------------------------------
if 'settings' not in ss or 1 not in ss['searches']:
	settings={'defaultDir':'.\\'}
	searches={1:'ERROR'}
	ss['settings']=settings
	ss['searches']=searches
ss.sync()

#-----------------------------------Finds Log's save location---------------------------------------------------------
inputDirectory = input('log directory ie(.\logs) (Press Enter to use most recent): ')
if inputDirectory == '':
	if 'lastDir' in ss['settings']:
		inputDirectory = ss['settings']['lastDir']
	else:
		inputDirectory = ss['settings']['defaultDir']
else:
	ss['settings']['lastDir'] = inputDirectory
		
#-----------------------------------Defines Filter text to parse for---------------------------------------------------
print('Saved searches: ')
for i in ss['searches'].keys():
	print(str(i)+': '+ss['searches'][i])
filterText = input('Enter searchterm, # of saved search (-# to delete), or press "Enter" for "Error": ')
if filterText=='':
	filterText=1
escape='N'
try:
	filterText=int(filterText)
	if filterText < 0:
		try:
			del ss['searches'][filterText*-1]
			escape='Y'
			ss.sync()
		except:
			print('Unable to delete, unknown key')
except:
	print('non-numeric input')
if escape=='Y':
	exit()
	
if filterText in ss['searches'].keys():
	filterText=ss['searches'][filterText]
else:
	filterText=str(filterText)
	if input('Would you like to save this search for later?(Y/y): ').upper() == 'Y':
		ss['searches'][len(ss['searches'])+1] = filterText

list10='N'
list10=input('Do you want only the [F]irst or [L]ast 10 values, Enter F/L or nothing: ').upper()

#------------------------------------defines save location for logs (or uses input)-------------------------------------
outputChoice = input('Output to File/Screen/Both[F,S,B]: ')
if outputChoice =='':
	outputChoice = 'S' #Makes Screen default output
if outputChoice.upper() == 'F' or outputChoice.upper() == 'B':
	outputFile = input('Output search results to file: ')
	if outputFile[:2] == '.\\':
		try:
			outFile = open(outputFile,'a')
		except:
			print('ERROR: Could not open output file.')
			exit()
	else:
		try:
			newOutputFile = str(inputDirectory)+str(outputFile) #fix this later
			outFile = open(newOutputFile,'a')
		except:
			print('ERROR: Could not open output file.')
			exit()
else:
	if outputChoice.upper() != 'S':
		print('ERROR: "%s" is not a valid output choice' % outputChoice.upper()) 
		exit()

#-----------------------------------searches log directory for files----------------------------------------------------
try:
	files = [f for f in listdir(inputDirectory) if isfile(join(inputDirectory, f)) and (f[-2:] == 'gz' or f[-3:] == 'log')]
except:
	print('ERROR: No .log or .gz files at this location: "%s"' % inputDirectory)
	exit()

#------------------------------------Prepares for output method----------------------------------------------------------
def outputLine(lineText):
	if outputChoice.upper() == 'F':
		outFile.write(lineText)
	elif outputChoice.upper() == 'B':
		outFile.write(lineText)
		print(lineText)		
	elif outputChoice.upper() == 'S':
		print(lineText)
		
#------------------------------------Iterates and finds search text------------------------------------------------------
totalMatchesFound = 0
listOfFiles=list(files)
if list10=='L':
	listOfFiles=reversed(listOfFiles)		
for file in listOfFiles:
	matchesFound = 0
	print('Extracting: ' + file)
	if file[-2:].upper() == 'GZ':
		unZip = gzip.open(join(inputDirectory, file),'r')
		lUnzip = list(unZip)
		if list10=='L':
			lUnzip=reversed(lUnzip)
		for line in lUnzip:
			text = line.decode('ascii')
			if filterText.upper() in text.upper():
				outputLine(text)
				matchesFound += 1
				totalMatchesFound += 1	
				if totalMatchesFound==10 and (list10=='F' or list10=='L'):
					print('Total matches found: %d' % totalMatchesFound)
					ss.close()
					exit()	
	elif file[-3:].upper() == 'LOG':
		logFile = open(join(inputDirectory, file),'r')
		lLogFile = list(logFile)
		if list10=='L':
			lLogFile=reversed(lLogFile)
		for line in lLogFile:
			if filterText.upper() in line.upper():
				outputLine(line)
				matchesFound += 1
				totalMatchesFound += 1
				if totalMatchesFound==10 and (list10=='F' or list10=='L'):
					print('Total matches found: %d' % totalMatchesFound)
					ss.close()
					exit()	
	print('Matches found: %d' % matchesFound)
print('Total matches found: %d' % totalMatchesFound)
ss.close()
