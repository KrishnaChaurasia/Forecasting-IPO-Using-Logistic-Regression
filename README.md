# Forecasting-IPO-Using-Logistic-Regression
IPO Market Forecasting Using Logistic Regression
The project involves the following steps:
	1.	Understanding the IPO Market
		a.	Concept of offering price, first day’s opening price and closing price
		b.	Difficult to buy shares at the offering price for the general public 
	2.	Data acquisition and cleaning
		a.	Importing and cleaning the data downloaded from IPOScoop https://www.iposcoop.com/scoop-track-record-from-2000-to-present/
	3.	Data Exploration:
		a.	The bar plots of mean and median of 1st day % change show that the long right tail suggesting heavy returns for potential buyers at offering price
		b.	Can the same be said about purchase done at the opening price
	4.	Baseline Strategy:
		a.	Buy all IPOs at their opening price and sell at the closing price
			i.	The result shows a profit of very insignificant amount (~ $27.25)
			ii.	Not a very good strategy to work with
	5.	Feature Engineering:
		a.	The baseline strategy does not account for various important parameters related to the IPO such as:
			i.	the recent performance of the market
			ii.	the prestige of the underwriters
			iii.	the day/month of the purchase
			Consideration of these factors is shown to impact the IPO market
	6.	Better strategy : Binary Classification using Logistic Regression
		a.	Applying the logistic regression algorithm after feature engineering results in better results
		b.	The plots show that the returns have increased considerably with the  current strategy
