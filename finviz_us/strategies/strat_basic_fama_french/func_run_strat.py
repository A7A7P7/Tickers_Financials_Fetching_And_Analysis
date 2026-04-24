
#%%
from finviz_us.strategies.strat_basic_fama_french.fama_french_helpers import ff_helpers

#%%

def run_basic_fam_fre(most_similar_tickers,dict_all_tickers_all_financials):

    list_profit_factor = ff_helpers.ticker_profitability_factor(most_similar_tickers,dict_all_tickers_all_financials)

    dict_profit = list_profit_factor[0]
    most_similar_tickers = list_profit_factor[1]
    unusable_tickers = list_profit_factor[2]

    dict_value_factor = ff_helpers.first_fetch_or_storage_on_directory(most_similar_tickers)

    dict_beta_factor = ff_helpers.first_fetch_or_storage_on_directory(most_similar_tickers)

    dict_momentum_factor = ff_helpers.first_fetch_or_storage_on_directory(most_similar_tickers)

    dict_investment = ff_helpers.ticker_investment_factor(most_similar_tickers,dict_all_tickers_all_financials)

    dict_buying_attractiveness_standardized = ff_helpers.standardized_raking_sector_buys(most_similar_tickers,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment)

    dict_scores_standardized = dict_buying_attractiveness_standardized[0]

    dict_buying_attractiveness = ff_helpers.raking_sector_buys(most_similar_tickers,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment)

    dict_scores = dict_buying_attractiveness[0]
    tickers_considered = dict_buying_attractiveness[1]

    return {'tickers_buy_rankings_standardized': dict_scores_standardized,'tickers_buy_rankings_no_standardized' : dict_scores , 'tickers_considered' : tickers_considered}


#%%
