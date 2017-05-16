def returnJustBodiesAndTopics(load, red, jsonInRedis):
    reports = load.getAllReports(red, jsonInRedis)
    justBodies = []
    justTopics = []
    for report in reports:
        justBodies.append(report.bodyText)
        justTopics.append(report.topics)
    reports = None
    return(justBodies, justTopics)
