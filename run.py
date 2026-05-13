#%%

from finviz_us.organize_tickers import organizing_tickers
from finviz_us.strategies.strat_broad_FV.func_strat_run import run_broad_fv as run_broad_fair_value_finviz
from finviz_us.strategies.strat_basic_fama_french.func_run_strat import run_basic_fam_fre as run_basic_fam_fre_finviz

directory_for_storage_retrieval_finviz = organizing_tickers.directory_for_storage_or_retrieval
dict_all_tickers_all_financials_finviz = organizing_tickers.dict_all_financials_three_statements
most_similar_tickers_finviz = organizing_tickers.most_similar_tickers

#%%

from yahoo_finance.organize_tickers import organizing_tickers
from yahoo_finance.strategies.strat_broad_FV.func_strat_run import run_broad_fv as run_broad_fair_value_yfinance
from yahoo_finance.strategies.strat_basic_fama_french.func_run_strat import run_basic_fam_fre as run_basic_fam_fre_yfinance

directory_for_storage_retrieval_yf = organizing_tickers.directory_for_storage_or_retrieval
dict_all_tickers_all_financials_yf = organizing_tickers.dict_all_financials_and_tickers
most_similar_tickers_yf = organizing_tickers.similar_tickers_lst

#%%

def run_with_finviz(directory_for_storage_retrieval_finviz,dict_all_tickers_all_financials_finviz,most_similar_tickers_finviz) :

    print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'fama_french'")
    print("EVERY TIME THE SCRIPT ASK YOU ABOUT A DIRECTORY, YOU WILL ALWAYS PROVIDE THE SAME DIRECTORY")

    strat_fam_french = run_basic_fam_fre_finviz(most_similar_tickers_finviz,dict_all_tickers_all_financials_finviz)

    print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'FV_from_financials'")

    strat_FV_from_financials = run_broad_fair_value_finviz(most_similar_tickers_finviz,dict_all_tickers_all_financials_finviz,directory_for_storage_retrieval_finviz)

    strategies = {
        "fama_french": strat_fam_french,
        "broad_FValue": strat_FV_from_financials
    }

    return strategies

def run_with_yf(directory_for_storage_retrieval_yf,dict_all_tickers_all_financials_yf,most_similar_tickers_yf) :

    print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'fama_french'")
    print("EVERY TIME THE SCRIPT ASK YOU ABOUT A DIRECTORY, YOU WILL ALWAYS PROVIDE THE SAME DIRECTORY")

    strat_fam_french = run_basic_fam_fre_yfinance(most_similar_tickers_yf,dict_all_tickers_all_financials_yf)

    print("NEXT INPUTS THAT YOU WILL PROVIDE ARE FOR STRATEGY 'FV_from_financials'")

    strat_FV_from_financials = run_broad_fair_value_yfinance(most_similar_tickers_yf,dict_all_tickers_all_financials_yf,directory_for_storage_retrieval_yf)

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

dict_strats_finviz = run_with_finviz(directory_for_storage_retrieval_finviz,dict_all_tickers_all_financials_finviz,most_similar_tickers_finviz)

#%%

strat_chosen_finviz = strat_choose(dict_strats_finviz)

#%%

dict_strats_yf = run_with_yf(directory_for_storage_retrieval_yf,dict_all_tickers_all_financials_yf,most_similar_tickers_yf)

#%%

strat_chosen_yf = strat_choose(dict_strats_yf)

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

