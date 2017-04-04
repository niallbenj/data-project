import json
from os import listdir
from os.path import isfile, join

class loadData():

    def __init__(self, direct):
        self.allJSON = [files for files in listdir(direct)]

    def returnData(self):
	self.
	for singleFile in self.allJSON:
	    myFile = json.loads(open(singleFile).read())
            entries = myFile['TrainingData']
	    for item in entries:
                publishDate = entries['webPublicationDate'] 
		topics = entries['topics']
		bodyText = entries['bodyText']
	return(publishDate, topics, bodyText)


main ()

for loop...
 loadData
dict = 
print(myFile['TrainingData']['1999a_TrainingData_00001']['bodyText'])
print(len(myFile['TrainingData']))
for item in myFile['TrainingData']:
    print(item)


