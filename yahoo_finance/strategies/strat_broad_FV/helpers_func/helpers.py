#%%

import pandas as pd
import numpy as np
import time
import datetime
import yfinance as yf

#%%

"""THIS STRATEGY USES ONLY COMPANIES OWN METRICS MEANING THAT
   FINAL OUTCOME OF UNDERVALUED OR OVERVALUED DOESN'T LOSE MEANING
   IF THE CURRENCY OF THE STOCK IS DIFFERENT BECAUSE TURNING THE REAL PRICE
   AND FV PRICE TO THE CURRENCY THAT ONE WANTS MULTIPLIES EACH OF THEM BY THE
   SAME RATE
"""

#%%

"""ORDER DICT"""

def order_dict_asc_des(dic:dict,order = 'des'):

    if order == 'asc':

        dic = dict(sorted(dic.items(), key=lambda item: item[0])) #ascending

    else:

        dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True)) #descending

    return dic

#%%

"""FUNCTIONS USED TO GET METRICS FOR ANALYSIS"""

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

#%%

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
#%%

"""GET MARKET PRICES FROM yfinance"""

def get_tickers_market_prices(tickers_lst:list):

    dict_price = dict()

    end_date = datetime.date.today()
    start_date = datetime.date.today() - pd.Timedelta(days=3)
    tickers_price_df = yf.download(tickers=tickers_lst,start=start_date,end=end_date,interval='1d')

    for ticker in tickers_lst:

        dict_price[ticker] = tickers_price_df.at[tickers_price_df.index[len(tickers_price_df) - 1],('Close',ticker)]
        print("PRICE OFF",ticker,dict_price[ticker])

    return dict_price

"""GET MARKET PRICES FROM STORED TICKERS"""

def get_stored_ticker_prices(directory_for_prices):

    df_prices = pd.read_csv(rf"{directory_for_prices}/prices.csv")
    df_prices = pd.DataFrame(data=list(df_prices['0']),index=list(df_prices['Unnamed: 0']))
    dict_price = pd.DataFrame.to_dict(df_prices)
    dict_price = dict_price[0]
    return dict_price


"""GET MARKET PRICES OR STORED PRICES"""

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

#%%

"""FILTER BY MRKT CAP"""

def filter_by_min_mkcap(tickers_lst:list,dict_tickers_inc_stat:dict):

    updated_ticker_list = list()

    print("VALUES ARE IN MILLIONS")

    minimum_mkcap = float(input('Minimum MkCap to consider companies: '))

    for ticker in tickers_lst:

        #GET MARKET CAP
        ticker_inc_stat_df = dict_tickers_inc_stat[ticker].copy()
        recent_mk_cap = ticker_inc_stat_df.loc['Market Capitalization',ticker_inc_stat_df.columns[0]]

        if recent_mk_cap > minimum_mkcap :

            updated_ticker_list.append(ticker)

    return updated_ticker_list


