def store(redis, singleTopic, reportNames, bestLabels):
    red2 = redis.Redis(host='localhost', port=6379, db=7)
    icount = 0
    for reportName, labels in zip(reportNames, bestLabels):
        for label in labels:
            if label == singleTopic:
                icount += 1
                red2.sadd(singleTopic, reportName)
    if (icount == 0):
        red2.sadd(singleTopic, 0)
