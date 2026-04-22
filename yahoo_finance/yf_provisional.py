
#%%
"""                          IGNORE THIS FILE FOR NOW IT IS NOT WORKING YET.                                         """
#%%

import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path
import os
import time
import datetime

#%%

blackrock_exchanges_yf_terminations = {
    'Bolsa De Madrid' : '.MC',
    'Borsa Italiana' : '.MI',
    'London Stock Exchange' : '.L',
    'Xetra' : '.DE',
    'Nyse Euronext - Euronext Paris' : '.PA',
    'Euronext Amsterdam' : '.AS',
    'Nyse Euronext - Euronext Brussels' : '.BR',
    'Nyse Euronext - Euronext Lisbon' : '.LS',
    'SIX Swiss Exchange' : '.SW',
    'Nasdaq Omx Nordic' : '.ST',
    'Omx Nordic Exchange Copenhagen A/S' : '.CO',
    'Nasdaq Omx Helsinki Ltd.' : '.HE',
    'Oslo Bors Asa' : '.OL',
    'Wiener Boerse Ag' : '.VI',
    'Irish Stock Exchange - All Market' : '.IR',
    'Warsaw Stock Exchange' : '.WA',
    'Athens Stock Exchange' : '.AT',
    'Prague Stock Exchange' : '.PR',
    'Budapest Stock Exchange' : '.BD'
}

#%%



#%%

"IEV_Blackrock_ETF_path" - r"C:\Users\Afons\Investments\ETFs_to_fetch_tickers\IEV_holdings.csv"
FilePath = r"C:\Users\Afons\Investments\ETFs_to_fetch_tickers"
FileName = "IEV_holdings.csv"

#%%

def get_tickers_to_yf_from_excel(file_path,file_name,dict_exchange_yf_terminations:dict):

    tickers_lst = []
    
    # Read all sheets in the excel file
    df = pd.read_csv(file_path+"/"+file_name,sep=None,engine="python")

    #REMOVE NaN Rows
    df = df.loc[:len(df)-2,:]
    df.rename(columns={df.columns[0] : 'Ticker'},inplace=True)

    #Proceed to make changes in ticker names to be usable by yf
    renamed_tickers = []
    sign_exchange = []


    for ticker in df['Ticker']:

        renamed_ticker = ticker.replace(" ","-").replace(".","")
        renamed_tickers.append(renamed_ticker)

    df['Ticker'] = renamed_tickers
    
    for exchange in df['Exchange']:

        sign_exchange.append(dict_exchange_yf_terminations[exchange])
    
    df['Exchange_Termination'] = sign_exchange

    df['Ticker+Termination'] = df['Ticker'] + df['Exchange_Termination']

    tickers_lst = df['Ticker+Termination'].to_list()

    return tickers_lst

#%%

def statement_match(statement_1:pd.DataFrame,statement_2:pd.DataFrame):

    size_stat_1 = len(statement_1)
    size_stat_2 = len(statement_2)
    size_match = size_stat_1 == size_stat_2
    stat_1_ind = statement_1.index 
    stat_2_ind = statement_2.index

    if size_match:
    
        lst_bool = list(stat_1_ind == stat_2_ind)
        content_match = lst_bool.count(True) == size_stat_1

        if content_match:
        
            return True
        
        else:
        
            return False
    
    else:
    
        return False

#%%

tickers_lst = get_tickers_to_yf_from_excel(r"C:\Users\Afons\Investments\ETFs_to_fetch_tickers","IEV_holdings.csv",blackrock_exchanges_yf_terminations)


#%%

tickers_lst

#%%

yf.Ticker("ABBN.SW").balance_sheet
# %%
yf.Ticker("GALP.LS").balance_sheet
# %%
len(yf.Ticker("EDP.LS").get_income_stmt())
# %%

len(yf.Ticker("ABBN.SW").get_income_stmt())
# %%

yf.Ticker("EDP").get_balance_sheet()
# %%

yf.Ticker("ABBN.SW").get_history_metadata()
# %%

year_start = int(input("Starting Fetching Year: "))
month_start = int(input("Starting Fetching Month: "))
day_start = int(input("Starting Fetching Day: "))
year_end = int(input("Ending Fetching Year: "))
month_end = int(input("Ending Fetching Month: "))
day_end = int(input("Ending Fetching Day: "))
end_date = datetime.datetime(year=year_end, month=month_end, day=day_end)
start_date = datetime.datetime(year=year_start, month=month_start, day=day_start)
#INTRADAY DATA ONLY GOES 60 DAYS BACKWARDS
wanted_tf = str(input("Possible Choices (Write exactly like the choices) : '1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo' "))


#%%
def extract_hist_tickers_price(lst_tickers:list,start_date:datetime.datetime,end_date:datetime.datetime,interval:str):

    ticker_df = yf.download(lst_tickers,start=start_date,end=end_date,interval=interval)

    dict_tickers_df = dict()

    for ticker in lst_tickers:

        columns_wanted = list()

        for i in range(len(ticker_df.columns)):

            if ticker_df.columns[i][1] == ticker:
                columns_wanted.append(ticker_df.columns[i])

        each_ticker_df = ticker_df.loc[:,columns_wanted]

        if len(each_ticker_df.dropna()) != 0:

            dict_tickers_df[ticker] = each_ticker_df
    
    return dict_tickers_df

#%%

dict_tickers_df = extract_hist_tickers_price(tickers_lst,start_date,end_date,wanted_tf)

#%%

tickers_lst = list(dict_tickers_df.keys())

#%%

tickers_lst

# %%

yf.Ticker()

#%%

dict_all_financials = {'bal_sheet' : {}, 'inc_stat' : {}, 'stat_cfs' : {}}

for ticker in tickers_lst:

    dict_all_financials['bal_sheet'][ticker] = yf.Ticker(ticker).get_balance_sheet()
    dict_all_financials['inc_stat'][ticker] = yf.Ticker(ticker).get_income_stmt()
    dict_all_financials['stat_cfs'][ticker] = yf.Ticker(ticker).get_cash_flow()

#%%

def assess_tickers_comparability_by_size_and_order_of_statements(list_dict_three_statements:list): #checks if tickers can be comparable by having similar variables in inc_stat, bal_sheet & stat_cfs

    dict_assessing_tickers_comparability = {'comparable_tickers_1' : []}

    #NUMBER OF TICKERS
    length_list_tickers = len(list_dict_three_statements[0])
    lst_tickers = list(list_dict_three_statements[0].keys())
    dict_assessing_tickers_comparability['comparable_tickers_1'].append(lst_tickers[0])

    for ind in range(1,length_list_tickers):

        ticker = lst_tickers[ind] #KEY FOR EACH TICKER OF FINANCIAL STATEMENTS

        size_dict_assessing = len(dict_assessing_tickers_comparability) #CHECK HOW MANY COMPARISONS ARE NEEDED TO DO

        lst_keys_dict_assessing = list(dict_assessing_tickers_comparability.keys())

        ticker_added = False

        for comparison in range(size_dict_assessing):
        
            comparable_statements = 0

            first_comparable_ticker = dict_assessing_tickers_comparability[lst_keys_dict_assessing[comparison]][0]

            #COMPARE WITH EACH STATEMENT BY SIZE AND CONTENT

            for statement in list_dict_three_statements: #'statement' is a df of bs,inc_stat and stat_cfs
            
                boolean = statement_match(statement[first_comparable_ticker],statement[ticker])

                if boolean:
                
                    comparable_statements += 1
                
            if comparable_statements == 3:

                dict_assessing_tickers_comparability[lst_keys_dict_assessing[comparison]].append(ticker)
                ticker_added = True
                break
            
            else:
            
                continue
        
        if ticker_added: #ticker was added
        
            continue
        
        else:
        
            #CREATION OF NEW COMPARABLES
            new_key = f"comparable_tickers_{size_dict_assessing+1}"
            dict_assessing_tickers_comparability[new_key] = list()
            dict_assessing_tickers_comparability[new_key].append(ticker)
    
    return dict_assessing_tickers_comparability

#%%

dict_comparable_tickers = assess_tickers_comparability_by_size_and_order_of_statements([dict_all_financials['bal_sheet'],dict_all_financials['inc_stat'],dict_all_financials['stat_cfs']])

# %%

dict_comparable_tickers
# %%

dict_diff_size_than_1 = dict()

for key in dict_comparable_tickers: 

    if len(dict_comparable_tickers[key]) != 1:

        dict_diff_size_than_1[key] = dict_comparable_tickers[key]


dict_diff_size_than_1

# %%


stat_cfs_comparable_tickers = assess_tickers_comparability([dict_all_financials['stat_cfs']])
# %%

stat_cfs_comparable_tickers
# %%

dict_stat_cfs_diff_size_than_1 = dict()

for key in dict_comparable_tickers: 

    if len(dict_comparable_tickers[key]) != 1:

        dict_stat_cfs_diff_size_than_1[key] = dict_comparable_tickers[key]


dict_stat_cfs_diff_size_than_1
# %%

len(dict_all_financials['stat_cfs']['NESN.SW'])
# %%

len(dict_all_financials['stat_cfs']['LISN.SW'])
# %%

def compare_statement_indexes(statement_df1:pd.DataFrame,statement_df2:pd.DataFrame):

    len_small = min(len(statement_df1),len(statement_df2))
    len_big = max(len(statement_df1),len(statement_df2))

    if len(statement_df1) == len_big:

        df_big = statement_df1
        df_small = statement_df2
    
    else:

        df_big = statement_df2
        df_small = statement_df1
    
    small_index_to_list = df_small.index.to_list()
    big_index_to_list = df_big.index.to_list()

    common_items = 0 

    for item in small_index_to_list:

        if item in big_index_to_list:

            common_items += 1
        
    return f"Both statements have {common_items} out {len_small} in the smaller statement and {len_big} in the larger statement"


    
#%%

compare_statement_indexes(dict_all_financials['stat_cfs']['MRK.DE'],dict_all_financials['stat_cfs']['SIE.DE'])


#%%

dict_all_financials['stat_cfs']['ENG.MC']
# %%

"""

Yahoo Finance Conrresponding Items for statement_df

Net Income - NetIncomeFromContinuingOperations

Depreciation - DepreciationAndAmortization

Other Funds (Non Cash) - OtherNonCashItems

Funds From Operations - NetIncomeFromContinuingOperations + DepreciationAndAmortization + OtherNonCashItems

Changes in Working Capital - ChangeInWorkingCapital

Income Taxes Payable - TaxesRefundPaid

Cash from Operating Activities - OperatingCashFlow

Capital Expenditures - CapitalExpenditure

Net Assets From Acquisitions - NetBusinessPurchaseAndSale

Sale of Fixed Assets and Businesses - SaleOfBusiness

Purchase or Sale of Investments - NetInvestmentPurchaseAndSale

Purchase of Investments - PurchaseOfInvestment

Sale Or Maturity of Investments - SaleOfInvestment

Other Uses - NetOtherInvestingChanges

Other Sources - 

Cash from Investing Activities - InvestingCashFlow

Cash Dividends Paid - CashDividendsPaid

Change in Capital Stock - IssuanceOfCapitalStock

Repurchase of Common Pref Stock - RepurchaseOfCapitalStock

Sale of Common Pref Stock - IssuanceOfCapitalStock

Proceedsfrom Stock Options - 

Issuance or Reduction of Debt, Net - NetIssuancePaymentsOfDebt

Change in Long Term Debt - NetLongTermDebtIssuance

Issuance of Long Term Debt - LongTermDebtIssuance

Reduction of Long Term Debt - LongTermDebtPayments

Net Financing Active Other Cash Flow - NetOtherFinancingCharges

Other Financing Activities Uses - NetOtherFinancingCharges

Cash from Financing Activities - FinancingCashFlow

Exchange Rate Effect - EffectOfExchangeRateChanges

Net Change in Cash - ChangesInCash

Free Cash Flow - FreeCashFlow

Preferred Dividends (Cash Flow) - 

Price to Free Cash Flow - 

Deferred Taxes & Investment Tax Credit - 


"""

dict_all_financials['stat_cfs']['ENG.MC'].loc['ChangeInReceivables',:] + dict_all_financials['stat_cfs']['ENG.MC'].loc['ChangeInInventory',:] + dict_all_financials['stat_cfs']['ENG.MC'].loc['ChangeInOtherCurrentAssets',:] - dict_all_financials['stat_cfs']['ENG.MC'].loc['ChangeInPayable',:] == dict_all_financials['stat_cfs']['ENG.MC'].loc['ChangeInWorkingCapital',:]

# %%

dict_all_financials['stat_cfs']['NESN.SW']
# %%

dict_all_financials['stat_cfs']['MC.PA']
# %%
dict_all_financials['stat_cfs']['VOW3.DE']

# %%

dict_all_financials['stat_cfs']['DTE.DE']
# %%

"""

Yahoo Finance Balance Sheet

Cash & Short Term Investments - CashCashEquivalentsAndShortTermInvestments

Short Term Receivables - AccountsReceivable

Inventories -  (Inventory - InventoriesAdjustmentsAllowances)

Other Current Assets - (CurrentAssets - Inventories(ABOVE) - Short Term Receivables(ABOVE) - Cash & Short Term Investments (ABOVE)

Total Current Assets - CurrentAssets

Net Property, Plant & Equipment - NetPPE

Total Investments and Advances - InvestmentsinAssociatesatCost + InvestmentsinJointVenturesatCost + LongTermEquityInvestment

Long-Term Note Receivable -  

Intangible Assets - GoodwillAndOtherIntangibleAssets

Deferred Tax Assets - NonCurrentDeferredTaxesAssets

Other Assets - TotalAssets - Total Current Assets(ABOVE) - Rest between this line and Total Current Assets

Total Assets - TotalAssets

Short Term Debt Incl. Current Port. of LT Debt - CurrentDebtAndCapitalLeaseObligation

Accounts Payable - AccountsPayable

Income Tax Payable - TotalTaxPayable

Other Current Liabilities - CurrentLiabilities - Payables - CurrentProvisions - Short Term Debt Incl. Current Port. of LT Debt(ABOVE)

Total Current Liabilities - CurrentLiabilities

Long Term Debt - LongTermDebtAndCapitalLeaseObligation

Provision for Risks Charges - LongTermProvisions

Deferred Tax Liabilities - NonCurrentDeferredTaxesLiabilities

Other Liabilities - TotalLiabilitiesNetMinorityInterest - Total Current Liabilities(ABOVE) - Long Term Debt(ABOVE) - Provision for Risks Charges(ABOVE) - Deferred Tax Liabilities(ABOVE)

Total Liabilities - TotalLiabilitiesNetMinorityInterest

Non-Equity Reserves - 

Preferred Stock - Carrying Value - 

Common Equity - CommonStockEquity

Total Shareholders Equity - TotalEquityGrossMinorityInterest

Accumulated Minority Interest - MinorityInterest

Total Equity - StockholdersEquity

Total Liabilities & Stockholders Equity - Total Liabilities(ABOVE) + Total Shareholders Equity(ABOVE)

Book Value Per Share - 

Tangible Book Value Per Share - 

Full-Time Employees - 

Price to Book Ratio - 

Return on Assets - 

Return on Equity - 

Return on Invested Capital - 

Quick Ratio - 

Current Ratio - 




"""



"""
Finviz Income Statement Metrics to Yahoo Finance.

Total Revenue :

Cost of Goods Sold Incl. D&A :

Gross Profit :

Selling, General and Administrative Excl. Other :

Research and Development :

Other Operating Expense :

Operating Income :

Interest Expense :

Unusual Expense :

Net Income Before Taxes :

Income Taxes :

Consolidated Net Income :

Net Income From Continuing Operations :

Net Income :

EPS (Recurring) : 

EPS (Basic, Before Extraordinaries) :

EPS (Diluted) :

EBITDA :

Non-Operating Income (Expense) :

Other After Tax Adjustments :

Stock Option Compensation Expense :

Price To Earnings Ratio :

Price To Sales Ratio :

Gross Margin :

Operating Margin :

Net Margin :

Shares Outstanding :

Market Capitalization : 


"""

dict_all_financials['bal_sheet']['NESN.SW'][50:]
# %%

dict_all_financials['bal_sheet']['MC.PA']
# %%
dict_all_financials['bal_sheet']['VOW3.DE']

# %%

dict_all_financials['bal_sheet']['DTE.DE']


#%%

compare_statement_indexes(dict_all_financials['bal_sheet']['NESN.SW'],dict_all_financials['bal_sheet']['MC.PA'])
# %%

def items_frequency_in_statements(dict_statement_tickers:dict):

    dict_frequency = {'NºTickers' : len(dict_statement_tickers)}
    tickers_on_dict = list(dict_statement_tickers.keys())

    for ticker in tickers_on_dict:

        df_analysis = dict_statement_tickers[ticker]
        index_lst = df_analysis.index.to_list()

        for item in index_lst:

            if item not in dict_frequency.keys():

                dict_frequency[item] = 1
            
            else:

                dict_frequency[item] = dict_frequency[item] + 1
    
    return dict_frequency

# %%

bal_sheet_item_freq = items_frequency_in_statements(dict_all_financials['bal_sheet'])
# %%
bal_sheet_item_freq
# %%

def order_dict_asc_des(dic:dict,order = 'des'):

    if order == 'asc':

        dic = dict(sorted(dic.items(), key=lambda item: item[0])) #ascending
    
    else:

        dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True)) #descending
    
    return dic
# %%

bal_sheet_item_freq = order_dict_asc_des(bal_sheet_item_freq)
# %%
bal_sheet_item_freq['AccountsReceivable']

# %%

def tickers_without_metric(dict_statement_tickers:dict,metrics_list:str):

    tickers_no_metric = list()
    tickers = list(dict_statement_tickers.keys())

    for ticker in tickers:

        for metric in metrics_list:

            if metric not in dict_statement_tickers[ticker].index:

                tickers_no_metric.append(ticker)
                break
    
    return tickers_no_metric


# %%

tickers_without_metric(dict_all_financials['bal_sheet'],[
    "CashCashEquivalentsAndShortTermInvestments",
])

#%%
tickers_without_metric(dict_all_financials['bal_sheet'],[
    "LongTermDebtAndCapitalLeaseObligation",
])

# %%

lst_keys_bal_sheet = list(bal_sheet_item_freq.keys())

# %%
lst_keys_bal_sheet[0:30]
# %%

dict_all_financials['bal_sheet']['EOAN.DE'][50:]


# %%

"""

path for balance sheet excel -  "C:\Users\Afons\Python_Files\Projects\Import_Financial_Statements\afonso_screener_v2\output\normalized\ticker\bal_sheet.csv"

path for income statement excel - "C:\Users\Afons\Python_Files\Projects\Import_Financial_Statements\afonso_screener_v2\output\normalized\ticker\inc_stat.csv"

path for stat of cash flows excel - "C:\Users\Afons\Python_Files\Projects\Import_Financial_Statements\afonso_screener_v2\output\normalized\ticker\stat_cfs.csv"

directory_to_tickers = r"C:\Users\Afons\Python_Files\Projects\Import_Financial_Statements\afonso_screener_v2\output\normalized"

"""

#%%

def financials_from_csv_into_dict_dfs(directory_to_tickers):

    dict_all_financials = {'bal_sheet' : {},'inc_stat' : {}, 'stat_cfs' : {}}
    path_dir = Path(directory_to_tickers)
    all_path_tickers = path_dir.iterdir()

    for ticker_path in all_path_tickers:

        ticker = ticker_path.as_posix().split("/")[9].replace("_",".")
        ticker_path_financials = ticker_path.iterdir()
        lst_financials_paths_csv = [path for path in ticker_path_financials]
        for i in range(len(lst_financials_paths_csv)):

            if i == 0 : #balance_sheet

                dict_all_financials['bal_sheet'][ticker] = pd.read_csv(lst_financials_paths_csv[i])

            elif i == 1: #inc_stat
            
                dict_all_financials['inc_stat'][ticker] = pd.read_csv(lst_financials_paths_csv[i])

            else: #stat_cfs

                dict_all_financials['stat_cfs'][ticker] = pd.read_csv(lst_financials_paths_csv[i])
    
    return dict_all_financials


# %%
directory = r"C:\Users\Afons\Python_Files\Projects\Import_Financial_Statements\afonso_screener_v2\output\normalized"

dict_financials = financials_from_csv_into_dict_dfs(directory)

#%%

dict_financials['bal_sheet']['AF.PA']

#%%

dict_financials['inc_stat']['AF.PA']


#%%

dict_financials['stat_cfs']['AF.PA']

#%%

len(dict_financials['bal_sheet'].keys())


    # %%
tuple_sub_direct = os.walk(directory)

#%%

tuple_sub_direct

#%%


tuple_sub_direct = [x[0] for x in os.walk(directory)]

tuple_sub_direct

#%%

next(os.walk('.'))[1]

#%%

path_dir = Path(r"C:\Users\Afons\Python_Files\Projects\Import_Financial_Statements\afonso_screener_v2\output\normalized")

paths_below = path_dir.iterdir()
# %%

for path in paths_below:

    print(path)
# %%
a2a_ticker_path = Path(r"C:\Users\Afons\Python_Files\Projects\Import_Financial_Statements\afonso_screener_v2\output\normalized\A2A_MI")

a2a_paths_below = a2a_ticker_path.iterdir()
lst_paths_below = []

for path in a2a_paths_below:

    lst_paths_below.append(path)
# %%

pd.read_csv(r"C:\Users\Afons\Python_Files\Projects\Import_Financial_Statements\afonso_screener_v2\output\normalized\A2A_MI\bal_sheet.csv")
# %%

lst_paths_below[0].as_posix().split("/")[9].replace("_",".")


# %%

Path().as_posix