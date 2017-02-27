#Paul Sheehan - C11443788

import pandas as pd
#remove warning of chained indexing when replacing outliers in the dataframe
pd.options.mode.chained_assignment = None

dataset = pd.read_csv('data/DataSet.txt', header=None)
fn= pd.read_csv('data/featureNames.txt', header=None)

#list of intger values which are used to index the categorical data,
#and continious data in our dataset
cathIndex = [2, 4, 6, 7, 8, 9, 10, 14, 15]
contIndex = [1, 3, 5, 11, 12, 13]

#Split featureNames into 2 new dataframes: categorical, continious
#Create new dataframe for categorical feature names
cathFn = [fn.iloc[2][0],fn.iloc[4][0],fn.iloc[6][0],
                       fn.iloc[7][0],fn.iloc[8][0],fn.iloc[9][0],
                       fn.iloc[10][0],fn.iloc[14][0],fn.iloc[15][0]];
#Create new dataframe for continious feature names
contFn = [fn.iloc[1][0],fn.iloc[3][0],
                       fn.iloc[5][0],fn.iloc[11][0],fn.iloc[12][0],
                       fn.iloc[13][0]];

#Column names for our categorical report
cathColumns = ['Feature', 'Count', '% Missing', 'Cardinality', 'Mode',
                           'Mode Count', '% Mode', '2nd Mode', '2n Mode Count',
                           '2nd Mode Percent']
#Column names for our categorical report
contColumns = ['Feature', 'Count', '% Missing', 'Cardinality', 'Min',
               'Quart1', 'Mean','Median', 'Quart3', 'Max', 'Standard Dev']

#This function fixes missing values in categorical data
def fixCat(i, j, m):
    #feature: workclass
    if(i == 2):
        #replace with mode
        dataset.iloc[j][i] = m
    #feature: occupation
    if(i == 7):
        #group as unemployed
        if(dataset.iloc[j][15] == ' <50k'):
            dataset.iloc[j][i] = "Unemployed"
        #replace with mode because they are earning money
        else:
            dataset.iloc[j][i] = m
    #feature: native country
    if(i == 14):
        #mode
        dataset.iloc[j][i] = mode

# #Empty dataframe for our categorical report
cathReport = pd.DataFrame(index=cathFn, columns=cathColumns)

# #These are empty lists for each column of the report
# #We will append each features analysis results
count = []
missing = []
cardinality = []
mode = []
modeCount = []
percentMode = []
secondMode = []
secondModeCount = []
percentSecondMode = []

#Iterate through columns of CAT data
for i in cathIndex:

    missingCounter = 0
    freqCounter = 0
    modeCounter = 0
    featureMode = dataset.iloc[:][i].mode()[0]
    featureModeCount = dataset[:][i].value_counts()[0]
    secondFeatureModeCount = dataset[:][i].value_counts()[1]

    print("1 Column Processed")

    #Iterate through each row of data
    for j in range(dataset[i].size):
        #Detects missing value
        if(dataset.iloc[j][i] == ' ?'):
            fixCat(i, j, featureMode)
            #Number of missing values for each feature
            missingCounter+=1
        #Number of total values for each feature
        freqCounter+=1

    #Append total values to our list
    count.append(freqCounter)
    #This is to avoid deviding by 0 error
    if(missingCounter > 0):
        #Gets percentage
        missing.append(round((missingCounter/freqCounter)*100))
    else:
        #0%
        missing.append(0)

    #Append the rest of the results, I used pandas library to get statistical values
    cardinality.append(len(dataset[:][i].unique()))
    mode.append(featureMode)
    modeCount.append(featureModeCount)
    percentMode.append(round((featureModeCount/freqCounter)*100))
    secondModeCount.append(secondFeatureModeCount)
    percentSecondMode.append(round((secondFeatureModeCount/freqCounter)*100))
    #Drop the 1st mode from the dataframe so that we can find the 2nd mode
    removeFirstMode = dataset.drop(dataset[dataset[:][i] == featureMode].index)
    secondFeatureMode = removeFirstMode.iloc[:][i].mode()[0]
    #append 2nd mode
    secondMode.append(secondFeatureMode)


#This adds all of the lists we just built to our categorical report
cathReport.loc[:]['Feature'] = cathFn
cathReport.loc[:]['Count'] = count
cathReport.loc[:]['% Missing'] = missing
cathReport.loc[:]['Cardinality'] = cardinality
cathReport.loc[:]['Mode'] = mode
cathReport.loc[:]['Mode Count'] = modeCount
cathReport.loc[:]['% Mode'] = percentMode
cathReport.loc[:]['2nd Mode'] = secondMode
cathReport.loc[:]['2n Mode Count'] = secondModeCount
cathReport.loc[:]['2nd Mode Percent'] = percentSecondMode

print("Categorical data complete")
#Export the categorical report to a csv.txt file
cathReport.to_csv('data/c11443788CAT.csv', index=False)

#We do the exact same process for our continuous data
#empty list of statistics
count = []
missing = []
cardinality = []
min = []
quart1 = []
mean = []
median = []
quart3 = []
max = []
stdDev = []


for i in contIndex:
    missingCounter = 0
    freqCounter = 0

    print("1 Column Processed")
    #1st quartile
    q1 = dataset[:][i].quantile(.25)
    #3rd quartile
    q3 = dataset[:][i].quantile(.75)
    #Turkey method to identify outliers
    innerFence = (((q3 - q1) * 1.5) - q1)
    outerFence = (((q3 - q1) * 3) + q3)
    catMean = round(dataset.iloc[:][i].mean())
    for j in range(dataset[i].size):
        #if the value is an outlier impute with mean of this column
        if(dataset.iloc[j][i] < innerFence or dataset.iloc[j][i] > outerFence):
            dataset.iloc[j][i] = catMean
            #Theres no missing data but no harm in looking
        freqCounter+=1

    count.append(freqCounter)
    if(missingCounter > 0):
        missing.append(round((missingCounter/freqCounter)*100))
    else:
        missing.append(0)

    cardinality.append(len(dataset[:][i].unique()))
    min.append(dataset[:][i].min())
    mean.append(catMean)
    median.append(round(dataset[:][i].median()))
    max.append(dataset[:][i].max())
    quart1.append(q1)
    quart3.append(q3)
    stdDev.append(round(dataset[:][i].std()))

contReport = pd.DataFrame(index=contFn, columns=contColumns)
print("Continuous data complete")
contReport.loc[:]['Feature'] = contFn
contReport.loc[:]['Count'] = count
contReport.loc[:]['% Missing'] = missing
contReport.loc[:]['Cardinality'] = cardinality
contReport.loc[:]['Min'] = min
contReport.loc[:]['Quart1'] = quart1
contReport.loc[:]['Mean'] = mean
contReport.loc[:]['Median'] = median
contReport.loc[:]['Quart3'] = quart3
contReport.loc[:]['Max'] = max
contReport.loc[:]['Standard Dev'] = stdDev

contReport.to_csv('data/c11443788CONT.csv', index=False)
