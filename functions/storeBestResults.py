def store(redis, singleTopic, reportNames, bestLabels):
    red2 = redis.Redis(host='localhost', port=6379, db=7)
    for reportName, labels in zip(reportNames, bestLabels):
        for label in labels:
            if label == singleTopic:
                red2.sadd(singleTopic, reportName)
