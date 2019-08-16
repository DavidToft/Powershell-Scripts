#JSearch.py
#version 1.0
#created by David Toft

import sys, json, csv

jsonimportfile=sys.argv[1]
print(jsonimportfile)
try:
	jData = open(jsonimportfile,'r+')
except:
	e = sys.exc_info()[1]
	print(e)
	print('Error opening json file')
	quit()
fields = ['@timestamp']
print('Which fields are you interested in? ("Enter" after each): ')
count=1
field="initialization"

while fields[-1] != '':
	field=input("Key("+str(count)+"): ")
	count+=1
	fields.append(field)
if fields[-1] == '': fields.remove(fields[-1])
headers = str(fields).replace('[','').replace(']','').replace("'",'')
csvOut = open(str(jsonimportfile[:-5]+'.csv'),'w+')
csvOut.write(headers+'\n')
for line in jData.readlines():
	i=json.loads(line)
	for j in range(len(fields)):
		try:
			if '.' in fields[j]:
				periodPlace=fields[j].find('.')
				print(i["_source"][fields[j][:periodPlace]][fields[j][periodPlace+1:]], end=", ",file=csvOut)
			else:
				print(i["_source"][fields[j]], end=", ", file=csvOut)
		except:
			print("Error, couldn't find "+fields[j]+' in json line: '+str(line), end='')
			print('Error: Not Found', end=", ", file=csvOut)
			pass
	print('\n',end='',file=csvOut)

jData.close()
csvOut.close()