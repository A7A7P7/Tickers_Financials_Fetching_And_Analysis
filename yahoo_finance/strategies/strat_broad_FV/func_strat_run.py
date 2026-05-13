#%%

from yahoo_finance.strategies.strat_broad_FV.helpers_func import helpers

#%%

def run_broad_fv(similar_tickers,dict_all_tickers_all_financials,directory_for_storage_and_retrieval):

    dict_price = helpers.choose_mkt_storage_prices(similar_tickers,dict_all_tickers_all_financials,directory_for_storage_and_retrieval)

    similar_tickers = helpers.filter_by_min_mkcap(similar_tickers,dict_all_tickers_all_financials['inc_stat'])

    dict_tickers_variables_and_usable_tickers = helpers.get_metrics_for_analysis(similar_tickers,dict_all_tickers_all_financials['bal_sheet'],dict_all_tickers_all_financials['inc_stat'])

    dict_tickers_variables = dict_tickers_variables_and_usable_tickers['dict_tickers_dfs']

    similar_tickers = dict_tickers_variables_and_usable_tickers['usable_tickers']

    unusable_tickers = dict_tickers_variables_and_usable_tickers['unusable_tickers']

    #INPUTS NEEDED TO MAKE THINGS WORK

    cagr_eps_min = float(input("MINIMAL CAGR EPS TO FILTER AND CONSIDER TICKERS (ANSWER IN ABS.VAL, SO 5% IS 0.05): "))

    cagr_rev_min = float(input("MINIMAL CAGR REVENUES TO FILTER AND CONSIDER TICKERS (ANSWER IN ABS.VAL, SO 5% IS 0.05): "))

    discount_rate = float(input("RATE TO DISCOUNT EPS IN FUTURE PERIODS (ANSWER IN ABS.VAL, SO 15% IS 0.15): "))

    n_year_forward = int(input("HOW MANY YEARS TO LOOK AHEAD: "))

    pct_shrink_cagr_eps = float(input("HOW MUCH DOES EACH STOCK HISTORICAL EPS CAGR IS REDUCED TO USE IN WORST AND BASE CASE SCENARIO (ANSWER IN ABS.VAL, SO 35% IS 0.35): "))

    pct_increase_cagr_eps = float(input("HOW MUCH DOES EACH STOCK HISTORICAL EPS CAGR IS INCREASED TO USE IN A BEST CASE SCENARIO (ANSWER IN ABS.VAL, SO 35% IS 0.35): "))

    worst_case_weight = float(input("WEIGHT OF WORST CASE SCENARIO (ANSWER IN ABS.VAL, SO 65% IS 0.65) :"))

    base_case_weight = float(input("WEIGHT OF BASE CASE SCENARIO (ANSWER IN ABS.VAL, SO 55% IS 0.55) :"))

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

    return {'price_scores' : price_factor['ticker_price_factor'] , 'used_tickers' : similar_tickers, 'unusable_tickers' : unusable_tickers}


