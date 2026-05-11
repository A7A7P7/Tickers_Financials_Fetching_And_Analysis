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

strat_chosen = strat_choose(dict_strats)

#%%

strat_chosen

#FROM STRATEGY 'broad_FValue' If Price SCORES IS EMPTY IT MEANS THAT THE TICKERS DIDN'T ACCOMPLISH ALL THE NEEDED PARAMETERS.
#SAME FOR 'fama_french', IF SOME TICKERS ARE NOT THERE IT MEANS SOME DATA MIGHT BE MISSING, OR THE COMPANY DOESN'T FULLFILL SOME SET OF CRITERIA

#%%

from finviz_us.helpers_file_root import helpers_root
from yahoo_finance.organize_tickers import organizing_tickers
from yahoo_finance.strategies.strat_broad_FV.func_strat_run import run_broad_fv
from yahoo_finance.strategies.strat_basic_fama_french.func_run_strat import run_basic_fam_fre

directory_for_storage_retrieval = organizing_tickers.directory_for_storage_or_retrieval
dict_all_tickers_all_financials = organizing_tickers.dict_all_financials_and_tickers
most_similar_tickers = organizing_tickers.similar_tickers_lst

