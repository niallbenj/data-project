def toCSV(csvWriter, reportName, labelsInReport, allLabels):
    csvRow = [0] * len(allLabels)
    for label in labelsInReport:
        csvRow[allLabels.index(label)] = 1
    csvRow.insert(0, reportName)
    csvWriter.writerow(csvRow)
