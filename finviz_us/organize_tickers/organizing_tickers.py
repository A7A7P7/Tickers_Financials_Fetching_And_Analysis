#%%

#IMPORT HELPER FUNCTIONS NEEDED
from finviz_us.organize_tickers.helpers_finviz import helpers_func

#%%

#PUT A NON EXISTENT DIRECTORY TO BE CREATED OR THE DIRECTORY THAT GIVES ACCESS TO EACH OF THE FOLDERS OF THE 3 STATEMENTS

"""IF YOU COPY A PATH FROM WINDOWS TAKE THE QUOTATIONS OUT."""
directory_for_storage_or_retrieval = input("DIRECTORY FOR STORAGE OR RETRIEVAL: ").strip().strip('"').strip("'")
tickers_lst = helpers_func.choosing_tickers(directory_for_storage_or_retrieval)

#dict_to_be_transformed
dict_all_financials_three_statements = { 'bal_sheet' : {}, 'inc_stat' : {}, 'stat_cfs' : {} }

#%%

"""

KNOW BEFOREHAND THAT IF IT IS THE 1ST TIME IT WILL TAKE LONG TO FETCH EVERYTHING, TOO MANY TICKERS;
TIME LIBRARY IS USED TO AVOID AS MANY TIMEOUTS AS POSSIBLE
IF YOU WANT TO CONDUCT THE TEST WITH LESS TICKERS, YOU CAN:

    1ST - CREATE YOUR OWN LIST AS ['ticker1','ticker2',...,'ticker_n']
    2ND - ON 'tickers_lst' REDUCE THE INPUTS OF THE FUNCTION USED AND LESS INDEXES WILL BE USED.
        FOR EXAMPLE USE ONLY THE INPUT 'djia = djia_lst' FOR TEST, CAUSE IT HAS LESS TICKERS.

"""

dict_all_financials_three_statements = helpers_func.fetch_update_or_get_from_directory(dict_all_financials_three_statements,tickers_lst,directory_for_storage_or_retrieval)

"""IF TIMEOUT OR CONNECTION INTERRUPTED, RE COMPUTE THE FUNCTION BUT WITH TICKERS_LST[LAST_INDEX_PRINTED:] AS INPUT
    WHERE 'LAST_INDEX_PRINTED' WILL BE THE LAST NUMBER PRINTED WHEN YOU RAN PREVIOUSLY 'get_dict_all_tickers_with_statements'
    ALSO PROVIDE THE SAME ANSWER FOR THE QUESTIONS ASKED IN THE FUNCTION AS YOU DID BEFORE
"""

#%%

#ASSESS COMPARATIBILITY OF TICKERS ACROSS ALL OF THEM, THE IDEA IS TO SEE IF VARIABLES IN ALL 3 STATEMENTS MATCH

dict_comparable_tickers = helpers_func.assess_tickers_comparability([dict_all_financials_three_statements['bal_sheet'],dict_all_financials_three_statements['inc_stat'],dict_all_financials_three_statements['stat_cfs']])

most_similar_tickers = helpers_func.get_tickers_that_most_match(dict_comparable_tickers)




