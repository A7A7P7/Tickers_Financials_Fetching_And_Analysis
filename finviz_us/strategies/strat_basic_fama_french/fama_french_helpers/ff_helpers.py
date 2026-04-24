#%%

import pandas as pd
import numpy as np
import time
import finvizfinance.quote as fvf
from pathlib import Path
import math

#%%

"""PROFITABILILITY FACTOR"""

def ticker_profitability_factor(tickers,dict_financials):

    inc_stat_dict = dict_financials['inc_stat']
    bs_dict = dict_financials['bal_sheet']
    possible_tickers = []
    unusable_tickers = []
    dict_profitability = dict()

    for ticker in tickers:

        cols_df_bs = list(bs_dict[ticker].columns)
        count_col_recurrence = []

        for i in range(len(cols_df_bs)):

            count_col_recurrence.append(cols_df_bs.count(cols_df_bs[i]))

        if count_col_recurrence.count(1) != len(count_col_recurrence): #CHANGES IN REPORTING, SO TICKER IS DROPPED

            unusable_tickers.append(ticker)

        else:

            possible_tickers.append(ticker)

    #get Operating Income of Past 5y and average
        #Needs Income Statement to get Revenues and Operating Income
    n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    while n_years_lookback_to_compute_average < 1 or n_years_lookback_to_compute_average > 8 :

        print("NUMBER BETWEEN 1 AND 7")
        n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    for ticker in possible_tickers:

        dict_profitability[ticker] = dict()

        #OPERATING MARGIN CALCULATION
        ticker_inc_stat = inc_stat_dict[ticker].copy()
        ticker_inc_stat = ticker_inc_stat.replace(",","",regex=True)
        record_revenues = pd.to_numeric(ticker_inc_stat.loc['Total Revenue'][1:n_years_lookback_to_compute_average+1])
        record_ebit = pd.to_numeric(ticker_inc_stat.loc['Operating Income'][1:n_years_lookback_to_compute_average+1])

        operating_margin_avg = (record_ebit/record_revenues).mean().round(decimals=2)
        if float(operating_margin_avg) == float("inf") or float(operating_margin_avg) == float("-inf"): #ANY TICKER HAS REVENUE OF 0

            dict_profitability[ticker][f"Op_Margin_{n_years_lookback_to_compute_average}y_AVG_AbsVal"] = "ANY TICKER HAS REVENUE OF 0 IN OF THE YEARS CONSIDERED"

        else:

            dict_profitability[ticker][f"Op_Margin_{n_years_lookback_to_compute_average}y_AVG_AbsVal"] = float(operating_margin_avg)

        #ROE AND DEBT ADJUSTMENT
        ticker_bs = bs_dict[ticker].copy()
        ticker_bs = ticker_bs.replace(",","",regex=True)
        record_roe = pd.to_numeric(ticker_bs.loc['Return on Equity'][0:n_years_lookback_to_compute_average])
        record_debt = pd.to_numeric(ticker_bs.loc['Long Term Debt'][0:n_years_lookback_to_compute_average]) + pd.to_numeric(ticker_bs.loc['Short Term Debt Incl. Current Port. of LT Debt'][0:n_years_lookback_to_compute_average])
        record_equity = pd.to_numeric(ticker_bs.loc['Total Shareholders Equity'][0:n_years_lookback_to_compute_average])

        if n_years_lookback_to_compute_average < 5:

            roe_debt_adjusted_avg = (record_roe * (1 - (record_debt/(record_debt+record_equity)))).mean().__round__(2)

        else:

            lst_hist_roe = []
            probs_lst = [1/n_years_lookback_to_compute_average for i in range(n_years_lookback_to_compute_average)]
            prob_adjustment = (1/n_years_lookback_to_compute_average) / 4
            years_with_adjust = math.floor(n_years_lookback_to_compute_average/2)
            for i in range(years_with_adjust):

                final_idx = n_years_lookback_to_compute_average-1
                probs_lst[final_idx-i] = probs_lst[final_idx-i] - prob_adjustment
                probs_lst[i] = probs_lst[final_idx-i] + prob_adjustment



            for i in range(len(record_equity)):

                roe_debt_adjusted_avg_yearly = (record_roe.at[ticker_bs.columns[i]] * (1 - (record_debt.at[ticker_bs.columns[i]]/(record_debt.at[ticker_bs.columns[i]]+record_equity.at[ticker_bs.columns[i]]))))
                weighted_roe = probs_lst[i] * roe_debt_adjusted_avg_yearly
                lst_hist_roe.append(weighted_roe)

            roe_debt_adjusted_avg = sum(lst_hist_roe)

        if float(roe_debt_adjusted_avg) == float("inf") or float(roe_debt_adjusted_avg) == float("-inf"):

            dict_profitability[ticker][f"ROE_Debt_Adjusted_%Val"] = "VALUES CANNOT BE COMPUTED, EITHER ROE, DEBT OR EQUITY HAVE INCOMPATIBLE VALUES"

        else:

            dict_profitability[ticker][f"ROE_Debt_Adjusted_%Val"] = float(roe_debt_adjusted_avg)

        if type(dict_profitability[ticker][f"Op_Margin_{n_years_lookback_to_compute_average}y_AVG_AbsVal"]) == str or type(dict_profitability[ticker][f"ROE_Debt_Adjusted_%Val"]) == str:

            dict_profitability[ticker]["Profitability_Factor_AbsVal"] = "CANNOT COMPUTE FACTOR AS THE REVENUE OF SOME YEARS CONSIDERED WAS 0"

        else:

            dict_profitability[ticker]["Profitability_Factor_AbsVal"] = ((dict_profitability[ticker][f"Op_Margin_{n_years_lookback_to_compute_average}y_AVG_AbsVal"] + dict_profitability[ticker][f"ROE_Debt_Adjusted_%Val"]/100) / 2).__round__(2)

        #print(f"{ticker} Profitability_Factor : ",dict_profitability[ticker]["Profitability_Factor_AbsVal"])

    return [dict_profitability,possible_tickers,unusable_tickers]


#%%

"""VALUE FACTOR"""

def ticker_value_factor(tickers):

    dict_value = dict()

    for ticker in tickers:

        dict_value[ticker] = dict()

        #IMPORTS DIRECTLY FROM FINVIZ, SO DO TIME.SLEEP
        price_earnings = fvf.finvizfinance(ticker).ticker_full_info()['fundament']['P/E']
        time.sleep(0.3)
        price_book = fvf.finvizfinance(ticker).ticker_full_info()['fundament']['P/B']
        print(ticker,"P/E",price_earnings,"AND P/B",price_book)

        if "-" in price_earnings:

            dict_value[ticker]['P/E'] = "No Earnings"

        else:

            dict_value[ticker]['P/E'] = float(price_earnings).__round__(2)

        if "-" in price_book:

            dict_value[ticker]['P/B'] = "Negative Equity"

        else:

            dict_value[ticker]['P/B'] = float(price_book).__round__(2)

        if type(dict_value[ticker]['P/B']) != type(0.0) or type(dict_value[ticker]['P/E']) != type(0.0):

            dict_value[ticker]['AVG_Value_Metrics'] = "Not Available, Either Current Equity or Earnings are Negative"

        else:

            dict_value[ticker]['AVG_Value_Metrics'] = ((0.75*dict_value[ticker]['P/E'] + 0.25*dict_value[ticker]['P/B'])).__round__(2)

    return dict_value

#%%

"""TICKER BETA"""

def ticker_beta(tickers):

    dict_beta = dict()

    for ticker in tickers:

        dict_beta[ticker] = dict()

        #IMPORTS DIRECTLY FROM FINVIZ, SO DO TIME.SLEEP
        beta = fvf.finvizfinance(ticker).ticker_full_info()['fundament']['Beta']

        if "-" in beta:

            if beta == "-":

                beta = f"{ticker} DOESN'T HAVE A BETA VALUE IN FINVIZ"

            else:

                beta = float(beta.replace("-","")) * (-1)

        else:

            beta = float(beta)

        dict_beta[ticker]['Beta'] = beta
        print("BETA OF",ticker,"IS",beta)
        time.sleep(0.3)

    return dict_beta

#%%

"""MOMENTUM FACTOR"""

def ticker_momentum(tickers):

    dict_momentum = dict()

    for ticker in tickers:

        dict_momentum[ticker] = dict()

        #IMPORTS DIRECTLY FROM FINVIZ, SO DO TIME.SLEEP
        past_month_performance = fvf.finvizfinance(ticker).ticker_full_info()['fundament']['Perf Month'].replace("%","")
        time.sleep(0.3)
        past_year_performance = fvf.finvizfinance(ticker).ticker_full_info()['fundament']['Perf Year'].replace("%","")

        if "-" in past_month_performance: #IT COMES AS A STRING, SO TO TURN INTO FLOAT, ONE NEEDS TO REMOVE NON-NUMBER CHARACTERS

            if past_month_performance == "-": #BASICALLY TICKERS THAT ARE RECENTLY IN THE STOCK MARKET AREN'T INCLUDED

                dict_momentum[ticker]['Momentum_Factor'] = "NON-EXISTENT, TICKER DOESN'T HAVE PERFORMANCE OF PAST MONTH"

            else:

                past_month_performance = float(past_month_performance.replace("-","")) * (-1) / 100 #PUT IN %

        else:

            past_month_performance = float(past_month_performance) / 100 #PUT IN %

        if "-" in past_year_performance: #IT COMES AS A STRING, SO TO TURN INTO FLOAT, ONE NEEDS TO REMOVE NON-NUMBER CHARACTERS

            if past_year_performance == "-": #BASICALLY TICKERS THAT ARE RECENTLY IN THE STOCK MARKET AREN'T INCLUDED

                dict_momentum[ticker]['Momentum_Factor'] = "NON-EXISTENT, TICKER DOESN'T HAVE PERFORMANCE OF PAST YEAR"

            else:

                past_year_performance = float(past_year_performance.replace("-","")) * (-1) / 100 #PUT IN %

        else:

            past_year_performance = float(past_year_performance) / 100 #PUT IN %

        if type(past_month_performance) == float and type(past_year_performance) == float:


            momentum_factor = ((1+past_year_performance)/(1+past_month_performance)) - 1
            dict_momentum[ticker]['Momentum_Factor'] = momentum_factor

        print(ticker,"MOMENTUM FACTOR: ",momentum_factor)
        time.sleep(0.1)

    return dict_momentum

#%%

"""INVESTMENT FACTOR"""

def ticker_investment_factor(tickers,dict_financials):

    stat_cfs_dict = dict_financials['stat_cfs']
    bs_dict = dict_financials['bal_sheet']
    dict_investment = dict()

    #get Operating Income of Past 5y and average
        #Needs Income Statement to get Revenues and Operating Income
    n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    while n_years_lookback_to_compute_average < 1 or n_years_lookback_to_compute_average > 8 :

        print("NUMBER BETWEEN 1 AND 7")
        n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    for ticker in tickers:

        dict_investment[ticker] = dict()

        #GROSS FIXED ASSET INCREASE
        ticker_stat_cfs = stat_cfs_dict[ticker].copy()
        ticker_stat_cfs = ticker_stat_cfs.replace(",","",regex=True)
        record_capex = pd.to_numeric(ticker_stat_cfs.loc['Capital Expenditures'][1:n_years_lookback_to_compute_average+1])
        record_assets_from_acquistions = pd.to_numeric(ticker_stat_cfs.loc['Net Assets From Acquisitions'][1:n_years_lookback_to_compute_average+1])
        record_assets_sales = pd.to_numeric(ticker_stat_cfs.loc['Sale of Fixed Assets and Businesses'][1:n_years_lookback_to_compute_average+1])

        gross_fixed_asset_increase = (-(record_capex+record_assets_from_acquistions-record_assets_sales)).mean().round(decimals=3)
        dict_investment[ticker][f"Gross_FixAsset_Inc_{n_years_lookback_to_compute_average}y_AVG_AbsVal"] = gross_fixed_asset_increase

        #TOTAL ASSETS
        ticker_bs = bs_dict[ticker].copy()
        ticker_bs = ticker_bs.replace(",","",regex=True)
        record_total_assets = pd.to_numeric(ticker_bs.loc['Total Assets'][0:n_years_lookback_to_compute_average])

        total_assets_average = (record_total_assets).mean().round(decimals=3)
        dict_investment[ticker][f"Total_Assets_{n_years_lookback_to_compute_average}y_AVG"] = total_assets_average

        dict_investment[ticker]["Investment_Factor_AbsVal"] = (dict_investment[ticker][f"Gross_FixAsset_Inc_{n_years_lookback_to_compute_average}y_AVG_AbsVal"] / dict_investment[ticker][f"Total_Assets_{n_years_lookback_to_compute_average}y_AVG"]).round(decimals = 3)

    return dict_investment

#%%

"""RANKING THE TICKERS USING THE FACTORS"""

def standardized_raking_sector_buys(tickers_lst:list,profit_data:dict,value_data:dict,beta_data:dict,momentum_data:dict,investment_data:dict):

    poss_first_filter = []
    possible_tickers = []
    unusable_tickers = []
    profitability_data = []
    valuation_data = []
    beta_numbers = []
    momentum_numbers = []
    investment_numbers = []
    dict_final_score = dict()

    for ticker in tickers_lst:

        cond_1 = type(profit_data[ticker]["Profitability_Factor_AbsVal"]) != str
        cond_2 = type(value_data[ticker]["AVG_Value_Metrics"]) != str
        cond_3 = type(beta_data[ticker]["Beta"]) != str
        cond_4 = type(momentum_data[ticker]["Momentum_Factor"]) != str
        cond_5 = type(investment_data[ticker]["Investment_Factor_AbsVal"]) != str
        combined_cond = cond_1 and cond_2 and cond_3 and cond_4 and cond_5

        if combined_cond:

            poss_first_filter.append(ticker)

        else:

            unusable_tickers.append(ticker)

    for ticker in poss_first_filter:

        profit_factor = profit_data[ticker]["Profitability_Factor_AbsVal"]
        value_factor = value_data[ticker]["AVG_Value_Metrics"]
        beta_factor = beta_data[ticker]["Beta"]
        momentum_factor = momentum_data[ticker]["Momentum_Factor"]
        investment_factor = investment_data[ticker]["Investment_Factor_AbsVal"]
        profit_factor_exists = ~(np.isnan(profit_factor))
        value_factor_exists = ~(np.isnan(value_factor))
        beta_factor_exists = ~(np.isnan(beta_factor))
        momentum_factor_exists = ~(np.isnan(momentum_factor))
        investment_factor_exists = ~(np.isnan(investment_factor))

        all_factors_exist = profit_factor_exists and value_factor_exists and beta_factor_exists and momentum_factor_exists and investment_factor_exists

        if all_factors_exist:

            possible_tickers.append(ticker)
            profitability_data.append(profit_factor)
            valuation_data.append(value_factor)
            beta_numbers.append(abs(beta_factor))
            momentum_numbers.append(momentum_factor)
            investment_numbers.append(investment_factor)

        else:

            unusable_tickers.append(ticker)

    #Profit Distribution
    profit_mean = np.mean(profitability_data)
    profit_std = np.std(profitability_data)

    #Value Distribution
    value_mean = np.mean(valuation_data) #ALWAYS POSITIVE, NO NEGATIVE P/E OR P/B
    value_std = np.std(valuation_data)
    valuation_data_mean_centered_zero = []

    for value in valuation_data:

        val_centered = value - value_mean
        valuation_data_mean_centered_zero.append(val_centered)


    #Beta Distribution
    beta_mean = np.mean(beta_numbers)
    beta_std = np.std(beta_numbers)

    beta_tickers_distance_from_zero = beta_numbers
    beta_dist_mean_centered_zero = []

    for beta in beta_tickers_distance_from_zero:

        val_centered = beta - beta_mean
        beta_dist_mean_centered_zero.append(val_centered)

    #Momentum Distribution
    mom_mean = np.mean(momentum_numbers)
    mom_std = np.std(momentum_numbers)


    #Investment Distribution
    investment_mean = np.mean(investment_numbers)
    investment_std = np.std(investment_numbers)

    for ticker in possible_tickers:

        idx_ticker = possible_tickers.index(ticker)

        profit_metric = (profit_data[ticker]["Profitability_Factor_AbsVal"] - profit_mean) / profit_std
        value_metric = valuation_data_mean_centered_zero[idx_ticker] / value_std
        beta_metric = beta_dist_mean_centered_zero[idx_ticker] / beta_std
        mom_metric = (momentum_data[ticker]['Momentum_Factor'] - mom_mean) / mom_std
        investment_metric = (investment_data[ticker]["Investment_Factor_AbsVal"] - investment_mean) / investment_std

        ticker_score = ((1/5)*(profit_metric-value_metric-beta_metric+mom_metric-investment_metric)).round(decimals = 3)
        #SINCE LOWER VALUE,BETA AND INVESTMENT IS BETTER, ONE TURNS THEM POSITIVE BY PUTTING MINUS
        dict_final_score[ticker] = ticker_score

    dict_copy = dict_final_score.copy()
    dict_final_score_ordered = {}

    while len(dict_copy) != 0:

        list_keys = list(dict_copy.keys())
        list_values = list(dict_copy.values())
        max_score = max(list_values)
        idx_max_score = list_values.index(max_score)
        ticker_max = list_keys[idx_max_score]
        dict_final_score_ordered[ticker_max] = max_score
        del dict_copy[ticker_max]

    dict_final_score = dict_final_score_ordered

    return [dict_final_score,possible_tickers,unusable_tickers]

"""NO MOMENTUM"""

def standardized_raking_sector_buys_no_momentum(tickers_lst:list,profit_data:dict,value_data:dict,beta_data:dict,momentum_data:dict,investment_data:dict):

    poss_first_filter = []
    possible_tickers = []
    unusable_tickers = []
    profitability_data = []
    valuation_data = []
    beta_numbers = []
    momentum_numbers = []
    investment_numbers = []
    dict_final_score = dict()

    for ticker in tickers_lst:

        cond_1 = type(profit_data[ticker]["Profitability_Factor_AbsVal"]) != str
        cond_2 = type(value_data[ticker]["AVG_Value_Metrics"]) != str
        cond_3 = type(beta_data[ticker]["Beta"]) != str
        cond_4 = type(momentum_data[ticker]["Momentum_Factor"]) != str
        cond_5 = type(investment_data[ticker]["Investment_Factor_AbsVal"]) != str
        combined_cond = cond_1 and cond_2 and cond_3 and cond_4 and cond_5

        if combined_cond:

            poss_first_filter.append(ticker)

        else:

            unusable_tickers.append(ticker)

    for ticker in poss_first_filter:

        profit_factor = profit_data[ticker]["Profitability_Factor_AbsVal"]
        value_factor = value_data[ticker]["AVG_Value_Metrics"]
        beta_factor = beta_data[ticker]["Beta"]
        momentum_factor = momentum_data[ticker]["Momentum_Factor"]
        investment_factor = investment_data[ticker]["Investment_Factor_AbsVal"]
        profit_factor_exists = ~(np.isnan(profit_factor))
        value_factor_exists = ~(np.isnan(value_factor))
        beta_factor_exists = ~(np.isnan(beta_factor))
        momentum_factor_exists = ~(np.isnan(momentum_factor))
        investment_factor_exists = ~(np.isnan(investment_factor))

        all_factors_exist = profit_factor_exists and value_factor_exists and beta_factor_exists and momentum_factor_exists and investment_factor_exists

        if all_factors_exist:

            possible_tickers.append(ticker)
            profitability_data.append(profit_factor)
            valuation_data.append(value_factor)
            beta_numbers.append(beta_factor)
            momentum_numbers.append(momentum_factor)
            investment_numbers.append(investment_factor)

        else:

            unusable_tickers.append(ticker)

    #Profit Distribution
    profit_mean = np.mean(profitability_data)
    profit_std = np.std(profitability_data)

    #Value Distribution
    value_mean = np.mean(valuation_data) #ALWAYS POSITIVE, NO NEGATIVE P/E OR P/B
    value_std = np.std(valuation_data)
    valuation_data_mean_centered_zero = []

    for value in valuation_data:

        val_centered = value - value_mean
        valuation_data_mean_centered_zero.append(val_centered)


    #Beta Distribution
    beta_mean = np.mean(beta_numbers)
    beta_std = np.std(beta_numbers)

    beta_tickers_distance_from_zero = beta_numbers
    beta_dist_mean_centered_zero = []

    for beta in beta_tickers_distance_from_zero:

        val_centered = beta - beta_mean
        beta_dist_mean_centered_zero.append(val_centered)

    #Momentum Distribution
    mom_mean = np.mean(momentum_numbers)
    mom_std = np.std(momentum_numbers)


    #Investment Distribution
    investment_mean = np.mean(investment_numbers)
    investment_std = np.std(investment_numbers)

    for ticker in possible_tickers:

        idx_ticker = possible_tickers.index(ticker)

        profit_metric = (profit_data[ticker]["Profitability_Factor_AbsVal"] - profit_mean) / profit_std
        value_metric = valuation_data_mean_centered_zero[idx_ticker] / value_std
        beta_metric = beta_dist_mean_centered_zero[idx_ticker] / beta_std
        mom_metric = (momentum_data[ticker]['Momentum_Factor'] - mom_mean) / mom_std
        investment_metric = (investment_data[ticker]["Investment_Factor_AbsVal"] - investment_mean) / investment_std

        ticker_score = ((1/4)*(profit_metric-value_metric-beta_metric-investment_metric)).round(decimals = 3)
        #SINCE LOWER VALUE,BETA AND INVESTMENT IS BETTER, ONE TURNS THEM POSITIVE BY PUTTING MINUS
        dict_final_score[ticker] = ticker_score

    dict_copy = dict_final_score.copy()
    dict_final_score_ordered = {}

    while len(dict_copy) != 0:

        list_keys = list(dict_copy.keys())
        list_values = list(dict_copy.values())
        max_score = max(list_values)
        idx_max_score = list_values.index(max_score)
        ticker_max = list_keys[idx_max_score]
        dict_final_score_ordered[ticker_max] = max_score
        del dict_copy[ticker_max]

    dict_final_score = dict_final_score_ordered

    return [dict_final_score,possible_tickers,unusable_tickers]

def raking_sector_buys(tickers_lst:list,profit_data:dict,value_data:dict,beta_data:dict,momentum_data:dict,investment_data:dict):

    poss_first_filter = []
    possible_tickers = []
    unusable_tickers = []
    profitability_data = []
    valuation_data = []
    beta_numbers = []
    beta_diff_from_zero = []
    momentum_numbers = []
    investment_numbers = []
    dict_final_score = dict()

    for ticker in tickers_lst:

        cond_1 = type(profit_data[ticker]["Profitability_Factor_AbsVal"]) != str
        cond_2 = type(value_data[ticker]["AVG_Value_Metrics"]) != str
        cond_3 = type(beta_data[ticker]["Beta"]) != str
        cond_4 = type(momentum_data[ticker]["Momentum_Factor"]) != str
        cond_5 = type(investment_data[ticker]["Investment_Factor_AbsVal"]) != str
        combined_cond = cond_1 and cond_2 and cond_3 and cond_4 and cond_5

        if combined_cond:

            poss_first_filter.append(ticker)

        else:

            unusable_tickers.append(ticker)

    for ticker in poss_first_filter:

        profit_factor = profit_data[ticker]["Profitability_Factor_AbsVal"]
        value_factor = value_data[ticker]["AVG_Value_Metrics"]
        beta_factor = beta_data[ticker]["Beta"]
        momentum_factor = momentum_data[ticker]["Momentum_Factor"]
        investment_factor = investment_data[ticker]["Investment_Factor_AbsVal"]
        profit_factor_exists = ~(np.isnan(profit_factor))
        value_factor_exists = ~(np.isnan(value_factor))
        beta_factor_exists = ~(np.isnan(beta_factor))
        momentum_factor_exists = ~(np.isnan(momentum_factor))
        investment_factor_exists = ~(np.isnan(investment_factor))

        all_factors_exist = profit_factor_exists and value_factor_exists and beta_factor_exists and momentum_factor_exists and investment_factor_exists

        if all_factors_exist:

            possible_tickers.append(ticker)
            profitability_data.append(profit_factor)
            valuation_data.append(value_factor)
            beta_numbers.append(beta_factor)
            beta_diff_from_zero.append(abs(beta_factor) - 0)
            momentum_numbers.append(momentum_factor)
            investment_numbers.append(investment_factor)

        else:

            unusable_tickers.append(ticker)

    #Profit Distribution
    profit_mean = np.mean(profitability_data)
    profit_std = np.std(profitability_data)

    #Value Distribution
    value_mean = np.mean(valuation_data)
    value_std = np.std(valuation_data)

    #ADJUSTMENT OF THE DISTRIBUTION TO HAVE MEAN ZERO AS MEAN IS POSITIVE
    #IMPORTANT TO CHANGE THE RANGE OF VALUES THAT VALUE FACTOR WILL
    #TO MAKE THE RANGE FROM [0,100] POSSIBLE
    mean_value_adjusted_to_zero = []

    for value in valuation_data:

        new_val = value - value_mean
        mean_value_adjusted_to_zero.append(new_val)

    #print("Value_Mean: ",value_mean,"And Value_Std: ",value_std)

    #Beta Distribution
    beta_mean = np.mean(beta_numbers)
    beta_std = np.std(beta_numbers)

    #ADJUSTMENT OF THE DISTRIBUTION
    beta_difference_from_zero = []

    for beta in beta_numbers:

        if beta == 0 or beta == 0.0:

            beta = 0.001

        beta_difference_from_zero.append(abs(beta))

    beta_diff_mean = np.mean(beta_difference_from_zero)

    #ADJUSTMENT OF THE DISTRIBUTION TO HAVE MEAN ZERO AS MEAN IS POSITIVE, MOST STOCKS HAVE POSITIVE BETA
    #IMPORTANT TO CHANGE THE RANGE OF VALUES THAT BETA FACTOR WILL HAVE
    #TO MAKE THE RANGE FROM [0,100] POSSIBLE, AS THAT WOULDN'T BE POSSIBLE BECAUSE ABS DISTANCE WAS ALWAYS POSITIVE
    beta_diff_adjusted_zero_mean = [] #NEGATIVE VALUES ARE CLOSE TO ZERO, POSITIVE ARE FARTHER FROM ZERO

    for beta_diff in beta_difference_from_zero:

        adjust_mean_zero = beta_diff - beta_diff_mean
        beta_diff_adjusted_zero_mean.append(adjust_mean_zero)

    #Momentum Distribution
    mom_mean = np.mean(momentum_numbers)
    mom_std = np.std(momentum_numbers)

    #Investment Distribution
    investment_mean = np.mean(investment_numbers)
    investment_std = np.std(investment_numbers)

    for ticker in possible_tickers:

        #VALUE AND BETA SUFFERED ADJUSTMENTS
        ticker_profit_factor = profit_data[ticker]["Profitability_Factor_AbsVal"]
        ticker_momentum_factor = momentum_data[ticker]['Momentum_Factor']
        ticker_investment_factor = investment_data[ticker]["Investment_Factor_AbsVal"]

        #PROFIT_FACTOR MEASUREMENTS

        max_profit_factor = max(profitability_data)
        min_profit_factor = min(profitability_data)
        max_profit = max_profit_factor > 0
        min_profit = min_profit_factor > 0

        if max_profit and min_profit:

            how_profitable = ticker_profit_factor / max_profit_factor

        elif max_profit and min_profit == False :

            if ticker_profit_factor >= 0 :

                how_profitable = ticker_profit_factor / max_profit_factor

            else:

                how_profitable = - (ticker_profit_factor / min_profit_factor)

        else: #max_profit == False and min_profit == False, max_profit == False and min_profit == True doesn't exist

            how_profitable = - (ticker_profit_factor / min_profit_factor)

        #VALUE_FACTOR MEASUREMENTS~

        max_value_factor = max(mean_value_adjusted_to_zero)
        min_value_factor = min(mean_value_adjusted_to_zero)
        max_value = max_value_factor > 0
        min_value = min_value_factor > 0
        idx_ticker_possible_tickers = possible_tickers.index(ticker)
        ticker_value_adjust_factor = mean_value_adjusted_to_zero[idx_ticker_possible_tickers]

        if max_value and min_value == False :

            if ticker_value_adjust_factor >= 0 :

                how_undervalued = - (ticker_value_adjust_factor / max_value_factor) #HIGHER VALUATIONS MEAN SUBTRACTION IN FINAL WEIGHT

            else:

                how_undervalued = ticker_value_adjust_factor / min_value_factor #LOWER VALUATION HAVE MORE WEIGHT IN FINAL SCORE

        #BETA_FACTOR MEASUREMENTS

        max_beta_factor = max(beta_diff_adjusted_zero_mean)
        min_beta_factor = min(beta_diff_adjusted_zero_mean)
        max_beta = max_beta_factor > 0
        min_beta = min_beta_factor > 0
        idx_ticker_possible_tickers = possible_tickers.index(ticker)
        ticker_beta_diff_factor = beta_diff_adjusted_zero_mean[idx_ticker_possible_tickers]


        if max_beta and min_beta:

            how_low_abs_beta =  - (ticker_beta_diff_factor / max_beta_factor) #BETA FURTHER FROM ZERO

        elif max_beta and min_beta == False :

            if ticker_beta_diff_factor >= 0 :

                how_low_abs_beta = - (ticker_beta_diff_factor / max_beta_factor) #BETA FURTHER FROM ZERO

            else:

                how_profitable = ticker_beta_diff_factor / min_beta_factor #BETA CLOSE TO 0.

        else: #max_profit == False and min_profit == False, max_profit == False and min_profit == True doesn't exist

            how_profitable = ticker_beta_diff_factor / min_beta_factor #BETA CLOSE TO 0.

        #MOMENTUM_FACTOR MEASUREMENTS

        max_momentum_factor = max(momentum_numbers)
        min_momentum_factor = min(momentum_numbers)
        max_mom = max_momentum_factor > 0
        min_mom = min_momentum_factor > 0

        if max_mom and min_mom:

            how_healthy_momentum = ticker_momentum_factor / max_momentum_factor

        elif max_mom and min_mom == False :

            if ticker_momentum_factor >= 0 :

                how_healthy_momentum = ticker_momentum_factor / max_momentum_factor

            else:

                how_healthy_momentum = - (ticker_momentum_factor / min_momentum_factor)

        else: #max_mom == False and min_mom == False, max_mom == False and min_mom == True doesn't exist

            how_healthy_momentum = - (ticker_momentum_factor / min_momentum_factor)


        #INVESTMENT_FACTOR MEASUREMENTS, ASSUMES TOTAL ASSETS ARE NEVER NEGATIVE

        max_investment_factor = max(investment_numbers)
        min_investment_factor = min(investment_numbers)
        max_inv = max_investment_factor > 0
        min_inv = min_investment_factor > 0

        if max_inv and min_inv:

            how_invested = - (ticker_investment_factor / max_investment_factor)

        elif max_inv and min_inv == False :

            if ticker_investment_factor >= 0 :

                how_invested = - (ticker_investment_factor / max_investment_factor)

            else:

                how_invested = ticker_investment_factor / min_investment_factor

        else: #max_mom == False and min_mom == False, max_mom == False and min_mom == True doesn't exist

            how_invested = ticker_investment_factor / min_investment_factor

        ticker_score = ((1/5)*(how_profitable + how_undervalued + how_low_abs_beta + how_healthy_momentum + how_invested)).round(decimals = 3)
        #SINCE LOWER VALUE,BETA AND INVESTMENT IS BETTER, ONE TURNS THEM POSITIVE BY PUTTING MINUS
        dict_final_score[ticker] = ticker_score * 100

    dict_copy = dict_final_score.copy()
    dict_final_score_ordered = {}

    while len(dict_copy) != 0:

        list_keys = list(dict_copy.keys())
        list_values = list(dict_copy.values())
        max_score = max(list_values)
        idx_max_score = list_values.index(max_score)
        ticker_max = list_keys[idx_max_score]
        dict_final_score_ordered[ticker_max] = max_score
        del dict_copy[ticker_max]

    dict_final_score = dict_final_score_ordered

    return [dict_final_score,possible_tickers,unusable_tickers]

def raking_sector_buys_value_only_pricetobook(tickers_lst:list,profit_data:dict,value_data:dict,beta_data:dict,momentum_data:dict,investment_data:dict):

    poss_first_filter = []
    possible_tickers = []
    unusable_tickers = []
    profitability_data = []
    valuation_data = []
    beta_numbers = []
    beta_diff_from_zero = []
    momentum_numbers = []
    investment_numbers = []
    dict_final_score = dict()

    for ticker in tickers_lst:

        cond_1 = type(profit_data[ticker]["Profitability_Factor_AbsVal"]) != str
        cond_2 = type(value_data[ticker]["P/B"]) != str
        cond_3 = type(beta_data[ticker]["Beta"]) != str
        cond_4 = type(momentum_data[ticker]["Momentum_Factor"]) != str
        cond_5 = type(investment_data[ticker]["Investment_Factor_AbsVal"]) != str
        combined_cond = cond_1 and cond_2 and cond_3 and cond_4 and cond_5

        if combined_cond:

            poss_first_filter.append(ticker)

        else:

            unusable_tickers.append(ticker)

    for ticker in poss_first_filter:

        profit_factor = profit_data[ticker]["Profitability_Factor_AbsVal"]
        value_factor = value_data[ticker]["P/B"]
        beta_factor = beta_data[ticker]["Beta"]
        momentum_factor = momentum_data[ticker]["Momentum_Factor"]
        investment_factor = investment_data[ticker]["Investment_Factor_AbsVal"]
        profit_factor_exists = ~(np.isnan(profit_factor))
        value_factor_exists = ~(np.isnan(value_factor))
        beta_factor_exists = ~(np.isnan(beta_factor))
        momentum_factor_exists = ~(np.isnan(momentum_factor))
        investment_factor_exists = ~(np.isnan(investment_factor))

        all_factors_exist = profit_factor_exists and value_factor_exists and beta_factor_exists and momentum_factor_exists and investment_factor_exists

        if all_factors_exist:

            possible_tickers.append(ticker)
            profitability_data.append(profit_factor)
            valuation_data.append(value_factor)
            beta_numbers.append(beta_factor)
            beta_diff_from_zero.append(abs(beta_factor) - 0)
            momentum_numbers.append(momentum_factor)
            investment_numbers.append(investment_factor)

        else:

            unusable_tickers.append(ticker)

    #Profit Distribution
    profit_mean = np.mean(profitability_data)
    profit_std = np.std(profitability_data)

    #print("Profit_Mean: ",profit_mean,"And Profit_Std: ",profit_std)

    #Value Distribution
    value_mean = np.mean(valuation_data)
    value_std = np.std(valuation_data)

    #ADJUSTMENT OF THE DISTRIBUTION
    mean_value_adjusted_to_zero = []

    for value in valuation_data:

        new_val = value - value_mean
        mean_value_adjusted_to_zero.append(new_val)

    #print("Value_Mean: ",value_mean,"And Value_Std: ",value_std)

    #Beta Distribution
    beta_mean = np.mean(beta_numbers)
    beta_std = np.std(beta_numbers)

    #ADJUSTMENT OF THE DISTRIBUTION
    beta_difference_from_zero = []

    for beta in beta_numbers:

        if beta == 0 or beta == 0.0:

            beta = 0.001

        beta_difference_from_zero.append(abs(beta))

    beta_diff_mean = np.mean(beta_difference_from_zero)

    beta_diff_adjusted_zero_mean = [] #NEGATIVE VALUES ARE CLOSE TO ZERO, POSITIVE ARE FARTHER FROM ZERO

    for beta_diff in beta_difference_from_zero:

        adjust_mean_zero = beta_diff - beta_diff_mean
        beta_diff_adjusted_zero_mean.append(adjust_mean_zero)

    #print("Beta_Mean: ",beta_mean,"And Beta_Std: ",beta_std)

    #Momentum Distribution
    mom_mean = np.mean(momentum_numbers)
    mom_std = np.std(momentum_numbers)

    #print("Mom_Mean: ",mom_mean,"And Mom_Std: ",mom_std)

    #Investment Distribution
    investment_mean = np.mean(investment_numbers)
    investment_std = np.std(investment_numbers)


    #print("Investment_Mean: ",investment_mean,"And Investment_Std: ",investment_std)

    for ticker in possible_tickers:

        ticker_profit_factor = profit_data[ticker]["Profitability_Factor_AbsVal"]
        ticker_value_factor = value_data[ticker]["P/B"]
        ticker_beta_factor = beta_data[ticker]["Beta"]
        ticker_momentum_factor = momentum_data[ticker]['Momentum_Factor']
        ticker_investment_factor = investment_data[ticker]["Investment_Factor_AbsVal"]

        profit_metric = (profit_data[ticker]["Profitability_Factor_AbsVal"] - profit_mean) / profit_std
        #print(f"{ticker} Profit_Metric_Standardized: ",profit_metric)
        value_metric = (value_data[ticker]["P/B"] - value_mean) / value_std
        #print(f"{ticker} Value_Metric_Standardized: ",value_metric)
        beta_metric = (beta_data[ticker]["Beta"] - beta_mean) / beta_std
        #print(f"{ticker} Beta_Metric_Standardized: ",beta_metric)
        mom_metric = (momentum_data[ticker]['Momentum_Factor'] - mom_mean) / mom_std
        #print(f"{ticker} Momentum_Metric_Standardized: ",mom_metric)
        investment_metric = (investment_data[ticker]["Investment_Factor_AbsVal"] - investment_mean) / investment_std
        #print(f"{ticker} Investment_Metric_Standardized: ",investment_metric)

        #PROFIT_FACTOR MEASUREMENTS

        max_profit_factor = max(profitability_data)
        min_profit_factor = min(profitability_data)
        max_profit = max_profit_factor > 0
        min_profit = min_profit_factor > 0

        if max_profit and min_profit:

            how_profitable = ticker_profit_factor / max_profit_factor

        elif max_profit and min_profit == False :

            if ticker_profit_factor >= 0 :

                how_profitable = ticker_profit_factor / max_profit_factor

            else:

                how_profitable = - (ticker_profit_factor / min_profit_factor)

        else: #max_profit == False and min_profit == False, max_profit == False and min_profit == True doesn't exist

            how_profitable = - (ticker_profit_factor / min_profit_factor)

        #VALUE_FACTOR MEASUREMENTS~

        max_value_factor = max(mean_value_adjusted_to_zero)
        min_value_factor = min(mean_value_adjusted_to_zero)
        max_value = max_value_factor > 0
        min_value = min_value_factor > 0
        idx_ticker_possible_tickers = possible_tickers.index(ticker)
        ticker_value_adjust_factor = mean_value_adjusted_to_zero[idx_ticker_possible_tickers]

        if max_value and min_value == False :

            if ticker_value_adjust_factor >= 0 :

                how_undervalued = - (ticker_value_adjust_factor / max_value_factor) #HIGHER VALUATIONS MEAN SUBTRACTION IN FINAL WEIGHT

            else:

                how_undervalued = ticker_value_adjust_factor / min_value_factor #LOWER VALUATION HAVE MORE WEIGHT IN FINAL SCORE

        #BETA_FACTOR MEASUREMENTS

        max_beta_factor = max(beta_diff_adjusted_zero_mean)
        min_beta_factor = min(beta_diff_adjusted_zero_mean)
        max_beta = max_beta_factor > 0
        min_beta = min_beta_factor > 0
        idx_ticker_possible_tickers = possible_tickers.index(ticker)
        ticker_beta_diff_factor = beta_diff_adjusted_zero_mean[idx_ticker_possible_tickers]


        if max_beta and min_beta:

            how_low_abs_beta =  - (ticker_beta_diff_factor / max_beta_factor) #BETA FURTHER FROM ZERO

        elif max_beta and min_beta == False :

            if ticker_beta_diff_factor >= 0 :

                how_low_abs_beta = - (ticker_beta_diff_factor / max_beta_factor) #BETA FURTHER FROM ZERO

            else:

                how_profitable = ticker_beta_diff_factor / min_beta_factor #BETA CLOSE TO 0.

        else: #max_profit == False and min_profit == False, max_profit == False and min_profit == True doesn't exist

            how_profitable = ticker_beta_diff_factor / min_beta_factor #BETA CLOSE TO 0.

        #MOMENTUM_FACTOR MEASUREMENTS

        max_momentum_factor = max(momentum_numbers)
        min_momentum_factor = min(momentum_numbers)
        max_mom = max_momentum_factor > 0
        min_mom = min_momentum_factor > 0

        if max_mom and min_mom:

            how_healthy_momentum = ticker_momentum_factor / max_momentum_factor

        elif max_mom and min_mom == False :

            if ticker_momentum_factor >= 0 :

                how_healthy_momentum = ticker_momentum_factor / max_momentum_factor

            else:

                how_healthy_momentum = - (ticker_momentum_factor / min_momentum_factor)

        else: #max_mom == False and min_mom == False, max_mom == False and min_mom == True doesn't exist

            how_healthy_momentum = - (ticker_momentum_factor / min_momentum_factor)


        #INVESTMENT_FACTOR MEASUREMENTS, ASSUMES TOTAL ASSETS ARE NEVER NEGATIVE

        max_investment_factor = max(investment_numbers)
        min_investment_factor = min(investment_numbers)
        max_inv = max_investment_factor > 0
        min_inv = min_investment_factor > 0

        if max_inv and min_inv:

            how_invested = - (ticker_investment_factor / max_investment_factor)

        elif max_inv and min_inv == False :

            if ticker_investment_factor >= 0 :

                how_invested = - (ticker_investment_factor / max_investment_factor)

            else:

                how_invested = ticker_investment_factor / min_investment_factor

        else: #max_mom == False and min_mom == False, max_mom == False and min_mom == True doesn't exist

            how_invested = ticker_investment_factor / min_investment_factor

        ticker_score = ((1/5)*(how_profitable + how_undervalued + how_low_abs_beta + how_healthy_momentum + how_invested)).round(decimals = 3)
        #SINCE LOWER VALUE,BETA AND INVESTMENT IS BETTER, ONE TURNS THEM POSITIVE BY PUTTING MINUS
        dict_final_score[ticker] = ticker_score * 100

    dict_copy = dict_final_score.copy()
    dict_final_score_ordered = {}

    while len(dict_copy) != 0:

        list_keys = list(dict_copy.keys())
        list_values = list(dict_copy.values())
        max_score = max(list_values)
        idx_max_score = list_values.index(max_score)
        ticker_max = list_keys[idx_max_score]
        dict_final_score_ordered[ticker_max] = max_score
        del dict_copy[ticker_max]

    dict_final_score = dict_final_score_ordered

    return [dict_final_score,possible_tickers,unusable_tickers]


#%%

"""TICKERS METRICS"""

def yield_ticker_metrics(possible_tickers:list,profit_data:dict,value_data:dict,beta_data:dict,momentum_data:dict,investment_data:dict,final_score:dict,years_used_in_profit_factor_avg:int,years_used_in_investment_factor_avg:int):

    all_tickers_metrics = dict()

    for ticker in possible_tickers:

        all_tickers_metrics[ticker] = dict()

        all_tickers_metrics[ticker]['Final_Score'] = final_score[ticker]
        all_tickers_metrics[ticker][f"Op_Margin_{years_used_in_profit_factor_avg}y_AVG_AbsVal"] = profit_data[ticker][f"Op_Margin_{years_used_in_profit_factor_avg}y_AVG_AbsVal"]
        all_tickers_metrics[ticker]["ROE_Debt_Adjusted_%Val"] = profit_data[ticker]["ROE_Debt_Adjusted_%Val"]
        all_tickers_metrics[ticker]['P/E'] = value_data[ticker]['P/E']
        all_tickers_metrics[ticker]['P/B'] = value_data[ticker]['P/B']
        all_tickers_metrics[ticker][f"Gross_FixAsset_Inc_{years_used_in_investment_factor_avg}y_AVG_AbsVal"] = investment_data[ticker][f"Gross_FixAsset_Inc_{years_used_in_investment_factor_avg}y_AVG_AbsVal"]
        all_tickers_metrics[ticker]['Momentum_Factor'] = momentum_data[ticker]['Momentum_Factor']
        all_tickers_metrics[ticker]['Beta'] = beta_data[ticker]['Beta']

    return all_tickers_metrics


#%%

"""UPDATE OR RETRIEVE TICKERS FACTOR SUCH AS VALUE, BETA OR MOMENTUM"""

def first_fetch_or_storage_on_directory(tickers_lst:list):

    directory_to_park_or_get_from_storage = Path(input("PROVIDE A DIRECTORY TO A/THE FOLDER WHERE STORAGE INTO CSV IS OR WILL OCCUR: ").strip().strip('"').strip("'"))
    values_needed_to_fetch_outside = ['Value','Beta','Momentum']
    value_beta_momentum = str(input(f"WHAT FACTOR ARE YOU SEEKING {values_needed_to_fetch_outside[0]},{values_needed_to_fetch_outside[1]} OR {values_needed_to_fetch_outside[2]} (ANSWER EITHER ONE OF THE FACTORS): "))
    value_beta_momentum = value_beta_momentum.upper()

    while (value_beta_momentum != "VALUE" and value_beta_momentum != "BETA" and value_beta_momentum != "MOMENTUM") == True :

        print("WRONG INPUT, RE-INSERT AN INPUT")
        value_beta_momentum = str(input(f"WHAT FACTOR ARE YOU SEEKING {values_needed_to_fetch_outside[0]},{values_needed_to_fetch_outside[1]} OR {values_needed_to_fetch_outside[2]} (ANSWER EITHER ONE OF THE FACTORS): "))
        value_beta_momentum = value_beta_momentum.upper()

    if value_beta_momentum == "VALUE":

        name = "value_factor"
        fetch_refetch_storage = input(f"DO YOU HAVE {value_beta_momentum} FACTOR STORED IN ANY DIRECTORY (ANSWER 'Yes' OR 'No'): ")
        while fetch_refetch_storage.upper() != 'YES' and fetch_refetch_storage.upper() != 'NO':

            print('INVALID ANSWER, REPEAT THE ANSWER')
            fetch_refetch_storage = input(f"DO YOU HAVE {value_beta_momentum} FACTOR STORED IN ANY DIRECTORY (ANSWER 'Yes' OR 'No'): ")

        if fetch_refetch_storage.upper() == 'NO':

            dict_value_factor = ticker_value_factor(tickers_lst)
            df_value_factor = pd.DataFrame(dict_value_factor.values(),dict_value_factor.keys())
            df_value_factor \
             .to_csv(directory_to_park_or_get_from_storage / f"{name}.csv")
            return dict_value_factor

        else: #ANSWER IS YES

            refetch_or_not = input(f"DO YOU WANT TO REFETCH DATA FOR {value_beta_momentum}, IT TAKES LONG IF LENGTH OF TICKERS LIST IS HIGH AS ALL TICKERS IN THE LIST ARE REVISITED AND FETCH (ANSWER 'Yes' OR 'No'): ")

            while refetch_or_not.upper() != 'YES' and refetch_or_not.upper() != 'NO':

                print('INVALID ANSWER, REPEAT THE ANSWER')
                refetch_or_not = input(f"DO YOU WANT TO REFETCH DATA FOR {value_beta_momentum}, IT TAKES LONG IF LENGTH OF TICKERS LIST IS HIGH AS ALL TICKERS IN THE LIST ARE REVISITED AND FETCH (ANSWER 'Yes' OR 'No'): ")

            if refetch_or_not.upper() == 'YES':

                dict_value_factor = ticker_value_factor(tickers_lst)
                keys_chosen_tickers = dict_value_factor.keys()

                #TAKE OUT THE STORED FILE AND CHECK OUT IF THE TICKER IS THERE, AND IF NOT PUT IT THERE, OTHERWISE JUST UPDATE

                df_value_factor = pd.read_csv(rf"{directory_to_park_or_get_from_storage}/{name}.csv")
                df_value_factor = pd.DataFrame({'P/E': df_value_factor['P/E'].values,'P/B' : df_value_factor['P/B'].values,'AVG_Value_Metrics' : df_value_factor['AVG_Value_Metrics'].values}, index=list(df_value_factor['Unnamed: 0']))
                dict_value = pd.DataFrame.to_dict(df_value_factor)
                dict_similar_to_the_funct = {}
                tickers = dict_value['P/E'].keys()
                for ticker in tickers:

                    dict_similar_to_the_funct[ticker] = dict()
                    for key in dict_value:

                        dict_similar_to_the_funct[ticker][key] = dict_value[key][ticker]

                for key in keys_chosen_tickers:

                    dict_similar_to_the_funct[key] = dict_value_factor[key]

                dict_value = dict_similar_to_the_funct

                #RE-STORE IT UNDER THE SAME DIRECTORY
                df_value_factor = pd.DataFrame(dict_value.values(),dict_value.keys())
                df_value_factor \
                 .to_csv(directory_to_park_or_get_from_storage / f"{name}.csv")
                return dict_value_factor

            else: #NO

                df_value_factor = pd.read_csv(rf"{directory_to_park_or_get_from_storage}/{name}.csv")
                df_value_factor = pd.DataFrame({'P/E': df_value_factor['P/E'].values,'P/B' : df_value_factor['P/B'].values,'AVG_Value_Metrics' : df_value_factor['AVG_Value_Metrics'].values}, index=list(df_value_factor['Unnamed: 0']))
                dict_value = pd.DataFrame.to_dict(df_value_factor)
                dic_value = dict()
                for ticker in dict_value['P/E'].keys():

                    dic_value[ticker] = {}

                    for key in dict_value:

                        value = dict_value[key][ticker]
                        try:
                            float_value = float(value)
                        except ValueError:
                            dic_value[ticker][key] = value
                        else:
                            dic_value[ticker][key] = float_value

                dict_value = dic_value

                return dict_value

    elif value_beta_momentum == "BETA":

        name = "market_factor"
        fetch_refetch_storage = input(f"DO YOU HAVE {value_beta_momentum} FACTOR STORED IN ANY DIRECTORY (ANSWER 'Yes' OR 'No'): ")
        while fetch_refetch_storage.upper() != 'YES' and fetch_refetch_storage.upper() != 'NO':

            print('INVALID ANSWER, REPEAT THE ANSWER')
            fetch_refetch_storage = input(f"DO YOU HAVE {value_beta_momentum} FACTOR STORED IN ANY DIRECTORY (ANSWER 'Yes' OR 'No'): ")

        if fetch_refetch_storage.upper() == 'NO':

            dict_market_factor = ticker_beta(tickers_lst)
            df_market_factor = pd.DataFrame(dict_market_factor.values(),dict_market_factor.keys())
            df_market_factor \
             .to_csv(directory_to_park_or_get_from_storage / f"{name}.csv")
            return dict_market_factor

        else: #ANSWER IS YES

            refetch_or_not = input(f"DO YOU WANT TO REFETCH DATA FOR {value_beta_momentum}, IT TAKES LONG IF LENGTH OF TICKERS LIST IS HIGH AS ALL TICKERS IN THE LIST ARE REVISITED AND FETCH (ANSWER 'Yes' OR 'No'): ")

            while refetch_or_not.upper() != 'YES' and refetch_or_not.upper() != 'NO':

                print('INVALID ANSWER, REPEAT THE ANSWER')
                refetch_or_not = input(f"DO YOU WANT TO REFETCH DATA FOR {value_beta_momentum}, IT TAKES LONG IF LENGTH OF TICKERS LIST IS HIGH AS ALL TICKERS IN THE LIST ARE REVISITED AND FETCH (ANSWER 'Yes' OR 'No'): ")

            if refetch_or_not.upper() == 'YES':

                dict_market_factor = ticker_beta(tickers_lst)
                keys_chosen_tickers = dict_market_factor.keys()

                #TAKE OUT THE STORED FILE AND CHECK OUT IF THE TICKER IS THERE, AND IF NOT PUT IT THERE, OTHERWISE JUST UPDATE
                df_market_factor = pd.read_csv(rf"{directory_to_park_or_get_from_storage}/{name}.csv")
                df_market_factor = pd.DataFrame(data=list(df_market_factor['Beta']),index=list(df_market_factor['Unnamed: 0']))
                dict_beta = pd.DataFrame.to_dict(df_market_factor)
                dict_beta = dict_beta[0]
                dict_similar_to_the_funct = {}
                tickers = dict_beta.keys()
                for ticker in tickers:

                    dict_similar_to_the_funct[ticker] = dict()
                    dict_similar_to_the_funct[ticker]['Beta'] = dict_beta[ticker]

                for key in keys_chosen_tickers:

                    dict_similar_to_the_funct[key] = dict_market_factor[key]

                dict_beta = dict_similar_to_the_funct

                #RE-STORE IT UNDER THE SAME DIRECTORY
                df_market_factor = pd.DataFrame(dict_beta.values(),dict_beta.keys())
                df_market_factor \
                .to_csv(directory_to_park_or_get_from_storage / f"{name}.csv")
                return dict_market_factor

            else: #NO

                df_market_factor = pd.read_csv(rf"{directory_to_park_or_get_from_storage}/{name}.csv")
                df_market_factor = pd.DataFrame(data=list(df_market_factor['Beta']),index=list(df_market_factor['Unnamed: 0']))
                dict_beta = pd.DataFrame.to_dict(df_market_factor)
                dict_beta = dict_beta[0]
                dic_beta = dict()

                for ticker in dict_beta.keys():

                    dic_beta[ticker] = dict()
                    value = dict_beta[ticker]
                    try:
                        float_value = float(value)
                    except ValueError:
                        dic_beta[ticker]['Beta'] = value
                    else:
                        dic_beta[ticker]['Beta'] = float_value

                dict_beta = dic_beta

                dict_beta

                return dict_beta

    else: #value_beta_momentum == "MOMENTUM"

        name = "momentum_factor"
        fetch_refetch_storage = input(f"DO YOU HAVE {value_beta_momentum} FACTOR STORED IN ANY DIRECTORY (ANSWER 'Yes' OR 'No'): ")
        while fetch_refetch_storage.upper() != 'YES' and fetch_refetch_storage.upper() != 'NO':

            print('INVALID ANSWER, REPEAT THE ANSWER')
            fetch_refetch_storage = input(f"DO YOU HAVE {value_beta_momentum} FACTOR STORED IN ANY DIRECTORY (ANSWER 'Yes' OR 'No'): ")

        if fetch_refetch_storage.upper() == 'NO':

            dict_momentum_factor = ticker_momentum(tickers_lst)
            df_momentum_factor = pd.DataFrame(dict_momentum_factor.values(),dict_momentum_factor.keys())
            df_momentum_factor \
             .to_csv(directory_to_park_or_get_from_storage / f"{name}.csv")
            return dict_momentum_factor

        else: #ANSWER IS NO

            refetch_or_not = input(f"DO YOU WANT TO REFETCH DATA FOR {value_beta_momentum}, IT TAKES LONG IF LENGTH OF TICKERS LIST IS HIGH AS ALL TICKERS IN THE LIST ARE REVISITED AND FETCH (ANSWER 'Yes' OR 'No'): ")

            while refetch_or_not.upper() != 'YES' and refetch_or_not.upper() != 'NO':

                print('INVALID ANSWER, REPEAT THE ANSWER')
                refetch_or_not = input(f"DO YOU WANT TO REFETCH DATA FOR {value_beta_momentum}, IT TAKES LONG IF LENGTH OF TICKERS LIST IS HIGH AS ALL TICKERS IN THE LIST ARE REVISITED AND FETCH (ANSWER 'Yes' OR 'No'): ")

            if refetch_or_not.upper() == 'YES':

                dict_momentum_factor = ticker_momentum(tickers_lst)
                keys_chosen_tickers = dict_momentum_factor.keys()

                #TAKE OUT THE STORED FILE AND CHECK OUT IF THE TICKER IS THERE, AND IF NOT PUT IT THERE, OTHERWISE JUST UPDATE
                df_momentum_factor = pd.read_csv(rf"{directory_to_park_or_get_from_storage}/{name}.csv")
                df_momentum_factor = pd.DataFrame(data=list(df_momentum_factor['Momentum_Factor']),index=list(df_momentum_factor['Unnamed: 0']))
                dict_momentum = pd.DataFrame.to_dict(df_momentum_factor)
                dict_momentum = dict_momentum[0]
                dict_similar_to_the_funct = {}
                tickers = dict_momentum.keys()
                for ticker in tickers:

                    dict_similar_to_the_funct[ticker] = dict()
                    dict_similar_to_the_funct[ticker]['Momentum_Factor'] = dict_momentum[ticker]

                for key in keys_chosen_tickers:

                    dict_similar_to_the_funct[key] = dict_momentum_factor[key]

                dict_momentum = dict_similar_to_the_funct

                #RE-STORE IT UNDER THE SAME DIRECTORY
                df_momentum_factor = pd.DataFrame(dict_momentum.values(),dict_momentum.keys())
                df_momentum_factor \
                .to_csv(directory_to_park_or_get_from_storage / f"{name}.csv")
                return dict_momentum_factor

            else: #NO

                df_momentum_factor = pd.read_csv(rf"{directory_to_park_or_get_from_storage}/{name}.csv")
                df_momentum_factor = pd.DataFrame(data=list(df_momentum_factor['Momentum_Factor']),index=list(df_momentum_factor['Unnamed: 0']))
                dict_momentum = pd.DataFrame.to_dict(df_momentum_factor)
                dict_momentum = dict_momentum[0]
                dic_momentum = dict()

                for ticker in dict_momentum.keys():

                    dic_momentum[ticker] = dict()
                    value = dict_momentum[ticker]
                    try:
                        float_value = float(value)
                    except ValueError:
                        dic_momentum[ticker]['Momentum_Factor'] = value
                    else:
                        dic_momentum[ticker]['Momentum_Factor'] = float_value

                dict_momentum = dic_momentum

                return dict_momentum
