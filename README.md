# Growing Instability: Classifying Crisis Reports
Below are the details for the data science challenge, starting on Monday 3rd April 2017 (6 week long) from DSTL.

### Getting Started
To get this project to run the following python dependencies are required. Run the following from root
```
sudo chmod +x ./scripts/setup.sh   # for permissions
./scripts/setup.sh   # install the required python modules
```
Then finally, run
```
python main.py
```

### Context
Imagine this scenario: A region’s stability is in decline due to unrest, crime and terrorism. We need a better understanding of this humanitarian crisis to decide how best to support the situation, gained through the information contained within a set of reports.

The challenge: We have acquired news articles containing potentially relevant information. Using these, we need you to use historical reports to determine the topics for new articles so that they can be classified and prioritised. This will allow analysts to focus on only the most pertinent details of this developing crisis.

### Data
The data for this challenge has been acquired from a major international news provider, the Guardian. The training data represents the past historical record, and the test data represents new documents that require classification.

The datasets consist of:

  - Training data (TrainingData.zip): All the news articles published between 1999 and 2014. [2.3GB]
  - Test data (TestData.zip): A sample of the news articles published between 2015 and 2016. [13.8MB]
  - Topic dictionary (topicDictionary.txt): A list of topics for classifying articles that improve awareness of the developing crisis. [2.1KB]
  - Sample submission (sampleSubmission.csv): A sample submission file with the correct format but random topic predictions. [2.4MB]

### The Solution
You are required to classify each test article by predicting its topics. Your solution must:

  - Classify each test article by predicting the presence or absence of only those topics that are provided in the topic dictionary.
  - For each test article, predict a ‘1’ or ‘0’ for each topic in the dictionary where ‘1’ predicts the topic is present and ‘0’ predicts it is absent.

Each article may be classified by predicting that is has multiple topics, only one topic, or no topics from the tag dictionary.

The training data can be used in any way you wish (subject to the data terms in the Official Rules) in order to build your solution and predict topics for the test articles as accurately as you can. 

# Input
The input is in the form of a configuration file found @ `input.yaml`, and can be adjusted directly. The following definitions are listed below. Grab the latest config in the repo for a default run.

### singleClassify
  -  `true` : A binary single classification or empty.
  - `false` : For a normal classification process.

### ignore
  -  `true` : Ignore the fact that sets already exist in redis.
  - `false` : Only allow new entries in `impList` to be accessed.

### improveOneTopic 
  -  `true` : target a specific label to include more labels.
  - `false` : see above for reverse.

### improveName
  - `str` : A string value of the label to improve on.

### allTrainingData 
  -  `true` : to read from folder `trainingData`.
  - `false` : to read from folder `subsetTraining`.

### optimize
  -  `true` : to calculate F1 scores with incremental classifier parameters.
  - `false` : Run classifier once with a set value list.

### jsonInRedis
  - `false` : useful for small cases where everything is read in (memory intensive).
  -  `true` : to store everything in Redis and called one at a time, useful for loading in multiple `*.json` files.

### latestFileNumber 
  - `int` : Number of .json files to include - 1 i.e. MUST be bigger than 1.

### includeSingles
  -  `true` : if single label classifier models have been built and are to be added to the main classification.
  - `false` : Dont include the extra labels.

