def reshapeBodyText(newText, exclude):
    newText = newText.decode()
    newText = ''.join(ch for ch in newText if ch not in exclude)
    newText = newText.split()
    myBodyText = [str(x).lower() for x in newText]
    return(myBodyText)


def guess(labels, notInTraining, myBodyText):
    for newLabel in notInTraining:
        value = 0
        totalCount = 0
        if newLabel in labels:
            pass
        else:
            for item in notInTraining[newLabel]:
                if item in myBodyText:
                    value = value + 1
                    totalCount = totalCount + myBodyText.count(item)
            if (value == len(notInTraining[newLabel])):
                if (totalCount > 6):
                    labels = labels + (newLabel, )
    return(labels)
