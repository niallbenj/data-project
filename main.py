import dataLoader
import stemmer
import readTopics
from sklearn.preprocessing import MultiLabelBinarizer

load = dataLoader.loadData("testData")
reports = load.getAllReports()
topicDictionary = readTopics.readTopics()
myArray = []
for report in reports:
    myArray.append(topicDictionary.generateMultiLabelArray(report.topics))
    wordsWithoutPunctuation = stemmer.getWords(report.bodyText)
    stemmedWords = stemmer.stemWords(wordsWithoutPunctuation)
    removedStopWords = stemmer.removeStopWords(stemmedWords)
    print(removedStopWords)

labeledTopics = MultiLabelBinarizer().fit_transform(myArray)
