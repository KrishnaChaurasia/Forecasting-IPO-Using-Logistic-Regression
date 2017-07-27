import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from patsy import dmatrix
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model

# Read the csv file
ipos = pd.read_csv('SCOOP-Rating-Performance-Final_2015.csv', encoding='latin-1')
ipos.columns
#Trade Date - Date of the trade
#Issuer - Issuer for the IPO
#Symbol - ID for the Issuer
#Offer Price - The price at which the offer was made to the bank
#Opening Price - The price at which it was opened for the public
#1st Day Close - The price at which it was opened for the public
#1st Day % Px Chng - The %age change between the offer price and the 1st day close price
#$ Change Opening -  The $ change between the offer price and the opening price
#$ Change Close -   The $ change between the offer price and the 1st day close price
#Lead/Joint-Lead Managers, Star Ratings, Performed - Other information

# Display a part of the data
ipos.head()

# Data Cleaning : Replace the $ and % sign to perform mathematical operations
ipos = ipos.applymap(lambda x : x if '$' not in str(x) else x.replace('$', ''))
ipos = ipos.applymap(lambda x : x if '%' not in str(x) else x.replace('%', ''))
ipos.head()

# A Date Field is out of bound, identify the index number and fix it
ipos.loc[811, 'Trade Date'] = '2012-11-20'

# Reomve the 'N/C' values and also change the types of each columns to appropriate types to apply statistical operations
ipos.replace('N/C', 0, inplace=True)
ipos['Trade Date'] = pd.to_datetime(ipos['Trade Date'])
ipos['Offer Price'] = ipos['Offer Price'].astype('float')
ipos['Opening Price'] = ipos['Opening Price'].astype('float')
ipos['1st Day Close'] = ipos['1st Day Close'].astype('float')
ipos['1st Day % Px Chng '] = ipos['1st Day % Px Chng '].astype('float')
ipos['$ Change Close'] = ipos['$ Change Close'].astype('float')
ipos['$ Change Opening'] = ipos['$ Change Opening'].astype('float')
ipos['Star Ratings'] = ipos['Star Ratings'].astype('int')

# Verifying the datatypes have changed
ipos.info()

# Let's now perform some Data Analysis tasks
# 1st Day % Px Chng is the | Offer Price - 1st Day Close Price | = Money left on the table due to the offering price,
# which can be infered from the next three plots

# 1st Day Percentage Gain Mean & Median Plots
ipos.groupby(ipos['Trade Date'].dt.year)['1st Day % Px Chng '].mean().plot(kind = 'bar', figsize=(15,10), title='1st Day Mean IPO Percentage Change')
plt.show()
ipos.groupby(ipos['Trade Date'].dt.year)['1st Day % Px Chng '].median().plot(kind = 'bar', figsize=(15,10), title='1st Day Median IPO Percentage Change')
plt.show()
ipos['1st Day % Px Chng '].describe()

# Observe that the most returns are clustered around zero but there is a long tail to the right 
ipos['1st Day % Px Chng '].hist(figsize=(15,7), bins=150, color='black')
plt.show()

# Are there opportunities to capture even with the purhcase at the opening price?
ipos['$ Change Open to Close'] = ipos['$ Change Close'] - ipos['$ Change Opening']
ipos['% Change Open to Close'] = (ipos['$ Change Open to Close'] / ipos['Opening Price']) * 100

# While IPOs can fall off after their opening, a drop of nearly a 100% (-98.522167) seems unrealistic
# Represents the outliers which needs to be taken care of
ipos['% Change Open to Close'].describe()

# Identifying and correcting the outlier
ipos[ipos['% Change Open to Close'] < -98]
ipos.loc[1771, '$ Change Opening'] = ipos.loc[1771, 'Offer Price'] - ipos.loc[1771, 'Opening Price']

# Identifying further outliers, at half the original value and correcting it
ipos[ipos['% Change Open to Close'] < -49]
ipos.loc[1007, '$ Change Opening'] = ipos.loc[1007, 'Offer Price'] - ipos.loc[1007, 'Opening Price']

# Again, let's see if there are opportunities to capture even with the purhcase at the opening price?
ipos['$ Change Open to Close'] = ipos['$ Change Close'] - ipos['$ Change Opening']
ipos['% Change Open to Close'] = (ipos['$ Change Open to Close'] / ipos['Opening Price']) * 100
ipos['% Change Open to Close'].describe()

# The long tail on the right shows there is still a ray of hope to take advantage of
ipos['% Change Open to Close'].hist(figsize=(15,8), bins=150)
plt.show()

# Strategy 1
# How about the stategy where we purchase every IPOs offered at the offering price and sell at the closing price?
ipos[(ipos['Trade Date'] >= '2014-01-01') & (ipos['Trade Date'] < '2015-01-01')]    ['$ Change Open to Close'].describe()

# The sum of greater than zero shows that we would have made a profit however of very small value
ipos[(ipos['Trade Date'] >= '2014-01-01') & (ipos['Trade Date'] < '2015-01-01')]    ['$ Change Open to Close'].sum()

# Let's see the winning shares, it shows that there are 123 IPOs with positive returns
ipos[(ipos['Trade Date'] >= '2014-01-01') & (ipos['Trade Date'] < '2015-01-01')      & (ipos['$ Change Open to Close'] > 0)]['$ Change Open to Close'].describe()

# While the count of losing shares(with negative returns) are 155 IPOs, which isn't a good strategy
# Moreover, the mean value of %age return is also just 1% which is not at all a good return
ipos[(ipos['Trade Date'] >= '2014-01-01') & (ipos['Trade Date'] < '2015-01-01')      & (ipos['$ Change Open to Close'] < 0)]['$ Change Open to Close'].describe()

# # Feature Engineering
sp = pd.read_csv(r'GSPC.csv', encoding='latin-1')
sp.sort_values('Date', inplace=True)
sp.reset_index(drop=True, inplace=True)
sp.head()

# Method to find weekly change
def weeklyChange(ipos):
    try:
        dayAgoIndex = sp[sp['Date'] == str(ipos.date())].index[0] - 1     #yesterday's data
        weekAgoIndex = dayAgoIndex - 7    #week's before data
        change = (sp.iloc[dayAgoIndex]['Close'] - sp.iloc[weekAgoIndex]['Close']) / sp.iloc[weekAgoIndex]['Close']
        return change * 100
    except:
        print("error : ", ipos.date())

# Apply the weekly change method to the Trade Date in the original ipos dataset
# Some dates have issues which needs to be corrected
ipos['SP Week Change'] = ipos['Trade Date'].map(weeklyChange)

ipos[ipos['Trade Date'] == '2015-02-21']
ipos[ipos['Trade Date'] == '2013-11-16']
ipos[ipos['Trade Date'] == '2009-08-01']

# Correcting the incorrect dates
ipos.loc[59, 'Trade Date'] = pd.to_datetime('2015-05-21')
ipos.loc[60, 'Trade Date'] = pd.to_datetime('2015-05-21')
ipos.loc[640, 'Trade Date'] = pd.to_datetime('2012-11-20')
ipos.loc[1139, 'Trade Date'] = pd.to_datetime('2015-12-08')

# Reapply and add the weekly change to the corrected dataset
ipos['SP Week Change'] = ipos['Trade Date'].map(weeklyChange)
ipos.head()

# Method to find Close to Opening change
def getCloseToOpenChange(ipos):
    try:
        todayOpenIdx = sp[sp['Date'] == str(ipos.date())].index[0]          #today's open
        ystrdayCloseIdx = sp[sp['Date'] == str(ipos.date())].index[0] - 1   #yesterday's close
        change = (sp.iloc[todayOpenIdx]['Open'] - sp.iloc[ystrdayCloseIdx]['Close']) - sp.iloc[ystrdayCloseIdx]['Close']
        return change * 100
    except:
        print('error : ', ipos)

# Apply the get close to open change method
ipos['SP Close To Open Change %'] = ipos['Trade Date'].map(getCloseToOpenChange)

# Cleanup the Lead Managers
ipos['Lead Mgr'] = ipos['Lead/Joint-Lead Managers'].map(lambda x : x.split('/')[0])
ipos['Lead Mgr'] = ipos['Lead Mgr'].map(lambda x : x.strip())

# Also, add total number of underwriters for each IPO
ipos['Total Underwriters'] = ipos['Lead/Joint-Lead Managers'].map(lambda x: len(x.split('/')))

# Add the week days and the month columns
ipos['Week Day'] = ipos['Trade Date'].dt.dayofweek.map({0:'Mon', 1:'Tues',2:'Wed',     3:'Thurs', 4:'Fri', 5:'Sat', 6:'Sun'})
ipos['Month'] = ipos['Trade Date'].map(lambda x: x.month)
ipos['Month'] = ipos['Month'].map({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr',5:'May', 6:'Jun',7:'Jul',     8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'})
ipos.head()

# Add Open to Close %
ipos['Gap Open %'] = (ipos['$ Change Opening'].astype('float') / ipos['Opening Price'].astype('float')) * 100
ipos.columns

# Patsy to perform data analysis tasks
from patsy import dmatrix
X = dmatrix('Month + Q("Week Day") + Q("Total Underwriters") + Q("Gap Open %") + Q("$ Change Opening") +    Q("Lead Mgr") + Q("Offer Price") + Q("Opening Price") +    Q("SP Close To Open Change %") + Q("SP Week Change")', data=ipos,return_type='dataframe')
X.head()

# Binary Classification
# Test the 2015 data, train all previous years
# Identify the index of 2015 starting date, which starts from 158
ipos[:159]

# Partition the training and test data
trainX, testX = X[159:], X[:159]
trainY = ipos['$ Change Open to Close'][159:].map(lambda x : 1 if x >= 0.05 else 0)
testY = ipos['$ Change Open to Close'][:159].map(lambda x : 1 if x >= 0.05 else 0)

# Fit the model using Logisitic Regression
clf = linear_model.LogisticRegression()
clf.fit(trainX, trainY)

# Testing the model shows an accuracy of 81%
clf.score(testX, testY)

# Let's see the predicted result
predLabel = clf.predict(testX)
results = []
for pl, tl, idx, chg in zip(predLabel, testY, testY.index, ipos.ix[testY.index]['$ Change Open to Close']):
    if pl == tl:
        results.append([idx, chg, pl, tl, 1])
    else:
        results.append([idx, chg, pl, tl, 0])

rf = pd.DataFrame(results, columns=['index', '$ change', 'predicted', 'actual', 'correct'])

rf[rf['predicted'] == 1]['$ change'].describe()

# Plot of returns
fig, ax = plt.subplots(figsize=(15,10))
rf[rf['predicted'] == 1]['$ change'].plot(kind='bar')
ax.set_title('Model Predicted Buys', y = 1.01)
ax.set_ylabel('$ Change Open to Close')
ax.set_xlabel('Index')
plt.show()