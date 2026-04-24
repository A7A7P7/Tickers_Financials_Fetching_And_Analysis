#%%
from finviz_us.helpers_file_root import helpers_root
from finviz_us.organize_tickers import organizing_tickers


#%%
#STRATEGIES
from finviz_us.strategies.strat_broad_FV.func_strat_run import run_broad_fv
from finviz_us.strategies.strat_basic_fama_french.func_run_strat import run_basic_fam_fre

#%%

directory_for_storage_retrieval = organizing_tickers.directory_for_storage_or_retrieval
dict_all_tickers_all_financials = organizing_tickers.dict_all_financials_three_statements
most_similar_tickers = organizing_tickers.most_similar_tickers

#%%

print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'fama_french'")

strat_fam_french = run_basic_fam_fre(most_similar_tickers,dict_all_tickers_all_financials)

#%%
print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'FV_from_financials'")

strat_FV_from_financials = run_broad_fv(most_similar_tickers,dict_all_tickers_all_financials,directory_for_storage_retrieval)

#%%

strategies = {
    "fama_french": strat_fam_french,
    "broad_FValue": strat_FV_from_financials
}

#%%

strategy_choosen = helpers_root.choose_strategy(strategies)

#%%

strategy_choosen['tickers_buy_rankings_no_standardized']['OXY']



# %%
