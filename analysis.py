import numpy as np
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import re
import matplotlib.pyplot as plt
import xlrd
import xlsxwriter
import datetime

#method calculates the percentage of the subset of rows from total rows
def calculatePercentage(subsetRowCount, totalCountOfRows):
    percentage = (subsetRowCount/totalCountOfRows)*100
    return round(percentage, 2)

#method creates bar graph
def createGraph(_data, _totalCountOfRows):
    _xAxisGroups = ('0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60+')
    _yLabel = 'Percentage Infected'
    _title = 'Percentage of People Infected for Each Age Group'

    y_pos = np.arange(len(_xAxisGroups))
    plt.bar(y_pos, _data, align='center', alpha=0.5)
    plt.xticks(y_pos, _xAxisGroups)
    plt.ylabel(_yLabel)
    plt.title(_title)

    # add percentage for each age group above bar graph
    for index, data in enumerate(arrayGroups):
        plt.text(x=index - .3, y=data + .5, s=f"{data}%", fontdict=dict(fontsize=12))

    # add number of people studied for each age group below percentage
    for index, data in enumerate(_data):
        numberObservedForEachGroup = (data * _totalCountOfRows) / 100
        numberObservedForEachGroup = round(numberObservedForEachGroup)
        plt.text(x=index - .3, y=data - 1.3, s=f"{numberObservedForEachGroup}", fontdict=dict(fontsize=12))

    plt.show()

#remove rows that have datetime type value for age
def dropDateTimeValueForAge(noRangeList):
    for index, row in noRangeList.iterrows():
        hold = row['age']
        if (type(row['age']) is datetime.datetime):  # if there is a datetime value in age column, remove row
            noRangeList.drop(index, inplace=True)

#computes average for rows containg an age range in age column
def computeAverageForAgeThatHasRange(rangeList):
    for index, row in rangeValuesArray.iterrows():  # go through each row
        hold = row['age']
        match = re.search(r'(\d\d?\d?)-(\d\d?\d?)', hold)  # check if there is a range format

        if (match):
            upper = int(match.group(2))
            lower = int(match.group(1))
            if (
                    upper - lower > 15):  # if age range greater than 15, drop the row (these kind of data points, if kept, could possibly give an inaccurate representation)
                rangeValuesArray.drop(index, inplace=True)  # remove row since there is invalid data
            else:
                newAgeAveraged = (upper + lower) / 2        # find average of the lower and upper bound
                rangeValuesArray['age'] = newAgeAveraged    # assign an average of the values
        else:
            rangeValuesArray.drop(index, inplace=True)      # remove row since there is invalid data

#Clean up input file
file_name = input("Enter file name: ")
print("Generating Results... \n")

df = pd.read_excel(file_name)

noEmptyValues = df[~df['age'].isna()]                                                           #keep only rows that do not contain empty data for age or N/A
noRangeValuesArray = noEmptyValues[~noEmptyValues['age'].str.contains("-", na=False)].copy()    #create a copy and store rows that do not have a range
rangeValuesArray = noEmptyValues[noEmptyValues['age'].str.contains("-", na=False)].copy()       #create a copy and store only rows that have a range

dropDateTimeValueForAge(noRangeValuesArray)                                 #remove any rows that have datetime.datetime type value
computeAverageForAgeThatHasRange(rangeValuesArray)                          #compute the average for age that has a range

#newResult will hold cleaned up data
newResult = pd.concat([noRangeValuesArray,  rangeValuesArray])              #join edited rows that have been averaged with rows that did not need to be edited
newResult.to_excel('CleanedUpData.xlsx', engine='xlsxwriter')

newDf = newResult

totalCountOfRows = len(newDf)

#split data by age group
lessThan10 = newDf.loc[newDf['age'] < 10]
lessthan20 = newDf.loc[(newDf['age'] >= 10) & (newDf['age'] < 20)]
lessthan30 = newDf.loc[(newDf['age'] >= 20) & (newDf['age'] < 30)]
lessthan40 = newDf.loc[(newDf['age'] >= 30) & (newDf['age'] < 40)]
lessthan50 = newDf.loc[(newDf['age'] >= 40) & (newDf['age'] < 50)]
lessthan60 = newDf.loc[(newDf['age'] >= 50) & (newDf['age'] < 60)]
greaterOrEqualTo60 = newDf.loc[newDf['age'] >= 60]

#calculate percentage of people infected for each age group
lessThan10Percentage = calculatePercentage(len(lessThan10), totalCountOfRows)
lessThan20Percentage = calculatePercentage(len(lessthan20), totalCountOfRows)
lessThan30Percentage = calculatePercentage(len(lessthan30), totalCountOfRows)
lessThan40Percentage = calculatePercentage(len(lessthan40), totalCountOfRows)
lessThan50Percentage = calculatePercentage(len(lessthan50), totalCountOfRows)
lessThan60Percentage = calculatePercentage(len(lessthan60), totalCountOfRows)
greaterOrEqualTo60Percentage = calculatePercentage(len(greaterOrEqualTo60), totalCountOfRows)

#add the percentage of people infected for each age group into an array
arrayGroups = []
arrayGroups.append(lessThan10Percentage)
arrayGroups.append(lessThan20Percentage)
arrayGroups.append(lessThan30Percentage)
arrayGroups.append(lessThan40Percentage)
arrayGroups.append(lessThan50Percentage)
arrayGroups.append(lessThan60Percentage)
arrayGroups.append(greaterOrEqualTo60Percentage)

#Matrix used for printing to console
matrix = []
matrix.append(["0-9", lessThan10Percentage])
matrix.append(["10-19", lessThan20Percentage])
matrix.append(["20-29", lessThan30Percentage])
matrix.append(["30-39", lessThan40Percentage])
matrix.append(["40-49", lessThan50Percentage])
matrix.append(["50-59", lessThan60Percentage])
matrix.append(["60+", greaterOrEqualTo60Percentage])

dataFrame = pd.DataFrame(matrix, columns = ['Age Group', 'Infected (%)'])
dataFrame.set_index('Age Group', inplace=True)

print(dataFrame)
print("\nNumber of Patients Studied: " + str(len(newDf)))

#create bar graph
createGraph(arrayGroups, totalCountOfRows)



