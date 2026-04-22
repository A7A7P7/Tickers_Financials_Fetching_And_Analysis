#%%

from finviz_us.organize_tickers import organizing_tickers
from finviz_us.strat_basic_fama_french.fama_french_helpers import ff_helpers

#REPX,SD,VITL,CL,CMRE,NOG,AMPY,CPRT,CALM,REI,RIG,VAL,EPM,OXY,ADBE

#%%

#DICT WITH ALL TICKERS ALL FINANCIALS
dict_all_tickers_all_financials = organizing_tickers.dict_all_financials_three_statements

#TICKERS FOR USAGE
most_similar_tickers = organizing_tickers.most_similar_tickers


#%%

#PROFIT FACTOR
list_profit_factor = ff_helpers.ticker_profitability_factor(most_similar_tickers,dict_all_tickers_all_financials)

dict_profit = list_profit_factor[0]
most_similar_tickers = list_profit_factor[1]
unusable_tickers = list_profit_factor[2]

#%%

dict_profit

#%%

dict_value_factor = ff_helpers.first_fetch_or_storage_on_directory(most_similar_tickers)

#%%

dict_value_factor

#%%

dict_beta_factor = ff_helpers.first_fetch_or_storage_on_directory(most_similar_tickers)

#%%

dict_beta_factor

#%%

dict_momentum_factor = ff_helpers.first_fetch_or_storage_on_directory(most_similar_tickers)

#%%

dict_momentum_factor

#%%

#INVESTMENT FACTOR
dict_investment = ff_helpers.ticker_investment_factor(most_similar_tickers,dict_all_tickers_all_financials)

#%%

#CLASSIFICATION OF TICKERS ACCORDING TO A BASIC FAMA-FRENCH
dict_buying_attractiveness = ff_helpers.standardized_raking_sector_buys(most_similar_tickers,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment)

dict_scores = dict_buying_attractiveness[0]
tickers_considered = dict_buying_attractiveness[1]

#%%

dict_scores

#%%

n_years_used_for_averages_in_profit_factor = int(input("NºYEARS USED FOR AVERAGES IN CALCULATION OF PROFIT FACTOR: "))
n_years_used_for_averages_in_investment_factor = int(input("NºYEARS USED FOR AVERAGES IN CALCULATION OF INVESTMENT FACTOR: "))

dict_tickers_main_metrics = ff_helpers.yield_ticker_metrics(tickers_considered,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment,dict_scores,n_years_used_for_averages_in_profit_factor,n_years_used_for_averages_in_investment_factor)

#%%

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

dict_tickers_main_metrics = yield_ticker_metrics(tickers_considered,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment,dict_scores,7,7)
#%%

dict_tickers_main_metrics

#%%

dict_buying_attractiveness_no_mom = ff_helpers.standardized_raking_sector_buys_no_momentum(most_similar_tickers,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment)

dict_scores_no_mom = dict_buying_attractiveness_no_mom[0]
tickers_considered_no_mom = dict_buying_attractiveness_no_mom[1]

# %%
dict_scores_no_mom

#%%

dict_buying_attractiveness_no_standard = ff_helpers.raking_sector_buys(most_similar_tickers,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment)

dict_scores_no_standard = dict_buying_attractiveness_no_standard[0]
tickers_considered_no_standard = dict_buying_attractiveness_no_standard[1]

#%%

dict_scores_no_standard

#%%

dict_buying_attractiveness_only_book = ff_helpers.raking_sector_buys_value_only_pricetobook(most_similar_tickers,dict_profit,dict_value_factor,dict_beta_factor,dict_momentum_factor,dict_investment)

dict_scores_no_mom_only_pb = dict_buying_attractiveness_only_book[0]
tickers_considered_no_mom_only_pb = dict_buying_attractiveness_only_book[1]

# %%
dict_scores_no_mom_only_pb

#%%