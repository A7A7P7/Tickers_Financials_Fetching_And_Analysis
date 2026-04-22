
#%%

"""                IGNORE THIS FILE FOR NOW IT ISN'T WORKING YET.               """

#%%

from organize_tickers import organizing_tickers
from help_func import help_func

#%%

tickers_lst = organizing_tickers.tickers_lst
dict_all_tickers_all_financials = organizing_tickers.dict_all_tickers_all_financials

#%%

tickers_net_current_asset_ratio = help_func.net_current_asset_ratio(tickers_lst,dict_all_tickers_all_financials['bal_sheet'],dict_all_tickers_all_financials['inc_stat'])

#%%

tickers_tangible_book_value_ratio = help_func.tangible_book_value_ratio(tickers_lst,dict_all_tickers_all_financials['bal_sheet'],dict_all_tickers_all_financials['inc_stat'])

tickers_tangible_book_value_ratio

#%%

tickers_ev_fcf_ratio = help_func.ev_fcf_ratio(tickers_lst,dict_all_tickers_all_financials['bal_sheet'],dict_all_tickers_all_financials['inc_stat'],dict_all_tickers_all_financials['stat_cfs'])

tickers_ev_fcf_ratio

#%%

tickers_price_fcf_ratio = help_func.price_to_fcf(tickers_lst,dict_all_tickers_all_financials['inc_stat'],dict_all_tickers_all_financials['stat_cfs'])

tickers_price_fcf_ratio

#%%

tickers_shareholder_yield = help_func.shareholder_yield(tickers_lst,dict_all_tickers_all_financials['inc_stat'],dict_all_tickers_all_financials['stat_cfs'])

tickers_shareholder_yield