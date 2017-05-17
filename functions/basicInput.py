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
    includeSingles = True if single label classifier models have been built
                          and are to be added to the main classification
                   = False Dont include the extra labels
    '''
    optimize = False  # False for main run / True for single
    allTrainingData = True
    jsonInRedis = True
    includeSingles = False
    latestFileNumber = 10  # go back to 4 for new classifier....
    return(optimize, allTrainingData, jsonInRedis, latestFileNumber,
           includeSingles)


def fileThresholds(red, fileStart):
    '''
    fileStart = which file to start classifying from
    '''
    return(int(red.hget(name='fileStartPosition', key=fileStart)))
