import dataLoader
import stemmer

load = dataLoader.loadData("testData")
reports = load.getAllReports()
for report in reports:
    wordsWithoutPunctuation = stemmer.getWords(report.bodyText)
    stemmedWords = stemmer.stemWords(wordsWithoutPunctuation)
    stemmer.removeStopWords(stemmedWords)
