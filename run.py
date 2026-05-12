#%%

#USAGE ONLY MAKES SENSE WHENEVER A LARGE NUMBER OF TICKERS IS COMPARED, OTHWERWISE THE ANALYSIS IS NARROWED.
def run_with_finviz_yf():

    data_prov_input = int(input("WHICH DATA PROVIDER YOU WANT TO FETCH FROM, 'finviz' (ANSWER 0) OR 'yfinance' (ANSWER 1): "))

    while data_prov_input != 0 and data_prov_input != 1:

        print("INVALID INPUT, ANSWER 0 FOR 'finviz_usage' OR 1 FOR 'yfinance' USAGE.")
        data_prov_input = int(input("WHICH DATA PROVIDER YOU WANT TO FETCH FROM, 'finviz' (ANSWER 0) OR 'yfinance' (ANSWER 1): "))

    if data_prov_input == 0: #FINVIZ USAGE

        from finviz_us.organize_tickers import organizing_tickers
        from finviz_us.strategies.strat_broad_FV.func_strat_run import run_broad_fv
        from finviz_us.strategies.strat_basic_fama_french.func_run_strat import run_basic_fam_fre

        directory_for_storage_retrieval = organizing_tickers.directory_for_storage_or_retrieval
        dict_all_tickers_all_financials = organizing_tickers.dict_all_financials_three_statements
        most_similar_tickers = organizing_tickers.most_similar_tickers

        print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'fama_french'")
        print("EVERY TIME THE SCRIPT ASK YOU ABOUT A DIRECTORY, YOU WILL ALWAYS PROVIDE THE SAME DIRECTORY")

        strat_fam_french = run_basic_fam_fre(most_similar_tickers,dict_all_tickers_all_financials)

        print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'FV_from_financials'")

        strat_FV_from_financials = run_broad_fv(most_similar_tickers,dict_all_tickers_all_financials,directory_for_storage_retrieval)

        strategies = {
            "fama_french": strat_fam_french,
            "broad_FValue": strat_FV_from_financials
        }

    else: #yfinance USAGE

        from yahoo_finance.organize_tickers import organizing_tickers
        from yahoo_finance.strategies.strat_broad_FV.func_strat_run import run_broad_fv
        from yahoo_finance.strategies.strat_basic_fama_french.func_run_strat import run_basic_fam_fre

        directory_for_storage_retrieval = organizing_tickers.directory_for_storage_or_retrieval
        dict_all_tickers_all_financials = organizing_tickers.dict_all_financials_and_tickers
        most_similar_tickers = organizing_tickers.similar_tickers_lst

        print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'fama_french'")
        print("EVERY TIME THE SCRIPT ASK YOU ABOUT A DIRECTORY, YOU WILL ALWAYS PROVIDE THE SAME DIRECTORY")

        strat_fam_french = run_basic_fam_fre(most_similar_tickers,dict_all_tickers_all_financials)

        print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'FV_from_financials'")

        strat_FV_from_financials = run_broad_fv(most_similar_tickers,dict_all_tickers_all_financials,directory_for_storage_retrieval)

        strategies = {
            "fama_french": strat_fam_french,
            "broad_FValue": strat_FV_from_financials
        }

    return strategies

def strat_choose(dict_strategies:dict):

    from finviz_us.helpers_file_root import helpers_root
    strategy_choosen = helpers_root.choose_strategy(dict_strategies)

    return strategy_choosen

#%%

dict_strats = run_with_finviz_yf()

#%%

#FIND A WAY TO INCORPORATE MKCAP INTO THE PARQUET FILE THAT IS CACHED.

strat_chosen = strat_choose(dict_strats)

#%%

len(strat_chosen['tickers_considered'])

#FROM STRATEGY 'broad_FValue' If Price SCORES IS EMPTY IT MEANS THAT THE TICKERS DIDN'T ACCOMPLISH ALL THE NEEDED PARAMETERS, SOME PARAMETERS ARE LACKING.
#SAME FOR 'fama_french', IF SOME TICKERS ARE NOT THERE IT MEANS SOME DATA MIGHT BE MISSING, OR THE COMPANY DOESN'T FULLFILL SOME SET OF CRITERIA

#%%

from finviz_us.helpers_file_root import helpers_root
from yahoo_finance.organize_tickers import organizing_tickers
from yahoo_finance.strategies.strat_broad_FV.func_strat_run import run_broad_fv
from yahoo_finance.strategies.strat_basic_fama_french.func_run_strat import run_basic_fam_fre

directory_for_storage_retrieval = organizing_tickers.directory_for_storage_or_retrieval
dict_all_tickers_all_financials = organizing_tickers.dict_all_financials_and_tickers
most_similar_tickers = organizing_tickers.similar_tickers_lst

#%%

dict_all_tickers_all_financials['inc_stat']["GALD.SW"]

# %%
dict_all_tickers_all_financials['bal_sheet']["GALD.SW"]

#%%

import pandas as pd
import numpy as np
import datetime
import yfinance as yf

def historical_metric(df_with_metric:pd.DataFrame,**kwargs):

    #KWARGS WILL BE THE STRs WITH THE NAMES OF THE METRICS

    dict_metric = dict()
    for kwarg in kwargs.values():

        dict_metric[kwarg] = dict()

        for fy in range(len(df_with_metric.columns)-1,-1,-1):

            fyear = df_with_metric.columns[fy]
            dict_metric[kwarg][fyear] = df_with_metric.at[kwarg,fyear]

    return dict_metric

def combine_dfs_from_dicts(**kwargs):

    lst_with_lst_of_index = []
    len_list= []
    final_lst = []

    #KWARGS WILL BE DFs WITH DIFFERENT_DFS
    for df in kwargs.values():

        lst_index = []
        for index in df.index:
            lst_index.append(index)

        len_list.append(len(lst_index))
        lst_with_lst_of_index.append(lst_index)

    ind_small_list = len_list.index(min(len_list))
    small_list = lst_with_lst_of_index[ind_small_list]

    for i in range(min(len_list)):

        index_small_list = small_list[i]

        count_belong = 0

        for lst in lst_with_lst_of_index:

            if index_small_list in lst:

                count_belong += 1

        if count_belong == len(lst_with_lst_of_index):

            final_lst.append(index_small_list)

    lst_dfs = []
    for df in kwargs.values():

        lst_dfs.append(df.loc[final_lst,:])

    return pd.concat(lst_dfs,axis=1)


def get_metrics_for_analysis(tickers_lst,dict_bs,dict_inc_stat):

    unusable_tickers = []
    usable_tickers = []
    dict_tickers_dfs = dict()

    for ticker in tickers_lst:

        print(ticker)

        ticker_dict_inc_stat_metrics = historical_metric(dict_inc_stat[ticker],m1 = "EPS (Diluted)", m2 = "Price To Earnings Ratio",m3 = "Total Revenue",m4 = "Operating Income",m5 = "Shares Outstanding (Diluted)")
        ticker_dict_bs_metrics = historical_metric(dict_bs[ticker],m1 = "Cash & Short Term Investments",m2 = "Short Term Debt Incl. Current Port. of LT Debt")

        ticker_df_bs = pd.DataFrame.from_dict(ticker_dict_bs_metrics)
        ticker_df_inc_stat = pd.DataFrame.from_dict(ticker_dict_inc_stat_metrics)

        n_data_types_inc_stat = len(ticker_df_inc_stat['EPS (Diluted)'].apply(type).value_counts())
        n_data_types_bal_sheet = len(ticker_df_bs['Cash & Short Term Investments'].apply(type).value_counts())

        if n_data_types_inc_stat != 1 or n_data_types_bal_sheet != 1: #IT MEANS COMPANY REPORTING DATES CHANGED, SO DROP THE COMPANY

            #IN THE NORMAL STATEMENT, THE SAME YEAR OF FISCAL YEAR HAS 2 COLUMNS WITH THE SAME NAME.

            unusable_tickers.append(ticker)
            print(ticker,"IS UNUSABLE, BECAUSE REPORTING DATES CHANGED")

        else:

            df_variables = combine_dfs_from_dicts(df1 = ticker_df_inc_stat, df2 = ticker_df_bs)

            usable_tickers.append(ticker)

            df_variables["Op.Margin"] = df_variables['Operating Income'] / df_variables['Total Revenue']

            df_variables['Sht_Debt_Coverage_Abs_Val'] = df_variables['Cash & Short Term Investments'] - df_variables['Short Term Debt Incl. Current Port. of LT Debt']

            df_variables = df_variables.loc[:,["EPS (Diluted)","Price To Earnings Ratio","Shares Outstanding (Diluted)","Total Revenue","Operating Income","Op.Margin","Cash & Short Term Investments","Short Term Debt Incl. Current Port. of LT Debt","Sht_Debt_Coverage_Abs_Val"]]

            dict_tickers_dfs[ticker] = df_variables

    print("NºTickers that are available for testing: ",len(usable_tickers))

    return {'dict_tickers_dfs' : dict_tickers_dfs, 'usable_tickers' : usable_tickers , 'unusable_tickers' : unusable_tickers}

def get_price_factor(tickers_lst:list,dict_price:dict,dict_df_metrics_organized:dict,cagr_eps_min:float,cagr_rev_min:float,discount_rate,n_years_forward,pct_shrink_cagr_eps:float,pct_increase_cagr_eps:float,worst_case_weight:float,base_case_weight:float):

    if (base_case_weight < 0 or base_case_weight > 1) or (worst_case_weight < 0 or worst_case_weight > 1)  or (base_case_weight+worst_case_weight < 0 or base_case_weight+worst_case_weight > 1):

        print("INVALID WEIGHTS, THEY NEED TO BE BOTH BETWEEN 0 AND 1 AND ALSO THEIR SUM BETWEEN 0 AND 1 TO COMPUTE 'best_case_weight'")
        while (base_case_weight < 0 or base_case_weight > 1) or (worst_case_weight < 0 or worst_case_weight > 1)  or (base_case_weight+worst_case_weight < 0 or base_case_weight+worst_case_weight > 1):

            print("INVALID WEIGHTS, THEY NEED TO BE BOTH BETWEEN 0 AND 1 AND ALSO THEIR SUM BETWEEN 0 AND 1 TO COMPUTE 'best_case_weight'")
            base_case_weight = float(input("Choose another weight for base_case: "))
            worst_case_weight = float(input("Choose another weight for worst_case: "))

    valuation_dict = dict()
    unusable_tickers = []
    usable_tickers = []

    for ticker in tickers_lst:

        print(ticker)

        df = dict_df_metrics_organized[ticker]
        n_years = len(df) - 1
        df_index = df.index

        #IF INDEX ARE NOT CONSECUTIVE, DROP THE TICKERS, HAVE JUMPS IN THE YEARS:
        years_consecutive = []
        first_year = int(df.index[0].replace('FY',''))
        for i in range(len(df_index)):

            year = first_year + i
            year_to_str = str(year) + str('FY')
            years_consecutive.append(year_to_str)

        lst_true = list(years_consecutive == df_index)

        if lst_true.count(True) == len(df_index):

            current_price = dict_price[ticker]
            last_eps = df.at[df_index[n_years],"EPS (Diluted)"]
            list_eps = list(df["EPS (Diluted)"])
            last_three_years_eps_avg = sum(list_eps[-3:]) / 3


            eps_cagr = ((df.at[df_index[n_years],"EPS (Diluted)"] / df.at[df_index[0],"EPS (Diluted)"]) ** (1/n_years)) - 1
            rev_cagr = ((df.at[df_index[n_years],"Total Revenue"] / df.at[df_index[0],"Total Revenue"]) ** (1/n_years)) - 1
            sh_out_cagr = ((df.at[df_index[n_years],"Shares Outstanding (Diluted)"] / df.at[df_index[0],"Shares Outstanding (Diluted)"]) ** (1/n_years)) - 1
            op_margin_cagr = ((df.at[df_index[n_years],"Op.Margin"] / df.at[df_index[0],"Op.Margin"]) ** (1/n_years)) - 1
            past_years_debt_coverage_approval = False
            all_years_debt_coverage_approval = False
            years_debt_approval_most_recent_3 = 0
            years_of_debt_approval = 0
            n_years_positive_eps = 0
            for year in range(len(df)):

                sht_debt_year = df.at[df_index[year],"Short Term Debt Incl. Current Port. of LT Debt"]
                debt_coverage_year = df.at[df_index[year],"Sht_Debt_Coverage_Abs_Val"]
                if debt_coverage_year >= sht_debt_year:
                    years_of_debt_approval +=1

                eps_year = df.at[df_index[year],"EPS (Diluted)"]
                if eps_year > 0:
                    n_years_positive_eps += 1

                if year >= len(df)-3:

                    sht_debt_year = df.at[df_index[year],"Short Term Debt Incl. Current Port. of LT Debt"]
                    debt_coverage_year = df.at[df_index[year],"Sht_Debt_Coverage_Abs_Val"]
                    if debt_coverage_year >= sht_debt_year*1.5:
                        years_debt_approval_most_recent_3 +=1

            past_years_debt_coverage_approval = True if years_debt_approval_most_recent_3 == 3 else False #GOOD DEBT LAST 3 YEARS
            all_years_debt_coverage_approval = True if years_of_debt_approval == len(df)-1 else False

            cond_eps_cagr = eps_cagr > cagr_eps_min
            cond_rev_cagr = rev_cagr > cagr_rev_min
            cond_sh_out = eps_cagr > sh_out_cagr
            cond_op_margin = op_margin_cagr > 0
            cond_years_public = n_years > 5
            last_eps_positive = last_eps > 0

            combined_conds = cond_eps_cagr and last_eps_positive and cond_rev_cagr and cond_sh_out and cond_op_margin and past_years_debt_coverage_approval and all_years_debt_coverage_approval and cond_years_public

            if combined_conds:

                usable_tickers.append(ticker)
                if n_years_positive_eps < n_years:

                    negative_values = df["EPS (Diluted)"].where(df["EPS (Diluted)"] < 0).sum()
                    total_sum = df["EPS (Diluted)"].sum()
                    pct_neg = negative_values / total_sum
                    df["Price To Earnings Ratio"] = df["Price To Earnings Ratio"] * (1+pct_neg)


                worst_case_cagr = eps_cagr*(1-pct_shrink_cagr_eps)
                base_case_cagr = eps_cagr*(1-(pct_shrink_cagr_eps*0.8))
                best_case_cagr = eps_cagr*(1+pct_increase_cagr_eps)

                pe_possible_values = df["Price To Earnings Ratio"].where(df["Price To Earnings Ratio"] > 0)

                pe_3_worst_values = pe_possible_values.sort_values(ascending=True)[0:3]
                pe_average_period = pe_possible_values.mean()
                pe_past_3_values = pe_possible_values[-3:].mean()

                worst_case_terminal_pe = pe_3_worst_values.mean() #Lowest 3 values from the period
                base_case_terminal_pe = min(pe_average_period,pe_past_3_values)
                best_case_terminal_pe = max(pe_average_period,pe_past_3_values)

                #INSTEAD OF last_eps YOU CAN TRY last_three_years_eps_avg

                """
                worst_case_share_p = last_three_years_eps_avg * ((1+worst_case_cagr) / (1+discount_rate))**n_years_forward * worst_case_terminal_pe
                base_case_share_p = last_three_years_eps_avg * ((1+base_case_cagr) / (1+discount_rate))**n_years_forward * base_case_terminal_pe
                best_case_share_p = last_three_years_eps_avg * ((1+best_case_cagr) / (1+discount_rate))**n_years_forward * best_case_terminal_pe
                """

                worst_case_share_p = last_eps * ((1+worst_case_cagr) / (1+discount_rate))**n_years_forward * worst_case_terminal_pe
                base_case_share_p = last_eps * ((1+base_case_cagr) / (1+discount_rate))**n_years_forward * base_case_terminal_pe
                best_case_share_p = last_eps * ((1+best_case_cagr) / (1+discount_rate))**n_years_forward * best_case_terminal_pe

                best_case_weight = 1 - base_case_weight - worst_case_weight

                fv_share_p = worst_case_weight * worst_case_share_p + base_case_weight * base_case_share_p + best_case_share_p * best_case_weight
                price_factor = np.float64(fv_share_p / current_price).round(decimals = 2)

                valuation_dict[ticker] = dict()
                valuation_dict[ticker]['Price_Factor'] = price_factor
                valuation_dict[ticker]['Fair_Value_Price'] = fv_share_p.round(decimals=3)
                valuation_dict[ticker]['Current_Price'] = current_price
                valuation_dict[ticker]['Under(+)/Over(-)_Valuation'] = f"{(price_factor-1)*100}% Undervalued" if price_factor > 1 else f"{(price_factor-1)*100}% Overvalued"

            else:

                unusable_tickers.append(ticker)

        else:

            if ticker not in unusable_tickers:

                unusable_tickers.append(ticker)

    #ORDER VALUATION_DICT IN A WAY WHERE MOST UNDERVALUED STOCKS APPEAR FIRST
    dict_price_factor = dict()

    for key in valuation_dict:

        dict_price_factor[key] = valuation_dict[key]['Price_Factor']

    lst_order_keys = list(order_dict_asc_des(dict_price_factor).keys())

    ordered_valuation_dict = dict()

    for key in lst_order_keys:

        ordered_valuation_dict[key] = valuation_dict[key]

    return {'ticker_price_factor' : ordered_valuation_dict,'usable_tickers' : usable_tickers, 'unusable_tickers' : unusable_tickers}

def order_dict_asc_des(dic:dict,order = 'des'):

    if order == 'asc':

        dic = dict(sorted(dic.items(), key=lambda item: item[0])) #ascending

    else:

        dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True)) #descending

    return dic

def choose_mkt_storage_prices(tickers_lst:list,directory_where_prices_are_stored):

    name = "prices"
    stored_prices_exist = input("IS THERE ANY CSV WITH STORAGE OF THE PRICES (ANSWER 'Yes' OR 'No'): ")

    while stored_prices_exist.upper() != "YES" and stored_prices_exist.upper() != "NO":

        print("INVALID INPUT,CHOOSE USE 'Yes' OR 'No'")
        stored_prices_exist = input("IS THERE ANY CSV WITH STORAGE OF THE PRICES (ANSWER 'Yes' OR 'No'): ")

    if stored_prices_exist.upper() == "YES":

        refetch_or_stored = input("DO YOU WANT TO RE-FETCH THE PRICES OF THE TICKERS IN YOUR LIST, MIND IF LIST IS TO LONG IT WILL TAKE LONGER (ANSWER 'Yes' OR 'No'): ")

        while refetch_or_stored.upper() != "YES" and refetch_or_stored.upper() != "NO":

            print("INVALID INPUT,CHOOSE USE 'Yes' OR 'No'")
            refetch_or_stored = input("DO YOU WANT TO RE-FETCH THE PRICES OF THE TICKERS IN YOUR LIST, MIND IF LIST IS TO LONG IT WILL TAKE LONGER (ANSWER 'Yes' OR 'No'): ")

        if refetch_or_stored.upper() == "YES":

            #GET TICKERS RE-FETCHED
            dict_price = get_tickers_market_prices(tickers_lst)

            #IMPORT CSV STORED AND UPDATED THAT LIST WITH THOSE TICKERS
            stored_dict_price = get_stored_ticker_prices(directory_where_prices_are_stored)

            for key in dict_price.keys():

                stored_dict_price[key] = dict_price[key]

            df_dict_prices = pd.DataFrame(stored_dict_price.values(),stored_dict_price.keys())
            df_dict_prices \
                .to_csv(rf"{directory_where_prices_are_stored}\{name}.csv")

            return dict_price

        else: #refetch_or_stored.upper() == "NO"

            #IMPORT CSV STORED
            stored_dict_price = get_stored_ticker_prices(directory_where_prices_are_stored)

            #GET TICKERS_PRICES
            dict_price = {}

            end_date = datetime.date.today()
            start_date = datetime.date.today() - pd.Timedelta(days=3)
            tickers_price_df = yf.download(tickers=tickers_lst,start=start_date,end=end_date,interval='1d')

            for ticker in tickers_lst:

                if ticker not in stored_dict_price.keys():

                    dict_price[ticker] = tickers_price_df.at[tickers_price_df.index[len(tickers_price_df) - 1],('Close',ticker)]

                else:

                    dict_price[ticker] = stored_dict_price[ticker]

            return dict_price

    else: #stored_prices_exist.upper() == "NO"

        dict_price = get_tickers_market_prices(tickers_lst)

        #PUT DICT_PRICE INTO CSV
        df_dict_prices = pd.DataFrame(dict_price.values(),dict_price.keys())
        df_dict_prices \
            .to_csv(rf"{directory_where_prices_are_stored}\{name}.csv")

        return dict_price

def get_stored_ticker_prices(directory_for_prices):

    df_prices = pd.read_csv(rf"{directory_for_prices}/prices.csv")
    df_prices = pd.DataFrame(data=list(df_prices['0']),index=list(df_prices['Unnamed: 0']))
    dict_price = pd.DataFrame.to_dict(df_prices)
    dict_price = dict_price[0]
    return dict_price
# %%

dict_metrics = get_metrics_for_analysis(list(dict_all_tickers_all_financials['bal_sheet'].keys()),dict_all_tickers_all_financials['bal_sheet'],dict_all_tickers_all_financials['inc_stat'])

#%%

dict_metrics

# %%
dict_metrics['dict_tickers_dfs']['EDP.LS']

# %%

dict_price_fact = get_price_factor(
    tickers_lst = list(dict_all_tickers_all_financials['bal_sheet'].keys()),
    dict_price = choose_mkt_storage_prices(list(dict_all_tickers_all_financials['bal_sheet'].keys()),directory_for_storage_retrieval),
    dict_df_metrics_organized = dict_metrics['dict_tickers_dfs'],
    cagr_eps_min = 0.02,
    cagr_rev_min = 0.02,
    discount_rate = 0.15,
    n_years_forward = 5,
    pct_shrink_cagr_eps = 0.7,
    pct_increase_cagr_eps = 0.05,
    worst_case_weight = 0.7,
    base_case_weight = 0.25
)



# %%

dict_price_fact

#%%

import pandas as pd
import numpy as np
import yfinance as yf
import time
from pathlib import Path
import math
import datetime


directory_for_storage_retrieval = organizing_tickers.directory_for_storage_or_retrieval
dict_all_tickers_all_financials = organizing_tickers.dict_all_financials_and_tickers
most_similar_tickers = organizing_tickers.similar_tickers_lst

def ticker_profitability_factor(tickers,dict_financials): #FACTOR CONSIDERS RATIOS, SO CURRENCY OF THE STOCK DOESN'T MAKE ANY DIFFERENCE

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

    while n_years_lookback_to_compute_average < 1 or n_years_lookback_to_compute_average > 4 :

        print("NUMBER BETWEEN 1 AND 4")
        n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    for ticker in possible_tickers:

        dict_profitability[ticker] = dict()

        #OPERATING MARGIN CALCULATION
        ticker_inc_stat = inc_stat_dict[ticker].copy()
        ticker_inc_stat = ticker_inc_stat.replace(",","",regex=True)
        record_revenues = pd.to_numeric(ticker_inc_stat.loc['Total Revenue'][1:n_years_lookback_to_compute_average+1])
        record_ebit = pd.to_numeric(ticker_inc_stat.loc['Operating Income'][1:n_years_lookback_to_compute_average+1])

        operating_margin_avg = (record_ebit/record_revenues).mean().__round__(2)
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

def ticker_value_factor(tickers,dict_financials): #ALSO RATIOS, SO CURRENCY OF THE STOCK DOESN'T MAKE ANY DIFFERENCE

    dict_value = dict()
    bal_sheet_dict = dict_financials['bal_sheet']
    inc_stat_dict = dict_financials['inc_stat']

    for ticker in tickers:

        dict_value[ticker] = dict()
        ticker_df_bal_sheet = bal_sheet_dict[ticker]
        ticker_df_columns_bal_sheet = ticker_df_bal_sheet.columns
        ticker_df_inc_stat = inc_stat_dict[ticker]
        ticker_df_columns_inc_stat = ticker_df_inc_stat.columns
        price_earnings = ticker_df_inc_stat.at["Price To Earnings Ratio",ticker_df_columns_inc_stat[0]]
        price_book = ticker_df_bal_sheet.at["Price to Book Ratio",ticker_df_columns_bal_sheet[0]]

        if np.isnan(price_earnings):

            try:

                pe = yf.Ticker(ticker).info["trailingPE"]

            except KeyError:

                print("yfinance ALSO DOESN'T HAVE PE RATIO FOR TICKER",ticker)
                dict_value[ticker]['P/E'] = "No Earnings"

            else:

                print("yfinance HAS P/E RATIO FOR TICKER",ticker, "OF",pe)
                dict_value[ticker]['P/E'] = float(pe).__round__(2)
                ticker_df_inc_stat.at["Price To Earnings Ratio",ticker_df_columns_inc_stat[0]] = dict_value[ticker]['P/E']
                inc_stat_dict[ticker] = ticker_df_inc_stat

        else:

            dict_value[ticker]['P/E'] = float(price_earnings)

        if np.isnan(price_book):

            try:

                pb = yf.Ticker(ticker).info["priceToBook"] #"CHECK ON THE INFO WHAT IS THE KEY FOR PB"

            except KeyError:

                print("yfinance ALSO DOESN'T HAVE PRICE TO BOOK RATIO FOR TICKER",ticker)
                dict_value[ticker]['P/B'] = "No Value"

            else:

                print("yfinance HAS P/B RATIO FOR TICKER",ticker, "OF",pb)
                dict_value[ticker]['P/B'] = float(pb).__round__(2)
                ticker_df_bal_sheet.at["Price to Book Ratio",ticker_df_columns_bal_sheet[0]] = dict_value[ticker]['P/B']
                bal_sheet_dict[ticker] = ticker_df_bal_sheet

        else:

            dict_value[ticker]['P/B'] = float(price_book)

        if type(dict_value[ticker]['P/B']) == float and type(dict_value[ticker]['P/E']) == float:

            dict_value[ticker]['AVG_Value_Metrics'] = ((0.75*dict_value[ticker]['P/E'] + 0.25*dict_value[ticker]['P/B'])).__round__(2)

        else:

            dict_value[ticker]['AVG_Value_Metrics'] = "Not Available, Either Current Equity or Earnings are Negative or No Values"

    return dict_value

def ticker_beta(tickers): #BETA SO CURRENCY OF THE STOCK ALSO DOESN'T MAKE ANY DIFFERENCE

    dict_beta = dict()

    for ticker in tickers:

        dict_beta[ticker] = dict()

        try:

            beta = yf.Ticker(ticker).info["beta"]

        except KeyError:

            beta = f"{ticker} DOESN'T HAVE A BETA VALUE IN yfinance"
            dict_beta[ticker]['Beta'] = beta
            print("yfinance DOESN'T HAVE THE BETA OF TICKER",ticker)

        else:

            dict_beta[ticker]['Beta'] = beta
            print("BETA OF",ticker,"IS",beta)

    return dict_beta

def dates_of_reporting_comparable(dict_inc_stat_tickers:dict,new_tickers:list):

    dict_comparable_reporting_dates = dict()

    for ticker in new_tickers:

        ticker_reporting_dates = dict_inc_stat_tickers[ticker].columns
        n_cols_ticker = len(ticker_reporting_dates)
        if len(dict_comparable_reporting_dates) == 0:

            dict_comparable_reporting_dates["comp_report_dates_0"] = list()
            dict_comparable_reporting_dates["comp_report_dates_0"].append(ticker)

        else:

            list_of_keys = list(dict_comparable_reporting_dates.keys())
            number_of_dict_keys = len(list_of_keys)
            keys_follow = 0

            while keys_follow < number_of_dict_keys:

                first_ticker_of_each_comparable = dict_comparable_reporting_dates[list_of_keys[keys_follow]][0]
                cols_of_that_ticker = dict_inc_stat_tickers[first_ticker_of_each_comparable].columns
                n_of_cols = len(cols_of_that_ticker)
                min_cols = min(n_cols_ticker,n_of_cols)
                if n_of_cols != n_cols_ticker:

                    ticker_reporting_dates_update = dict_inc_stat_tickers[ticker].columns[0:min_cols]
                    cols_of_that_ticker_update = dict_inc_stat_tickers[first_ticker_of_each_comparable].columns[0:min_cols]

                else:

                    ticker_reporting_dates_update = ticker_reporting_dates
                    cols_of_that_ticker_update = cols_of_that_ticker

                list_true_cols = list(ticker_reporting_dates_update == cols_of_that_ticker_update)
                numb_of_equal_rep_dates = list_true_cols.count(True)

                if min_cols == numb_of_equal_rep_dates:

                    dict_comparable_reporting_dates[list_of_keys[keys_follow]].append(ticker)
                    break

                else:

                    keys_follow += 1

            if keys_follow == number_of_dict_keys:

                dict_comparable_reporting_dates[f"comp_report_dates_{keys_follow}"] = list()
                dict_comparable_reporting_dates[f"comp_report_dates_{keys_follow}"].append(ticker)

    for key in dict_comparable_reporting_dates:

        #ENSURE THE TICKER WITH HIGHEST NºCOLS IS AT BEGGINING, IMPORTANT FOR NEXT USAGE
        n_cols_per_ticker = []

        for ticker in dict_comparable_reporting_dates[key]:

            n_cols_per_ticker.append(len(dict_inc_stat_tickers[ticker].columns))
            max_cols = max(n_cols_per_ticker)
            if len(dict_inc_stat_tickers[ticker].columns) == max_cols:

                if len(n_cols_per_ticker) > 0:

                    current_idx = len(n_cols_per_ticker) - 1
                    ticker_in_beg = dict_comparable_reporting_dates[key][0]
                    dict_comparable_reporting_dates[key][0] = ticker
                    dict_comparable_reporting_dates[key][current_idx] = ticker_in_beg

    return dict_comparable_reporting_dates

def ticker_momentum(dict_inc_stat_tickers:dict,tickers:list): #ONLY CONSIDERS PRICING PERFORMANCE, ALSO CURRENCY OF THE STOCK DOESN'T MAKE ANY DIFFERENCE, IT WILL BE A RATIO.

    #THE IDEA OF THE FUNCTION IS TO GET AN AVERAGE OF THE PRICES NEAR REPORTING TO CALCULATE RATIOS THAT NEED PRICES
    dict_comparable_reporting = dates_of_reporting_comparable(dict_inc_stat_tickers,tickers)
    lst_different_comparables = [dict_comparable_reporting[key] for key in dict_comparable_reporting]
    dict_momentum = dict()

    for lst in lst_different_comparables:

        current_month = datetime.date.today().month
        previous_month = current_month - 1 if current_month != 1 else 12
        year_for_date = datetime.date.today().year if current_month != 1 else datetime.date.today().year - 1

        end_date = datetime.date(year_for_date,previous_month,1)
        start_date = datetime.date(year_for_date-1,previous_month,1)

        #PRICING DOWNLOAD
        try:

            comp_tickers_df = yf.download(tickers=lst,start=start_date,end=end_date,interval='1d')

        except IndexError:

            print(rf"THIS/THESE {lst} TICKERS DON'T HAVE PRICING HISTORY")
            for ticker in lst:

                dict_momentum[ticker] = dict()
                dict_momentum[ticker]['Momentum_Factor'] = f"NON-EXISTENT,{ticker} DOESN'T HAVE PRICING HISTORY TO COMPUTE MOMENTUM"

        else:

            if len(comp_tickers_df) == 0:

                for ticker in lst:

                    dict_momentum[ticker] = dict()
                    dict_momentum[ticker]['Momentum_Factor'] = f"NON-EXISTENT,{ticker} DOESN'T HAVE PRICING HISTORY TO COMPUTE MOMENTUM"
                    print(rf"TICKER {ticker} DON'T HAVE PRICING HISTORY FOR MOMENTUM FACTOR")

            else:

                com_tickers_df_idx = comp_tickers_df.index

                for ticker in lst:

                    dict_momentum[ticker] = dict()
                    past_year_performance = (comp_tickers_df.at[com_tickers_df_idx[len(comp_tickers_df)-1],("Close",ticker)] / comp_tickers_df.at[com_tickers_df_idx[0],("Close",ticker)])-1
                    day_of_last_idx = com_tickers_df_idx[len(comp_tickers_df)-1].day
                    idx_of_end_past_month = len(comp_tickers_df)-1 if day_of_last_idx >= 20 else len(comp_tickers_df)-2
                    idx_of_start_past_month = len(comp_tickers_df) - 19 if day_of_last_idx >= 20 else len(comp_tickers_df) - 20
                    past_month_performance = (comp_tickers_df.at[com_tickers_df_idx[idx_of_end_past_month],("Close",ticker)] / comp_tickers_df.at[com_tickers_df_idx[idx_of_start_past_month],("Close",ticker)])-1

                    if np.isnan(past_year_performance) or np.isnan(past_month_performance):

                        dict_momentum[ticker]['Momentum_Factor'] = f"NON-EXISTENT,{ticker} DOESN'T HAVE PRICING HISTORY TO COMPUTE MOMENTUM"
                        print(rf"TICKER {ticker} DON'T HAVE PRICING HISTORY FOR MOMENTUM FACTOR")

                    else:

                        momentum_factor = ((1+past_year_performance)/(1+past_month_performance)) - 1
                        dict_momentum[ticker]['Momentum_Factor'] = momentum_factor
                        print(rf"TICKER {ticker} MOMENTUM FACTOR IS {momentum_factor}")

    return dict_momentum

def ticker_investment_factor(tickers,dict_financials): #ALSO CURRENCY OF THE STOCK DOESN'T MAKE ANY DIFFERENCE IN FINAL ASSESSMENT, IT IS ALSO A RATIO

    stat_cfs_dict = dict_financials['stat_cfs']
    bs_dict = dict_financials['bal_sheet']
    dict_investment = dict()

    #get Operating Income of Past 5y and average
        #Needs Income Statement to get Revenues and Operating Income
    n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    while n_years_lookback_to_compute_average < 1 or n_years_lookback_to_compute_average > 4 :

        print("NUMBER BETWEEN 1 AND 3")
        n_years_lookback_to_compute_average = int(input('NUMBER OF YEARS TO CONSIDER FOR AVERAGES: '))

    for ticker in tickers:

        dict_investment[ticker] = dict()

        #GROSS FIXED ASSET INCREASE
        ticker_stat_cfs = stat_cfs_dict[ticker].copy()
        ticker_stat_cfs = ticker_stat_cfs.replace(",","",regex=True)
        record_capex = pd.to_numeric(ticker_stat_cfs.loc['Capital Expenditures'][1:n_years_lookback_to_compute_average+1])
        record_assets_from_acquistions = pd.to_numeric(ticker_stat_cfs.loc['Net Assets from Acquisitions'][1:n_years_lookback_to_compute_average+1])
        record_assets_sales = pd.to_numeric(ticker_stat_cfs.loc['Sale of Fixed Assets and Businesses'][1:n_years_lookback_to_compute_average+1])
        gross_fixed_asset_increase = (-(record_capex+record_assets_from_acquistions-record_assets_sales)).mean().__round__(3)
        dict_investment[ticker][f"Gross_FixAsset_Inc_{n_years_lookback_to_compute_average}y_AVG_AbsVal"] = gross_fixed_asset_increase

        #TOTAL ASSETS
        ticker_bs = bs_dict[ticker].copy()
        ticker_bs = ticker_bs.replace(",","",regex=True)
        record_total_assets = pd.to_numeric(ticker_bs.loc['Total Assets'][0:n_years_lookback_to_compute_average])

        total_assets_average = (record_total_assets).mean().round(decimals=3)
        dict_investment[ticker][f"Total_Assets_{n_years_lookback_to_compute_average}y_AVG"] = total_assets_average

        dict_investment[ticker]["Investment_Factor_AbsVal"] = (dict_investment[ticker][f"Gross_FixAsset_Inc_{n_years_lookback_to_compute_average}y_AVG_AbsVal"] / dict_investment[ticker][f"Total_Assets_{n_years_lookback_to_compute_average}y_AVG"]).round(decimals = 3)

        dict_investment[ticker]["Investment_Factor_AbsVal"] = "No Value" if np.isnan(dict_investment[ticker]["Investment_Factor_AbsVal"]) else dict_investment[ticker]["Investment_Factor_AbsVal"]

    return dict_investment

def first_fetch_or_storage_on_directory(tickers_lst:list,dict_all_three_statements:dict):

    dict_inc_stat_tickers = dict_all_three_statements['inc_stat']
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

            dict_value_factor = ticker_value_factor(tickers_lst,dict_all_three_statements)
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

                dict_value_factor = ticker_value_factor(tickers_lst,dict_all_three_statements)
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

            dict_momentum_factor = ticker_momentum(dict_inc_stat_tickers,tickers_lst)
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

                dict_momentum_factor = ticker_momentum(dict_inc_stat_tickers,tickers_lst)
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
        cond_2 = type(value_data[ticker]["AVG_Value_Metrics"]) != str and value_data[ticker]["AVG_Value_Metrics"] != float('-inf') and value_data[ticker]["AVG_Value_Metrics"] != float('inf')
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
        cond_2 = type(value_data[ticker]["AVG_Value_Metrics"]) != str and value_data[ticker]["AVG_Value_Metrics"] != float('-inf') and value_data[ticker]["AVG_Value_Metrics"] != float('inf')
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

        if max_profit and min_profit: #ALL COMPANIES INCLUDED ARE PROFITABLE

            how_profitable = ticker_profit_factor / max_profit_factor

        elif max_profit and min_profit == False : #SOME COMPANIES ARE PROFITABLE OTHERS ARE NOT

            if ticker_profit_factor >= 0 : #COMPANY IN QUESTION IS PROFITABLE

                how_profitable = ticker_profit_factor / max_profit_factor

            else: # COMPANY IN QUESTION IS NOT PROFITABLE, SO MINUS IS THERE TO KEEP UNPROFITABILITY

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

        if max_value and min_value: #I DON'T THINK IT IS POSSIBLE, BUT IF HIGH IT MEANS BY VALUE IT IS OVERVALUED

            how_undervalued =  - (ticker_value_adjust_factor / max_value_factor) #P/B AND P/E TENDS TO BE HIGHER

        elif max_value and min_value == False : #TECHNICALLY THIS SHOULD WILL ALWAYS BE THE CASE BECAUSE MEAN ADJUSTED TO ZERO VALUES ASSUME SOME VALUES WILL BE HIGHER THAN ZERO AND OTHERS LOWER

            if ticker_value_adjust_factor >= 0 :

                how_undervalued = - (ticker_value_adjust_factor / max_value_factor ) #P/B AND P/E TENDS TO BE HIGHER

            else:

                how_undervalued = ticker_value_adjust_factor / min_value_factor #P/B AND P/E TENDS TO BE LOWER

        else: #max_value == False and min_value == False, max_value == False and min_value == True doesn't exist

            how_undervalued = ticker_value_adjust_factor / min_value_factor #BETA CLOSE TO 0.

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

                how_low_abs_beta = ticker_beta_diff_factor / min_beta_factor #BETA CLOSE TO 0.

        else: #max_profit == False and min_profit == False, max_profit == False and min_profit == True doesn't exist

            how_low_abs_beta = ticker_beta_diff_factor / min_beta_factor #BETA CLOSE TO 0.

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

        ticker_score = ((1/5)*(how_profitable + how_undervalued + how_low_abs_beta + how_healthy_momentum + how_invested)).__round__(3)
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

dict_profit = ticker_profitability_factor(most_similar_tickers,dict_all_tickers_all_financials)[0]

#%%

dict_value_factor = first_fetch_or_storage_on_directory(most_similar_tickers,dict_all_tickers_all_financials)

#%%

dict_beta_factor = first_fetch_or_storage_on_directory(most_similar_tickers,dict_all_tickers_all_financials)

#%%

dict_momentum_factor = first_fetch_or_storage_on_directory(most_similar_tickers,dict_all_tickers_all_financials)

#%%

dict_investment = ticker_investment_factor(most_similar_tickers,dict_all_tickers_all_financials)

#%%

dict_profit[0].keys()

#%%

dict_value_factor

#%%

dict_value_factor['DTG.DE']['P/B'] * dict_value_factor['DTG.DE']['P/E']

dict_value_factor['DTG.DE']["AVG_Value_Metrics"]

#%%

type(dict_beta_factor['LTMC.MI']['Beta'])

#%%

type(dict_momentum_factor['AI.PA']['Momentum_Factor'])

#%%

dict_investment

#%%

dict_buying_attractiveness_standardized = standardized_raking_sector_buys(most_similar_tickers,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment)

dict_scores_standardized = dict_buying_attractiveness_standardized[0]

dict_buying_attractiveness = raking_sector_buys(most_similar_tickers,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment)

dict_scores = dict_buying_attractiveness[0]
tickers_considered = dict_buying_attractiveness[1]

#%%

dict_scores

# %%

dict_scores_standardized

# %%

