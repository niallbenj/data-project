def basic():
    '''
    allTrainingData = True to read from folder `trainingData`
                    = False to read from folder `subsetTraining`

    optimize = True to calculate F1 scores with incremental classifier
                    parameters
             = False Run classifier once with a set value list

    jsonInRedis = False useful for small cases where everything is read in
                    (memory intensive)
                = True to store everything in Redis and called one at a time,
                    useful for loading in multiple `*.json` files
    latestFileNumber = Number of .json files to include - 1
                       i.e. MUST be bigger than 1....
    '''
    optimize = True
    allTrainingData = True
    jsonInRedis = True
    latestFileNumber = 2
    return(optimize, allTrainingData, jsonInRedis, latestFileNumber)


def fileThresholds(red, fileStart):
    '''
    fileStart = which file to start classifying from
    '''
    return(int(red.hget(name='fileStartPosition', key=fileStart)))
