def returnJustBodiesAndTopics(load):
    reports = load.getAllReports()
    justBodies = []
    justTopics = []
    for report in reports:
        justBodies.append(report.bodyText)
        justTopics.append(report.topics)
    reports = []
    return(justBodies, justTopics)
