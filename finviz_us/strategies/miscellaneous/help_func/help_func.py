#%%

import pandas as pd
import numpy as np
import time
import finvizfinance.quote as fvf

#%%

"""ORDER DICTS"""

def order_dict_asc_des(dic:dict,order = 'des'):

    if order == 'asc':

        dic = dict(sorted(dic.items(), key=lambda item: item[0])) #ascending
    
    else:

        dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True)) #descending
    
    return dic

#%%

"""NET CURRENT ASSET RATIO"""

def net_current_asset_ratio(tickers_list:list,dict_tickers_bs:dict,dict_tickers_inc_stat:dict):

    dict_ratio = dict()
    dict_ratio['Positive_Values'] = dict()
    dict_ratio['Negative_Values'] = dict()

    for ticker in tickers_list:

        current_price = float(fvf.finvizfinance(ticker).ticker_full_info()['fundament']['Price'])
        time.sleep(0.1)

        #GET CURRENT ASSETS, TOTAL LIABILITIES AND PREFERRED STOCK
        ticker_bs_df = dict_tickers_bs[ticker].copy()
        ticker_bs_df = ticker_bs_df.replace(",","",regex=True)
        recent_current_assets = pd.to_numeric(ticker_bs_df.loc['Total Current Assets',ticker_bs_df.columns[0]])
        recent_total_liabilities = pd.to_numeric(ticker_bs_df.loc['Total Liabilities',ticker_bs_df.columns[0]])

        #GET SHARES OUTSTANDING
        ticker_inc_stat_df = dict_tickers_inc_stat[ticker].copy()
        ticker_inc_stat_df = ticker_inc_stat_df.replace(",","",regex=True)
        recent_shares_outstanding = pd.to_numeric(ticker_inc_stat_df.loc['Shares Outstanding',ticker_inc_stat_df.columns[1]])

        net_current_asset_value_ratio = current_price / ((recent_current_assets - recent_total_liabilities) / recent_shares_outstanding)

        if net_current_asset_value_ratio < 0:

            dict_ratio['Negative_Values'][ticker] = net_current_asset_value_ratio.round(decimals = 3)
        
        else:

            dict_ratio['Positive_Values'][ticker] = net_current_asset_value_ratio.round(decimals = 3)
    
    dict_ratio['Positive_Values'] = order_dict_asc_des(dict_ratio['Positive_Values'],'asc')
    dict_ratio['Negative_Values'] = order_dict_asc_des(dict_ratio['Negative_Values'])

    return dict_ratio

"""dict_ratio['Positive_Values'] BELOW 1 MEANS COMPANY ACCOUNTING WISE LARGELY UNDERVALUED"""

#%%

"""TANGIBLE BOOK VALUE RATIO"""

def tangible_book_value_ratio(tickers_list:list,dict_tickers_bs:dict,dict_tickers_inc_stat:dict,dict_price:dict):

    dict_ratio = dict()
    dict_ratio['Positive_Values'] = dict()
    dict_ratio['Negative_Values'] = dict()

    for ticker in tickers_list:

        current_price = dict_price[ticker]

        #GET CURRENT ASSETS, TOTAL LIABILITIES AND PREFERRED STOCK
        ticker_bs_df = dict_tickers_bs[ticker].copy()
        ticker_bs_df = ticker_bs_df.replace(",","",regex=True)
        recent_equity = pd.to_numeric(ticker_bs_df.loc['Total Equity',ticker_bs_df.columns[0]])
        recent_intangible_assets = pd.to_numeric(ticker_bs_df.loc['Intangible Assets',ticker_bs_df.columns[0]])
        recent_preferred_stock = pd.to_numeric(ticker_bs_df.loc['Preferred Stock - Carrying Value',ticker_bs_df.columns[0]])

        #GET SHARES OUTSTANDING
        ticker_inc_stat_df = dict_tickers_inc_stat[ticker].copy()
        ticker_inc_stat_df = ticker_inc_stat_df.replace(",","",regex=True)
        recent_shares_outstanding = pd.to_numeric(ticker_inc_stat_df.loc['Shares Outstanding',ticker_inc_stat_df.columns[1]])

        cond_intangible_assets = np.isnan(recent_intangible_assets)
        cond_preferred_stock = np.isnan(recent_preferred_stock)

        if cond_intangible_assets or cond_preferred_stock:
        
            if cond_intangible_assets and cond_preferred_stock:
            
                tangible_book_value_ratio = current_price / ((recent_equity - 0 - 0) / recent_shares_outstanding)
            
            elif cond_preferred_stock and (cond_intangible_assets == False):
            
                tangible_book_value_ratio = current_price / ((recent_equity - recent_intangible_assets - 0) / recent_shares_outstanding)

            elif cond_preferred_stock == False or cond_intangible_assets:
            
                tangible_book_value_ratio = current_price / ((recent_equity - 0 - recent_preferred_stock) / recent_shares_outstanding)

        else:
        
            tangible_book_value_ratio = current_price / ((recent_equity - recent_intangible_assets - recent_preferred_stock) / recent_shares_outstanding)

        if tangible_book_value_ratio < 0:

            dict_ratio['Negative_Values'][ticker] = tangible_book_value_ratio.round(decimals = 3)
        
        else:

            dict_ratio['Positive_Values'][ticker] = tangible_book_value_ratio.round(decimals = 3)
    
    dict_ratio['Positive_Values'] = order_dict_asc_des(dict_ratio['Positive_Values'],'asc')
    dict_ratio['Negative_Values'] = order_dict_asc_des(dict_ratio['Negative_Values'])
        
    return dict_ratio

"""dict_ratio['Positive_Values'] BELOW 1 MEANS COMPANY ACCOUNTING WISE MEANS UNDERVALUED AS EQUITY HOLDERS TECHNICALLY WOULD RECEIVE MORE THAN CURRENT PRICE IF ASSETS WERE TO BE LIQUIDATED"""

#%%

"""ENTERPRISE VALUE / FREE CASH FLOW"""

def ev_fcf_ratio(tickers_lst:list,dict_tickers_bs:dict,dict_tickers_inc_stat:dict,dict_tickers_stat_cfs:dict):

    dict_ratio = dict()
    dict_ratio['Positive_Values_both_metrics_Negative'] = dict()
    dict_ratio['Positive_Values_both_metrics_Positive'] = dict()
    dict_ratio['Negative_Values'] = dict()

    #GET AVERAGE PAST X AMOUNT OF YEARS FCF

    n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    while n_years_lookback_to_compute_average < 1 or n_years_lookback_to_compute_average > 8 :

        print("NUMBER BETWEEN 1 AND 7")
        n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    for ticker in tickers_lst:

        #GET MARKET CAP
        ticker_inc_stat_df = dict_tickers_inc_stat[ticker].copy()
        ticker_inc_stat_df = ticker_inc_stat_df.replace(",","",regex=True)
        recent_mk_cap = pd.to_numeric(ticker_inc_stat_df.loc['Market Capitalization',ticker_inc_stat_df.columns[1]])

        #GET DEBT AND CASH
        ticker_bs_df = dict_tickers_bs[ticker].copy()
        ticker_bs_df = ticker_bs_df.replace(",","",regex=True)
        recent_cash = pd.to_numeric(ticker_bs_df.loc['Cash & Short Term Investments',ticker_bs_df.columns[0]])
        recent_sht_debt = pd.to_numeric(ticker_bs_df.loc['Short Term Debt Incl. Current Port. of LT Debt',ticker_bs_df.columns[0]])
        recent_lt_debt = pd.to_numeric(ticker_bs_df.loc['Long Term Debt',ticker_bs_df.columns[0]])
        
        ticker_stat_cfs_df = dict_tickers_stat_cfs[ticker].copy()
        ticker_stat_cfs_df = ticker_stat_cfs_df.replace(",","",regex=True)
        avg_fcf = pd.to_numeric(ticker_stat_cfs_df.loc['Free Cash Flow',ticker_stat_cfs_df.columns[1:n_years_lookback_to_compute_average+1]]).mean()

        no_sht_debt = np.isnan(recent_sht_debt)
        no_lt_debt = np.isnan(recent_lt_debt)

        if no_sht_debt or no_lt_debt:
        
            if no_sht_debt and no_lt_debt:
            
                recent_sht_debt = 0
                recent_lt_debt = 0

            elif no_sht_debt == False and no_lt_debt:
            
                recent_lt_debt = 0

            elif no_sht_debt and no_lt_debt == False:
            
                recent_sht_debt = 0

        ev = recent_mk_cap + recent_sht_debt + recent_lt_debt - recent_cash

        if ev > 0 and avg_fcf > 0:

            dict_ratio['Positive_Values_both_metrics_Positive'][ticker] = (ev / avg_fcf).round(decimals=3)

        else:

            if ev < 0 and avg_fcf < 0:

                dict_ratio['Positive_Values_both_metrics_Negative'][ticker] = (ev / avg_fcf).round(decimals=3)

            else:

                dict_ratio['Negative_Values'][ticker] = (ev / avg_fcf).round(decimals=3)

        dict_ratio['Positive_Values_both_metrics_Positive'] = order_dict_asc_des(dict_ratio['Positive_Values_both_metrics_Positive'],'asc')
        dict_ratio['Negative_Values'] = order_dict_asc_des(dict_ratio['Negative_Values'])

    return dict_ratio

"""dict_ratio['Positive_Values_both_metrics_Positive'] BELOW 1 MEANS COMPANY PRODUCES MORE CASH FLOW THAN THE VALUE IT HAS
   MIGHT SIGNAL UNDERVALUATION OR;
   OR INVESTORS MIGHT SEE UNCERTAINTY OR PRICE IN THE EFFECT OF A LARGE EVENT THAT MIGHT LEAD TO COMPANY FACING HARD TIMES
"""

#%%

"""PRICE Per_SHARE / FCF Per_SHARE"""

def price_to_fcf(tickers_lst:list,dict_tickers_inc_stat:dict,dict_tickers_stat_cfs:dict,dict_price:dict):

    dict_ratio = dict()

    dict_ratio['Positive_Values'] = dict()
    dict_ratio['Negative_Values'] = dict()

    #GET AVERAGE PAST X AMOUNT OF YEARS FCF

    n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    while n_years_lookback_to_compute_average < 1 or n_years_lookback_to_compute_average > 8 :

        print("NUMBER BETWEEN 1 AND 7")
        n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    for ticker in tickers_lst:
    
        current_price = dict_price[ticker]
        
        ticker_stat_cfs_df = dict_tickers_stat_cfs[ticker].copy()
        ticker_stat_cfs_df = ticker_stat_cfs_df.replace(",","",regex=True)
        avg_fcf = pd.to_numeric(ticker_stat_cfs_df.loc['Free Cash Flow',ticker_stat_cfs_df.columns[1:n_years_lookback_to_compute_average+1]]).mean()

        #GET SHARES OUTSTANDING
        ticker_inc_stat_df = dict_tickers_inc_stat[ticker].copy()
        ticker_inc_stat_df = ticker_inc_stat_df.replace(",","",regex=True)
        recent_shares_outstanding = pd.to_numeric(ticker_inc_stat_df.loc['Shares Outstanding',ticker_inc_stat_df.columns[1]])

        price_to_fcf = (current_price / (avg_fcf / recent_shares_outstanding)).round(decimals=3)

        if price_to_fcf < 0 :

            dict_ratio['Negative_Values'][ticker] = price_to_fcf
        
        else:

            dict_ratio['Positive_Values'][ticker] = price_to_fcf

        dict_ratio['Positive_Values'] = order_dict_asc_des(dict_ratio['Positive_Values'],'asc')
        dict_ratio['Negative_Values'] = order_dict_asc_des(dict_ratio['Negative_Values'])
    
    return dict_ratio

"""dict_ratio['Positive_Values'] BELOW 1 MEANS COMPANY PRODUCES MORE CASH FLOW THAN THE VALUE IT HAS
   MIGHT SIGNAL UNDERVALUATION OR;
   OR INVESTORS MIGHT SEE UNCERTAINTY OR PRICE IN THE EFFECT OF A LARGE EVENT THAT MIGHT LEAD TO COMPANY FACING HARD TIMES
"""

#%%

"""SHAREHOLDER YIELD : (dividends + share buybacks) / AVG_FCF """

def shareholder_yield(tickers_lst:list,dict_tickers_inc_stat:dict,dict_tickers_stat_cfs:dict):

    dict_ratio = dict()

    dict_ratio['Positive_Values'] = dict()
    dict_ratio['Negative_Values'] = dict()

    #GET AVERAGE PAST X AMOUNT OF YEARS FCF

    n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    while n_years_lookback_to_compute_average < 1 or n_years_lookback_to_compute_average > 8 :

        print("NUMBER BETWEEN 1 AND 7")
        n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    for ticker in tickers_lst:

        #GET SHARES OUTSTANDING
        ticker_inc_stat_df = dict_tickers_inc_stat[ticker].copy()
        ticker_inc_stat_df = ticker_inc_stat_df.replace(",","",regex=True)
        recent_shares_outstanding = pd.to_numeric(ticker_inc_stat_df.loc['Shares Outstanding',ticker_inc_stat_df.columns[1]])
        
        ticker_stat_cfs_df = dict_tickers_stat_cfs[ticker].copy()
        ticker_stat_cfs_df = ticker_stat_cfs_df.replace(",","",regex=True)
        avg_fcf = pd.to_numeric(ticker_stat_cfs_df.loc['Free Cash Flow',ticker_stat_cfs_df.columns[1:n_years_lookback_to_compute_average+1]]).mean()

        #GET DIVIDENDS PAID & SHARE BUYBACKS
        dividends_paid = -(pd.to_numeric(ticker_stat_cfs_df.loc['Cash Dividends Paid',ticker_stat_cfs_df.columns[1]]))
        share_buybacks = -(pd.to_numeric(ticker_stat_cfs_df.loc['Repurchase of Common Pref Stock',ticker_stat_cfs_df.columns[1]]))

        no_dividend = np.isnan(dividends_paid)
        no_buyback = np.isnan(share_buybacks)

        if no_dividend or no_buyback:
        
            if no_dividend and no_buyback:
            
                dividends_paid = 0
                share_buybacks = 0
            
            elif no_dividend and no_buyback == False:
                
                dividends_paid = 0
            
            elif no_dividend == False and no_buyback:
            
                share_buybacks = 0
        
        shareholder_yield = (dividends_paid + share_buybacks) / avg_fcf

        if shareholder_yield < 0:

            dict_ratio['Negative_Values'][ticker] = shareholder_yield.round(decimals = 3)
        
        else:

            dict_ratio['Positive_Values'][ticker] = shareholder_yield.round(decimals = 3)

        dict_ratio['Positive_Values'] = order_dict_asc_des(dict_ratio['Positive_Values'])
        dict_ratio['Negative_Values'] = order_dict_asc_des(dict_ratio['Negative_Values'])

    return dict_ratio


"""dict_ratio['Positive_Values'] Values Close to 1 mean that the company distributes a large portion of their FCF to Shareholders
"""