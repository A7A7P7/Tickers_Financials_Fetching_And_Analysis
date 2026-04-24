#%%

def choose_strategy(dict_strategies:dict):

    size_dict = len(dict_strategies)
    lst_keys = list(dict_strategies.keys())
    int_strat = int(input(f"CHOOSE AN INTEGER NUMBER FROM 0 TO {size_dict-1}: "))

    while int_strat > size_dict - 1 or int_strat < 0:

        print("INVALID INPUT, GIVE AN INTEGER WITHIN THE EXPECTED RANGE")
        int_strat = int(input(f"CHOOSE AN INTEGER NUMBER FROM 0 TO {size_dict-1}: "))

    strategy_name = lst_keys[int_strat]
    strat_confirm = input(f"THE STRATEGY CHOOSEN IS NAMED {strategy_name}, IS THAT THE ONE YOU WANT (ANSWER 'Yes' OR 'No'): ")

    while strat_confirm.upper() != 'YES' and strat_confirm.upper() != 'NO':

        print("INVALID INPUT, ANSWER 'Yes' OR 'No'")
        strat_confirm = input(f"THE STRATEGY CHOOSEN IS NAMED {strategy_name}, IS THAT THE ONE YOU WANT (ANSWER 'Yes' OR 'No'): ")

    if strat_confirm.upper() == 'YES':

        return dict_strategies[strategy_name]

    else: #strat_confirm.upper() == 'NO'

        strat_popped = dict_strategies.pop(strategy_name)
        lst_keys.remove(strategy_name)
        size_dict = len(dict_strategies)

        while size_dict != 0:

            lst_keys = list(dict_strategies.keys())
            int_strat = int(input(f"CHOOSE AN INTEGER NUMBER FROM 0 TO {size_dict-1}: "))

            while int_strat > size_dict - 1 or int_strat < 0:

                print("INVALID INPUT, GIVE AN INTEGER WITHIN THE EXPECTED RANGE")
                int_strat = int(input(f"CHOOSE AN INTEGER NUMBER FROM 0 TO {size_dict-1}: "))

            strategy_name = lst_keys[int_strat]
            strat_confirm = input(f"THE STRATEGY CHOOSEN IS NAMED {strategy_name}, IS THAT THE ONE YOU WANT (ANSWER 'Yes' OR 'No'): ")

            while strat_confirm.upper() != 'YES' and strat_confirm.upper() != 'NO':

                print("INVALID INPUT, ANSWER 'Yes' OR 'No'")
                strat_confirm = input(f"THE STRATEGY CHOOSEN IS NAMED {strategy_name}, IS THAT THE ONE YOU WANT (ANSWER 'Yes' OR 'No'): ")

            if strat_confirm.upper() == 'YES':

                return dict_strategies[strategy_name]

            else:

                strat_popped = dict_strategies.pop(strategy_name)
                lst_keys.remove(strategy_name)
                size_dict = len(dict_strategies)

        return "RAN OUT OF STRATEGIES, NONE WAS CHOOSEN"
