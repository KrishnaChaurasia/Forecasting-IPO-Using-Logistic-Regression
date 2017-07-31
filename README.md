# Forecasting-IPO-Using-Logistic-Regression
IPO Market Forecasting Using Logistic Regression<br/>
The project involves the following steps:
1. Understanding the IPO Market <br/>
    a. Concept of offering price, first day’s opening price and closing price <br />
    b. Difficult to buy shares at the offering price for the general public <br />
2.	Data acquisition and cleaning <br />
	a.	Importing and cleaning the data downloaded from IPOScoop https://www.iposcoop.com/scoop-track-record-from-2000-to-present/ <br />
3.	Data Exploration: <br />
    a.	The bar plots of mean and median of 1st day % change show that the long right tail suggesting heavy returns for potential buyers at offering price <br />
	b.	Can the same be said about purchase done at the opening price? <br />
4.	Baseline Strategy: <br />
    1.	Buy all IPOs at their opening price and sell at the closing price <br />
	2.	The result shows a profit of very insignificant amount (~ $27.25) <br />
	Not a very good strategy to work with <br />
5.	Feature Engineering: <br />
    a.	The baseline strategy does not account for various important parameters related to the IPO such as: <br />
    1.	the recent performance of the market <br />
    2.	the prestige of the underwriters <br />
    3.	the day/month of the purchase <br />
    Consideration of these factors is shown to impact the IPO market <br />
6.	Better strategy : Binary Classification using Logistic Regression <br />
	a.	Applying the logistic regression algorithm after feature engineering results in better results <br />
	b.	The plots show that the returns have increased considerably with the  current strategy <br />
