#%%

import pandas as pd
import numpy as np
import finvizfinance.quote as fvf
from finvizfinance.screener.overview import Overview
from pathlib import Path
import time

#%%

"""TICKERS ORGANIZATION"""

def choosing_tickers(directory_for_storage_or_retrieval):

    tickers_lst = []

    first_time = input("DOES THE DIRECTORY USED AS INPUT HAS ANY FILES STORED THERE (ANSWER 'Yes' OR 'No'):")

    while first_time.upper() != "YES" and first_time.upper() != "NO" :

        print("WRONG INPUT, PROCESS WILL BE REPEATED")
        first_time = str(input("DOES THE DIRECTORY USED HAS INPUT HAS ANY FILES STORED THERE (ANSWER 'Yes' OR 'No'):"))

    if first_time.upper() == "YES":

        all_tickers_or_some = input("DO YOU WANT TO RETRIEVE ALL STORED TICKERS FROM THE DIRECTORY (ANSWER 'Yes' OR 'No'): ")

        while all_tickers_or_some.upper() != 'YES' and all_tickers_or_some.upper() != 'NO' :

            print("INVALID INPUT, INPUT WILL BE ASKED AGAIN")
            all_tickers_or_some = input("DO YOU WANT TO RETRIEVE ALL STORED TICKERS FROM THE DIRECTORY (ANSWER 'Yes' OR 'No'): ")

        if all_tickers_or_some.upper() == "YES":

            print("ALL TICKERS USED WILL BE RETRIEVED FROM YOUR STORAGE DIRECTORY")

            path = Path(rf"{directory_for_storage_or_retrieval}/bal_sheet")
            for file in path.iterdir():

                ticker = file.stem
                tickers_lst.append(ticker)
        
        else: #all_tickers_or_some.upper() == "NO"

            n_tickers = int(input("HOW MANY TICKERS DO YOU WANT TO RETRIEVE: "))
            tickers_lst = []
            for i in range(n_tickers):

                ticker = str(input("TICKER: ")).upper()
                tickers_lst.append(ticker)

    else: #first_time.upper() == "NO":

        personal_list_answer = input("DO YOU WANT TO DO YOUR OWN LIST OR YOU WANT TO BE ASKED IF YOU WANT TICKERS FROM US INDEXES (ANSWER 'Yes' FOR OWN LIST OR 'No' FOR TICKERS FROM US INDEXES):")

        while personal_list_answer.upper() != "YES" and personal_list_answer.upper() != "NO" :

            print("WRONG INPUT, PROCESS WILL BE REPEATED")
            personal_list_answer = str(input("DO YOU WANT TO DO YOUR OWN LIST OR YOU WANT TO BE ASKED IF YOU WANT TICKERS FROM US INDEXES (ANSWER 'Yes' OR 'No'):"))
        
        if personal_list_answer.upper() == "YES":

            n_tickers = int(input("HOW MANY TICKERS YOU WANT IN YOUR LIST: "))
            tickers_lst = []
            for i in range(n_tickers):

                ticker = str(input("TICKER: ")).upper()
                tickers_lst.append(ticker)

        else: #personal_list_answer.upper() == "NO":

            print("DECIDE WHICH INDEXES YOU WANT IN YOUR TICKERS LIST")
            choosing_possibilities = ['S&P 500', 'NASDAQ 100', 'DJIA', 'RUSSELL 2000']
            indexes_list_with_separate_list_of_indexes = []

            for idx in range(len(choosing_possibilities)):

                yes_no = input(f"DO YOU WANT {choosing_possibilities[idx]} TICKERS IN YOUR LIST (ANSWER 'Yes' or 'No'): ")

                while yes_no.upper() != "YES" and yes_no.upper() != "NO" :

                    print("WRONG INPUT, PROCESS WILL BE REPEATED")
                    yes_no = input(f"DO YOU WANT {choosing_possibilities[idx]} TICKERS IN YOUR LIST: ")

                if yes_no.upper() == "YES":

                    foverview = Overview()

                    filters_dict = {'Index':choosing_possibilities[idx]}

                    foverview.set_filter(filters_dict=filters_dict)

                    df = foverview.screener_view()

                    lst_tickers = list(df['Ticker'])

                    indexes_list_with_separate_list_of_indexes.append(lst_tickers)
            
            for index in indexes_list_with_separate_list_of_indexes:

                for ticker in index:

                    if ticker not in tickers_lst:

                        tickers_lst.append(ticker) 
            
    return tickers_lst

def getting_tickers_from_index(possibilities_list=list):

    print("0 - 'S&P 500' ; 1 - 'NASDAQ 100' ; 2 - 'DJIA' ; 3 - 'RUSSELL 2000'")

    ind_choosen = int(input('Number of the Index choose to get tickers: '))

    while ind_choosen < 0 or ind_choosen > 4:
    
        print('WRONG INPUT, IT NEEDS TO BE AN INTEGER WITHIN THE INTERVAL [0,4]')
        ind_choosen = int(input('Number of the Index choose to get tickers: '))
    
    message_confirming = str(input(f"'{possibilities_list[ind_choosen]}' was choosen to get tickers, answer 'Yes' to continue or 'No' to change"))

    if message_confirming == "Yes" or message_confirming == "No":
        
        if message_confirming == "Yes":

            foverview = Overview()

            filters_dict = {'Index':possibilities_list[ind_choosen]}

            foverview.set_filter(filters_dict=filters_dict)

            df = foverview.screener_view()

            lst_tickers = list(df['Ticker'])

            return lst_tickers


        else:
        
            ind_choosen = int(input('Number of the Index choose to get tickers: '))

            while ind_choosen < 0 or ind_choosen > 4:
            
                print('WRONG INPUT, IT NEEDS TO BE AN INTEGER WITHIN THE INTERVAL [0,4]')
                ind_choosen = int(input('Number of the Index choose to get tickers: '))

            foverview = Overview()

            filters_dict = {'Index':possibilities_list[ind_choosen]}

            foverview.set_filter(filters_dict=filters_dict)

            df = foverview.screener_view()

            lst_tickers = list(df['Ticker'])

            return lst_tickers
            
        
    else:
        
        print("WRONG ANSWER, USE EITHER 'Yes' OR 'No' EXACTLY LIKE WHAT IS IN THE PARENTHESIS.")
        message_confirming = str(input(f"{possibilities_list[ind_choosen]} was choosen to get tickers, answer 'Yes' to continue or 'No' to change"))

        while message_confirming != 'Yes' and message_confirming != 'No':
        
            print("WRONG ANSWER, USE EITHER 'Yes' OR 'No' EXACTLY LIKE WHAT IS IN THE PARENTHESIS.")
            message_confirming = str(input(f"{possibilities_list[ind_choosen]} was choosen to get tickers, answer 'Yes' to continue or 'No' to change"))

        foverview = Overview()

        filters_dict = {'Index':possibilities_list[ind_choosen]}

        foverview.set_filter(filters_dict=filters_dict)

        df = foverview.screener_view()

        lst_tickers = list(df['Ticker'])

        return lst_tickers

def combine_tickers_from_different_indexes(**index_lists):

    combined_lst = list()

    "kwargs are lists of tickers"

    for lst in index_lists.values():
    
        for ticker in lst:
        
            if ticker not in combined_lst:
            
                combined_lst.append(ticker)
    
    return combined_lst

#%%

"""BALANCE SHEET RETRIEVAL"""

def get_bs_hist(ticker:str,ann_or_quar:str):

    if ann_or_quar != "A" or ann_or_quar != "Q":

        while (ann_or_quar != "A" and ann_or_quar != "Q"):
            
            print("WRONG INPUT USE 'A' FOR ANNUAL OR 'Q' FOR QUARTERLY AS INPUT")

            ann_or_quar = str(input("Annual - 'A' or Quarterly - 'Q'"))
        
        df_bs = fvf.Statements().get_statements(ticker,'B',ann_or_quar)

        time.sleep(0.5)

        # df_1 = df_bs.set_axis(df_bs.iloc[0],axis=1).iloc[2:].replace(',',"",regex=True).apply(pd.to_numeric, errors='coerce')

        # df_2 = df_bs.set_axis(df_bs.iloc[0],axis=1).iloc[1:2]

        # df_final = pd.concat([df_2,df_1],axis=0)
        
        # return df_final

        return df_bs

    else:

        df_bs = fvf.Statements().get_statements(ticker,'B',ann_or_quar)

        time.sleep(0.5)

        # df_1 = df_bs.set_axis(df_bs.iloc[0],axis=1).iloc[2:].replace(',',"",regex=True).apply(pd.to_numeric, errors='coerce')

        # df_2 = df_bs.set_axis(df_bs.iloc[0],axis=1).iloc[1:2]

        # df_final = pd.concat([df_2,df_1],axis=0)
        
        # return df_final

        return df_bs

def get_dict_with_bal_sheets(tickers_lst:list):

    dict_bs = dict()

    for ticker in tickers_lst:

        dict_bs[ticker] = get_bs_hist(ticker,'A')

    return dict_bs

#%%

"""INCOME STATEMENT RETRIEVAL"""

def get_inc_stat_hist(ticker:str,ann_or_quar:str):

    if ann_or_quar != "A" or ann_or_quar != "Q":

        while (ann_or_quar != "A" and ann_or_quar != "Q"):
            
            print("WRONG INPUT USE 'A' FOR ANNUAL OR 'Q' FOR QUARTERLY AS INPUT")

            ann_or_quar = str(input("Annual - 'A' or Quarterly - 'Q'"))
        
        df_inc = fvf.Statements().get_statements(ticker,'I',ann_or_quar)

        # df_1 = df_inc.set_axis(df_inc.iloc[0],axis=1).iloc[3:].replace(',',"",regex=True).apply(pd.to_numeric, errors='coerce')

        # df_2 = df_inc.set_axis(df_inc.iloc[0],axis=1).iloc[1:3]

        # df_final = pd.concat([df_2,df_1],axis=0)
        
        # return df_final

        return df_inc

    else:

        df_inc = fvf.Statements().get_statements(ticker,'I',ann_or_quar)

        # # df_1 = df_inc.set_axis(df_inc.iloc[0],axis=1).iloc[3:].replace(',',"",regex=True).apply(pd.to_numeric, errors='coerce')

        # # df_2 = df_inc.set_axis(df_inc.iloc[0],axis=1).iloc[1:3]

        # # df_final = pd.concat([df_2,df_1],axis=0)
        
        # return df_final

        return df_inc
    
def get_dict_with_inc_stats(tickers_lst:list):

    dict_inc_stat = dict()

    for ticker in tickers_lst:

        dict_inc_stat[ticker] = get_inc_stat_hist(ticker,'A')

    return dict_inc_stat

#%%

"""STATEMENT OF CASH FLOWS RETRIEVAL"""

def get_stat_cfs_hist(ticker:str,ann_or_quar:str):

    if ann_or_quar != "A" or ann_or_quar != "Q":

        while (ann_or_quar != "A" and ann_or_quar != "Q"):
            
            print("WRONG INPUT USE 'A' FOR ANNUAL OR 'Q' FOR QUARTERLY AS INPUT")

            ann_or_quar = str(input("Annual - 'A' or Quarterly - 'Q'"))

        df_stat = fvf.Statements().get_statements(ticker,'C',ann_or_quar)

        # # df_1 = df_inc.set_axis(df_inc.iloc[0],axis=1).iloc[3:].replace(',',"",regex=True).apply(pd.to_numeric, errors='coerce')

        # # df_2 = df_inc.set_axis(df_inc.iloc[0],axis=1).iloc[1:3]

        # # df_final = pd.concat([df_2,df_1],axis=0)

        # return df_final

        return df_stat

    else:

        df_stat = fvf.Statements().get_statements(ticker,'C',ann_or_quar)

        # df_1 = df_inc.set_axis(df_inc.iloc[0],axis=1).iloc[3:].replace(',',"",regex=True).apply(pd.to_numeric, errors='coerce')

        # df_2 = df_inc.set_axis(df_inc.iloc[0],axis=1).iloc[1:3]

        # df_final = pd.concat([df_2,df_1],axis=0)
        
        # return df_final

        return df_stat

def get_dict_with_stats_cfs(tickers_lst:list):

    dict_stat_cfs = dict()

    for ticker in tickers_lst:

        dict_stat_cfs[ticker] = get_stat_cfs_hist(ticker,'A')

    return dict_stat_cfs

#%%

"""COMBING ALL THE 3 STATEMENTS"""

def dict_all_tickers_and_three_statements(tickers_lst:list):

    complete_dict = {}
    complete_dict['bal_sheet'] = get_dict_with_bal_sheets(tickers_lst)
    complete_dict['inc_stat'] = get_dict_with_inc_stats(tickers_lst)
    complete_dict['stat_cfs'] = get_dict_with_stats_cfs(tickers_lst)

    return complete_dict

#ANOTHER WAY OF COMBINING THE 3 STATEMENTS

def get_dict_all_tickers_with_statements(dict_three_statements:dict,tickers_lst:list):

    for ticker in tickers_lst:

        for key in dict_three_statements:

            print(key,":",ticker,"; Index in tickers_lst",tickers_lst.index(ticker))

            if key == 'bal_sheet':

                dict_three_statements["bal_sheet"][ticker] = get_bs_hist(ticker,'A')

            elif key == 'inc_stat':

                dict_three_statements["inc_stat"][ticker] = get_inc_stat_hist(ticker,'A')

            else: #'stat_cfs'

                dict_three_statements["stat_cfs"][ticker] = get_stat_cfs_hist(ticker,'A')
            
            time.sleep(0.3)
    
    return dict_three_statements

#%%

"""STORAGE OF THE FILES INTO A CHOOSEN DIRECTORY AND PARQUET; AND THE REVERSE FROM PARQUET TO DF """

def parquet_to_df(path_to_parquet_files:str,ticker:str):

    path = Path(path_to_parquet_files)
    for file in path.glob("*.parquet"):

        if file.stem == ticker:
            break
        else:

            continue
    
    return pd.read_parquet(file)

def create_and_store_or_update_tickers_parquet_files_from_df_financials(dict_three_financials_to_transform:dict,tickers_lst:list,path_for_folder):

        n_tickers = len(tickers_lst)

        #CREATE DIRECTORIES IF NEEDED
        Path(path_for_folder).mkdir(exist_ok=True)
        Path(rf"{path_for_folder}/bal_sheet").mkdir(exist_ok=True)
        Path(rf"{path_for_folder}/inc_stat").mkdir(exist_ok=True)
        Path(rf"{path_for_folder}/stat_cfs").mkdir(exist_ok=True)

        for key in dict_three_financials_to_transform:

            folder_path = Path(rf"{path_for_folder}/{key}")

            for n in range(n_tickers):

                if folder_path.exists(): #PATH EXISTS

                    specific_ticker_path = Path(rf"{folder_path}/{tickers_lst[n]}.parquet")

                    if specific_ticker_path.exists(): #NEEDS UPDATE

                        print(tickers_lst[n],key,"exists but it is update")

                        #VALUES EXIST BUT ARE UPDATED
                        
                        #GET SAVED DF
                        str_path = f"{path_for_folder}/{key}"
                        ticker_saved_financial = parquet_to_df(str_path,tickers_lst[n])
                        df_fetched = dict_three_financials_to_transform[key][tickers_lst[n]]
                        columns_to_be_added = []

                        #IF NEW VALUES APPEAR, THE IDEA ISN'T TO LOSE THE OLDEST VALUE, SO ADD INTO THE DF THOSE VALUES

                        oldest_df_periods = list(ticker_saved_financial.loc['Period'])
                        recent_df_periods = list(df_fetched.loc['Period'])

                        for period in oldest_df_periods:

                            if period not in recent_df_periods:

                                recent_df_periods.append(period)
                        
                        df_periods_not_in_recent_df = df_fetched

                        n_cols_added = len(recent_df_periods) - len(df_fetched)

                        for i in range(len(df_fetched),len(df_fetched) + n_cols_added):

                            period = recent_df_periods[i]
                            col_name = ticker_saved_financial.loc['Period'].eq(period).idxmax()
                            col_df = ticker_saved_financial[col_name].to_frame()
                            col_df.columns = [i]
                            df_periods_not_in_recent_df = pd.concat([df_periods_not_in_recent_df,col_df],axis=1)
                        
                        df_to_be_stored = df_periods_not_in_recent_df
                        
                        for file in specific_ticker_path.iterdir():

                            file.unlink()
                        
                        end_point = specific_ticker_path / rf"{tickers_lst[n]}.parquet"

                        df_to_be_stored.to_parquet(end_point)

                    else:

                        print(tickers_lst[n],key,"is added to storage")
                        
                        #THAT PATH IS CREATED WITH THE VALUES
                        specific_ticker_path.mkdir(exist_ok=True)
                        ticker_statement = dict_three_financials_to_transform[key][tickers_lst[n]]
                        end_point = specific_ticker_path / rf"{tickers_lst[n]}.parquet"
                        ticker_statement.to_parquet(end_point) #ticker_statement.to_parquet(folder_path / f"{tickers_lst[n]}.parquet")
                
                else: #PATH DOESN'T EXIST

                    print(tickers_lst[n],key,"is being stored in a new directory")

                    #PATH IS CREATED AND VALUES ARE IMPRINTED
                    folder_path.mkdir(exist_ok=True) #CREATE THE PATH
                    ticker_statement = dict_three_financials_to_transform[key][tickers_lst[n]]
                    end_point = folder_path / rf"{tickers_lst[n]}.parquet"
                    ticker_statement.to_parquet(end_point)

def updated_parquet_to_df(path_to_financials:str,tickers_lst:list): #Path(r"C:\Users\Afons\Documentos\Investments\finviz_financials")

    dict_all_tickers_all_financials_updated = {'bal_sheet' : dict(), 'inc_stat' : dict(), 'stat_cfs' : dict()}

    for key in dict_all_tickers_all_financials_updated:

        for n in range(len(tickers_lst)):

            path = Path(f"{path_to_financials}/{key}/{tickers_lst[n]}.parquet")

            if path.exists():

                print("Turning",key,"from parquet to DF from the ticker",tickers_lst[n])

                saved_df = pd.read_parquet(path)

                #PERFORM CHANGES ON THE DF FOR THEM TO BE WORKABLE

                if key == 'bal_sheet':

                    df_1 = saved_df.set_axis(saved_df.iloc[0],axis=1).iloc[2:].replace(',',"",regex=True).apply(pd.to_numeric, errors='coerce')

                    df_2 = saved_df.set_axis(saved_df.iloc[0],axis=1).iloc[1:2]

                    df_final = pd.concat([df_2,df_1],axis=0)

                    dict_all_tickers_all_financials_updated[key][tickers_lst[n]] = df_final


                elif key == 'inc_stat':

                    df_1 = saved_df.set_axis(saved_df.iloc[0],axis=1).iloc[3:].replace(',',"",regex=True).apply(pd.to_numeric, errors='coerce')

                    df_2 = saved_df.set_axis(saved_df.iloc[0],axis=1).iloc[1:3]

                    df_final = pd.concat([df_2,df_1],axis=0)

                    dict_all_tickers_all_financials_updated[key][tickers_lst[n]] = df_final

                else: #'stat_cfs'

                    df_1 = saved_df.set_axis(saved_df.iloc[0],axis=1).iloc[3:].replace(',',"",regex=True).apply(pd.to_numeric, errors='coerce')

                    df_2 = saved_df.set_axis(saved_df.iloc[0],axis=1).iloc[1:3]

                    df_final = pd.concat([df_2,df_1],axis=0)

                    dict_all_tickers_all_financials_updated[key][tickers_lst[n]] = df_final
            
            else:
            
                print(f"{tickers_lst[n]} FINANCIALS WERE NOT FOUND")

    return dict_all_tickers_all_financials_updated

#%%

"""DECIDE IF WANT STORED DATA OR NEW DATA"""

def use_stored_or_updated_financials(dict_three_statements,tickers_lst,directory_for_storage_or_retrieval):

    yes_no = str(input("DO YOU ALREADY HAVE A DIRECTORY WITH THE TICKERS, ANSWER 'Yes' or 'No': "))

    while yes_no.upper() != "YES" and yes_no.upper() != "NO" :

        print("WRONG INPUT, PROCESS WILL BE REPEATED")
        yes_no = str(input("DO YOU ALREADY HAVE A DIRECTORY WITH THE TICKERS, ANSWER 'Yes' or 'No': "))

    if yes_no.upper() == "YES":

        want_update = str(input("DO YOU WANT TO UPDATE  HAVE A DIRECTORY WITH THE TICKERS, ANSWER 'Yes' or 'No': "))

        while want_update.upper() != "YES" and want_update.upper() != "NO":

            print("WRONG INPUT, PROCESS WILL BE REPEATED")
            want_update = str(input("DO YOU WANT TO UPDATE  HAVE A DIRECTORY WITH THE TICKERS, ANSWER 'Yes' or 'No': "))

        if want_update.upper() == "NO":

            #NO_UPDATE_GET_FROM_GET_FROM_PARQUET
            dict_ticker_financials = updated_parquet_to_df(directory_for_storage_or_retrieval,tickers_lst)
            return dict_ticker_financials

        else: #want_update.upper() == "YES"

            #UPDATE_FROM_FINVIZ_AND_STORE
            all_tickers_financials = get_dict_all_tickers_with_statements(dict_three_statements,tickers_lst)
            create_and_store_or_update_tickers_parquet_files_from_df_financials(all_tickers_financials,tickers_lst,directory_for_storage_or_retrieval)
            return all_tickers_financials

    else:

        #UPDATE_FROM_FINVIZ_AND_STORE
        all_tickers_financials = get_dict_all_tickers_with_statements(dict_three_statements,tickers_lst)
        create_and_store_or_update_tickers_parquet_files_from_df_financials(all_tickers_financials,tickers_lst,directory_for_storage_or_retrieval)
        return all_tickers_financials

"""SEE IF IT IS USER 1ST TIME AND ASSESS WHAT THEY WANT TO DO"""

def fetch_update_or_get_from_directory(dict_three_statements:dict,tickers_lst:list,directory_for_storage_or_retrieval):

    first_time = str(input("IS IT YOUR 1ST TIME USING THE SCRIPT: "))

    while first_time.upper() != "YES" and first_time.upper() != "NO":

        print("WRONG INPUT, USE 'Yes' OR 'No'")
        first_time = str(input("IS IT YOUR 1ST TIME USING THE SCRIPT: "))
    
    if first_time.upper() == "YES" :

        print("IT WILL TAKE LONG OF LEN OF TICKERS_LST IS HIGH")
        #FETCH FROM FINVIZ DIRECTLY
        all_tickers_financials = get_dict_all_tickers_with_statements(dict_three_statements,tickers_lst)
        create_and_store_or_update_tickers_parquet_files_from_df_financials(all_tickers_financials,tickers_lst,directory_for_storage_or_retrieval)
        dict_ticker_financials = updated_parquet_to_df(directory_for_storage_or_retrieval,tickers_lst)
        return dict_ticker_financials
    
    else: #first_time.upper() == "NO"

        want_update = str(input("DO YOU WANT TO RE-FETCH THE TICKERS IN YOUR LIST (IT WILL TAKE LONG IF LEN OF TICKERS_LST IS HIGH AS ALL TICKERS ARE UPDATED), ANSWER 'Yes' or 'No': "))

        while want_update.upper() != "YES" and want_update.upper() != "NO":

            print("WRONG INPUT, PROCESS WILL BE REPEATED")
            want_update = str(input("DO YOU WANT TO RE-FETCH THE TICKERS IN YOUR LIST (IT WILL TAKE LONG IF LEN OF TICKERS_LST IS HIGH AS ALL TICKERS ARE UPDATED), ANSWER 'Yes' or 'No': "))

        if want_update.upper() == "NO":

            #NO_UPDATE_GET_FROM_GET_FROM_PARQUET
            dict_ticker_financials = updated_parquet_to_df(directory_for_storage_or_retrieval,tickers_lst)
            return dict_ticker_financials

        else: #want_update.upper() == "YES"

            #UPDATE_FROM_FINVIZ_AND_STORE
            all_tickers_financials = get_dict_all_tickers_with_statements(dict_three_statements,tickers_lst)
            create_and_store_or_update_tickers_parquet_files_from_df_financials(all_tickers_financials,tickers_lst,directory_for_storage_or_retrieval)
            dict_ticker_financials = updated_parquet_to_df(directory_for_storage_or_retrieval,tickers_lst)
            return dict_ticker_financials

#%%

"""ASSESSMENT OF COMPARATIBILITY ACROSS TICKERS"""

def statement_match(statement_1:pd.DataFrame,statement_2:pd.DataFrame):

    size_stat_1 = len(statement_1)
    size_stat_2 = len(statement_2)
    size_match = size_stat_1 == size_stat_2
    stat_1_ind = statement_1.index 
    stat_2_ind = statement_2.index

    if size_match:
    
        lst_bool = list(stat_1_ind == stat_2_ind)
        content_match = lst_bool.count(True) == size_stat_1

        if content_match:
        
            return True
        
        else:
        
            return False
    
    else:
    
        return False

def assess_tickers_comparability(list_dict_three_statements:list): #checks if tickers can be comparable by having similar variables in inc_stat, bal_sheet & stat_cfs

    dict_assessing_tickers_comparability = {'comparable_tickers_1' : []}

    #NUMBER OF TICKERS
    length_list_tickers = len(list_dict_three_statements[0])
    lst_tickers = list(list_dict_three_statements[0].keys())
    dict_assessing_tickers_comparability['comparable_tickers_1'].append(lst_tickers[0])

    for ind in range(1,length_list_tickers):

        ticker = lst_tickers[ind] #KEY FOR EACH TICKER OF FINANCIAL STATEMENTS

        size_dict_assessing = len(dict_assessing_tickers_comparability) #CHECK HOW MANY COMPARISONS ARE NEEDED TO DO

        lst_keys_dict_assessing = list(dict_assessing_tickers_comparability.keys())

        ticker_added = False

        for comparison in range(size_dict_assessing):
        
            comparable_statements = 0

            first_comparable_ticker = dict_assessing_tickers_comparability[lst_keys_dict_assessing[comparison]][0]

            #COMPARE WITH EACH STATEMENT BY SIZE AND CONTENT

            for statement in list_dict_three_statements: #'statement' is a df of bs,inc_stat and stat_cfs
            
                boolean = statement_match(statement[first_comparable_ticker],statement[ticker])

                if boolean:
                
                    comparable_statements += 1
                
            if comparable_statements == 3:

                dict_assessing_tickers_comparability[lst_keys_dict_assessing[comparison]].append(ticker)
                ticker_added = True
                break
            
            else:
            
                continue
        
        if ticker_added: #ticker was added
        
            continue
        
        else:
        
            #CREATION OF NEW COMPARABLES
            new_key = f"comparable_tickers_{size_dict_assessing+1}"
            dict_assessing_tickers_comparability[new_key] = list()
            dict_assessing_tickers_comparability[new_key].append(ticker)
    
    return dict_assessing_tickers_comparability

def get_comparables_by_industry(dict_comparables:dict):

    #HERE THE INPUT IS A DICT WITH EACH KEY HAVING VALUES OFF THE TICKERS THAT ARE COMPARABLE
    #THE INPUT IS A RESULT OF USAGE OF FUNCTION 'assess_tickers_comparability'

    dict_industry_comparables = dict()

    for key in dict_comparables:

        dict_industry_comparables[key] = dict()

        for ticker in dict_comparables[key]:

            ticker_industry = get_industry_ticker(ticker)
            time.sleep(0.1)

            if ticker_industry not in dict_industry_comparables[key].keys():

                dict_industry_comparables[key][ticker_industry] = list()
                dict_industry_comparables[key][ticker_industry].append(ticker)
            
            else:

                dict_industry_comparables[key][ticker_industry].append(ticker)
    
    #RETURNS A DICT WITH SAME KEYS AS THE INPUT BUT WITHIN THOSE KEYS THE VALUES HAVE MORE KEYS DIVIDING EACH TICKER IN SAME SECTORS
    
    return dict_industry_comparables

def get_tickers_that_most_match(dict_comparables:dict):

    lst_sizes = []
    for key in dict_comparables:

        lst_sizes.append(len(dict_comparables[key]))
    
    max_size = max(lst_sizes)
    idx_max_size = lst_sizes.index(max_size)
    key = list(dict_comparables.keys())[idx_max_size]
    lst_sizes = dict_comparables[key]
    
    return lst_sizes

#%%

"""SIMPLIFIED FUNCTIONS FOR FAMA-FRENCH MODEL FACTOR ANALYSIS"""

