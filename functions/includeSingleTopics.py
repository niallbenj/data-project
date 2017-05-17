def include(red, newLabels, reportName, count2):
    allKeys = red.keys("*")
    for singleKey in allKeys:
        member = red.sismember(singleKey, reportName)
        decodedKey = singleKey.decode("utf-8")
        if member and (decodedKey not in newLabels):
            count2 += 1
            newLabels = newLabels + (decodedKey, )
            print(newLabels)
    return(newLabels, count2)
