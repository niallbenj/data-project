import dataLoader
import stemmer

load = dataLoader.loadData("testData")
result = load.getAllReports()
for report in result:
    wordsWithoutPunctuation = stemmer.getWords(report.bodyText)
    stemmer.stemParagraph(wordsWithoutPunctuation)
        
