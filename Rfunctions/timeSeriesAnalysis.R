#'
#' @title Import JSON objects and store only the publication 
#'        Data and the topic list for time series trends
#'        
#' @output if onlyTopics = True:
#'           -> topicCounts per half-year
#'           
#'         if onlyTopics = False:
#'           -> How many articles in a day per half-year
#'

library('rjson')
library('prophet')
library('rredis')

########################################
rredis::redisConnect(host = 'localhost',
                     port = 6379)
rredis::redisSelect(1)
rredis::redisFlushDB()

###############################################
workingDirectory <- "~/Desktop/project/data-project/trainingData/"
dataFiles <- list.files(path = workingDirectory,
                       pattern = ".json")
dataFiles <- sort(dataFiles)
onlyTopics <- TRUE

################################
for (i in 1:length(dataFiles)) {
  print(paste0("Reading data file ", i, "/", length(dataFiles)))
  dataSet <- paste0(workingDirectory, dataFiles[i])
  jsonData <- rjson::fromJSON(paste(readLines(dataSet), collapse=""))
  rredis::redisConnect(host = 'localhost',
                       port = 6379)
  rredis::redisSelect(1)
  
  for (j in 1:length(jsonData$TrainingData)) {
    newDate <- jsonData$TrainingData[[j]]$webPublicationDate
    topics <- jsonData$TrainingData[[j]]$topics
    
    if (onlyTopics) {
      if (length(topics) > 0) {
        for (k in 1:length(topics)) {
          rredis::redisIncr(key=paste0(dataFiles[i], ":", topics[k]))
        }
      }
    } else {
      newDate <- strptime(newDate, format = '%d-%m-%Y')
      
      # Check if the date exists within this JSON or not..
      belongsToSet <- rredis::redisSIsMember(set = as.character('dates'), 
                                             element = as.character(newDate))
  
      if (belongsToSet) {
        rredis::redisIncr(key = as.character(newDate))
      } else {
        rredis::redisSAdd(set = as.character('dates'),
                          element = charToRaw(as.character(newDate)))
        rredis::redisSet(key = as.character(newDate),
                         value = charToRaw(as.character(1)))
      }
    }
  }
  # Delete the Set.. nothing more to do for topics!!
  if (!onlyTopics) {
    rredis::redisDelete(key = as.character('dates'))
    
    allKeys <- rredis::redisKeys(pattern = '*')
    totalNumb <- 0
    for (k in 1:length(allKeys)) {
      counts <- rredis::redisGet(key = allKeys[k])
      rredis::redisDelete(key = allKeys[k])
      counts <- as.integer(counts)
      totalNumb <- totalNumb + counts
      holdFrame <- data.frame(timestamp = allKeys[k],
                              count = counts)
      if (k != 1) {
        totalFrame <- rbind(totalFrame, holdFrame)
      } else {
        totalFrame <- holdFrame
      }
    }
    
    if (i != 1) {
      biggestFrame <- rbind(biggestFrame, totalFrame)
    } else {
      biggestFrame <- totalFrame
    }
  }
}

##### TOPIC INFORMATION #####
topicNames <- c("test")
topicNames <- read.delim(file = "~/Desktop/project/data-project/topicDictionary.txt", header= FALSE, sep = "\n")
notTopicNames <- read.delim(file = "~/Desktop/project/data-project/NOTinTopicDictionary.txt", header= FALSE, sep = ",")
topicDataFrame <- data.frame()
rredis::redisSelect(1)

#### GET TOPICS FROM REDIS - PROPHET #####
for (i in 1:nrow(topicNames)) {
  singleTopic <- as.character(topicNames$V1[i])
  count <- 0
  value <- 0
  bigFrame <- data.frame()
  for (j in 1:length(dataFiles)) {
    count <- count + 1
    value <- rredis::redisGet(key = paste0(dataFiles[j], ":", singleTopic))
    if (!is.null(value)) {
      value <- as.integer(value)
    }
    holdingFrame <- data.frame(ds = Sys.Date() + count,
                               y = value)
    if (j == 1) {
      bigFrame <- holdingFrame
    } else {
      bigFrame <- rbind(bigFrame, holdingFrame)
    }
  }
  
  forecastInt <- 0
  if (sum(bigFrame$y) > 50) {
    m <- prophet(bigFrame)
    future <- make_future_dataframe(m, periods = 1)
    forecast <- predict(m, future)
    forecastFloat <- forecast$trend_upper[33]
    forecastInt <- as.integer(forecastFloat)

    if (forecastFloat > forecast$trend_upper[32]) {
      forecastInt <- as.integer(forecastFloat*(forecast$trend_upper[32]/forecastFloat))
    }
  }

  holdFrame <- data.frame(topicName = singleTopic,
                          forecast = forecastInt)
  if (i == 1) {
    topicDataFrame <- holdFrame
  } else {
    topicDataFrame <- rbind(topicDataFrame, holdFrame)
  }
}

#### GET TOPICS FROM REDIS - CALCULATE GRADIENT BETWEEN LAST TWO POINTS #####
bigFrame <- data.frame()
for (i in 1:nrow(topicNames)) {
  singleTopic <- as.character(topicNames$V1[i])
 
  fileLast <- "2014b_TrainingData.json"
  filePrev <- "2014a_TrainingData.json"
  value2 <- rredis::redisGet(key = paste0(fileLast, ":", singleTopic))
  value1 <- rredis::redisGet(key = paste0(filePrev, ":", singleTopic))

  if (is.null(value2) || is.null(value1)) {
    predictedOutput <- 0
  } else {
    value2 <- as.integer(value2)
    value1 <- as.integer(value1)
    if (value2 < 3 || value1 < 3) {
      predictedOutput <- -1
    } else {
      gradient = value2 - value1
      intersect = value2 - 2*(gradient)
      predictedOutput = 3*(gradient) + intersect
    }
    if (predictedOutput < 0) {
      predictedOutput <- 0
    }    
  }
  
  holdingFrame <- data.frame(topicName = singleTopic,
                             forecast = predictedOutput)

  if (i == 1) {
    bigFrame <- holdingFrame
  } else {
    bigFrame <- rbind(bigFrame, holdingFrame)
  }
}


# Delete specific patterns if required.
deleteThese <- rredis::redisKeys(pattern = 'x')
for (i in 1:length(deleteThese)) {
  rredis::redisDelete(key=deleteThese[i])
}

############ UNIQUE ARTICLES PER DAY ######################
# Keep results in totalFrameNew before any manipulations
totalFrameNew <- biggestFrame
halfYear <- 182 # half a year...
predictData <- biggestFrame[order(as.Date(biggestFrame$timestamp)), ]
names(predictData) <- c("ds", "y")
m <- prophet(predictData)
future <- make_future_dataframe(m, periods = 1)
forecast <- predict(m, future)
as.integer(forecast$trend_upper[33])
plot(m, forecast)
