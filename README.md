# Tickers_Financials_Fetching_And_Analysis
Fetches Bal_Sheet, Inc_Statement &amp; Stat_CashFlows from quoted companies using Library "finvizfinance" and then proceeds to conduct quantitative analysis based on those Numbers and some functions created by the user.

What the project does ?

The idea of this project is to facilitate the screening of quoted companies all around the world without the need of paid resources. First I started with US Companies as there is a finvizfinance library that allows for scrape from FinViz which has free resources available for investors. Then the idea is to escalate the procedure to european companies using yahoo finance library (yfinance). Based on the scraping of the 3 financials statements (Balance Sheet, Income Statement and Statement of Cash Flows) and on the performance and some metrics of each ticker, I've built two ways of evaluating a stock purchase solely using quantitative methods either from financials or stock market performance. Qualitatitive analysis has been left out of the equation.


Why the project is useful?

As explained above, the project helps to standardize and get in a faster manner the financials of the companies, which reduces the time that one uses scrape and organize financials of the companies that one has interest in. Regardless off this, if a large numbers of tickers is scraped at the same time and in the same batch, the project still takes some time (45 minutes - 1 hour) to fetch the 3 statements off around 1800 tickers. However, if one stores the financials, which the project does, in your own computer the time diminishes, as one doesn't need neither to connect to FinViz API nor impose time limits on the scraping to avoid timeouts.

Besides this, I consider the project important for people like me, who feel overwhelmed navigating through all the noise, commentary, opinions and information around the stock markets and each company. Moreover, for somebody like me, who has a hard time deriving its own views around the near future and farther future to where the world and the stock market will move, this project provides me with some quantitative info and more clarity on the evaluation of stocks based on frameworks studied and conducted by others well known people in finance. With this, one continues into the frameworks that, for now, I've implemented for US Companies based on finvizfinance library.

The 1st framework is a simplified version of the 5 Factor Investing Model developed and theorized by Eugene Fama & Kenneth French where the authors claim that stock returns have more explainibility besides market factor, described by CAPM through Beta. In their view and throughout research over a large time span, they found the following:

  1 - Companies that have lower valuations multiples described broadly by Price to Book Ratio tend to outperform companies that have higher multiples, as the expectations on the latter will turn overperformance more difficult as better performance is already baked/priced in into the price at a given time. so Returns of Lower P/B > Returns of Higher P/B

  2 - Companies that have higher profitability tend to outperfom companies that present more fragile profit performance. This seems more intuitive as more profitable companies can weather difficult times better than fragile companies as their financials are stronger, so more resilience on the downside. Moreover, their ability to generate profits and cash flows is associated with the more capabilities of capitalizing on growth opportunities to broaden or strengthen their revenue stream, contrarily to weaker companies. Profitability in the model will be measured by incorporating operating margins and Return on Equity (ROE) adjusted by the level of debt throughout a number of years that the user can choose. More than 7 years are not possible as one doesn't have that data in FinViz as one is using the free tier.

  3 - Companies that encompass less market risk tend to outperform, over large periods of time (IMPORTANT), companies that present more level of risk. This will be measured in a simplified manner by BETA, which is basically a measure that shows how much more volatile is a given stock compared to the benchmark (S&P500 in most cases).  This is less intuitive, but companies with less risk tend to have better returns, when risk adjusted, and moreover, usually are steady performers capping, their downside, usually when compared to more riskier companies.

  4 - Companies that experience either positive/negative past recent returns have more likelihood of experiencing positive/negative returns in the near future, suggesting and corroborating with the idea of persistence in stock returns. This tends to be explained by the combination of bias across different market agents and actors and some herding mentality that might lead to higher momentum impulses to either the up or downside. The large growth in investment vehicles such as ETFs in the past years might be a factor heavily contributing to this narrative. The momentum factor will be calculated based on the returns of a stock during the last completed month and the last completed year to reach a metric capable of capturing this factor.

  5 - Companies that conduct conservative investment internal policies usually outperform aggressive investment internal policies, as companies preserving and prioritizing capital and capital discipline tend to have the expectations between investments and growth stemming from those investments more alligned, leading to outperformance in the long-run whereas aggressive investment companies tend to overinvest and then experiencing lagging returns when realization of returns comes out lower when compared to expectations. The metric used to attain this variable is an average of fixed assets growth during a given timeframe as a % of the average growth on Total Assets during the same timeframe.

The idea behind the 2nd framework is to find companies that have impeccable historical records, where there is persistence of revenues, EPS growth. The operating margins also grow or are sustained across time. The growth in the share dilution is also lower than the EPS growth to ensure that the dilution is, at least, being compensated with higher growth in earnings. Moreover, debt coverage is also considered and the companies choosen need to have coverage of their short term debt ensured by cash and short term investments. All of this conditions need to be verified during, at least, 5 years to ensure some persistence and excelence on companies metrics.

  



How users can get started with the project
Where users can get help with your project
Who maintains and contributes to the project
