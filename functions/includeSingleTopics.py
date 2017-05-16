def include(red, newLabels, reportName):
    allKeys = red.keys("*")
    for singleKey in allKeys:
        member = red.sismember(singleKey, reportName)
        if member:
            newLabels = newLabels + (singleKey, )
    return(newLabels)
