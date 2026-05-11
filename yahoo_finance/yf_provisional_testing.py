
#%%
# =============================================================================
# BALANCE SHEET MAP
# =============================================================================
BALANCE_SHEET_MAP = {
    # ---- Current Assets ----
    "Cash & Short Term Investments": (
        ("direct",
        [
            "CashCashEquivalentsAndShortTermInvestments",
            "CashAndCashEquivalents",
            "CashEquivalents"
        ]), #CHECKED
    ),
    "Short Term Receivables": (
        ("direct",
        ["AccountsReceivable", "Receivables"]), #CHECKED
    ),
    "Inventories": (
        # yfinance already reports `Inventory` as net (after adjustments),
        # so we don't need to subtract `InventoriesAdjustmentsAllowances`.
        # Software/services companies (e.g. SAP) legitimately have no
        # Inventory row at all — handled by OPTIONAL_ITEMS.
        ("direct",
        ["Inventory"]), #CHECKED
    ),
    "Total Current Assets": (
        ("direct",
        ["CurrentAssets"]),
    ),
    "Other Current Assets": (
        ("residual",
        "CurrentAssets",
        [
            "Inventory",
            {"Short Term Receivables" : {"var1" : "AccountsReceivable","var2" : "Receivables"}},
            {"Cash & Short Term Investments" : {"var1" : "CashCashEquivalentsAndShortTermInvestments","var2" : "CashAndCashEquivalents","var3" : "CashEquivalents"}}
        ]),
    ),
    # ---- Non-Current Assets ----
    "Net Property, Plant & Equipment": (
        ("direct",
        ["NetPPE"]), #CHECKD
    ),
    "Total Investments and Advances": (
        ("sum",
        [
            "InvestmentsinAssociatesatCost",
            "InvestmentsinJointVenturesatCost",
            "LongTermEquityInvestment",
        ]),
    ),
    "Long-Term Note Receivable": (
        ("direct",
        [
            "NonCurrentNoteReceivables",  # ASML style
            "LongTermNoteReceivable",
            "NotesReceivable",
        ]),
    ),
    "Intangible Assets": (
        ("direct",
        [
            "GoodwillAndOtherIntangibleAssets",
            "GoodWill",  # fallback — only goodwill, no other intangibles
            "OtherIntangibleAssets",
        ]),
    ),
    "Deferred Tax Assets": (
        ("direct",
        ["NonCurrentDeferredTaxesAssets", "DeferredTaxAssets"]),
    ),
    "Other Assets": (
        ("residual",
        "TotalAssets",
        [
            "CurrentAssets",
            "NetPPE",
            {"Intangible Assets" : {"var1" : "GoodwillAndOtherIntangibleAssets","var2" : "GoodWill","var3" : "OtherIntangibleAssets"}},
            {"Deferred Tax Assets" : {"var1" : "NonCurrentDeferredTaxesAssets","var2" : "DeferredTaxAssets"}},
            "InvestmentsinAssociatesatCost",
            "InvestmentsinJointVenturesatCost",
            "LongTermEquityInvestment",
        ]),
    ),
    "Total Assets": (
        ("direct",
        ["TotalAssets"]),
        ("sum",
        ["CurrentAssets","TotalNonCurrentAssets"]),
    ),
    # ---- Current Liabilities ----
    "Short Term Debt Incl. Current Port. of LT Debt": (
        ("direct",
        ["CurrentDebtAndCapitalLeaseObligation", "CurrentDebt"]),
    ),
    "Accounts Payable": (
        ("direct",
        ["AccountsPayable", "Payables"]),
    ),
    "Income Tax Payable": (
        ("direct",
        ["TotalTaxPayable", "IncomeTaxPayable"]),
    ),
    "Other Current Liabilities": (
        ("residual",
        "CurrentLiabilities",
        [
            {"Accounts Payable" : {"var1" : "AccountsPayable","var2" : "Payables"}},
            "CurrentProvisions",
            {"Short Term Debt Incl. Current Port. of LT Debt" : {"var1" : "CurrentDebtAndCapitalLeaseObligation","var2" : "CurrentDebt"}},
            {"Income Tax Payable" : {"var1" : "TotalTaxPayable","var2" : "IncomeTaxPayable"}}
        ]),
    ),
    "Total Current Liabilities": (
        ("direct",
        ["CurrentLiabilities"]),
    ),
    # ---- Non-Current Liabilities ----
    "Long Term Debt": (
        ("direct",
        ["LongTermDebtAndCapitalLeaseObligation", "LongTermDebt"]),
    ),
    "Provision for Risks & Charges": (
        ("direct",
        ["LongTermProvisions", "NonCurrentProvisions"]),
    ),
    "Deferred Tax Liabilities": (
        ("direct",
        ["NonCurrentDeferredTaxesLiabilities", "DeferredTaxLiabilities"]),
    ),
    "Other Liabilities": (
        ("residual",
        "TotalLiabilitiesNetMinorityInterest",
        [
            "CurrentLiabilities",
            {"Long Term Debt" : {"var1" : "LongTermDebtAndCapitalLeaseObligation","var2" : "LongTermDebt"}},
            {"Provision for Risks & Charges" : {"var1" : "LongTermProvisions","var2" : "NonCurrentProvisions"}},
            {"Deferred Tax Liabilities" : {"var1" : "NonCurrentDeferredTaxesLiabilities","var2" : "DeferredTaxLiabilities"}}
        ]),
    ),
    "Total Liabilities": (
        ("direct",
        ["TotalLiabilitiesNetMinorityInterest"]),
    ),
    # ---- Equity ----
    "Preferred Stock - Carrying Value": (
        ("direct",
        ["PreferredStock", "PreferredStockEquity"]),
    ),
    "Common Equity": (
        ("direct",
        ["CommonStockEquity"]),
    ),
    "Total Shareholders Equity": (
        ("direct",
        ["TotalEquityGrossMinorityInterest"]),
    ),
    "Accumulated Minority Interest": (
        ("direct",
        ["MinorityInterest"]),
    ),
    "Total Equity": (
        ("direct",
        ["StockholdersEquity"]),
    ),
    "Total Liabilities & Stockholders Equity": (
        ("sum",
        [
            "TotalLiabilitiesNetMinorityInterest",
            "TotalEquityGrossMinorityInterest",
        ]),
    ),
}

# =============================================================================
# INCOME STATEMENT MAP
# =============================================================================
INCOME_STATEMENT_MAP = {
    # ---- Revenue & Gross ----
    "Total Revenue": (
        ("direct",
        [
            "TotalRevenue",
            "OperatingRevenue"
        ]),
    ),
    "Cost of Revenue/COGS": (    #NOT NAMED LIKE THIS, IT IS NAMED 'Cost of Goods Sold Incl. D&A' BUT HERE WILL BE COGS WITHOUT DEPRECIATION
        ("direct",
        [
            "CostOfRevenue",
            "ReconciledCostOfRevenue"
        ]),
    ),
    "Gross Profit": (
        ("direct",
        ["GrossProfit"]),
    ),
    # ---- Operating Expenses ----
    "Selling, General & Administrative": (
        ("direct",
        [
            "SellingGeneralAndAdministration",
            "GeneralAndAdministrativeExpense",
            "SellingAndMarketingExpense"
        ]),
    ),
    "Research & Development": (
        ("direct",
        ["ResearchAndDevelopment"]),
    ),
    "Operating Expenses (Total)": (
        ("direct",
        ["OperatingExpense"]),
    ),
    "EBITDA": (
        ("direct",
        [
            "EBITDA",
            "NormalizedEBITDA"
        ]),
    ),
    "D&A": (
        ("direct",
        [
            "DepreciationAndAmortizationInIncomeStatement",
            "ReconciledDepreciation",
            "DepreciationIncomeStatement"
        ]),
    ),
    "Operating Income": (
        ("direct",
        [
            "OperatingIncome",
            "TotalOperatingIncomeAsReported",
            "EBIT"
        ]),
    ),
    # ---- Below the Line ----
    "Interest Expense": (
        ("direct",
        [
            "InterestExpense",
            "InterestExpenseNonOperating"
        ]),
    ),
    "EBT": (
        ("direct",
        ["PretaxIncome"]),
    ),
    "Other Expense/Income": (
        ("residual",
        {"Operating Income" : {"var1" : "OperatingIncome","var2" : "TotalOperatingIncomeAsReported", "var3" : "EBIT"}},
        [
            "PretaxIncome",
            {"Interest Expense":{"var1" : "InterestExpense", "var2" : "InterestExpenseNonOperating"}}
        ]),
    ),
    "Income Tax": (
        ("direct",
        [
            "TaxProvision",
            "IncomeTaxExpense"
        ]),
    ),
    "Net Income": (
        # PRIORITY ORDER MATTERS — we want the exact numerator that Diluted
        # EPS uses, so that the identity `NI ≈ DilutedEPS × DilutedShares`
        # holds by construction. That field is `DilutedNIAvailtoComStockholders`.
        #
        # For companies with meaningful special items (Safran 2023 Collins
        # Aerospace acquisition gain, Sanofi 2022 EUROAPI spin-off, Iberdrola
        # 2024 Neoenergia sale, ...) `NetIncomeCommonStockholders` can be
        # significantly LARGER than `DilutedNIAvailtoComStockholders` because
        # yfinance reports EPS on a normalized-earnings basis while NICS
        # includes the headline figure with special items.
        #
        # Preferring the diluted-available-to-common field keeps the canonical
        # Net Income aligned with the EPS that ratios / factor models will use.
        # Fallback chain handles tickers that don't expose it.
        ("direct",
        [
            "DilutedNIAvailtoComStockholders",
            "NetIncomeCommonStockholders",
            "NetIncome",
            "NetIncomeFromContinuingOperations",
        ]),
    ),
    # ---- Per-Share ----
    "EPS (Basic)": (
        ("direct",
        ["BasicEPS"]),
    ),
    "EPS (Diluted)": (
        ("direct",
        ["DilutedEPS"]),
    ),
    "Shares Outstanding (Basic)": (
        ("direct",
        ["BasicAverageShares"]),
    ),
    "Shares Outstanding (Diluted)": (
        ("direct",
        ["DilutedAverageShares"]),
    ),
    "Prices Around Reporting Dates": (
        ("direct",
        ["Avg Prices Around Earnings"]),
    ),
    "Currency of Prices": (
        ("direct",
        ["Currency used in Pricing"]),
    ),
    "Currency of Financial Reporting": (
        ("direct",
        ["Currency used in Financial Reporting"]),
    ),
    "Market Capitalization": (
        ("direct",
        ["MkCap"]),
    )
}

# =============================================================================
# CASH FLOW STATEMENT MAP
# =============================================================================
CASH_FLOW_MAP = {
    # ---- Operating Activities ----
    "Net Income (CFS)": (
        ("direct",
        [
            "NetIncomeFromContinuingOperations",
            "NetIncome",
        ]),
    ),
    "Depreciation & Amortization": (
        ("direct",
        [
            "DepreciationAndAmortization",
            "DepreciationAmortizationDepletion",
        ]),
    ),
    "Other Non-Cash Items": (
        ("direct",
        ["OtherNonCashItems"]),
    ),
    "Changes in Working Capital": (
        ("direct",
        ["ChangeInWorkingCapital"]),
    ),
    "Income Taxes Payable": (
        ("direct",
        ["TaxesRefundPaid"]),
    ),
    "Deferred Income Tax": (
        ("direct",        #NOT PRESENT IN FINVIZ, ALSO
        [
            "DeferredTax",
            "DeferredIncomeTax"
        ]),
    ),
    "Cash from Operating Activities": (
        ("direct",
        [
            "OperatingCashFlow",
            "CashFlowFromContinuingOperatingActivities"
        ]),
    ),
    # ---- Investing Activities ----
    "Capital Expenditures": (
        ("direct",
        [
            "CapitalExpenditure",
            "CapitalExpenditureReported",
            "PurchaseOfPPE"
        ]),
    ),
    "Net Assets from Acquisitions": (
        ("direct",
        [
            "NetBusinessPurchaseAndSale",
            "NetPPEPurchaseAndSale"
        ]),
    ),
    "Purchase of Businesses": (
        ("direct",                                 #NOT INCLUDED IN FINVIZ
        ["PurchaseOfBusiness"]),
    ),
    "Sale of Fixed Assets and Businesses": (
        ("sum",
        [
            "SaleOfBusiness",
            "SaleOfPPE"
        ]),
    ),
    "Purchase of Investments": (
        ("direct",
        ["PurchaseOfInvestment"]),
    ),
    "Sale or Maturity of Investments": (
        ("direct",
        ["SaleOfInvestment"]),
    ),
    "Other Investing Activities": (
        ("direct",
        ["NetOtherInvestingChanges"]),
    ),
    "Cash from Investing Activities": (
        ("direct",
        [
            "InvestingCashFlow",
            "CashFlowFromContinuingInvestingActivities"
        ]),
    ),
    # ---- Financing Activities ----
    "Cash Dividends Paid": (
        ("direct",
        [
            "CashDividendsPaid",
            "CommonStockDividendPaid"
        ]),
    ),
    "Repurchase of Common & Preferred Stock": (
        ("direct",
        [
            "RepurchaseOfCapitalStock",
            "CommonStockPayments",  # yfinance reports the payment leg here
        ]),
    ),
    "Issuance of Common Stock": (
        # Prefer gross issuance when available; otherwise fall back to net.
        # Almost every European ticker reports at least `NetCommonStockIssuance`.
        ("direct",
        [
            "CommonStockIssuance",
            "IssuanceOfCapitalStock",
            "NetCommonStockIssuance",
        ]),
    ),
    "Net Issuance/Payments of Debt": (
        ("direct",
        ["NetIssuancePaymentsOfDebt"]),
    ),
    "Issuance of Long Term Debt": (
        # Prefer the gross LT-specific field; fall back to the general
        # `IssuanceOfDebt` (aggregate of ST+LT) for companies like Air Liquide
        # that only break it out at the aggregate level. Note: this means the
        # value may include short-term debt for such companies — acceptable
        # for screening, and the alternative is NaN.
        ("direct",
        [
            "LongTermDebtIssuance",
            "IssuanceOfDebt"
        ]),
    ),
    "Reduction of Long Term Debt": (
        # Same logic as above: prefer specific, fall back to aggregate.
        ("direct",
        [
            "LongTermDebtPayments",
            "RepaymentOfDebt"
        ]),
    ),
    "Other Financing Activities": (
        ("direct",
        ["NetOtherFinancingCharges"]),
    ),
    "Cash from Financing Activities": (
        ("direct",
        ["FinancingCashFlow",
         "CashFlowFromContinuingFinancingActivities"
        ]),
    ),
    # ---- Reconciliation ----
    "Exchange Rate Effect": (
        ("direct",
        ["EffectOfExchangeRateChanges"]),
    ),
    "Net Change in Cash": (
        ("direct",
        [
            "ChangesInCash",
            "ChangeInCashSupplementalAsReported"
        ]),
    ),
    # ---- Derived ----
    "Free Cash Flow": (
        ("direct",
        ["FreeCashFlow"]),
    ),
}


#%%
"""                          IGNORE THIS FILE FOR NOW IT IS NOT WORKING YET.                                         """
#%%

from ftplib import all_errors
from itertools import count
from math import e, nan
from operator import length_hint
from re import A, search
from types import NoneType
from altair import DataSource
from curl_cffi import CurlError
import pandas as pd
import numpy as np
#from streamlit.cursor import T
#from tenacity import P
import yfinance as yf
from pathlib import Path
import os
import time
import datetime
import random

#%%

from organize_tickers.helpers_org import helpers

"""WHEN IT SAYS 'Ticker': No earnings dates found, symbol may be delisted THAT AIN'T TRUE MOST OF TIMES, IT IS BASICALLY 'yfinance' LACK OF DATA"""

#%%

def collection_of_tickers_statements(directory_for_storage_or_retrieval,
    bal_sheet_map,
    bal_sheet_map_index,
    inc_stat_map,
    inc_stat_map_index,
    stat_cfs_map,
    stat_cfs_map_index,
):

    initial_ticker_lst = chosen_tickers(directory_for_storage_or_retrieval)

    dict_all_financials = {'bal_sheet' : {}, 'inc_stat' : {}, 'stat_cfs' : {}}

    fetch_from_cache = input("WERE YOUR TICKERS FETCHED FROM YOUR STORAGE, EXCEL FILES ARE CONSIDERED AS 'No' (ANSWER 'Yes' OR 'No'): ")

    while fetch_from_cache.upper() != "YES" and fetch_from_cache.upper() != "NO":

        print("INVALID INPUT, USE 'Yes' FOR TICKERS FETCHED FROM YOUR STORAGE AND 'No' FOR INDIVIDUAL TICKERS OR TICKERS FETCHED FROM ETFs IN EXCEL.")
        fetch_from_cache = input("WERE YOUR TICKERS FETCHED YOUR STORAGE, EXCEL FILES ARE CONSIDERED AS 'No' (ANSWER 'Yes' OR 'No'): ")

    if fetch_from_cache.upper() == "YES":

        want_update = str(input("DO YOU WANT TO RE-FETCH THE TICKERS IN YOUR LIST (IT WILL TAKE LONG IF LEN OF TICKERS_LST IS HIGH AS ALL TICKERS ARE UPDATED), ANSWER 'Yes' or 'No': "))

        while want_update.upper() != "YES" and want_update.upper() != "NO":

            print("WRONG INPUT, PROCESS WILL BE REPEATED")
            want_update = str(input("DO YOU WANT TO RE-FETCH THE TICKERS IN YOUR LIST (IT WILL TAKE LONG IF LEN OF TICKERS_LST IS HIGH AS ALL TICKERS ARE UPDATED), ANSWER 'Yes' or 'No': "))

        if want_update.upper() == "NO":

            #NO_UPDATE_GET_FROM_GET_FROM_PARQUET
            dict_ticker_financials = updated_parquet_to_df(directory_for_storage_or_retrieval,initial_ticker_lst,bal_sheet_map,bal_sheet_map_index,inc_stat_map,inc_stat_map_index,stat_cfs_map,stat_cfs_map_index)
            return dict_ticker_financials

        else: #want_update.upper() == "YES"

            #GET ALL THE TICKERS FINANCIALS
            for chunk in chunked(initial_ticker_lst, 10):  # 3–5 is safer

                dict_all_financials = get_dict_all_tickers_with_statements(dict_all_financials, chunk)

                time.sleep(1 + random.uniform(0, 1))  # jitter

            #dict_all_financials = get_dict_all_tickers_with_statements(dict_all_financials,initial_ticker_lst)

            #ADDITIONS INTO THE DATAFRAMES OF THE STATEMENTS THE PRICES
            addition_on_financial_statements(dict_all_financials,initial_ticker_lst,directory_for_storage_or_retrieval)

            #STORAGE OF THE TICKERS IN CACHE ON THE DIRECTORY
            create_and_store_or_update_tickers_parquet_files_from_df_financials(dict_all_financials,initial_ticker_lst,directory_for_storage_or_retrieval)

            #TURN THOSE FROM PARQUET INTO USABLE DF
            dict_ticker_financials = updated_parquet_to_df(directory_for_storage_or_retrieval,initial_ticker_lst,bal_sheet_map,bal_sheet_map_index,inc_stat_map,inc_stat_map_index,stat_cfs_map,stat_cfs_map_index)

            return dict_ticker_financials

    else: #fetch_from_cache.upper() == "NO"

        #GET ALL THE TICKERS FINANCIALS
        for chunk in chunked(initial_ticker_lst, 10):  # 3–5 is safer

            dict_all_financials = get_dict_all_tickers_with_statements(dict_all_financials, chunk)

            time.sleep(1 + random.uniform(0, 1))  # jitter

        #dict_all_financials = get_dict_all_tickers_with_statements(dict_all_financials,initial_ticker_lst)

        #ENSURE THAT ALL YOUR TICKERS HAVE THE THREE STATEMENTS
        dict_all_financials = match_tickers_with_three_statements(dict_all_financials,initial_ticker_lst)

        #ENSURE THAT FINANCIAL TICKERS ARE OUTSIDE OF THE TICKERS_LST
        dict_all_financials = dict_excluding_financial_services(dict_all_financials)
        ticker_lst_test = list(dict_all_financials["bal_sheet"].keys())

        #ADDITIONS INTO THE DATAFRAMES OF THE STATEMENTS THE PRICES
        addition_on_financial_statements(dict_all_financials,ticker_lst_test,directory_for_storage_or_retrieval)

        print("Starting the function create_and_store_or_update_tickers_parquet_files_from_df_financials")
        #STORAGE OF THE TICKERS IN CACHE ON THE DIRECTORY
        create_and_store_or_update_tickers_parquet_files_from_df_financials(dict_all_financials,ticker_lst_test,directory_for_storage_or_retrieval)

        #TURN THOSE FROM PARQUET INTO USABLE DF
        dict_ticker_financials = updated_parquet_to_df(directory_for_storage_or_retrieval,ticker_lst_test,bal_sheet_map,bal_sheet_map_index,inc_stat_map,inc_stat_map_index,stat_cfs_map,stat_cfs_map_index)

        return dict_ticker_financials

def get_tickers_from_directory(path:str):

    path = Path(rf"{path}\inc_stat")
    tickers_lst = []

    for file in path.iterdir():

        ticker = file.stem
        tickers_lst.append(ticker)

    return tickers_lst

def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

def chosen_tickers(directory_for_storage_or_retrieval):

    first_time_script = input("IS IT YOUR 1ST TIME USING THE SCRIPT RELATED TO 'y_finance' (ANSWER 'Yes' OR 'No')? ")

    while first_time_script.upper() != "YES" and first_time_script.upper() != "NO":

        print("INVALID INPUT, ANSWER EITHER 'Yes' or 'No'")
        first_time_script = input("IS IT YOUR 1ST TIME USING THE SCRIPT RELATED TO 'y_finance' (ANSWER 'Yes' OR 'No')? ")

    if first_time_script.upper() == "YES":

        #CREATE THE DIRECTORY, IF IT EXISTS ALSO OK, PUT A PRINT SAYING THAT IT IS CREATED.
        Path(directory_for_storage_or_retrieval).mkdir(exist_ok=True)

        etf_or_not = int(input("DO YOU WANT DATA FROM INDIVIDUAL TICKERS SELECTED BY YOU (ANSWER 0) OR STORED ETFS (ANSWER 1) :"))

        while etf_or_not != 0 and etf_or_not != 1 :

            print("INVALID INPUT, ANSWER '0' FOR INDIVIDUAL TICKERS OR '1' FOR STORED ETFS")
            etf_or_not = int(input("DO YOU WANT DATA FROM INDIVIDUAL TICKERS SELECTED BY YOU (ANSWER 0) OR STORED ETFS (ANSWER 1) :"))

        if etf_or_not == 1:

            etf_stored = input("DO YOU HAVE ETF WITH TICKERS STORED IN A DIRECTORY (ANSWER 'Yes' OR 'No'): ")

            while etf_stored.upper() != "YES" and etf_stored.upper() != "NO":

                print("INVALID INPUT, ANSWER EITHER 'Yes' or 'No'")
                etf_stored = input("DO YOU HAVE ETF WITH TICKERS STORED IN A DIRECTORY (ANSWER 'Yes' OR 'No'): ")

            if etf_stored.upper() == "YES":

                #GET DIRECTORY AND WORK FROM IT
                directory_to_etf = input("PUT THE ETF EXCEL DIRECTORY IN HERE: ")
                directory_to_etf = directory_to_etf.strip('"') #In the case where directory comes with commas
                suffix = Path(directory_to_etf).suffix

                if suffix == ".csv" : #iShares or BlackRock excel

                    #GET THE TERMINATIONS OF EACH EXCHANGE FOR EUROPEAN TICKERS
                    exchanges_termination_dict = helpers.get_european_exchange_terminations()
                    tickers_lst = helpers.get_tickers_to_yf_from_excel_blackrock(directory_to_etf,exchanges_termination_dict)

                else: #".xlsx"

                    dict_tickers = helpers.get_tickers_to_yf_from_excel_state_street(directory_to_etf)
                    tickers_lst = dict_tickers["usable_tickers"]

                return tickers_lst

            else: #etf_stored.upper() == "NO"

                print("READ THE 'README.md' ON THE PROJECT AND MAKE A STORAGE OF ETF(s) TO BE ABLE TO FETCH IN YOUR DEVICE, THEN REPEAT THE PROCESS")

                return []

        else: #etf_or_not == 0

            certainty_ticker = input("ARE YOU CERTAIN OF WHICH EXCHANGES YOU WANT FOR YOUR TICKERS? 'yfinance' USUALLY USES THE 'ticker.exchange_termination' TO IDENTIFY TICKERS AND THEIR EXCHANGES (ANSWER 'Yes' or 'No'): ")

            while certainty_ticker.upper() != "YES" and certainty_ticker.upper() != "NO":

                print("INVALID INPUT, ANSWER EITHER 'Yes' IF YOU ARE CERTAIN OF THE EXCHANGE TERMINATION OF EACH TICKER & 'No' IF YOU ARE NOT")
                certainty_ticker = input("ARE YOU CERTAIN OF WHICH EXCHANGES YOU WANT FOR YOUR TICKERS? 'yfinance' USUALLY USES THE 'ticker.exchange_termination' TO IDENTIFY TICKERS AND THEIR EXCHANGES (ANSWER 'Yes' or 'No'): ")

            if certainty_ticker.upper() == "YES" :

                #INDIVIDUAL TICKERS
                n_tickers = int(input("HOW MANY TICKERS, DO YOU WANT: "))
                count_tickers_collected = 0
                tickers_lst = []

                while count_tickers_collected < n_tickers:

                    count_tickers_collected += 1
                    ticker = input(f"TICKER NAME {count_tickers_collected} (WITH EXCHANGE TERMINATION): ")
                    tickers_lst.append(ticker)

                return tickers_lst

            else:

                #INDIVIDUAL TICKERS
                n_tickers = int(input("HOW MANY TICKERS, DO YOU WANT: "))
                count_tickers_collected = 0
                tickers_lst = []

                while count_tickers_collected < n_tickers:

                    count_tickers_collected += 1
                    ticker = input(f"TICKER NAME {count_tickers_collected} (NO EXCHANGE TERMINATION): ")
                    ticker = ticker.upper()+"."
                    #DF WITH ALL THE SYMBOLS OF THE TICKER IN DIFFERENT EXCHANGES
                    ticker_references_df = yf.Lookup(ticker).get_stock(count=1000)
                    ticker_symbols = ticker_references_df.index
                    size_str_ticker = len(ticker)
                    tickers_for_analysis = []
                    home_country_tickers = []
                    for symbol in ticker_symbols:

                        if symbol[:size_str_ticker] == ticker:

                            try:

                                home_country = yf.Ticker(symbol).info['country']

                            except KeyError:

                                print(symbol,"WON'T BE CONSIDERED")

                            else:

                                tickers_for_analysis.append(symbol)
                                if home_country not in home_country_tickers:
                                    home_country_tickers.append(home_country)

                    print("Possible Tickers Home Countries are: ",home_country_tickers)
                    #GET COUNTRY INFO BECAUSE SOME COUNTRIES ARE QUOTED OUTSIDE OF THEIR HOME COUNTRY, TRY TO AVOID THOSE STOCKS
                    #CHOOSE THE HOME COUNTRY OF THE TICKER YOU WANT, DEFAULT WILL BE THE LAST ONE
                    count_len_home_country = 0
                    try:

                        home_country = home_country_tickers[len(home_country_tickers)-1] #last index

                    except IndexError:

                        print(f"Wanted ticker wasn't found by the Lookup Search so you need to get the ticker with exact exchange ,go to yahoo finance print {ticker} and try to find the exchange that you want to complete the ticker USE THAT IN THE NEXT INPUT ")
                        ticker = input(f"TICKER {count_tickers_collected} (ALREADY WITH THE .'exchange'): ")
                        tickers_lst.append(ticker)

                    else:

                        while count_len_home_country <= len(home_country_tickers):

                            home = input(f"Is the home country of the ticker you want {home_country_tickers[count_len_home_country].upper()} ?(Answer 'Yes' or 'No'): ")
                            while home.upper() != "YES" and home.upper() != "NO":

                                print("INVALID INPUT, ANSWER 'Yes' OR 'No'")
                                home = input(f"Is the home country of the ticker you want {home_country_tickers[count_len_home_country].upper()} ?(Answer 'Yes' or 'No'): ")

                            if home.upper() == "YES":

                                home_country = home_country_tickers[count_len_home_country]
                                break

                            else: #NO

                                count_len_home_country += 1

                        possible_tickers = [t for t in tickers_for_analysis if yf.Ticker(t).info['country'] == home_country]
                        possible_exchanges_long_name = []
                        possible_exchanges_short_name = []

                        for t in possible_tickers:

                            try:

                                lst_ticker_exchange = t.split(".")
                                full_name = yf.Ticker(t).info['fullExchangeName']

                            except KeyError :

                                possible_tickers.remove(t)
                                print(symbol,"WON'T BE CONSIDERED BECAUSE IT IS NOT IN AN EXCHANGE")

                            else:

                                possible_exchanges_long_name.append(full_name)
                                possible_exchanges_short_name.append(lst_ticker_exchange[1])

                        print("Possible Tickers Exchanges are: ",possible_exchanges_long_name)

                        for tickr in possible_tickers:

                            ticker_idx = possible_tickers.index(tickr)

                            ticker_accept = input(f"The home country of ticker is '{home_country.upper()}' & the ticker {tickr} is quoted at '{possible_exchanges_long_name[ticker_idx].upper()}'-'{possible_exchanges_short_name[ticker_idx].upper()}', do you want to fetch this version of the ticker (answer 'Yes' or 'No'): ")
                            if ticker_accept.upper() != "YES" and ticker_accept.upper() != "NO":

                                print("INVALID INPUT ANSWER 'Yes' OR 'No'")
                                ticker_accept = input(f"The home country of ticker is '{home_country.upper()}' & the ticker {tickr} is quoted at '{possible_exchanges_long_name[ticker_idx].upper()}'-'{possible_exchanges_short_name[ticker_idx].upper()}', do you want to fetch this version of the ticker (answer 'Yes' or 'No'): ")

                            if ticker_accept.upper() == "YES":

                                ticker = tickr
                                tickers_lst.append(ticker)
                                break

                return tickers_lst

    else: #first_time_script.upper() == "NO"

        ask_for_storage = input("DO YOU HAVE ANY DIRECTORY WITH ANY STORAGE OF FINANCIALS BASED ON THIS SCRIPT? (ANSWER 'Yes' OR 'No'): ")

        while ask_for_storage.upper() != "YES" and ask_for_storage.upper() != "NO":

            print("INVALID INPUT, ANSWER 'Yes' IF STORAGE EXISTS OTHERWISE ANSWER 'No'")
            ask_for_storage = input("DO YOU HAVE ANY DIRECTORY WITH ANY STORAGE OF FINANCIALS BASED ON THIS SCRIPT? (ANSWER 'Yes' OR 'No'): ")

        if ask_for_storage.upper() == "YES":

            ask_for_usage = input("DO YOU WANT TO USE THAT DIRECTORY TO FETCH THE TICKERS THERE? (ANSWER 'Yes' OR 'No'): ")

            while ask_for_usage.upper() != "YES" and ask_for_usage.upper() != "NO":

                print("INVALID INPUT, ANSWER 'Yes' IF STORAGE EXISTS OTHERWISE ANSWER 'No'")
                ask_for_usage = input("DO YOU WANT TO USE THAT DIRECTORY TO FETCH THE TICKERS THERE? (ANSWER 'Yes' OR 'No'): ")

            if ask_for_usage.upper() == "YES":

                #USE FILE.STEM TO GET THE TICKER LIST
                tickers_lst = []

                for file in Path(rf"{directory_for_storage_or_retrieval}\inc_stat").iterdir():

                    ticker = file.stem
                    tickers_lst.append(ticker)

                return tickers_lst

            else:#NO

                ind_tickers_or_etf = int(input("DO YOU WANT TO USE INDIVIDUAL TICKERS SELECTED BY YOU (ANSWER 0) OR TICKERS FROM AN ETF (ANSWER 1): "))

                while ind_tickers_or_etf != 0 and ind_tickers_or_etf != 1:

                    print("INVALID INPUT, ANSWER '0' FOR INDIVIDUAL TICKERS OR '1' FOR ETFS")
                    ind_tickers_or_etf = int(input("DO YOU WANT TO USE INDIVIDUAL TICKERS SELECTED BY YOU (ANSWER 0) OR TICKERS FROM AN ETF (ANSWER 1): "))

                if ind_tickers_or_etf == 0:

                    certainty_ticker = input("ARE YOU CERTAIN OF WHICH EXCHANGES YOU WANT FOR YOUR TICKERS? 'yfinance' USUALLY USES THE 'ticker.exchange_termination' TO IDENTIFY TICKERS AND THEIR EXCHANGES (ANSWER 'Yes' or 'No'): ")

                    while certainty_ticker.upper() != "YES" and certainty_ticker.upper() != "NO":

                        print("INVALID INPUT, ANSWER EITHER 'Yes' IF YOU ARE CERTAIN OF THE EXCHANGE TERMINATION OF EACH TICKER & 'No' IF YOU ARE NOT")
                        certainty_ticker = input("ARE YOU CERTAIN OF WHICH EXCHANGES YOU WANT FOR YOUR TICKERS? 'yfinance' USUALLY USES THE 'ticker.exchange_termination' TO IDENTIFY TICKERS AND THEIR EXCHANGES (ANSWER 'Yes' or 'No'): ")

                    if certainty_ticker.upper() == "YES" :

                        #INDIVIDUAL TICKERS
                        n_tickers = int(input("HOW MANY TICKERS, DO YOU WANT: "))
                        count_tickers_collected = 0
                        tickers_lst = []

                        while count_tickers_collected < n_tickers:

                            count_tickers_collected += 1
                            ticker = input(f"TICKER NAME {count_tickers_collected} (WITH EXCHANGE TERMINATION): ")
                            tickers_lst.append(ticker)

                        return tickers_lst

                    else:

                        #INDIVIDUAL TICKERS
                        n_tickers = int(input("HOW MANY TICKERS, DO YOU WANT: "))
                        count_tickers_collected = 0
                        tickers_lst = []

                        while count_tickers_collected < n_tickers:

                            count_tickers_collected += 1
                            ticker = input(f"TICKER NAME {count_tickers_collected} (NO EXCHANGE TERMINATION): ")
                            ticker = ticker.upper()+"."
                            #DF WITH ALL THE SYMBOLS OF THE TICKER IN DIFFERENT EXCHANGES
                            ticker_references_df = yf.Lookup(ticker).get_stock(count=1000)
                            ticker_symbols = ticker_references_df.index
                            size_str_ticker = len(ticker)
                            tickers_for_analysis = []
                            home_country_tickers = []
                            for symbol in ticker_symbols:

                                if symbol[:size_str_ticker] == ticker:

                                    try:

                                        home_country = yf.Ticker(symbol).info['country']

                                    except KeyError:

                                        print(symbol,"WON'T BE CONSIDERED")

                                    else:

                                        tickers_for_analysis.append(symbol)
                                        if home_country not in home_country_tickers:
                                            home_country_tickers.append(home_country)

                            print("Possible Tickers Home Countries are: ",home_country_tickers)
                            #GET COUNTRY INFO BECAUSE SOME COUNTRIES ARE QUOTED OUTSIDE OF THEIR HOME COUNTRY, TRY TO AVOID THOSE STOCKS
                            #CHOOSE THE HOME COUNTRY OF THE TICKER YOU WANT, DEFAULT WILL BE THE LAST ONE
                            count_len_home_country = 0
                            try:

                                home_country = home_country_tickers[len(home_country_tickers)-1] #last index

                            except IndexError:

                                print(f"Wanted ticker wasn't found by the Lookup Search so you need to get the ticker with exact exchange ,go to yahoo finance print {ticker} and try to find the exchange that you want to complete the ticker USE THAT IN THE NEXT INPUT ")
                                ticker = input(f"TICKER {count_tickers_collected} (ALREADY WITH THE .'exchange'): ")
                                tickers_lst.append(ticker)

                            else:

                                while count_len_home_country <= len(home_country_tickers):

                                    home = input(f"Is the home country of the ticker you want {home_country_tickers[count_len_home_country].upper()} ?(Answer 'Yes' or 'No'): ")
                                    while home.upper() != "YES" and home.upper() != "NO":

                                        print("INVALID INPUT, ANSWER 'Yes' OR 'No'")
                                        home = input(f"Is the home country of the ticker you want {home_country_tickers[count_len_home_country].upper()} ?(Answer 'Yes' or 'No'): ")

                                    if home.upper() == "YES":

                                        home_country = home_country_tickers[count_len_home_country]
                                        break

                                    else: #NO

                                        count_len_home_country += 1

                                possible_tickers = [t for t in tickers_for_analysis if yf.Ticker(t).info['country'] == home_country]
                                possible_exchanges_long_name = []
                                possible_exchanges_short_name = []

                                for t in possible_tickers:

                                    try:

                                        lst_ticker_exchange = t.split(".")
                                        full_name = yf.Ticker(t).info['fullExchangeName']

                                    except KeyError :

                                        possible_tickers.remove(t)
                                        print(symbol,"WON'T BE CONSIDERED BECAUSE IT IS NOT IN AN EXCHANGE")

                                    else:

                                        possible_exchanges_long_name.append(full_name)
                                        possible_exchanges_short_name.append(lst_ticker_exchange[1])

                                print("Possible Tickers Exchanges are: ",possible_exchanges_long_name)

                                for tickr in possible_tickers:

                                    ticker_idx = possible_tickers.index(tickr)

                                    ticker_accept = input(f"The home country of ticker is '{home_country.upper()}' & the ticker {tickr} is quoted at '{possible_exchanges_long_name[ticker_idx].upper()}'-'{possible_exchanges_short_name[ticker_idx].upper()}', do you want to fetch this version of the ticker (answer 'Yes' or 'No'): ")
                                    if ticker_accept.upper() != "YES" and ticker_accept.upper() != "NO":

                                        print("INVALID INPUT ANSWER 'Yes' OR 'No'")
                                        ticker_accept = input(f"The home country of ticker is '{home_country.upper()}' & the ticker {tickr} is quoted at '{possible_exchanges_long_name[ticker_idx].upper()}'-'{possible_exchanges_short_name[ticker_idx].upper()}', do you want to fetch this version of the ticker (answer 'Yes' or 'No'): ")

                                    if ticker_accept.upper() == "YES":

                                        ticker = tickr
                                        tickers_lst.append(ticker)
                                        break

                        return tickers_lst

                else: #ind_tickers_or_etf == 1

                    directory_of_storage = input("DIRECTORY OF THE EXCEL FILE WITH THE ETF HOLDINGS: ")
                    directory_of_storage = directory_of_storage.strip('"')
                    suffix = Path(directory_of_storage).suffix

                    if suffix == ".csv" : #iShares or BlackRock excel

                        #GET THE TERMINATIONS OF EACH EXCHANGE FOR EUROPEAN TICKERS
                        exchanges_termination_dict = helpers.get_european_exchange_terminations()
                        tickers_lst = helpers.get_tickers_to_yf_from_excel_blackrock(directory_of_storage,exchanges_termination_dict)
                        return tickers_lst

                    else: #".xlsx"

                        dict_tickers = helpers.get_tickers_to_yf_from_excel_state_street(directory_of_storage)
                        tickers_lst = dict_tickers['usable_tickers']

                    return tickers_lst

        else: #NO

            ind_tickers_or_etf = int(input("DO YOU WANT TO USE INDIVIDUAL TICKERS SELECTED BY YOU (ANSWER 0) OR TICKERS FROM AN ETF (ANSWER 1): "))

            while ind_tickers_or_etf != 0 and ind_tickers_or_etf != 1:

                print("INVALID INPUT, ANSWER '0' FOR INDIVIDUAL TICKERS OR '1' FOR ETFS")
                ind_tickers_or_etf = int(input("DO YOU WANT TO USE INDIVIDUAL TICKERS SELECTED BY YOU (ANSWER 0) OR TICKERS FROM AN ETF (ANSWER 1): "))

            if ind_tickers_or_etf == 0:

                certainty_ticker = input("ARE YOU CERTAIN OF WHICH EXCHANGES YOU WANT FOR YOUR TICKERS? 'yfinance' USUALLY USES THE 'ticker.exchange_termination' TO IDENTIFY TICKERS AND THEIR EXCHANGES (ANSWER 'Yes' or 'No'): ")

                while certainty_ticker.upper() != "YES" and certainty_ticker.upper() != "NO":

                    print("INVALID INPUT, ANSWER EITHER 'Yes' IF YOU ARE CERTAIN OF THE EXCHANGE TERMINATION OF EACH TICKER & 'No' IF YOU ARE NOT")
                    certainty_ticker = input("ARE YOU CERTAIN OF WHICH EXCHANGES YOU WANT FOR YOUR TICKERS? 'yfinance' USUALLY USES THE 'ticker.exchange_termination' TO IDENTIFY TICKERS AND THEIR EXCHANGES (ANSWER 'Yes' or 'No'): ")

                if certainty_ticker.upper() == "YES" :

                    #INDIVIDUAL TICKERS
                    n_tickers = int(input("HOW MANY TICKERS, DO YOU WANT: "))
                    count_tickers_collected = 0
                    tickers_lst = []

                    while count_tickers_collected < n_tickers:

                        count_tickers_collected += 1
                        ticker = input(f"TICKER NAME {count_tickers_collected} (WITH EXCHANGE TERMINATION): ")
                        tickers_lst.append(ticker)

                    return tickers_lst

                else:

                    #INDIVIDUAL TICKERS
                    n_tickers = int(input("HOW MANY TICKERS, DO YOU WANT: "))
                    count_tickers_collected = 0
                    tickers_lst = []

                    while count_tickers_collected < n_tickers:

                        count_tickers_collected += 1
                        ticker = input(f"TICKER NAME {count_tickers_collected} (NO EXCHANGE TERMINATION): ")
                        ticker = ticker.upper()+"."
                        #DF WITH ALL THE SYMBOLS OF THE TICKER IN DIFFERENT EXCHANGES
                        ticker_references_df = yf.Lookup(ticker).get_stock(count=1000)
                        ticker_symbols = ticker_references_df.index
                        size_str_ticker = len(ticker)
                        tickers_for_analysis = []
                        home_country_tickers = []
                        for symbol in ticker_symbols:

                            if symbol[:size_str_ticker] == ticker:

                                try:

                                    home_country = yf.Ticker(symbol).info['country']

                                except KeyError:

                                    print(symbol,"WON'T BE CONSIDERED")

                                else:

                                    tickers_for_analysis.append(symbol)
                                    if home_country not in home_country_tickers:
                                        home_country_tickers.append(home_country)

                        print("Possible Tickers Home Countries are: ",home_country_tickers)
                        #GET COUNTRY INFO BECAUSE SOME COUNTRIES ARE QUOTED OUTSIDE OF THEIR HOME COUNTRY, TRY TO AVOID THOSE STOCKS
                        #CHOOSE THE HOME COUNTRY OF THE TICKER YOU WANT, DEFAULT WILL BE THE LAST ONE
                        count_len_home_country = 0
                        try:

                            home_country = home_country_tickers[len(home_country_tickers)-1] #last index

                        except IndexError:

                            print(f"Wanted ticker wasn't found by the Lookup Search so you need to get the ticker with exact exchange ,go to yahoo finance print {ticker} and try to find the exchange that you want to complete the ticker USE THAT IN THE NEXT INPUT ")
                            ticker = input(f"TICKER {count_tickers_collected} (ALREADY WITH THE .'exchange'): ")
                            tickers_lst.append(ticker)

                        else:

                            while count_len_home_country <= len(home_country_tickers):

                                home = input(f"Is the home country of the ticker you want {home_country_tickers[count_len_home_country].upper()} ?(Answer 'Yes' or 'No'): ")
                                while home.upper() != "YES" and home.upper() != "NO":

                                    print("INVALID INPUT, ANSWER 'Yes' OR 'No'")
                                    home = input(f"Is the home country of the ticker you want {home_country_tickers[count_len_home_country].upper()} ?(Answer 'Yes' or 'No'): ")

                                if home.upper() == "YES":

                                    home_country = home_country_tickers[count_len_home_country]
                                    break

                                else: #NO

                                    count_len_home_country += 1

                            possible_tickers = [t for t in tickers_for_analysis if yf.Ticker(t).info['country'] == home_country]
                            possible_exchanges_long_name = []
                            possible_exchanges_short_name = []

                            for t in possible_tickers:

                                try:

                                    lst_ticker_exchange = t.split(".")
                                    full_name = yf.Ticker(t).info['fullExchangeName']

                                except KeyError :

                                    possible_tickers.remove(t)
                                    print(symbol,"WON'T BE CONSIDERED BECAUSE IT IS NOT IN AN EXCHANGE")

                                else:

                                    possible_exchanges_long_name.append(full_name)
                                    possible_exchanges_short_name.append(lst_ticker_exchange[1])

                            print("Possible Tickers Exchanges are: ",possible_exchanges_long_name)

                            for tickr in possible_tickers:

                                ticker_idx = possible_tickers.index(tickr)

                                ticker_accept = input(f"The home country of ticker is '{home_country.upper()}' & the ticker {tickr} is quoted at '{possible_exchanges_long_name[ticker_idx].upper()}'-'{possible_exchanges_short_name[ticker_idx].upper()}', do you want to fetch this version of the ticker (answer 'Yes' or 'No'): ")
                                if ticker_accept.upper() != "YES" and ticker_accept.upper() != "NO":

                                    print("INVALID INPUT ANSWER 'Yes' OR 'No'")
                                    ticker_accept = input(f"The home country of ticker is '{home_country.upper()}' & the ticker {tickr} is quoted at '{possible_exchanges_long_name[ticker_idx].upper()}'-'{possible_exchanges_short_name[ticker_idx].upper()}', do you want to fetch this version of the ticker (answer 'Yes' or 'No'): ")

                                if ticker_accept.upper() == "YES":

                                    ticker = tickr
                                    tickers_lst.append(ticker)
                                    break

                    return tickers_lst

            else: #ind_tickers_or_etf == 1

                directory_of_storage = input("DIRECTORY OF THE EXCEL FILE WITH THE ETF HOLDINGS: ")
                directory_of_storage = directory_of_storage.strip('"')
                suffix = Path(directory_of_storage).suffix

                if suffix == ".csv" : #iShares or BlackRock excel

                    #GET THE TERMINATIONS OF EACH EXCHANGE FOR EUROPEAN TICKERS
                    exchanges_termination_dict = helpers.get_european_exchange_terminations()
                    tickers_lst = helpers.get_tickers_to_yf_from_excel_blackrock(directory_of_storage,exchanges_termination_dict)


                else: #".xlsx"

                    dict_tickers = helpers.get_tickers_to_yf_from_excel_state_street(directory_of_storage)
                    tickers_lst = dict_tickers['usable_tickers']

                return tickers_lst

def get_bs_hist(ticker:str,frequency:str):

    while frequency.lower() != "yearly" and frequency.lower() != "quarterly":

        print("WRONG INPUT USE 'yearly' FOR ANNUAL OR 'quarterly' FOR QUARTERLY AS INPUT")

        frequency = str(input("Annual - 'yearly' or Quarterly - 'quarterly'"))

    df = yf.Ticker(ticker).get_balance_sheet(freq=frequency)

    return df


def get_inc_stat_hist(ticker:str,frequency:str):

    while frequency.lower() != "yearly" and frequency.lower() != "quarterly":

        print("WRONG INPUT USE 'yearly' FOR ANNUAL OR 'quarterly' FOR QUARTERLY AS INPUT")

        frequency = str(input("Annual - 'yearly' or Quarterly - 'quarterly'"))

    df = yf.Ticker(ticker).get_income_stmt(freq=frequency)

    return df

def get_stat_cfs_hist(ticker:str,frequency:str):

    while frequency.lower() != "yearly" and frequency.lower() != "quarterly":

        print("WRONG INPUT USE 'yearly' FOR ANNUAL OR 'quarterly' FOR QUARTERLY AS INPUT")

        frequency = str(input("Annual - 'yearly' or Quarterly - 'quarterly'"))

    df = yf.Ticker(ticker).get_cash_flow(freq=frequency)

    return df


def get_dict_all_tickers_with_statements(dict_three_statements:dict,tickers_lst:list):

    for ticker in tickers_lst:

        print(ticker,"IS TRYING TO BE FETCHED BEING FETCHED")

        info_keys = yf.Ticker(ticker).info.keys()

        #ENSURE THE CURRENCY OF REPORTING OF THE TICKER IS KNOWN.
        if 'financialCurrency' not in info_keys and 'currency' not in info_keys:

            continue

        else:

            for key in dict_three_statements:

                print(key,":",ticker,)

                if key == 'bal_sheet':

                    df_bs = get_bs_hist(ticker,'yearly')
                    years_on_df = [df_bs.columns[i].year for i in range(len(df_bs.columns))]
                    years_appear = [years_on_df.count(years_on_df[i]) for i in range(len(years_on_df))]
                    one_appearance = years_appear.count(1)
                    no_exist = len(df_bs) == 0
                    dates_reporting_changed = one_appearance != len(years_appear)
                    if no_exist or dates_reporting_changed:

                        if no_exist:

                            print(ticker,"DOESN'T HAVE BAL_SHEET, IT WON'T ENTER IN THE DICT OF THREE STATEMENTS OF TICKERS")
                            break

                        else:

                            print(ticker,"CHANGED REPORTING YEARS, THEREFORE IT WON'T BE CONSIDERED")
                            break
                    else:

                        dict_three_statements["bal_sheet"][ticker] = df_bs

                elif key == 'inc_stat':

                    df_inc = get_inc_stat_hist(ticker,'yearly')
                    years_on_df = [df_inc.columns[i].year for i in range(len(df_inc.columns))]
                    years_appear = [years_on_df.count(years_on_df[i]) for i in range(len(years_on_df))]
                    one_appearance = years_appear.count(1)
                    no_exist = len(df_inc) == 0
                    dates_reporting_changed = one_appearance != len(years_appear)
                    if no_exist or dates_reporting_changed:

                        if no_exist:

                            print(ticker,"DOESN'T HAVE BAL_SHEET, IT WON'T ENTER IN THE DICT OF THREE STATEMENTS OF TICKERS")
                            break
                        else:

                            print(ticker,"CHANGED REPORTING YEARS, THEREFORE IT WON'T BE CONSIDERED")
                            break
                    else:

                        dict_three_statements["inc_stat"][ticker] = df_inc

                else: #'stat_cfs'

                    df_stat = get_stat_cfs_hist(ticker,'yearly')
                    years_on_df = [df_stat.columns[i].year for i in range(len(df_stat.columns))]
                    years_appear = [years_on_df.count(years_on_df[i]) for i in range(len(years_on_df))]
                    one_appearance = years_appear.count(1)
                    no_exist = len(df_stat) == 0
                    dates_reporting_changed = one_appearance != len(years_appear)
                    if no_exist or dates_reporting_changed:

                        if no_exist:

                            print(ticker,"DOESN'T HAVE BAL_SHEET, IT WON'T ENTER IN THE DICT OF THREE STATEMENTS OF TICKERS")
                            break
                        else:

                            print(ticker,"CHANGED REPORTING YEARS, THEREFORE IT WON'T BE CONSIDERED")
                            break
                    else:

                        dict_three_statements["stat_cfs"][ticker] = df_stat

    return dict_three_statements

def match_tickers_with_three_statements(dict_all_financials,tickers_lst:list):

    keys_bs = dict_all_financials['bal_sheet'].keys()
    keys_inc = dict_all_financials['inc_stat'].keys()
    keys_stat = dict_all_financials['stat_cfs'].keys()
    dict_three_statements = {'bal_sheet' : {}, 'inc_stat' : {}, 'stat_cfs' : {}}

    for ticker in tickers_lst:

        if ticker in keys_bs and ticker in keys_inc and ticker in keys_stat:

            dict_three_statements["bal_sheet"][ticker] = dict_all_financials["bal_sheet"][ticker]
            dict_three_statements["inc_stat"][ticker] = dict_all_financials["inc_stat"][ticker]
            dict_three_statements["stat_cfs"][ticker] = dict_all_financials["stat_cfs"][ticker]

    return dict_three_statements

def dict_excluding_financial_services(dict_three_statements:dict):

    lst_tickers = dict_three_statements['bal_sheet'].keys()
    usable_tickers = []
    non_usable_tickers = []
    refurbished_dict_three_statements = {'bal_sheet' : {}, 'inc_stat' : {}, 'stat_cfs' : {}}

    for ticker in lst_tickers:

        df_bs = dict_three_statements['bal_sheet'][ticker]
        if "CashCashEquivalentsAndFederalFundsSold" not in df_bs.index and "CurrentAssets" in df_bs.index and "TotalLiabilitiesNetMinorityInterest" in df_bs.index and "CurrentLiabilities" in df_bs.index:
            usable_tickers.append(ticker)

        else:

            print("TICKER",ticker,"WON'T BE CONSIDERED BECAUSE IT IS RELATED TO FINANCIAL SERVICES")
            non_usable_tickers.append(ticker)

    for ticker in usable_tickers:

        refurbished_dict_three_statements["bal_sheet"][ticker] = dict_three_statements['bal_sheet'][ticker]
        refurbished_dict_three_statements["inc_stat"][ticker] = dict_three_statements['inc_stat'][ticker]
        refurbished_dict_three_statements["stat_cfs"][ticker] = dict_three_statements['stat_cfs'][ticker]

    return refurbished_dict_three_statements


def parquet_to_df(path_to_parquet_files:str,ticker:str):

    path = Path(path_to_parquet_files)
    for file in path.glob("*.parquet"):

        if file.stem == ticker:
            break
        else:

            continue

    return pd.read_parquet(file)

def addition_on_financial_statements(dict_three_financials_included:dict,tickers_in_usage:list,directory_for_storage_or_retrieval):

    currencies = ["EUR","USD","GBP","GBp","CHF","NOK","SEK","DKK","HUF","CZK","PLN","RUB","NZD","CAD","AUD","JPY","CNH","CNY","RON","BRL","TRY","SGD","HOK","MXM","ZAR","ILS","INR","AED","SAR"]
    dict_inc_stat_tickers = dict_three_financials_included['inc_stat']
    tickers = list(dict_inc_stat_tickers.keys())
    new_tickers = list()
    #DIRECTORY TO SEE EACH TICKERS ALREADY EXIST
    path_inc_stat = Path(directory_for_storage_or_retrieval+r"\inc_stat")
    #ADDITIONS THE INCOME STATEMENT, SHOULD ALSO ADD THE CURRENCY IN WHICH PRICE IS CONSIDERED
    path_exists = path_inc_stat.exists()
    if path_exists: #SOME TICKERS ALREADY EXIST

        tickers_already_stored = list()

        for file in path_inc_stat.iterdir():

            ticker_stored = file.stem
            tickers_already_stored.append(ticker_stored)

        for ticker in tickers_in_usage:

            if ticker not in tickers_already_stored:

                print(ticker,"IS A NEW TICKER, NEVER WAS STORED")
                new_tickers.append(ticker)

        #CONDUCT UPDATES ONLY ON NEW TICKERS

        prices_near_reporting(dict_inc_stat_tickers,new_tickers)
        time.sleep(30)

        for ticker in tickers_in_usage:

            if ticker not in new_tickers:

                print("TICKER:",ticker,"ALREADY HAS PRICING ADJUSTMENTS AND MARKET CAPS ON ITS DF, SO NO NEED FOR ADJUSTMENTS")

            else:

                df_new_ticker = dict_inc_stat_tickers[ticker]
                len_cols = len(df_new_ticker.columns)
                cols = list(df_new_ticker.columns)
                curr_in_numb_price = [currencies.index(df_new_ticker.at["Currency used in Pricing",cols[i]]) for i in range(len_cols)]
                curr_in_numb_fin_rep = [currencies.index(df_new_ticker.at["Currency used in Financial Reporting",cols[i]]) for i in range(len_cols)]
                df_new_ticker = df_new_ticker.astype(object)
                df_new_ticker.loc["Currency used in Pricing"] = curr_in_numb_price
                df_new_ticker.loc["Currency used in Financial Reporting"] = curr_in_numb_fin_rep
                df_new_ticker.loc["Currency used in Pricing"] = df_new_ticker.loc["Currency used in Pricing"].astype(np.float64)
                df_new_ticker.loc["Currency used in Financial Reporting"] = df_new_ticker.loc["Currency used in Financial Reporting"].astype(int)
                #NEEDS TO TURN THE INDEXES RELATED TO CURRENCY IN NUMERIC TO BE USED LATER TO TRANSFORM INTO THE FINVIZ EQUIVALENT
                mkcap_list = []

                try:
                    mcap = yf.Ticker(ticker).info["marketCap"]

                except KeyError:

                    print("CURRENT MARKET CAP OF TICKER",ticker,"IS NOT AVAILABLE AT yfinance")
                    mkcap_list = [np.nan for i in range(len_cols)]
                    time.sleep(0.3 + random.uniform(0, 0.3))

                else:

                    mkcap_in_millions = mcap / 1000000
                    mkcap_list.append(mkcap_in_millions) #TO PUT MKCAP IN MILLIONS
                    for i in range(len_cols-1):
                        mkcap_list.append(np.nan)
                    time.sleep(0.3 + random.uniform(0, 0.3))

                df_new_ticker.loc["MkCap"] = mkcap_list
                df_new_ticker.loc["MkCap"] = df_new_ticker.loc["MkCap"].astype(np.float64)
                dict_inc_stat_tickers[ticker] = df_new_ticker

    else: #EVERY TICKER DIDN'T EXIST BEFORE NON-EXISTENT PATH, NO NEED TO CREATE, BECAUSE WHENEVER STORAGE OCCUR IT WILL BE CREATED

        prices_near_reporting(dict_inc_stat_tickers,tickers)

        for ticker in tickers:

            print("STORAGE PATH DIDN'T EXIST, SO",ticker,"CACHING WASN'T AVAILABLE")
            df_new_ticker = dict_inc_stat_tickers[ticker]
            len_cols = len(df_new_ticker.columns)
            cols = df_new_ticker.columns
            curr_in_numb_price = [currencies.index(df_new_ticker.at["Currency used in Pricing",cols[i]]) for i in range(len_cols)]
            curr_in_numb_fin_rep = [currencies.index(df_new_ticker.at["Currency used in Financial Reporting",cols[i]]) for i in range(len_cols)]
            df_new_ticker = df_new_ticker.astype(object)
            df_new_ticker.loc["Currency used in Pricing"] = curr_in_numb_price
            df_new_ticker.loc["Currency used in Financial Reporting"] = curr_in_numb_fin_rep
            df_new_ticker.loc["Currency used in Pricing"] = df_new_ticker.loc["Currency used in Pricing"].astype(int)
            df_new_ticker.loc["Currency used in Financial Reporting"] = df_new_ticker.loc["Currency used in Financial Reporting"].astype(int)
            #NEEDS TO TURN THE INDEXES RELATED TO CURRENCY IN NUMERIC TO BE USED LATER TO TRANSFORM INTO THE FINVIZ EQUIVALENT
            mkcap_list = []

            try:
                mcap = yf.Ticker(ticker).info["marketCap"]

            except KeyError:

                print("CURRENT MARKET CAP OF TICKER",ticker,"IS NOT AVAILABLE AT yfinance")
                mkcap_list = [np.nan for i in range(len_cols)]
                time.sleep(0.3 + random.uniform(0, 0.3))

            else:

                mkcap_in_millions = mcap / 1000000
                mkcap_list.append(mkcap_in_millions) #TO PUT MKCAP IN MILLIONS
                for i in range(len_cols-1):
                    mkcap_list.append(np.nan)
                time.sleep(0.3 + random.uniform(0, 0.3))

            df_new_ticker.loc["MkCap"] = mkcap_list
            df_new_ticker.loc["MkCap"] = df_new_ticker.loc["MkCap"].astype(np.float64)
            dict_inc_stat_tickers[ticker] = df_new_ticker



    #ALSO ADD CHANGES TO THE BALANCE SHEET LIKE INCLUDING THE REPORTING CURRENCY OF FINANCIALS

def add_on_financials_after_updates(tickers_for_update:list,directory_for_storage_or_retrieval):

    currencies = ["EUR","USD","GBP","GBp","CHF","NOK","SEK","DKK","HUF","CZK","PLN","RUB","NZD","CAD","AUD","JPY","CNH","CNY","RON","BRL","TRY","SGD","HOK","MXM","ZAR","ILS","INR","AED","SAR"]

    #TICKERS HAVE ALREADY BEEN COLLECTED, SO PRICING INDEXES ARE ALREADY IN NUMBERS

    dict_inc_stat_updated_tickers = dict()
    #READ THE PARQUET AND TURN INTO A DICT AND TICKERS COLLECTION
    for ticker in tickers_for_update:

        #GET SAVED DF
        str_path = rf"{directory_for_storage_or_retrieval}\inc_stat"
        ticker_saved_financial = parquet_to_df(str_path,ticker)
        dict_inc_stat_updated_tickers[ticker] = ticker_saved_financial
        #ALREADY WITH THE PRICING INDEXES AND MKCAP

    #ADD THE PRICES UPDATES

    prices_near_reporting(dict_inc_stat_updated_tickers,tickers_for_update)
    #PREVIOUS FUNCTION SHOULD ENSURE THAT PRICING INDEXES ARE TURNED INTO STRs WITH THE CURRENCIES
    time.sleep(30)

    #STORAGE THE TICKERS ONCE AGAIN
    print(tickers_for_update)
    for ticker in tickers_for_update:

        print("PRICES OF TICKER",ticker,"WERE UPDATED AND DF OF INCOME STATEMENT WILL BE RE-STORED.")

        df_to_be_stored = dict_inc_stat_updated_tickers[ticker]
        #PRICING INDEXES SHOULD BE ONCE AGAIN IN STR 'EUR','GBP' AND SO ON
        len_cols = len(df_to_be_stored.columns)
        cols = list(df_to_be_stored.columns)
        curr_in_numb_price = [currencies.index(df_to_be_stored.at["Currency used in Pricing",cols[i]]) for i in range(len_cols)]
        curr_in_numb_fin_rep = [currencies.index(df_to_be_stored.at["Currency used in Financial Reporting",cols[i]]) for i in range(len_cols)]
        df_to_be_stored = df_to_be_stored.astype(object)
        df_to_be_stored.loc["Currency used in Pricing"] = curr_in_numb_price
        df_to_be_stored.loc["Currency used in Financial Reporting"] = curr_in_numb_fin_rep
        mkcap_list = []

        try:
            mcap = yf.Ticker(ticker).info["marketCap"]

        except KeyError:

            print("CURRENT MARKET CAP OF TICKER",ticker,"IS NOT AVAILABLE AT yfinance")
            mkcap_list = [np.nan for i in range(len_cols)]
            time.sleep(0.3 + random.uniform(0, 0.3))

        else:

            mkcap_in_millions = mcap / 1000000
            mkcap_list.append(mkcap_in_millions) #TO PUT MKCAP IN MILLIONS
            for i in range(len_cols-1):
                mkcap_list.append(np.nan)
            time.sleep(0.3 + random.uniform(0, 0.3))

        df_to_be_stored.loc["MkCap"] = mkcap_list
        df_to_be_stored.loc["MkCap"] = df_to_be_stored.loc["MkCap"].astype(np.float64)

        dict_inc_stat_updated_tickers[ticker] = df_to_be_stored


        folder_path = Path(rf"{directory_for_storage_or_retrieval}/inc_stat")
        specific_ticker_path = Path(rf"{folder_path}/{ticker}.parquet")

        for file in specific_ticker_path.iterdir():

            #REMOVAL OF THE PREVIOUS FILE
            file.unlink()

        end_point = specific_ticker_path / rf"{ticker}.parquet"
        temp_end_point = specific_ticker_path / rf"{ticker}.parquet.tmp"

        #THIS IS DONE TO AVOID FILE CORRUPTION IF SCRIPT IS STOPPED MIDTIME
        df_to_be_stored.to_parquet(temp_end_point, engine="pyarrow", index=True)

        os.replace(temp_end_point,end_point)


def create_and_store_or_update_tickers_parquet_files_from_df_financials(dict_three_financials_to_transform:dict,tickers_lst:list,path_for_folder):

    path_for_folder = path_for_folder.strip('"')

    updated_tickers = []

    n_tickers = len(tickers_lst)

    #CREATE DIRECTORIES IF NEEDED
    Path(path_for_folder).mkdir(exist_ok=True)
    Path(rf"{path_for_folder}/bal_sheet").mkdir(exist_ok=True)
    Path(rf"{path_for_folder}/inc_stat").mkdir(exist_ok=True)
    Path(rf"{path_for_folder}/stat_cfs").mkdir(exist_ok=True)

    if len(dict_three_financials_to_transform['bal_sheet']) == 0:

        for key in dict_three_financials_to_transform:

            folder_path = Path(rf"{path_for_folder}/{key}")

            for n in range(n_tickers):

                #GET SAVED DF
                str_path = rf"{path_for_folder}\{key}"
                ticker_saved_financial = parquet_to_df(str_path,tickers_lst[n])
                dict_three_financials_to_transform[key][tickers_lst[n]] = ticker_saved_financial

        add_on_financials_after_updates(tickers_lst,path_for_folder)

    else:

        for key in dict_three_financials_to_transform:

            folder_path = Path(rf"{path_for_folder}/{key}")

            for n in range(n_tickers):

                if folder_path.exists(): #PATH EXISTS

                    specific_ticker_path = Path(rf"{folder_path}/{tickers_lst[n]}.parquet")

                    if specific_ticker_path.exists(): #NEEDS UPDATE - BOTH PATH FOR THE FINANCIAL STATEMENT AND FOR THE TICKER EXIST.

                        print(tickers_lst[n],key,"exists but an update might be needed")

                        #VALUES EXIST BUT ARE UPDATED

                        #GET SAVED DF
                        str_path = rf"{path_for_folder}\{key}"
                        ticker_saved_financial = parquet_to_df(str_path,tickers_lst[n])
                        df_fetched = dict_three_financials_to_transform[key][tickers_lst[n]]

                        #IF NEW VALUES APPEAR, THE IDEA ISN'T TO LOSE THE OLDEST VALUE, SO ADD INTO THE DF THOSE VALUES

                        #COLUMNS ON THE STORED DF
                        oldest_df_periods = list(ticker_saved_financial.columns)
                        #COLUMNS ON THE MOST RECENT DF
                        recent_df_periods = list(df_fetched.columns)

                        #COLUMNS THAT WILL BE ADDED TO DF
                        for period in oldest_df_periods:

                            if period not in recent_df_periods:

                                recent_df_periods.append(period)

                        df_periods_not_in_recent_df = df_fetched

                        n_cols_added = len(recent_df_periods) - len(df_fetched.columns)

                        if n_cols_added != 0:

                            print(ticker,"will need an update, the",key,"has new values in yfinance")
                            #IT IS AN EXISTING TICKER, BUT THERE
                            ticker = tickers_lst[n]
                            if ticker not in updated_tickers:

                                updated_tickers.append(ticker)

                            for i in range(len(df_fetched.columns),len(df_fetched.columns) + n_cols_added):

                                #COLUMNS TO BE ADDED ARE TRANSFORMED INTO DF
                                #MIGHT RUN INTO THE PROBLEM WHERE COLUMNS DO NOT HAVE THE SAME Nº OF INDEXES, NEED TO SOLVE THAT
                                period = recent_df_periods[i]
                                col_df = ticker_saved_financial[period].to_frame()
                                df_periods_not_in_recent_df = pd.concat([df_periods_not_in_recent_df,col_df],axis=1)

                            df_to_be_stored = df_periods_not_in_recent_df

                            for file in specific_ticker_path.iterdir():

                                #REMOVAL OF THE PREVIOUS FILE
                                file.unlink()

                            end_point = specific_ticker_path / rf"{tickers_lst[n]}.parquet"
                            temp_end_point = specific_ticker_path / rf"{tickers_lst[n]}.parquet.tmp"

                            #THIS IS DONE TO AVOID FILE CORRUPTION IF SCRIPT IS STOPPED MIDTIME
                            df_to_be_stored.to_parquet(temp_end_point, engine="pyarrow", index=True)

                            os.replace(temp_end_point,end_point)

                        else: #df_fetched doesn't have the adjustments that other tickers have regarding prices

                            print(tickers_lst[n],"won't be updated as its",key,"is matching in yfinance and the cached values.")
                            index_df_fetched = df_fetched.index
                            cond_to_update = "Currency used in Pricing" not in index_df_fetched

                            if cond_to_update:

                                ticker = tickers_lst[n]
                                if ticker not in updated_tickers:

                                    updated_tickers.append(ticker)

                                for file in specific_ticker_path.iterdir():

                                    #REMOVAL OF THE PREVIOUS FILE
                                    file.unlink()

                                end_point = specific_ticker_path / rf"{tickers_lst[n]}.parquet"
                                temp_end_point = specific_ticker_path / rf"{tickers_lst[n]}.parquet.tmp"

                                #THIS IS DONE TO AVOID FILE CORRUPTION IF SCRIPT IS STOPPED MIDTIME
                                df_fetched.to_parquet(temp_end_point, engine="pyarrow", index=True)

                                os.replace(temp_end_point,end_point)

                    else: #PATH EXISTS FOR THE FINANCIAL STATEMENT BUT NOT FOR THE TICKER

                        print("Storage exists, but ticker",tickers_lst[n],"didn't have any cached files for",key)
                        #THAT PATH IS CREATED WITH THE VALUES
                        specific_ticker_path.mkdir(exist_ok=True)
                        ticker_statement = dict_three_financials_to_transform[key][tickers_lst[n]]
                        end_point = specific_ticker_path / rf"{tickers_lst[n]}.parquet"
                        temp_end_point = specific_ticker_path / rf"{tickers_lst[n]}.parquet.tmp"
                        #THIS IS DONE TO AVOID FILE CORRUPTION IF SCRIPT IS STOPPED MIDTIME
                        ticker_statement.to_parquet(temp_end_point, engine="pyarrow", index=True)
                        os.replace(temp_end_point,end_point)

                else: #PATH DOESN'T EXIST FOR THE FINANCIAL

                    #PATH IS CREATED AND VALUES ARE IMPRINTED
                    folder_path.mkdir(exist_ok=True) #CREATE THE PATH
                    ticker_statement = dict_three_financials_to_transform[key][tickers_lst[n]]
                    end_point = folder_path / rf"{tickers_lst[n]}.parquet"
                    temp_end_point = folder_path / rf"{tickers_lst[n]}.parquet.tmp"
                    #THIS IS DONE TO AVOID FILE CORRUPTION IF SCRIPT IS STOPPED MIDTIME
                    ticker_statement.to_parquet(temp_end_point, engine="pyarrow", index=True)
                    os.replace(temp_end_point,end_point)

        #PRINT THE LIST OF UPDATED TICKERS
        add_on_financials_after_updates(updated_tickers,path_for_folder)

def updated_parquet_to_df(path_to_financials:str,tickers_lst:list,bs_map,bs_map_index,inc_stat_map,inc_stat_map_index,stat_cfs_map,stat_cfs_map_index):

    currencies = ["EUR","USD","GBP","GBp","CHF","NOK","SEK","DKK","HUF","CZK","PLN","RUB","NZD","CAD","AUD","JPY","CNH","CNY","RON","BRL","TRY","SGD","HOK","MXM","ZAR","ILS","INR","AED","SAR"]

    path_to_financials = path_to_financials.strip('"')

    dict_all_tickers_all_financials_updated = {'bal_sheet' : dict(), 'inc_stat' : dict(), 'stat_cfs' : dict()}

    tickers_available = []

    for key in dict_all_tickers_all_financials_updated:

        for n in range(len(tickers_lst)):

            ticker = tickers_lst[n]

            path = Path(f"{path_to_financials}/{key}/{ticker}.parquet")

            if path.exists():

                print("Turning",key,"from parquet to DF from the ticker",ticker)

                saved_df = pd.read_parquet(path)

                #PERFORM CHANGES ON THE DF FOR THEM TO BE WORKABLE

                if key == 'bal_sheet':

                    #OUTSIDE OF THE FUNCTIONS THE DEFINE SOME VARIABLES WITH THE MAP
                    #THINK THAT 'bs_map_index' AS ONE VARIABLE

                    dict_values_per_column = getting_values_for_each_column_of_statement(bs_map,saved_df)
                    df = final_df_bal_sheet(dict_values_per_column,bs_map_index)
                    dict_all_tickers_all_financials_updated["bal_sheet"][ticker] = df


                elif key == 'inc_stat':

                    #OUTSIDE OF THE FUNCTIONS THE DEFINE SOME VARIABLES WITH THE MAP
                    #THINK THAT 'inc_stat_map_index' AS ONE VARIABLE

                    #saved_df.loc["Currency used in Pricing"] = saved_df.loc["Currency used in Pricing"].astype(int)
                    #saved_df.loc["Currency used in Financial Reporting"] = saved_df.loc["Currency used in Financial Reporting"].astype(int)
                    #saved_df.loc["Currency used in Pricing"] = [currencies[int(saved_df.at["Currency used in Pricing",cols[i]])] for i in range(cols_len)]
                    #saved_df.loc["Currency used in Financial Reporting"] = [currencies[int(saved_df.at["Currency used in Financial Reporting",cols[i]])] for i in range(cols_len)]

                    dict_values_per_column = getting_values_for_each_column_of_statement(inc_stat_map,saved_df)
                    df = final_df_inc_stat(dict_values_per_column,inc_stat_map_index)
                    cols_len = len(df.columns)
                    cols = df.columns
                    df.loc["Currency of Prices"] = [currencies[int(df.loc["Currency of Prices",cols[i]])] for i in range(cols_len)]
                    df.loc["Currency of Financial Reporting"] = [currencies[int(df.loc["Currency of Financial Reporting",cols[i]])] for i in range(cols_len)]
                    dict_all_tickers_all_financials_updated["inc_stat"][ticker] = df

                else: #'stat_cfs'

                    #OUTSIDE OF THE FUNCTIONS THE DEFINE SOME VARIABLES WITH THE MAP
                    #THINK THAT 'stat_cfs_map_index' AS ONE VARIABLE

                    dict_values_per_column = getting_values_for_each_column_of_statement(stat_cfs_map,saved_df)
                    df = final_df_stat_cfs(dict_values_per_column,stat_cfs_map_index)
                    dict_all_tickers_all_financials_updated["stat_cfs"][ticker] = df

                tickers_available.append(ticker)

            else:

                print(f"{ticker} FINANCIALS WERE NOT FOUND")

    #PUT THE PRICING IN EUROS
    dict_all_tickers_all_financials_updated = match_fin_reporting_and_prices_to_same_currency_euro(dict_all_tickers_all_financials_updated)

    #UPDATE THE TICKER
    add_ons_to_df_inc_stat(dict_all_tickers_all_financials_updated["inc_stat"],tickers_available)
    add_ons_to_df_bal_sheet(dict_all_tickers_all_financials_updated["bal_sheet"],dict_all_tickers_all_financials_updated["inc_stat"],tickers_available)

    return dict_all_tickers_all_financials_updated

def getting_values_for_each_column_of_statement(fin_statement_map:dict,fin_stat_ticker_df:pd.DataFrame):

    columns_for_df = fin_stat_ticker_df.columns
    index_for_df = fin_statement_map.keys()
    vals_for_each_col = {}
    dict_equivalent_matching = {}

    """I NEED A DICT OF THIS FORMAT FOR PD.DATAFRAME.FROM_DICT

       {fy : [val1,val2],fy : [val1,val2]}, where fy will be the column and val1..valN will be the values for the indexes


    """

    for fy in columns_for_df:

        vals_for_each_col[fy] = []
        dict_equivalent_matching[fy] = dict()

        for key in index_for_df:

            dict_equivalent_matching[fy][key] = ""

            method_worked = False

            #print(key)
            var_tuple = fin_statement_map[key]

            for cal_method_var_used in var_tuple:

                method = cal_method_var_used[0]
                index_fin_stat_ticker = fin_stat_ticker_df.index

                if method == "direct":

                    possible_vars = cal_method_var_used[1]
                    #print(possible_vars)
                    any_var_in_df = False

                    for var in possible_vars:

                        #print(var)

                        if var in index_fin_stat_ticker :

                            nan_val = np.isnan(fin_stat_ticker_df.at[var,fy])
                            value = np.nan if nan_val else fin_stat_ticker_df.at[var,fy]
                            if value != np.nan :
                                dict_equivalent_matching[fy][key] = var
                                any_var_in_df = True
                                method_worked = True
                                vals_for_each_col[fy].append(value)
                                break

                    if any_var_in_df == True:

                        #STOP THE LOOP ON 'cal_method_var_used'
                        break

                elif method == "sum":

                    lst_val_to_sum = []
                    possible_vars = cal_method_var_used[1]
                    any_var_in_df = False

                    for var in possible_vars:

                        if var in index_fin_stat_ticker :

                            nan_val = np.isnan(fin_stat_ticker_df.at[var,fy])
                            value = np.nan if nan_val else fin_stat_ticker_df.at[var,fy]
                            if value != np.nan :

                                any_var_in_df = True
                                method_worked = True
                                if dict_equivalent_matching[fy][key] == "":

                                    dict_equivalent_matching[fy][key] = var

                                else:

                                    dict_equivalent_matching[fy][key] = dict_equivalent_matching[fy][key] + "+" + var
                            lst_val_to_sum.append(value)

                    if any_var_in_df == True:

                        #STOP THE LOOP ON 'cal_method_var_used'
                        vals_for_each_col[fy].append(sum(lst_val_to_sum))
                        break

                else: #method == "residual"

                    name_var_to_subract_from = cal_method_var_used[1]

                    if type(name_var_to_subract_from) == str:

                        dict_equivalent_matching[fy][key] = name_var_to_subract_from

                        try:

                            value_to_subtract_from = fin_stat_ticker_df.at[name_var_to_subract_from,fy]

                        except KeyError:

                            print(name_var_to_subract_from,"IS NOT PRESENT IN THE FINANCIAL STATEMENT THAT IS BEING FETCHED")

                        else:

                            nan_val = np.nan if np.isnan(value_to_subtract_from) else value_to_subtract_from
                            possible_vars = cal_method_var_used[2]
                            definitive_vars = []
                            for var in possible_vars:

                                if type(var) == str:

                                    definitive_vars.append(var)

                                else: #type dict

                                    var_to_be_calculated = list(var.keys())[0]
                                    var_in_yf_df = dict_equivalent_matching[fy][var_to_be_calculated]

                                    if var_in_yf_df == "None":

                                        continue

                                    else:

                                        definitive_vars.append(var_in_yf_df)

                            for var in definitive_vars:

                                if var in index_fin_stat_ticker:

                                    value = fin_stat_ticker_df.at[var,fy]
                                    nan_val = np.isnan(value)
                                    value = np.nan if nan_val else value
                                    if value != np.nan :
                                        dict_equivalent_matching[fy][key] = dict_equivalent_matching[fy][key] + "-" + var
                                    value_to_subtract_from = value_to_subtract_from - value

                            if value_to_subtract_from <= 0:

                                continue

                            else:

                                method_worked = True
                                vals_for_each_col[fy].append(value_to_subtract_from)

                    else: #dict

                        name_var_to_subract_from = list(cal_method_var_used[1].keys())[0] # 'cal_method_var_used[1]' IT IS A DICT
                        name_var_to_subract_from = dict_equivalent_matching[fy][name_var_to_subract_from]
                        dict_equivalent_matching[fy][key] = name_var_to_subract_from

                        try:

                            value_to_subtract_from = fin_stat_ticker_df.at[name_var_to_subract_from,fy]

                        except KeyError:

                            print(name_var_to_subract_from,"IS NOT PRESENT IN THE FINANCIAL STATEMENT THAT IS BEING FETCHED")

                        else:

                            nan_val = np.nan if np.isnan(value_to_subtract_from) else value_to_subtract_from
                            possible_vars = cal_method_var_used[2]
                            definitive_vars = []
                            for var in possible_vars:

                                if type(var) == str:

                                    definitive_vars.append(var)

                                else: #type dict

                                    var_to_be_calculated = list(var.keys())[0]
                                    var_in_yf_df = dict_equivalent_matching[fy][var_to_be_calculated]

                                    if var_in_yf_df == "None":

                                        continue

                                    else:

                                        definitive_vars.append(var_in_yf_df)

                            for var in definitive_vars:

                                if var in index_fin_stat_ticker:

                                    value = fin_stat_ticker_df.at[var,fy]
                                    nan_val = np.isnan(value)
                                    value = np.nan if nan_val else value
                                    if value != np.nan :
                                        dict_equivalent_matching[fy][key] = dict_equivalent_matching[fy][key] + "-" + var
                                    value_to_subtract_from = value_to_subtract_from - value

                            if value_to_subtract_from <= 0:

                                continue

                            else:

                                method_worked = True
                                vals_for_each_col[fy].append(value_to_subtract_from)

            if method_worked == False:

                vals_for_each_col[fy].append(np.float64(np.nan))
                dict_equivalent_matching[fy][key] = "None"

    return vals_for_each_col


def create_ticker_bal_sheet_proxy_finviz(bal_sheet_map:dict,bal_sheet_ticker:pd.DataFrame):

    columns_for_df = bal_sheet_ticker.columns
    index_for_df = bal_sheet_map.keys()
    vals_for_each_col = {}
    dict_equivalent_matching = {}

    for fy in columns_for_df:

        vals_for_each_col[fy] = []
        dict_equivalent_matching[fy] = dict()

        for key in index_for_df:

            dict_equivalent_matching[fy][key] = ""
            method = bal_sheet_map[key][0]
            index_bal_sheet_ticker = bal_sheet_ticker.index

            if method == "direct":

                possible_vars = bal_sheet_map[key][1]
                any_var_in_df = False

                for var in possible_vars:

                    if var in index_bal_sheet_ticker :

                        nan_val = np.isnan(bal_sheet_ticker.at[var,fy])
                        value = 0 if nan_val else bal_sheet_ticker.at[var,fy]
                        if value != 0 :
                            dict_equivalent_matching[fy][key] = var
                            any_var_in_df = True
                            vals_for_each_col[fy].append(value)
                        break

                if any_var_in_df == False:

                    vals_for_each_col[fy].append("NO VALUES FOR METRIC")
                    dict_equivalent_matching[fy][key] = "None"

            elif method == "sum":

                lst_val_to_sum = []
                possible_vars = bal_sheet_map[key][1]
                any_var_in_df = False

                for var in possible_vars:

                    if var in index_bal_sheet_ticker :

                        nan_val = np.isnan(bal_sheet_ticker.at[var,fy])
                        value = 0 if nan_val else bal_sheet_ticker.at[var,fy]
                        if value != 0 :

                            any_var_in_df = True
                            if dict_equivalent_matching[fy][key] == "":

                                dict_equivalent_matching[fy][key] = var

                            else:

                                dict_equivalent_matching[fy][key] = dict_equivalent_matching[fy][key] + "+" + var
                        lst_val_to_sum.append(value)

                if any_var_in_df == False:

                    vals_for_each_col[fy].append("NO VALUES FOR METRIC")
                    dict_equivalent_matching[fy][key] = "None"

                else:

                    vals_for_each_col[fy].append(sum(lst_val_to_sum))

            else: #method == "residual"

                name_var_to_subract_from = bal_sheet_map[key][1]
                dict_equivalent_matching[fy][key] = name_var_to_subract_from
                value_to_subtract_from = bal_sheet_ticker.at[name_var_to_subract_from,fy]
                nan_val = 0 if np.isnan(value_to_subtract_from) else value_to_subtract_from
                possible_vars = bal_sheet_map[key][2]
                definitive_vars = []
                for var in possible_vars:

                    if type(var) == str:

                        definitive_vars.append(var)

                    else: #type dict

                        var_to_be_calculated = list(var.keys())[0]
                        var_in_yf_df = dict_equivalent_matching[fy][var_to_be_calculated]

                        if var_in_yf_df == "None":

                            continue

                        else:

                            definitive_vars.append(var_in_yf_df)

                for var in definitive_vars:

                    if var in index_bal_sheet_ticker:

                        value = bal_sheet_ticker.at[var,fy]
                        nan_val = np.isnan(value)
                        value = 0 if nan_val else value
                        if value != 0 :
                            dict_equivalent_matching[fy][key] = dict_equivalent_matching[fy][key] + "-" + var
                        value_to_subtract_from = value_to_subtract_from - value

                if value_to_subtract_from == 0:

                    vals_for_each_col[fy].append("NO VALUES FOR METRIC")

                else:

                    vals_for_each_col[fy].append(value_to_subtract_from)

    return vals_for_each_col

def final_df_bal_sheet(dict_values_per_column:dict,df_bal_index):

    df_period_end = pd.DataFrame(data=[dict_values_per_column.keys()],columns=dict_values_per_column.keys(),index=['Period End Date'])
    df = pd.DataFrame.from_dict(dict_values_per_column)
    df = df.apply(pd.to_numeric, errors='coerce') / 1000000 #VALUES IN MILLIONS
    df.index = df_bal_index
    df = pd.concat([df_period_end,df],axis=0)
    df.loc['Period End Date'] = pd.to_datetime(df.loc['Period End Date']).dt.date
    df_idx_lst = list(df.index)
    tot_assets_vals = df.loc['Total Current Assets'].copy()
    other_c_assets_vals = df.loc['Other Current Assets'].copy()
    df.loc['Total Current Assets'] = other_c_assets_vals
    df.loc['Other Current Assets'] = tot_assets_vals
    idx_ebt = df_idx_lst.index('Total Current Assets')
    df_idx_lst[idx_ebt] = "Other Current Assets"
    df_idx_lst[idx_ebt+1] = "Total Current Assets"
    df.index = df_idx_lst

    series_time = df.loc['Period End Date']
    fys = []
    for date in series_time:

        month = date.month
        if month < 6:

            fy = f"FY {int(date.year) - 1}"

        else:

            fy = f"FY {date.year}"

        fys.append(fy)

    df.columns = fys

    return df


def create_ticker_inc_stat_proxy_finviz(inc_stat_map:dict,inc_stat_ticker:pd.DataFrame):

    columns_for_df = inc_stat_ticker.columns
    index_for_df = inc_stat_map.keys()
    vals_for_each_col = {}
    dict_equivalent_matching = {}

    for fy in columns_for_df:

        vals_for_each_col[fy] = []
        dict_equivalent_matching[fy] = dict()

        for key in index_for_df:

            dict_equivalent_matching[fy][key] = ""
            method = inc_stat_map[key][0]
            index_inc_stat_ticker = inc_stat_ticker.index

            if method == "direct":

                possible_vars = inc_stat_map[key][1]
                any_var_in_df = False

                for var in possible_vars:

                    if var in index_inc_stat_ticker :

                        nan_val = np.isnan(inc_stat_ticker.at[var,fy])
                        value = 0 if nan_val else inc_stat_ticker.at[var,fy]
                        if value != 0 :
                            dict_equivalent_matching[fy][key] = var
                            any_var_in_df = True
                            vals_for_each_col[fy].append(value)
                        break

                if any_var_in_df == False:

                    vals_for_each_col[fy].append("NO VALUES FOR METRIC")
                    dict_equivalent_matching[fy][key] = "None"

            else: #method == "residual"

                name_var_to_subract_from = list(inc_stat_map[key][1])[0] #IT IS A DICT
                name_var_to_subract_from = dict_equivalent_matching[fy][name_var_to_subract_from]
                dict_equivalent_matching[fy][key] = name_var_to_subract_from

                if dict_equivalent_matching[fy][key] != "None" :

                    value_to_subtract_from = inc_stat_ticker.at[name_var_to_subract_from,fy]
                    nan_val = 0 if np.isnan(value_to_subtract_from) else value_to_subtract_from
                    possible_vars = inc_stat_map[key][2]
                    definitive_vars = []
                    for var in possible_vars:

                        if type(var) == str:

                            definitive_vars.append(var)

                        else: #type dict

                            var_to_be_calculated = list(var.keys())[0]
                            var_in_yf_df = dict_equivalent_matching[fy][var_to_be_calculated]

                            if var_in_yf_df == "None":

                                continue

                            else:

                                definitive_vars.append(var_in_yf_df)

                    for var in definitive_vars:

                        if var in index_inc_stat_ticker:

                            value = inc_stat_ticker.at[var,fy]
                            nan_val = np.isnan(value)
                            value = 0 if nan_val else value
                            if value != 0 :
                                dict_equivalent_matching[fy][key] = dict_equivalent_matching[fy][key] + "-" + var
                            value_to_subtract_from = value_to_subtract_from - value

                    if value_to_subtract_from == 0:

                        vals_for_each_col[fy].append("NO VALUES FOR METRIC")

                    else:

                        vals_for_each_col[fy].append(value_to_subtract_from)

                else:

                    vals_for_each_col[fy].append("NO VALUES FOR METRIC")


    return vals_for_each_col

def final_df_inc_stat(dict_values_per_column:dict,df_inc_index):

    df_period_end = pd.DataFrame(data=[dict_values_per_column.keys()],columns=dict_values_per_column.keys(),index=['Period End Date'])
    df = pd.DataFrame.from_dict(dict_values_per_column)
    df.index = df_inc_index
    fin_rep_currency_ser = df.loc["Currency of Financial Reporting"]
    currency_prices_ser = df.loc["Currency of Prices"]
    df = df.apply(pd.to_numeric, errors='coerce') / 1000000 #VALUES IN MILLIONS
    df.loc["Currency of Financial Reporting"] = fin_rep_currency_ser
    df.loc["Currency of Prices"] = currency_prices_ser
    df.loc["EPS (Basic)"] = df.loc["EPS (Basic)"] * 1000000
    df.loc["EPS (Diluted)"] = df.loc["EPS (Diluted)"] * 1000000
    df.loc["Prices Around Reporting Dates"] = df.loc["Prices Around Reporting Dates"] * 1000000
    df.loc["Prices Around Reporting Dates"] = df.loc["Prices Around Reporting Dates"].round(decimals=2)
    df.loc["Market Capitalization"] = df.loc["Market Capitalization"] * 1000000
    df.loc["Market Capitalization"] = df.loc["Market Capitalization"].round(decimals=2)
    df = pd.concat([df_period_end,df],axis=0)
    df.loc['Period End Date'] = pd.to_datetime(df.loc['Period End Date']).dt.date
    df_idx_lst = list(df.index)
    ebt_vals = df.loc['EBT'].copy()
    other_exp_inc_vals = df.loc['Other Expense/Income'].copy()
    df.loc['EBT'] = other_exp_inc_vals
    df.loc['Other Expense/Income'] = ebt_vals
    idx_ebt = df_idx_lst.index('EBT')
    df_idx_lst[idx_ebt] = "Other Expense/Income"
    df_idx_lst[idx_ebt+1] = "EBT"
    df.index = df_idx_lst

    series_time = df.loc['Period End Date']
    fys = []
    for date in series_time:

        month = date.month
        if month < 6:

            fy = f"FY {int(date.year) - 1}"

        else:

            fy = f"FY {date.year}"

        fys.append(fy)

    df.columns = fys

    return df


def create_ticker_stat_cfs_proxy_finviz(stat_cfs_map:dict,stat_cfs_ticker:pd.DataFrame):

    columns_for_df = stat_cfs_ticker.columns
    index_for_df = stat_cfs_map.keys()
    vals_for_each_col = {}
    dict_equivalent_matching = {}

    for fy in columns_for_df:

        vals_for_each_col[fy] = []
        dict_equivalent_matching[fy] = dict()

        for key in index_for_df:

            dict_equivalent_matching[fy][key] = ""
            method = stat_cfs_map[key][0]
            index_stat_cfs_ticker = stat_cfs_ticker.index

            if method == "direct":

                possible_vars = stat_cfs_map[key][1]
                any_var_in_df = False

                for var in possible_vars:

                    if var in index_stat_cfs_ticker :

                        nan_val = np.isnan(stat_cfs_ticker.at[var,fy])
                        value = 0 if nan_val else stat_cfs_ticker.at[var,fy]
                        if value != 0 :
                            dict_equivalent_matching[fy][key] = var
                            any_var_in_df = True
                            vals_for_each_col[fy].append(value)
                        break

                if any_var_in_df == False:

                    vals_for_each_col[fy].append("NO VALUES FOR METRIC")
                    dict_equivalent_matching[fy][key] = "None"

            else: #method == "sum"

                lst_val_to_sum = []
                possible_vars = stat_cfs_map[key][1]
                any_var_in_df = False

                for var in possible_vars:

                    if var in index_stat_cfs_ticker :

                        nan_val = np.isnan(stat_cfs_ticker.at[var,fy])
                        value = 0 if nan_val else stat_cfs_ticker.at[var,fy]
                        if value != 0 :

                            any_var_in_df = True
                            if dict_equivalent_matching[fy][key] == "":

                                dict_equivalent_matching[fy][key] = var

                            else:

                                dict_equivalent_matching[fy][key] = dict_equivalent_matching[fy][key] + "+" + var
                        lst_val_to_sum.append(value)

                if any_var_in_df == False:

                    vals_for_each_col[fy].append("NO VALUES FOR METRIC")
                    dict_equivalent_matching[fy][key] = "None"

                else:

                    vals_for_each_col[fy].append(sum(lst_val_to_sum))


    return vals_for_each_col

def final_df_stat_cfs(dict_values_per_column:dict,df_stat_cfs_index):

    df_period_end = pd.DataFrame(data=[dict_values_per_column.keys()],columns=dict_values_per_column.keys(),index=['Period End Date'])
    df = pd.DataFrame.from_dict(dict_values_per_column)
    df = df.apply(pd.to_numeric, errors='coerce') / 1000000 #VALUES IN MILLIONS
    df.index = df_stat_cfs_index
    df = pd.concat([df_period_end,df],axis=0)
    df.loc['Period End Date'] = pd.to_datetime(df.loc['Period End Date']).dt.date

    series_time = df.loc['Period End Date']
    fys = []
    for date in series_time:

        month = date.month
        if month < 6:

            fy = f"FY {int(date.year) - 1}"

        else:

            fy = f"FY {date.year}"

        fys.append(fy)

    df.columns = fys

    return df

"""BUILD A FUNCTION TO SEE IF THE COLUMNS (REPORTING DATES MATCH)"""

def dates_of_reporting_comparable(dict_inc_stat_tickers:dict,new_tickers:list):

    dict_comparable_reporting_dates = dict()

    for ticker in new_tickers:

        ticker_reporting_dates = dict_inc_stat_tickers[ticker].columns
        n_cols_ticker = len(ticker_reporting_dates)

        if len(dict_comparable_reporting_dates) == 0:

            dict_comparable_reporting_dates["comp_report_dates_1"] = list()
            dict_comparable_reporting_dates["comp_report_dates_1"].append(ticker)

        else:

            list_of_keys = list(dict_comparable_reporting_dates.keys())
            number_of_dict_keys = len(list_of_keys)
            keys_follow = 0

            while keys_follow < number_of_dict_keys:

                first_ticker_of_each_comparable = dict_comparable_reporting_dates[list_of_keys[keys_follow]][0]
                cols_of_that_ticker = dict_inc_stat_tickers[first_ticker_of_each_comparable].columns
                n_of_cols = len(cols_of_that_ticker)
                min_cols = min(n_cols_ticker,n_of_cols)
                if n_of_cols != n_cols_ticker:

                    ticker_reporting_dates_update = dict_inc_stat_tickers[ticker].columns[0:min_cols]
                    cols_of_that_ticker_update = dict_inc_stat_tickers[first_ticker_of_each_comparable].columns[0:min_cols]

                else:

                    ticker_reporting_dates_update = ticker_reporting_dates
                    cols_of_that_ticker_update = cols_of_that_ticker

                list_true_cols = list(ticker_reporting_dates_update == cols_of_that_ticker_update)
                numb_of_equal_rep_dates = list_true_cols.count(True)

                if min_cols == numb_of_equal_rep_dates:

                    dict_comparable_reporting_dates[list_of_keys[keys_follow]].append(ticker)
                    break

                else:

                    keys_follow += 1

            if keys_follow == number_of_dict_keys:

                dict_comparable_reporting_dates[f"comp_report_dates{keys_follow}"] = list()
                dict_comparable_reporting_dates[f"comp_report_dates{keys_follow}"].append(ticker)

    for key in dict_comparable_reporting_dates:

        #ENSURE THE TICKER WITH HIGHEST NºCOLS IS AT BEGGINING, IMPORTANT FOR NEXT USAGE
        n_cols_per_ticker = []

        for ticker in dict_comparable_reporting_dates[key]:

            n_cols_per_ticker.append(len(dict_inc_stat_tickers[ticker].columns))
            max_cols = max(n_cols_per_ticker)
            if len(dict_inc_stat_tickers[ticker].columns) == max_cols:

                if len(n_cols_per_ticker) > 0:

                    current_idx = len(n_cols_per_ticker) - 1
                    ticker_in_beg = dict_comparable_reporting_dates[key][0]
                    dict_comparable_reporting_dates[key][0] = ticker
                    dict_comparable_reporting_dates[key][current_idx] = ticker_in_beg

    return dict_comparable_reporting_dates

"""SEE IF COMPANIES HAVE THE EARNINGS AVAILABLE FOR TO GET AVG PRICES"""

def num_of_earnings_compared_to_years(columns_of_df,index_of_earnings_df):

    #TRAP THE EARNINGS DATE INTO THE DATE OF THE COLUMN AND 100 DAYS AFTER, ASSUMING REPORTING IN QUARTERS WITH ORDINALS
    earnings_of_interest = []
    idx_ear_non_repeated = []

    #AVOID REPETITION OF DATES
    for date in index_of_earnings_df:

        if date not in idx_ear_non_repeated:

            idx_ear_non_repeated.append(date)

    for col in columns_of_df:

        date = col
        end_date_range = date + pd.Timedelta(days = 100)
        date_init_ordinal = date.toordinal()
        date_end_ordinal = end_date_range.toordinal()

        size_earnings_of_interest = len(earnings_of_interest)

        for earning_date in idx_ear_non_repeated:

            earning_date_ordinal = earning_date.toordinal()

            if date_init_ordinal < earning_date_ordinal <= date_end_ordinal:

                if len(earnings_of_interest) > 0:

                    prev_val = earnings_of_interest[-1]

                    try:

                        np.isnan(prev_val)

                    except TypeError:

                        cond_prev_val = date_init_ordinal < prev_val.toordinal() <= date_end_ordinal

                        if cond_prev_val:

                            earnings_of_interest.remove(prev_val)

                        earnings_of_interest.append(earning_date)

                    else:

                        earnings_of_interest.append(earning_date)

                else:

                    earnings_of_interest.append(earning_date)

        if size_earnings_of_interest == len(earnings_of_interest):

            earnings_of_interest.append(np.nan)

    return earnings_of_interest

#FUNCTION TO GET EACH TICKER WITH AN INDEX WITH THE PRICES AROUND THEIR EARNINGS
def prices_near_reporting(dict_inc_stat_tickers:dict,new_tickers:list):

    #THE IDEA OF THE FUNCTION IS TO GET AN AVERAGE OF THE PRICES NEAR REPORTING TO CALCULATE RATIOS THAT NEED PRICES
    dict_comparable_reporting = dates_of_reporting_comparable(dict_inc_stat_tickers,new_tickers)
    lst_different_comparables = [dict_comparable_reporting[key] for key in dict_comparable_reporting]

    for lst in lst_different_comparables:

        end_date = datetime.date.today() - pd.Timedelta(days=1)

        #'dates_of_reporting_comparable' already ensures that lst[0] tickers has the highest number of columns
        start_date = dict_inc_stat_tickers[lst[0]].columns[len(dict_inc_stat_tickers[lst[0]].columns)-1]

        #PRICING DOWNLOAD
        comp_tickers_df = yf.download(tickers=lst,start=start_date,end=end_date,interval='1d')

        for ticker in lst:

            price_action_ticker = comp_tickers_df.loc[:,(['Close','High','Low','Volume'],ticker)]

            if len(price_action_ticker) != 0:

                start_date_ticker = list(price_action_ticker.index)[0]
                end_date_ticker = list(price_action_ticker.index)[len(list(price_action_ticker.index))-1]
                df_ticker = dict_inc_stat_tickers[ticker]
                df_ticker_columns = list(df_ticker.columns)
                lst_index_in_ordinal = [price_action_ticker.index[i].toordinal() for i in range(len(price_action_ticker))]


                avg_prices_around_reporting_dates = []

                try:
                    ticker_earnings_ind = yf.Ticker(ticker).earnings_dates.index

                except (AttributeError,KeyError):

                    for i in range(len(df_ticker_columns)):

                        #HERE INSTEAD OF USING NaN, ONE COULD USE THE AVERAGE OF THE FOLLOWING THREE MONTHS
                        avg_prices_around_reporting_dates.append(np.nan)

                else:

                    earnings_of_interest = num_of_earnings_compared_to_years(df_ticker_columns,ticker_earnings_ind)
                    print("GETTING PRICES NEAR REPORTING DATES OFF TICKER",ticker,"WITHIN THE STARTING DATE OFF",start_date_ticker,"AND END DATE THE CURRENT TIME GIVEN BY",end_date_ticker)
                    for earnings_date in earnings_of_interest:

                        if type(earnings_date) == float : #nan equals a float, earnings_date are supposed to be datetimes.

                            #HERE INSTEAD OF USING NaN, ONE COULD USE THE AVERAGE OF THE FOLLOWING THREE MONTHS
                            avg_prices_around_reporting_dates.append(earnings_date)

                        else:

                            start_date = earnings_date - pd.Timedelta(days=25)
                            end_date = earnings_date + pd.Timedelta(days=5)

                            start_date_to_ordinal = start_date.toordinal()
                            end_date_to_ordinal = end_date.toordinal()

                            start_front = start_date_to_ordinal
                            start_back = start_date_to_ordinal
                            cond_start_front = start_front in lst_index_in_ordinal
                            cond_start_back = start_back in lst_index_in_ordinal
                            combined_comb_start = cond_start_back or cond_start_front
                            count_loop_start = 0
                            cond_loop_start = count_loop_start <= 15
                            val_start_exists = False

                            end_front = end_date_to_ordinal
                            end_back = end_date_to_ordinal
                            cond_end_front = end_front in lst_index_in_ordinal
                            cond_end_back = end_back in lst_index_in_ordinal
                            combined_comb_end = cond_end_back or cond_end_front
                            count_loop_end = 0
                            cond_loop_end = count_loop_end <= 15
                            val_end_exists = False

                            while (combined_comb_start == False and cond_loop_start == True):

                                count_loop_start += 1
                                start_front += 1
                                start_back -= 1
                                cond_start_front = start_front in lst_index_in_ordinal
                                cond_start_back = start_back in lst_index_in_ordinal
                                combined_comb_start = cond_start_back or cond_start_front
                                cond_loop_start = count_loop_start <= 15

                            if combined_comb_start:

                                if start_front not in lst_index_in_ordinal:

                                    start_date = price_action_ticker.index[lst_index_in_ordinal.index(start_back)]

                                else:

                                    start_date = price_action_ticker.index[lst_index_in_ordinal.index(start_front)]

                                val_start_exists = True



                            while (combined_comb_end == False and cond_loop_end == True):

                                count_loop_end += 1
                                end_front += 1
                                end_back -= 1
                                cond_end_front = end_front in lst_index_in_ordinal
                                cond_end_back = end_back in lst_index_in_ordinal
                                combined_comb_end = cond_end_back or cond_end_front
                                cond_loop_end = count_loop_end <= 15

                            if combined_comb_end:

                                if end_front not in lst_index_in_ordinal:

                                    end_date = price_action_ticker.index[lst_index_in_ordinal.index(end_back)]

                                else:

                                    end_date = price_action_ticker.index[lst_index_in_ordinal.index(end_front)]

                                val_end_exists = True

                            if val_start_exists and val_end_exists:

                                avg_price_month_reporting_date = price_action_ticker.loc[[start_date,end_date],('Close',ticker)].mean()
                                avg_prices_around_reporting_dates.append(avg_price_month_reporting_date)

                            else:

                                avg_prices_around_reporting_dates.append(np.nan)

                dict_inc_stat_tickers[ticker].loc["Avg Prices Around Earnings"] = avg_prices_around_reporting_dates

                try:

                    currency_of_reporting_financials = yf.Ticker(ticker).info['financialCurrency']

                except KeyError:

                    try:

                        curr_pricing = yf.Ticker(ticker).info['currency']

                    except KeyError:

                        print("CURRENCIES USED BY TICKER",ticker,"AREN'T RECOGNIZED BY 'yfinance'")
                        #DEFAULT TO 'EUR'
                        lst_curr = ["EUR" for i in range(len(avg_prices_around_reporting_dates))]
                        dict_inc_stat_tickers[ticker].loc["Currency used in Pricing"] = lst_curr
                        dict_inc_stat_tickers[ticker].loc["Currency used in Financial Reporting"] = lst_curr

                    else:

                        #BOTH CURRENCY OF REPORTING AND PRICING ARE ASSUMED TO BE THE SAME
                        lst_curr = [curr_pricing for i in range(len(avg_prices_around_reporting_dates))]
                        dict_inc_stat_tickers[ticker].loc["Currency used in Pricing"] = lst_curr
                        dict_inc_stat_tickers[ticker].loc["Currency used in Financial Reporting"] = lst_curr

                else:

                    try:

                        curr_pricing = yf.Ticker(ticker).info['currency']

                    except KeyError:

                        lst_curr = [currency_of_reporting_financials for i in range(len(avg_prices_around_reporting_dates))]
                        dict_inc_stat_tickers[ticker].loc["Currency used in Pricing"] = lst_curr
                        dict_inc_stat_tickers[ticker].loc["Currency used in Financial Reporting"] = lst_curr

                    else:

                        #REPORTING FINANCIALS AND PRICING MIGHT HAVE DIFFERENT CURRENCIES
                        lst_curr = [curr_pricing for i in range(len(avg_prices_around_reporting_dates))]
                        lst_fin_reporting = [currency_of_reporting_financials for i in range(len(avg_prices_around_reporting_dates))]
                        dict_inc_stat_tickers[ticker].loc["Currency used in Pricing"] = lst_curr
                        dict_inc_stat_tickers[ticker].loc["Currency used in Financial Reporting"] = lst_fin_reporting

            else:

                print(ticker,"DOESN'T HAVE ANY DF WITH ITS PRICING HISTORY,THEREFORE PRICING WILL BE FILLED WITH 'np.nan'")
                df_ticker = dict_inc_stat_tickers[ticker]
                df_ticker_columns = list(df_ticker.columns)
                avg_prices_around_reporting_dates = [np.nan for i in range(len(df_ticker_columns))]

                try:

                    currency_of_reporting_financials = yf.Ticker(ticker).info['financialCurrency']

                except KeyError:

                    try:

                        curr_pricing = yf.Ticker(ticker).info['currency']

                    except KeyError:

                        print("CURRENCIES USED BY TICKER",ticker,"AREN'T RECOGNIZED BY 'yfinance'")
                        #DEFAULT TO 'EUR'
                        lst_curr = ["EUR" for i in range(len(avg_prices_around_reporting_dates))]
                        dict_inc_stat_tickers[ticker].loc["Currency used in Pricing"] = lst_curr
                        dict_inc_stat_tickers[ticker].loc["Currency used in Financial Reporting"] = lst_curr

                    else:

                        #BOTH CURRENCY OF REPORTING AND PRICING ARE ASSUMED TO BE THE SAME
                        lst_curr = [curr_pricing for i in range(len(avg_prices_around_reporting_dates))]
                        dict_inc_stat_tickers[ticker].loc["Currency used in Pricing"] = lst_curr
                        dict_inc_stat_tickers[ticker].loc["Currency used in Financial Reporting"] = lst_curr

                else:

                    try:

                        curr_pricing = yf.Ticker(ticker).info['currency']

                    except KeyError:

                        lst_curr = [currency_of_reporting_financials for i in range(len(avg_prices_around_reporting_dates))]
                        dict_inc_stat_tickers[ticker].loc["Currency used in Pricing"] = lst_curr
                        dict_inc_stat_tickers[ticker].loc["Currency used in Financial Reporting"] = lst_curr

                    else:

                        #REPORTING FINANCIALS AND PRICING MIGHT HAVE DIFFERENT CURRENCIES
                        lst_curr = [curr_pricing for i in range(len(avg_prices_around_reporting_dates))]
                        lst_fin_reporting = [currency_of_reporting_financials for i in range(len(avg_prices_around_reporting_dates))]
                        dict_inc_stat_tickers[ticker].loc["Currency used in Pricing"] = lst_curr
                        dict_inc_stat_tickers[ticker].loc["Currency used in Financial Reporting"] = lst_fin_reporting


            #CHECK IF TICKERS HAVE THE SAME Nº OF YEARS AS EARNINGS AS AFTER THE ANNUAL REPORT

#CURRENCY OF REPORTING AND PRICES SHOULD ALREADY BE STORED IN THE DF

def match_fin_reporting_and_prices_to_same_currency_euro(dict_three_statements_and_tickers:dict):

    exchange_rates_needed = []
    ##EUR/CUR - MEANS THAT 1 UNIT OF EURO IS THE EXCHANGE RATE OF CUR CURRENCY
    dict_inc_stat_tickers = dict_three_statements_and_tickers['inc_stat']
    dict_bal_sheet_tickers = dict_three_statements_and_tickers['bal_sheet']
    dict_stat_cfs_tickers = dict_three_statements_and_tickers['stat_cfs']
    tickers = dict_inc_stat_tickers.keys()
    for ticker in tickers:

        df = dict_inc_stat_tickers[ticker]
        currency_price = df.at["Currency of Prices",df.columns[0]]
        curr_fin_rep = df.at["Currency of Financial Reporting",df.columns[0]]

        if currency_price != "EUR":

            exchange_currency = "EUR"+currency_price.upper()+"=X"

            if exchange_currency not in exchange_rates_needed:

                exchange_rates_needed.append(exchange_currency)

        if curr_fin_rep != "EUR":

            exchange_currency = "EUR"+curr_fin_rep.upper()+"=X"

            if exchange_currency not in exchange_rates_needed:

                exchange_rates_needed.append(exchange_currency)

    if exchange_rates_needed != []:

        quarter_date = datetime.date.today() - pd.Timedelta(days=90)
        df_exchange_rates = yf.download(exchange_rates_needed,start = quarter_date,end = datetime.date.today() ,interval = '1d')

        for ticker in tickers:

            #WILL USE AN AVERAGE RATE OF PAST 3 MONTHS
            df = dict_inc_stat_tickers[ticker]
            df_bal = dict_bal_sheet_tickers[ticker]
            df_stat = dict_stat_cfs_tickers[ticker]
            currency_price = df.at["Currency of Prices",df.columns[0]]
            curr_fin_rep = df.at["Currency of Financial Reporting",df.columns[0]]
            if currency_price.upper() != "EUR":

                if currency_price == "GBp":

                    currency_price = currency_price.upper()
                    exchange_rate = "EUR"+currency_price+"=X"
                    exchange_rate_val = df_exchange_rates.loc[:,('Close',exchange_rate)].mean()
                    df.loc["Prices Around Reporting Dates"] = df.loc["Prices Around Reporting Dates"] * (1/(exchange_rate_val*100))

                else:

                    currency_price = currency_price.upper()
                    exchange_rate = "EUR"+currency_price+"=X"
                    exchange_rate_val = df_exchange_rates.loc[:,('Close',exchange_rate)].mean()
                    df.loc["Prices Around Reporting Dates"] = df.loc["Prices Around Reporting Dates"] * (1/exchange_rate_val)

            if curr_fin_rep.upper() != "EUR":

                if curr_fin_rep == "GBp":

                    curr_fin_rep = curr_fin_rep.upper()
                    exchange_rate = "EUR"+curr_fin_rep+"=X"
                    exchange_rate_val = df_exchange_rates.loc[:,('Close',exchange_rate)].mean()
                    list_vals_non_multiplying = ["Period End Date","Shares Outstanding (Basic)","Shares Outstanding (Diluted)","Prices Around Reporting Dates","Currency of Prices","Currency of Financial Reporting"]
                    val_to_mult = (1/(exchange_rate_val*100))
                    index_df = df.index
                    for var in index_df:

                        if var not in list_vals_non_multiplying:

                            df.loc[var] = df.loc[var] * val_to_mult
                            df.loc[var] = df.loc[var].astype(np.float64)

                    len_df_columns = len(df.columns)
                    standard_currency = ["EUR" for i in range(len_df_columns)]
                    df.loc["Currency of Prices"] = standard_currency
                    df.loc["Currency of Financial Reporting"] = standard_currency

                    bal_index = df_bal.index
                    for var in bal_index:

                        if var not in list_vals_non_multiplying:

                            df_bal.loc[var] = df_bal.loc[var] * val_to_mult
                            df_bal.loc[var] = df_bal.loc[var].astype(np.float64).round(decimals = 2)

                    stat_index = df_stat.index
                    for var in stat_index:

                        if var not in list_vals_non_multiplying:

                            df_stat.loc[var] = df_stat.loc[var] * val_to_mult
                            df_stat.loc[var] = df_stat.loc[var].astype(np.float64).round(decimals = 2)


                else:

                    curr_fin_rep = curr_fin_rep.upper()
                    exchange_rate = "EUR"+curr_fin_rep+"=X"
                    exchange_rate_val = df_exchange_rates.loc[:,('Close',exchange_rate)].mean()
                    list_vals_non_multiplying = ["Period End Date","Shares Outstanding (Basic)","Shares Outstanding (Diluted)","Prices Around Reporting Dates","Currency of Prices","Currency of Financial Reporting"]
                    val_to_mult = (1/exchange_rate_val)
                    index_df = df.index
                    for var in index_df:

                        if var not in list_vals_non_multiplying:

                            df.loc[var] = df.loc[var] * val_to_mult
                            df.loc[var] = df.loc[var].astype(np.float64)

                    bal_index = df_bal.index
                    for var in bal_index:

                        if var not in list_vals_non_multiplying:

                            df_bal.loc[var] = df_bal.loc[var] * val_to_mult
                            df_bal.loc[var] = df_bal.loc[var].astype(np.float64).round(decimals = 2)

                    stat_index = df_stat.index
                    for var in stat_index:

                        if var not in list_vals_non_multiplying:

                            df_stat.loc[var] = df_stat.loc[var] * val_to_mult
                            df_stat.loc[var] = df_stat.loc[var].astype(np.float64).round(decimals = 2)

    return dict_three_statements_and_tickers


def add_ons_to_df_inc_stat(dict_inc_stat_tickers:dict,new_tickers:list):

    for ticker in new_tickers:

        df_inc_stat = dict_inc_stat_tickers[ticker]

        #DEAL WITH COMPANIES THAT CHANGED REPORTING AND HAVE COLUMNS WITH SAME NAMES
        # df_inc_stat.columns = [f"{c}_{i}" for i, c in enumerate(df_inc_stat.columns)]
        # for col in df_inc_stat.columns:

        #     most_current_month_end_fiscal_year = df_inc_stat.at['Period End Date',df_inc_stat.columns[0]].month
        #     if df_inc_stat.at['Period End Date',col].month != most_current_month_end_fiscal_year:

        #         df_inc_stat.drop(columns = col,inplace=True)
        #     else:

        #         df_inc_stat.rename(columns = {col : col[0:7]},inplace=True)

        df_inc_stat.loc["Prices Around Reporting Dates"] = df_inc_stat.loc["Prices Around Reporting Dates"].astype(np.float64).round(decimals=2)
        price_series = df_inc_stat.loc["Prices Around Reporting Dates"]
        mkcap_series = df_inc_stat.loc["Market Capitalization"]

        #Price To Earnings
        pe_list = []

        #mkcap

        mkcap_list = []

        count_loop = 0

        for col in df_inc_stat.columns:

            rev = df_inc_stat.at["Total Revenue",col]

            if rev == 0:

                df_inc_stat.at["Total Revenue",col] = np.nan

            eps = df_inc_stat.at["EPS (Diluted)",col]

            if eps <= 0.1:

                eps_basic = df_inc_stat.at["EPS (Basic)",col]

                if eps_basic >= 0.1:

                    df_inc_stat.at["EPS (Diluted)",col] = eps_basic
                    eps = df_inc_stat.at["EPS (Diluted)",col]
                    price_val = df_inc_stat.at["Prices Around Reporting Dates",col]
                    pe_list.append(price_val/eps)

                else:

                    pe_list.append(np.nan)

            else:

                price_val = df_inc_stat.at["Prices Around Reporting Dates",col]
                pe_list.append(price_val/eps)

            price = df_inc_stat.at["Prices Around Reporting Dates",col]
            shares = df_inc_stat.at["Shares Outstanding (Basic)",col]

            if np.isnan(price) and count_loop > 0:

                mkcap_list.append(np.nan)

            else: #price exists or count_loop <= 0

                if count_loop <= 0:

                    latest_mkcap = df_inc_stat.at["Market Capitalization",col]

                    if np.isnan(latest_mkcap):

                        mkcap_val = price * shares
                        mkcap_list.append(mkcap_val)

                    else:

                        mkcap_list.append(latest_mkcap)

                else: #price exists

                    mkcap_val = price * shares
                    mkcap_list.append(mkcap_val)

            count_loop += 1

        rev_series = df_inc_stat.loc["Total Revenue"]

        df_inc_stat.loc["Price To Earnings Ratio"] = pe_list
        df_inc_stat.loc["Price To Earnings Ratio"] = df_inc_stat.loc["Price To Earnings Ratio"].astype(np.float64).round(decimals = 1)

        #Price To Sales
        sales_p_share_series = rev_series / df_inc_stat.loc["Shares Outstanding (Diluted)"]
        df_inc_stat.loc["Price To Sales Ratio"] = price_series / sales_p_share_series
        df_inc_stat.loc["Price To Sales Ratio"] = df_inc_stat.loc["Price To Sales Ratio"].astype(np.float64).round(decimals = 1)

        #Gross Margin
        gp_series = df_inc_stat.loc["Gross Profit"]
        series_gp_margin = gp_series / rev_series
        df_inc_stat.loc["Gross Margin"] = series_gp_margin
        df_inc_stat.loc["Gross Margin"] = df_inc_stat.loc["Gross Margin"].astype(np.float64).round(decimals = 3)

        #Operating Margin
        op_series = df_inc_stat.loc["Operating Income"]
        series_op_margin = op_series / rev_series
        df_inc_stat.loc["Operating Margin"] = series_op_margin
        df_inc_stat.loc["Operating Margin"] = df_inc_stat.loc["Operating Margin"].astype(np.float64).round(decimals = 3)

        #Net Margin
        ni_series = df_inc_stat.loc["Net Income"]
        series_net_margin = ni_series / rev_series
        df_inc_stat.loc["Net Margin"] = series_net_margin
        df_inc_stat.loc["Net Margin"] = df_inc_stat.loc["Net Margin"].astype(np.float64).round(decimals = 3)

        #MkCap
        df_inc_stat.loc["Market Capitalization"] = mkcap_list
        df_inc_stat.loc["Market Capitalization"] = df_inc_stat.loc["Market Capitalization"].astype(np.float64).round()

        new_indexes = ["Price To Earnings Ratio","Price To Sales Ratio","Gross Margin","Operating Margin","Net Margin","Market Capitalization"]
        index_df_without_new_indexes = df_inc_stat.loc[df_inc_stat.index.difference(new_indexes)].index
        list_vals_non_multiplying = ["Period End Date","Shares Outstanding (Basic)","Shares Outstanding (Diluted)","Prices Around Reporting Dates","Currency of Prices","Currency of Financial Reporting"]

        for var in index_df_without_new_indexes:

            if var not in list_vals_non_multiplying:

                if var == "EPS (Basic)" or var == "EPS (Diluted)":

                    df_inc_stat.loc[var] = df_inc_stat.loc[var].astype(np.float64).round(decimals = 3)

                else:

                    df_inc_stat.loc[var] = df_inc_stat.loc[var].astype(np.float64).round(decimals = 0)


def add_ons_to_df_bal_sheet(dict_bal_sheet_tickers:dict,dict_inc_stat_tickers:dict,new_tickers:list):

    for ticker in new_tickers:

        df_inc_stat = dict_inc_stat_tickers[ticker]
        df_bs = dict_bal_sheet_tickers[ticker]

        # df_inc_stat.columns = [f"{c}_{i}" for i, c in enumerate(df_inc_stat.columns)]
        # for col in df_inc_stat.columns:

        #     most_current_month_end_fiscal_year = df_inc_stat.at['Period End Date',df_inc_stat.columns[0]].month
        #     if df_inc_stat.at['Period End Date',col].month != most_current_month_end_fiscal_year:

        #         df_inc_stat = df_inc_stat.drop(columns = col)
        #     else:

        #         df_inc_stat.rename(columns = {col : col[0:7]})

        # df_bs.columns = [f"{c}_{i}" for i, c in enumerate(df_bs.columns)]
        # for col in df_bs.columns:

        #     most_current_month_end_fiscal_year = df_bs.at['Period End Date',df_bs.columns[0]].month
        #     if df_bs.at['Period End Date',col].month != most_current_month_end_fiscal_year:

        #         df_bs = df_bs.drop(columns = col)
        #     else:

        #         df_bs.rename(columns = {col : col[0:7]})

        price_series = df_inc_stat.loc["Prices Around Reporting Dates"]
        shares_out_series = df_inc_stat.loc["Shares Outstanding (Basic)"]
        tot_equity_series = df_bs.loc['Total Equity']

        #BOOK VALUE PER SHARE
        df_bs.loc["Book Value Per Share"] = tot_equity_series / shares_out_series

        #TANGIBLE BOOK VALUE PER SHARE
        for col in df_bs.columns:

            val_pref_stock = df_bs.at["Preferred Stock - Carrying Value",col]

            if np.isnan(val_pref_stock):

                df_bs.at["Preferred Stock - Carrying Value",col] = 0


        pref_stock = df_bs.loc["Preferred Stock - Carrying Value"]
        int_assets = df_bs.loc["Intangible Assets"]

        tbv_series = tot_equity_series - pref_stock - int_assets
        df_bs.loc["Tangible Book Value Per Share"] = tbv_series / shares_out_series
        df_bs.loc["Tangible Book Value Per Share"] = df_bs.loc["Tangible Book Value Per Share"].astype(np.float64).round(decimals = 2)

        #PRICE TO BOOK
        book_per_share_series = df_bs.loc["Book Value Per Share"]
        df_bs.loc["Price to Book Ratio"] = price_series / book_per_share_series
        df_bs.loc["Price to Book Ratio"] = df_bs.loc["Price to Book Ratio"].astype(np.float64).round(decimals = 2)

        #ROA
        tot_assets = df_bs.loc['Total Assets']
        net_inc = df_inc_stat.loc['Net Income']
        series_roa = net_inc / tot_assets
        df_bs.loc['Return on Assets'] = series_roa
        df_bs.loc['Return on Assets'] = df_bs.loc['Return on Assets'].astype(np.float64).round(decimals = 3)

        #ROE
        net_inc = df_inc_stat.loc['Net Income']
        series_roe = net_inc / tot_equity_series
        df_bs.loc['Return on Equity'] = series_roe
        df_bs.loc['Return on Equity'] = df_bs.loc['Return on Equity'].astype(np.float64).round(decimals = 3)

        #ROIC
        debt_equity = df_bs.loc['Long Term Debt'] + df_bs.loc['Short Term Debt Incl. Current Port. of LT Debt'] + tot_equity_series
        net_inc = df_inc_stat.loc['Net Income']
        series_roic = net_inc / debt_equity
        df_bs.loc["Return on Invested Capital"] = series_roic
        df_bs.loc['Return on Invested Capital'] = df_bs.loc['Return on Invested Capital'].astype(np.float64).round(decimals = 3)

        #QUICK_RATIO
        series_quick_ratio = df_bs.loc['Cash & Short Term Investments'] / df_bs.loc['Total Current Liabilities']
        df_bs.loc["Quick Ratio"] = series_quick_ratio
        df_bs.loc["Quick Ratio"] = df_bs.loc["Quick Ratio"].astype(np.float64).round(decimals = 2)

        #CURRENT_RATIO
        series_curr_ratio = df_bs.loc['Total Current Assets'] / df_bs.loc['Total Current Liabilities']
        df_bs.loc["Current Ratio"] = series_curr_ratio
        df_bs.loc["Current Ratio"] = df_bs.loc["Current Ratio"].astype(np.float64).round(decimals = 2)

#%%

len(['LEG.DE','DHER.DE','SON.LS','JMT.LS','EDP.LS','EDPR.LS','TDSA.LS','MC.PA','CTT.LS','EVO.ST'])

#SEE WHEN DOWNLOADING TICKERS HOW DAYS OF OBSERVATION CAN ONE GET

end_date = datetime.date.today() - pd.Timedelta(days=1)
start_date = datetime.date(2020,12,31)

tickers_df = yf.download(
    tickers = ['LEG.DE','DHER.DE','SON.LS','JMT.LS','EDP.LS','EDPR.LS','TDSA.LS','MC.PA','CTT.LS','EVO.ST'],
    start = start_date,
    end = end_date,
    interval = '1d'
)

tickers_df


#%%

currencies = ["EUR","USD","GBP","GBp","CHF","NOK","SEK","DKK","HUF","CZK","PLN","RUB","NZD","CAD","AUD","JPY","CNH","CNY","RON","BRL","TRY","SGD","HOK","MXM","ZAR","ILS","INR","AED","SAR"]

df_test = parquet_to_df(rf"{directory_for_storage_or_retrieval}\inc_stat","IBE.MC")

len_cols = len(df_test.columns)
print(len_cols,type(len_cols))
cols = list(df_test.columns)
print(cols[0])
curr_in_numb_price = [currencies.index(df_test.at["Currency used in Pricing",cols[i]]) for i in range(len_cols)]
curr_in_numb_fin_rep = [currencies.index(df_test.at["Currency used in Financial Reporting",cols[i]]) for i in range(len_cols)]
df_test = df_test.astype(object)
df_test.loc["Currency used in Pricing"] = curr_in_numb_price
df_test.loc["Currency used in Financial Reporting"] = curr_in_numb_fin_rep
df_test.loc["Currency used in Pricing"] = df_test.loc["Currency used in Pricing"].astype(np.float64)
df_test.loc["Currency used in Financial Reporting"] = df_test.loc["Currency used in Financial Reporting"].astype(int)

currencies.ind

#%%

add_on_financials_after_updates(['IBE.MC'],directory_for_storage_or_retrieval)

#%%

directory_for_storage_or_retrieval = input("Directory for storage or retrieval: ").strip('"')
#%%

bs_map = BALANCE_SHEET_MAP
bs_map_index = list(bs_map.keys())
inc_stat_map = INCOME_STATEMENT_MAP
inc_stat_map_index = list(inc_stat_map.keys())
stat_cfs_map = CASH_FLOW_MAP
stat_cfs_map_index = list(stat_cfs_map.keys())

#%%
directory_for_storage_or_retrieval

#TEST THE UPDATE FUNCTION OF 'create_and_store_or_update_tickers_parquet_files_from_df_financials'

#%%

dict_from_colection = collection_of_tickers_statements(
    directory_for_storage_or_retrieval,
    bs_map,
    bs_map_index,
    inc_stat_map,
    inc_stat_map_index,
    stat_cfs_map,
    stat_cfs_map_index
)

#I GOT TWO OPTIONS, FOR TICKERS THAT ALREADY EXIST EITHER I FULLY UPDATE THEM OR DISCARD THEM FROM UPDATES
#%%

dict_from_colection["inc_stat"]['FCP.LS']

#%%

yf.Ticker("VSURE.ST").get_income_stmt()

#%%

yf.download(tickers=['VSURE.ST','EDP.LS'],start=datetime.date(2022,12,31),end=datetime.date.today()-pd.Timedelta(days=1),interval='1d').loc[:,(['Close','High','Low','Volume'],'VSURE.ST')]

#%%

yf

#%%

dict_from_colection["inc_stat"]['EDP.LS']

#%%

dict_from_colection["stat_cfs"]['EDP.LS']

#%%

parquet_to_df(rf"{directory_for_storage_or_retrieval}\stat_cfs","EDP.LS")

#%%

#dict_all_financials['inc_stat']['GTT.PA']
df_inc_stat = parquet_to_df(rf"{directory_for_storage_or_retrieval}\inc_stat","MRK.DE")
dict_vals_cols = getting_values_for_each_column_of_statement(inc_stat_map,df_inc_stat)
df_inc = final_df_inc_stat(dict_vals_cols,inc_stat_map_index)
df_inc


#%%

lst = ['LEG.DE','DHER.DE','G1A.DE','DTG.DE','HOLN.SW','NHY.OL','ORSTED.CO','SDZ.SW','YAR.OL','CA.PA','DIM.PA','ABI.BR','EVO.ST','PSN.L','KPN.AS']


chunked(lst,5)

#%%


ticker_lst_test = chosen_tickers(directory_for_storage_or_retrieval)

#%%

dict_ticker_financials = updated_parquet_to_df(directory_for_storage_or_retrieval,ticker_lst_test,bs_map,bs_map_index,inc_stat_map,inc_stat_map_index,stat_cfs_map,stat_cfs_map_index)

#%%

dict_from_colection['inc_stat']['FCP.LS']

#%%

yf.Ticker("KOA.OL").get_income_stmt()


#%%

ticker_lst_test = chosen_tickers(directory_for_storage_or_retrieval)

#%%

len(ticker_lst_test)

#%%
ticker_lst_test


#%%

dict_all_financials = {'bal_sheet' : {}, 'inc_stat' : {}, 'stat_cfs' : {}}

#%%

dict_all_financials = get_dict_all_tickers_with_statements(dict_all_financials,ticker_lst_test)
#ALL THE NUMBERS OF THE THREE STATEMENT APPEAR IN THE UNIT OF THE CURRENCY NOT IN THOUSANDS

#%%

dict_with_statements_of_tickers = dict_all_financials

#%%

dict_with_statements_of_tickers

#%%

dict_all_financials = dict_with_statements_of_tickers

#%%

dict_all_financials = match_tickers_with_three_statements(dict_all_financials,ticker_lst_test)

#%%

dict_all_financials = dict_excluding_financial_services(dict_all_financials)
ticker_lst_test = list(dict_all_financials["bal_sheet"].keys())

#%%

tickers = dict_all_financials['inc_stat'].keys()

lst_index_to_exclude = ["Avg Prices Around Earnings","Currency used in Pricing","Currency used in Financial Reporting"]

for ticker in tickers:

    df = dict_all_financials['inc_stat'][ticker]
    df = df.loc[df.index.difference(lst_index_to_exclude)]
    dict_all_financials['inc_stat'][ticker] = df

#%%

#ADDITIONS INTO THE DATAFRAMES OF THE STATEMENTS THE PRICES
addition_on_financial_statements(dict_all_financials,ticker_lst_test,directory_for_storage_or_retrieval)

#%%

dict_all_financials

#%%

dict_all_financials['inc_stat']['RPI.L'] #PFSE.DE

#%%

l = ['a','b','c','d','e','f','g']

prices = list(dict_all_financials['inc_stat']['RPI.L'].loc["Currency used in Pricing"])
cols = dict_all_financials['inc_stat']['RPI.L'].columns
ab = [l[dict_all_financials['inc_stat']['RPI.L'].loc["Currency used in Pricing",cols[i]]] for i in range(len(prices))]

ab

#%%

dict_with_statements_of_tickers = dict_all_financials

#%%

#THIS FUNCTION ONLY WITH EMPTY 'dict_all_financials' & ticker_lst_test WITH CACHE STORAGE, WILL UPDATE THE PRICES OF THE TICKER, CURRENCY OF PRICE AND CURRENCY OF FINANCIAL REPORTING OF TICKERS
create_and_store_or_update_tickers_parquet_files_from_df_financials(dict_all_financials,ticker_lst_test,directory_for_storage_or_retrieval)

#%%

dict_all_financials['inc_stat']['GTT.PA'].loc["Currency used in Pricing"].astype(int)

#%%

#TURN THOSE FROM PARQUET INTO USABLE DF
dict_ticker_financials = updated_parquet_to_df(directory_for_storage_or_retrieval,ticker_lst_test,bs_map,bs_map_index,inc_stat_map,inc_stat_map_index,stat_cfs_map,stat_cfs_map_index)

#%%



#%%

print(yf.Ticker("ADEN.SW").info['currency'],yf.Ticker("ADEN.SW").info['financialCurrency'])

#%%

yf.Ticker("SCP.LS").info.keys()

#%%


#%%

tick_lst = get_tickers_from_directory(directory_for_storage_or_retrieval)

nan_vals_tickers = []

for ticker in tick_lst:

    print(ticker)
    df = parquet_to_df(rf"{directory_for_storage_or_retrieval}\inc_stat",ticker)
    cols = df.columns
    val_curr_p = df.at["Currency used in Pricing",cols[0]]
    val_fin_curr = df.at["Currency used in Financial Reporting",cols[0]]
    if np.isnan(val_curr_p) and np.isnan(val_fin_curr):

        nan_vals_tickers.append(ticker)

nan_vals_tickers

#%%

parquet_to_df(rf"{directory_for_storage_or_retrieval}\inc_stat","ADEN.SW")

#%%

yf.Ticker("KOA.OL").get_income_stmt().loc["DilutedAverageShares","2025-12-31"]

#%%
currencies = ["EUR","USD","GBP","GBp","CHF","NOK","SEK","DKK","HUF","CZK","PLN","RUB","NZD","CAD","AUD","JPY","CNH","CNY","RON","BRL","TRY","SGD","HOK","MXM","ZAR","ILS","INR","AED","SAR"]

dict_ticker_fin = {'bal_sheet' : {},'inc_stat': {},'stat_cfs' : {}}

#dict_all_financials['inc_stat']['GTT.PA']
df_inc_stat = parquet_to_df(rf"{directory_for_storage_or_retrieval}\inc_stat","EDP.LS")
dict_vals_cols = getting_values_for_each_column_of_statement(inc_stat_map,df_inc_stat)
df_inc = final_df_inc_stat(dict_vals_cols,inc_stat_map_index)
df_inc

#%%

df_inc.at["Shares Outstanding (Diluted)","FY 2025"]

#%%
cols_len = len(df_inc.columns)
cols = df_inc.columns
df_inc.loc["Currency of Prices"] = [currencies[int(df_inc.loc["Currency of Prices",cols[i]])] for i in range(cols_len)]
df_inc.loc["Currency of Financial Reporting"] = [currencies[int(df_inc.loc["Currency of Financial Reporting",cols[i]])] for i in range(cols_len)]
dict_ticker_fin["inc_stat"]["ADEN.SW"] = df_inc
df_inc

#%%

df_inc_stat = parquet_to_df(rf"{directory_for_storage_or_retrieval}\bal_sheet","FCP.LS")
dict_vals_cols = getting_values_for_each_column_of_statement(bs_map,df_inc_stat)
df_bal = final_df_bal_sheet(dict_vals_cols,bs_map_index)
dict_ticker_fin["bal_sheet"]["ADEN.SW"] = df_bal
df_bal

df_inc_stat = parquet_to_df(rf"{directory_for_storage_or_retrieval}\stat_cfs","FCP.LS")
dict_vals_cols = getting_values_for_each_column_of_statement(stat_cfs_map,df_inc_stat)
df_stat = final_df_stat_cfs(dict_vals_cols,stat_cfs_map_index)
dict_ticker_fin["stat_cfs"]["ADEN.SW"] = df_stat
df_stat


df_inc

#%%

yf.Ticker("KOA.OL").info['marketCap'] / 1000000

#%%

type(df_inc.at["Currency of Financial Reporting","FY 2024"])


#%%

dict_ticker_fin = match_fin_reporting_and_prices_to_same_currency_euro(dict_ticker_fin)



#%%

prices_near_reporting(dict_all_financials['inc_stat'],["ADEN.SW"])

#%%

dict_all_financials['inc_stat']["ADEN.SW"]

#%%

df_inc_stat


#%%

match_tickers_with_three_statements(dict_all_financials,['FLS.CO','NVG.LS','SON.LS','GTT.PA'])


#%%

dict_adjust_inc_stat['inc_stat'].keys()

#%%

for ticker in dict_adjust_inc_stat['inc_stat'].keys():

    ticker_df = dict_adjust_inc_stat['inc_stat'][ticker]
    pe_series = ticker_df.loc["Price To Earnings Ratio"]
    count_nan_tick = 0
    for val in pe_series:

        if np.isnan(val):

            count_nan_tick+=1

    if count_nan_tick == 0:

        tickers_pe_full.append(ticker)

#%%

len(tickers_pe_full)

#%%

tickers_pe_full

#%%

dict_ticker_financials['inc_stat']["THULE.ST"]

#%%

dict_vals_cols.keys()

#%%

dict_vals_cols[pd.Timestamp('2025-12-31 00:00:00')]


#%%

dict_ticker_financials

#%%

print(len(ticker_lst_test),len(dict_three_statements['bal_sheet']),len(dict_three_statements['inc_stat']),len(dict_three_statements['stat_cfs']))


#%%

dict_all_financials = comparable_tickers(dict_all_financials)
ticker_lst_test = list(dict_all_financials['bal_sheet'].keys())

#%%

len(ticker_lst_test)

#%%

ticker_lst_test.index("ABF.L")

#%%

small_lst = ticker_lst_test[0:100]

#%%

"""SEE IN THE FINVIZ FRAMEWORK THE TICKER STORAGE, HOW IT BECAME"""


#%%

#%%

len(dict_all_financials['bal_sheet'].keys())

#%%

#FINANCIAL TICKERS ARE LEFT OUT


#%%


#%%

yf.Ticker("VSURE.ST").info['currency']

#%%

yf.Ticker("VSURE.ST").get_balance_sheet()

#%%

len(yf.download(["VSURE.ST"],start=datetime.date(2020,12,31),end=datetime.date.today()-pd.Timedelta(days=1),interval='1d'))

#%%

ticker_earnings_ind = yf.Ticker('VSURE.ST').earnings_dates.index

#%%

ticker_earnings_ind

#%%

print(type(ticker_earnings_ind))

#%%



#%%

ear_of_interest = num_of_earnings_compared_to_years(dict_all_financials['inc_stat']['STMN.SW'].columns,ticker_earnings_ind)

#%%

ear_of_interest


#%%


comp_df = parquet_to_df(rf"{directory_for_storage_or_retrieval}\inc_stat",'1SXP.DE')
comp_df_one = parquet_to_df(rf"{directory_for_storage_or_retrieval}\bal_sheet",'1SXP.DE')
comp_df_two = parquet_to_df(rf"{directory_for_storage_or_retrieval}\stat_cfs",'1SXP.DE')

#%%




#%%

"""PUT THESE IN THE README.md
   IF YOU WANT TO FETCH TICKERS FROM AN ETF CSV THAT YOU HAVE, THE CODE IS PREPARED TO DEAL WITH
   BlackRock (THROUGH ITS SUBSIDIARY SPECIALIZED IN ETFs iShares) & State Street. WHEN YOU EXPORT THOSE
   CSVs FROM EACH OF THE PROVIDERS MAKE SURE THAT:

        - YOU ONLY HAVE EQUITIES;
        - EVERY INFO OUTSIDE OF THE DATA RANGE CONRRESPONDING TO SECURITIES DISAPPEARS FROM THE CSV FILE
          MAKING THE DATA RANGE WITH SECURITIES THE ONLY PRESENT FILE
        - EACH LINE CONRRESPONDS TO A SINGLE EQUITY INFO - THE PROVIDER MOST LIKELY ALREADY ENSURES THAT;
        - THE TOP LEFT ENTRY OF THE RANGE CONRRESPONDING TO THE DATA STARTS AT A1, MEANING THAT
          TITLES OF THE RANGE WILL BE AT ROW 1;
        - TO MAKE THINGS EASIER STORE EVERY CSV REGARDING ETFs IN THE SAME DIRECTORY;


"""



# %%

#%%

def financials_from_csv_into_dict_dfs(directory_to_tickers): #USE THE PATH BEFORE THE CSVs

    dict_all_financials = {'bal_sheet' : {},'inc_stat' : {}, 'stat_cfs' : {}}
    path_dir = Path(directory_to_tickers)
    all_path_tickers = path_dir.iterdir()

    for ticker_path in all_path_tickers:

        ticker = ticker_path.as_posix().split("/")[9].replace("_",".")
        ticker_path_financials = ticker_path.iterdir()
        lst_financials_paths_csv = [path for path in ticker_path_financials]
        for i in range(len(lst_financials_paths_csv)):

            if i == 0 : #balance_sheet

                dict_all_financials['bal_sheet'][ticker] = pd.read_csv(lst_financials_paths_csv[i])

            elif i == 1: #inc_stat

                dict_all_financials['inc_stat'][ticker] = pd.read_csv(lst_financials_paths_csv[i])

            else: #stat_cfs

                dict_all_financials['stat_cfs'][ticker] = pd.read_csv(lst_financials_paths_csv[i])

    return dict_all_financials


# %%
directory = r"C:\Users\Afons\Python_Files\Projects\Import_Financial_Statements\afonso_screener_v2\output\normalized"

dict_financials = financials_from_csv_into_dict_dfs(directory)
#%%


path_parent_directory_of_script = Path(r"C:\Users\Afons\Python_Files\Tickers_Financials_Fetching_And_Analysis")

for folder in path_parent_directory_of_script.iterdir():

    print(folder)


# %%
