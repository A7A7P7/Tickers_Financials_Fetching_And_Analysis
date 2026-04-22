
#%%

"""STRATEGY RELATED TO FAMA FRENCH MODEL"""

from finviz_us.data_tickers_and_strats.strat_basic_fama_french import basic_fam_fre

#%%

#DICT WITH ALL TICKERS ALL FINANCIALS
dict_all_tickers_all_financials = basic_fam_fre.dict_all_tickers_all_financials

#TICKERS FOR USAGE
most_similar_tickers = basic_fam_fre.most_similar_tickers

dict_profit = basic_fam_fre.dict_profit
dict_value_factor = basic_fam_fre.dict_value_factor
dict_beta_factor = basic_fam_fre.dict_beta_factor
dict_momentum_factor = basic_fam_fre.dict_momentum_factor
dict_investment = basic_fam_fre.dict_investment
dict_scores_no_standard = basic_fam_fre.dict_scores_no_standard

#%%

"""STRATEGY RELATED TO FV BASED ON FINANCIAL"""

from data_tickers_and_strats.strat_broad_FV import strat_run

directory_for_storage = strat_run.directory_for_storage

#DICT WITH ALL TICKERS ALL FINANCIALS
dict_all_tickers_all_financials = strat_run.dict_all_tickers_all_financials

#TICKERS FOR USAGE AND NON USAGE
similar_tickers = strat_run.similar_tickers
unusable_tickers = strat_run.unusable_tickers2

dict_price = strat_run.dict_price
dict_metrics_organized = strat_run.dict_tickers_variables

#INPUTS FOR FINAL FUNCTION

cagr_eps_min = strat_run.cagr_eps_min
cagr_rev_min = strat_run.cagr_rev_min
discount_rate = strat_run.discount_rate
n_year_forward = strat_run.n_year_forward
pct_shrink_cagr_eps = strat_run.pct_shrink_cagr_eps
pct_increase_cagr_eps = strat_run.pct_increase_cagr_eps
worst_case_weight = strat_run.worst_case_weight
base_case_weight = strat_run.base_case_weight

price_factor_scores = strat_run.price_factor_scores

