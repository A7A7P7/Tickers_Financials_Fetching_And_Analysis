#%%
from finviz_us.organize_tickers import organizing_tickers
#%%

"""IT WILL ASK YOU FOR THE NUMBER OF THE INDEXES, TO GET THE MAXIMUM OF THE TICKERS, YOU WILL:

    WHENEVER ASKED FOR THE NUMBER OF THE INDEX, BY ORDER, ANSWER 1,2,3,4 AND THEN:
    IT WILL TELL YOU WHICH MARKET INDEX YOU ARE ASSESSING, SO YOU EITHER STATE:
    "Yes" - TO CONFIRM
    "No" - TO REPEAT THE PROCEDURE IF SOMETHING FAILS
"""

directory_for_storage = organizing_tickers.directory_for_storage_or_retrieval

#DICT WITH ALL TICKERS ALL FINANCIALS
dict_all_tickers_all_financials = organizing_tickers.dict_all_financials_three_statements

#TICKERS FOR USAGE
similar_tickers = organizing_tickers.most_similar_tickers

#%%

dict_price = helpers.choose_mkt_storage_prices(similar_tickers,directory_for_storage)

#%%

#FILTER BY MARKET CAP
similar_tickers = helpers.filter_by_min_mkcap(similar_tickers,dict_all_tickers_all_financials['inc_stat'])

# %%

dict_tickers_variables_and_usable_tickers = helpers.get_metrics_for_analysis(similar_tickers,dict_all_tickers_all_financials['bal_sheet'],dict_all_tickers_all_financials['inc_stat'])

dict_tickers_variables = dict_tickers_variables_and_usable_tickers['dict_tickers_dfs']

similar_tickers = dict_tickers_variables_and_usable_tickers['usable_tickers']

unusable_tickers = dict_tickers_variables_and_usable_tickers['unusable_tickers']

#%%

cagr_eps_min = float(input("MINIMAL CAGR EPS TO FILTER AND CONSIDER TICKERS (ANSWER IN ABS.VAL, SO 5% IS 0.05): "))
#%%
cagr_rev_min = float(input("MINIMAL CAGR REVENUES TO FILTER AND CONSIDER TICKERS (ANSWER IN ABS.VAL, SO 5% IS 0.05): "))
#%%
discount_rate = float(input("RATE TO DISCOUNT EPS IN FUTURE PERIODS (ANSWER IN ABS.VAL, SO 15% IS 0.15): "))
#%%
n_year_forward = int(input("HOW MANY YEARS TO LOOK AHEAD: "))
#%%
pct_shrink_cagr_eps = float(input("HOW MUCH DOES EACH STOCK HISTORICAL EPS CAGR IS REDUCED TO USE IN WORST AND BASE CASE SCENARIO (ANSWER IN ABS.VAL, SO 35% IS 0.35): "))
#%%
pct_increase_cagr_eps = float(input("HOW MUCH DOES EACH STOCK HISTORICAL EPS CAGR IS INCREASED TO USE IN A BEST CASE SCENARIO (ANSWER IN ABS.VAL, SO 35% IS 0.35): "))
#%%
worst_case_weight = float(input("WEIGHT OF WORST CASE SCENARIO (ANSWER IN ABS.VAL, SO 65% IS 0.65) :"))
#%%
base_case_weight = float(input("WEIGHT OF BASE CASE SCENARIO (ANSWER IN ABS.VAL, SO 55% IS 0.55) :"))

#%%

#PRICE FACTOR, UNDER OR OVER VALUATION
price_factor = helpers.get_price_factor(tickers_lst = similar_tickers,
    dict_price = dict_price,
    dict_df_metrics_organized = dict_tickers_variables,
    cagr_eps_min =  cagr_eps_min,
    cagr_rev_min = cagr_rev_min ,
    discount_rate = discount_rate ,
    n_years_forward = n_year_forward ,
    pct_shrink_cagr_eps = pct_shrink_cagr_eps ,
    pct_increase_cagr_eps = pct_increase_cagr_eps ,
    worst_case_weight = worst_case_weight,
    base_case_weight = base_case_weight
)

#%%

price_factor_scores = price_factor['ticker_price_factor']
unusable_tickers2 = price_factor['unusable_tickers']

# %%
price_factor_scores

# %%
