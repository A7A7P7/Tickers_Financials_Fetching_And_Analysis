#%%

#IMPORT HELPER FUNCTIONS NEEDED
from yahoo_finance.organize_tickers.helpers_org import helpers

#%%

"""MAPPING OF THE STATEMENTS TO BECOME SIMILAR TO FINVIZ"""

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

"""VARIABLES NEEDED TO GET STATEMENTS & EVERYTHING"""

directory_for_storage_or_retrieval = input("Directory for storage or retrieval: ").strip('"')
bs_map = BALANCE_SHEET_MAP
bs_map_index = list(bs_map.keys())
inc_stat_map = INCOME_STATEMENT_MAP
inc_stat_map_index = list(inc_stat_map.keys())
stat_cfs_map = CASH_FLOW_MAP
stat_cfs_map_index = list(stat_cfs_map.keys())

#%%

dict_all_financials_and_tickers = helpers.collection_of_tickers_statements(
    directory_for_storage_or_retrieval,
    bs_map,
    bs_map_index,
    inc_stat_map,
    inc_stat_map_index,
    stat_cfs_map,
    stat_cfs_map_index
)

#%%

similar_tickers_lst = list(dict_all_financials_and_tickers['inc_stat'].keys())
