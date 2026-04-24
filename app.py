"""
Streamlit dashboard — friendly wrapper around Afonso's stock-screener project.

Purpose: help non-technical users understand the project, verify their setup,
and explore stored financials without touching the interactive scripts.

Run it with:
    streamlit run app.py
"""
from __future__ import annotations

import importlib
import platform
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Screener — Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

REPO_ROOT = Path(__file__).resolve().parent
REQ_PACKAGES = [
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("pyarrow", "pyarrow"),
    ("finvizfinance", "finvizfinance"),
    ("yfinance", "yfinance"),
    ("requests", "requests"),
    ("beautifulsoup4", "bs4"),
    ("streamlit", "streamlit"),
    ("plotly", "plotly"),
]

# ─── Sidebar navigation ───────────────────────────────────────────────────────
st.sidebar.title("📈 Stock Screener")
st.sidebar.caption("Quantitative analysis of US & European equities")

PAGES = {
    "🏠  Home": "home",
    "📚  Strategies explained": "strategies",
    "🛠️   Setup check": "setup",
    "▶️   Run scripts": "run",
    "🔍  Explore stored data": "explore",
    "❓  Help / FAQ": "help",
}
choice = st.sidebar.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
page = PAGES[choice]

st.sidebar.divider()
st.sidebar.markdown(
    "**Project:** `Tickers_Financials_Fetching_And_Analysis`\n\n"
    "Built by **Afonso** · UI wrapper for onboarding."
)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def check_package(import_name: str) -> tuple[bool, str]:
    try:
        mod = importlib.import_module(import_name)
        ver = getattr(mod, "__version__", "unknown")
        return True, ver
    except ImportError:
        return False, ""


def check_python_version() -> tuple[bool, str]:
    v = sys.version_info
    ok = v.major == 3 and v.minor >= 11
    return ok, f"{v.major}.{v.minor}.{v.micro}"


def check_venv_active() -> tuple[bool, str]:
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    return in_venv, sys.prefix


def load_parquet_safely(path: Path) -> pd.DataFrame | None:
    try:
        return pd.read_parquet(path)
    except Exception as e:  # noqa: BLE001
        st.error(f"Failed to read {path.name}: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "home":
    st.title("📈 Quantitative Stock Screener")
    st.markdown(
        """
        **One-line summary:** download the last years of financial statements
        for US-listed companies and rank them using two
        peer-reviewed investing frameworks.
        """
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Companies supported", "~1,800 US", "EU in progress")
    col2.metric("Strategies", "2", "Fama-French + Fair Value")
    col3.metric("Data source", "FinViz + Yahoo", "free tier")

    st.divider()

    st.subheader("What this project does (in plain language)")
    st.markdown(
        """
        Picking stocks usually means reading a lot of noise — news, opinions,
        hot takes, Twitter, Reddit. This project throws all that away and asks
        one cold, quantitative question:

        > **Given only the numbers a company reports, is its stock attractive
        > to buy right now?**

        It does this by:

        1. 🔍  **Scraping** the 3 financial statements (Balance Sheet,
           Income Statement, Cash Flow Statement) from FinViz.
        2. 💾  **Storing** the data locally as Parquet files — so you don't
           need to re-download every time (scraping 1,800 tickers takes
           ~1 hour).
        3. 📊  **Scoring** each stock using two complementary frameworks:
            - **Fama-French 5-Factor model** (value, profitability, beta,
              momentum, investment)
            - **Fair Value by financial persistence** (revenue/EPS growth,
              margin stability, debt coverage — all over a 5+ year window)
        4. 🏆  **Ranking** tickers so you can focus on the top candidates.

        *Qualitative factors (management, narrative, moat) are deliberately
        excluded — the analysis is only based on reported financials
        by each company and market performance of the company to compute
        pricing ratios.*
        """
    )

    st.info(
        "👉 If this is your first time, head to **🛠️ Setup check** to verify "
        "your environment, then read **📚 Strategies explained**."
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: STRATEGIES EXPLAINED
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "strategies":
    st.title("📚 Strategies Explained")
    st.caption("How the two screening frameworks work — beginner-friendly version.")

    tab1, tab2 = st.tabs(["1️⃣  Fama-French 5-Factor", "2️⃣  Fair Value / Persistence"])

    with tab1:
        st.subheader("The Fama-French 5-Factor Model (simplified)")
        st.markdown(
            """
            Two Nobel-caliber researchers, Eugene Fama and Kenneth French,
            spent decades studying what actually drives stock returns.
            They concluded that besides raw market exposure (Beta), five
            specific factors systematically predict higher returns. This
            project implements a simplified version:
            """
        )

        factors = [
            (
                "📉  **Value**",
                "Low Price-to-Book companies tend to outperform expensive ones. "
                "Reasoning: expensive stocks have perfection already priced in.",
            ),
            (
                "💰  **Profitability**",
                "Measured as operating margin + debt-adjusted Return on Equity "
                "over N years. Profitable companies survive bad times and "
                "compound faster.",
            ),
            (
                "⚖️  **Beta (market risk)**",
                "Less volatile companies tend to beat more volatile ones on a "
                "risk-adjusted basis over long periods. Counter-intuitive but "
                "robust in the data.",
            ),
            (
                "🚀  **Momentum**",
                "Recent winners tend to keep winning (short-term). Measured "
                "from returns in the last completed month + last completed year.",
            ),
            (
                "🏗️  **Investment discipline**",
                "Companies that grow their fixed assets *conservatively* (vs. "
                "their total asset growth) tend to outperform aggressive "
                "over-investors.",
            ),
        ]
        for title, body in factors:
            st.markdown(f"{title}  \n{body}")
            st.markdown("")

        st.success(
            """
            The script gets the most value when the list of tickers starts to get larger. Why?

            Final Version of the script ranks the tickers in accordance to their own individual
            rankings on each factor. Basically on each factor, the best ticker gets a score of 1 as
            their factor value is the highest. Then that factor is equally weighted with other
            factors.
            So, 5 factors, each value has a 20%, to then to a ranking which ranges from [-100,100],
            where -100 : Extreme Sell and 100 : Extreme Buy.

            Therefore, Higher Rankings, according to the script are seen as better buys considering
            Factor Investing by Eugene Fama and Kenneth French.
            """
        )

        st.error(
            """
            NOTE: Some Factors needed adjustments on their values for the factor to make possible
            the existence of buy rankings from the range of [-100,100]

            Since Value_Factor is never negative as uses P/E & P/B ratios as base and those,
            one needed to adjust tickers value factor by subtracting the mean (always positive)
            to work with a distribution that could result in deductions as it exists with other
            factors.

            Beta_Factor adjust the beta value to the absolute value and calculates its distance
            from zero as a measure of risk and volatility. Volatility and risk wise, when measured
            by beta a stock with the same absolute beta is as risky and volatile, the direction of
            returns is the only thing changing. Therefore, since there is no negative distance,
            mean adjustments were conducted to make sure beta factor followed similar behavior to
            other factors.

            """
        )

    with tab2:
        st.subheader("Fair Value by Financial Persistence")
        st.markdown(
            """
            The second strategy is more demanding: it filters for companies
            with **impeccable historical records**. Everything below must
            hold for **at least 5 years**:
            """
        )

        conditions = [
            "📈  Revenue grows (or is at worst flat) every year.",
            "💵  EPS (earnings per share) grows every year.",
            "📊  Operating margins expand or stay stable.",
            "🧮  Share dilution grows slower than EPS — "
            "so existing shareholders are genuinely wealthier.",
            "🛡️  Short-term debt is fully covered by cash + short-term investments.",
        ]
        for c in conditions:
            st.markdown(f"- {c}")

        st.markdown("")
        st.markdown(
            """
            For companies that pass the filter, the script then runs a
            **3-scenario DCF** (worst / base / best) using:

            - Your chosen minimum **CAGR EPS** and **CAGR Revenue**.
            - A **discount rate** (e.g. 0.15 for 15%).
            - A **forward horizon** (years).
            - Adjustments to historical CAGR for worst/base/best cases.

            Output: an **under/overvaluation score** per ticker.
            """
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SETUP CHECK
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "setup":
    st.title("🛠️ Setup Check")
    st.caption("Verify your environment is ready to run the project.")

    # --- Python ---
    st.subheader("1. Python version")
    ok, ver = check_python_version()
    if ok:
        st.success(f"✅ Python {ver} (≥ 3.11 required)")
    else:
        st.error(
            f"❌ Python {ver} — this project targets 3.11+. "
            "Install a newer version from python.org."
        )

    # --- Virtual env ---
    st.subheader("2. Virtual environment")
    in_venv, prefix = check_venv_active()
    if in_venv:
        st.success(f"✅ Running inside a venv at `{prefix}`")
    else:
        st.warning(
            "⚠️ You don't appear to be inside a virtual environment. "
            "Run `setup.sh` (Unix) or `setup.ps1` (Windows) from the "
            "project root, then restart this app with `streamlit run app.py`."
        )

    # --- Packages ---
    st.subheader("3. Required packages")
    rows = []
    all_ok = True
    for pkg_name, import_name in REQ_PACKAGES:
        installed, ver = check_package(import_name)
        rows.append(
            {
                "Package": pkg_name,
                "Installed": "✅" if installed else "❌",
                "Version": ver if installed else "—",
            }
        )
        if not installed:
            all_ok = False

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if all_ok:
        st.success("All required packages are installed. You're good to go.")
    else:
        st.error(
            "Some packages are missing. Run "
            "`python -m pip install -r requirements.txt` inside your venv."
        )

    # --- System info ---
    st.subheader("4. System info")
    sysinfo = {
        "OS": f"{platform.system()} {platform.release()}",
        "Python executable": sys.executable,
        "Working directory": str(REPO_ROOT),
        "Git available": "✅" if shutil.which("git") else "❌",
    }
    st.table(pd.DataFrame(sysinfo.items(), columns=["Item", "Value"]))


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: RUN SCRIPTS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "run":
    st.title("▶️ Run the strategies")
    st.caption(
        "Afonso's scripts are interactive — they ask questions via terminal "
        "input (directories, Yes/No, number of years). The cleanest way to "
        "run them is in a VSCode terminal."
    )

    st.warning(
        "⚠️ **Streamlit can't drive `input()` prompts.** Use the commands "
        "below in an activated venv terminal, or use VSCode's F5 debug configs."
    )

    st.subheader("Option A — VSCode Run menu (easiest)")
    st.markdown(
        """
        1. Open this folder in VSCode (`code .` from the project root).
        2. Accept the prompt to install recommended extensions.
        3. Press **F5** or go to *Run and Debug* (Ctrl+Shift+D).
        4. Pick the configuration you want from the dropdown:
            - ▶ **Run Fama-French strategy (US)**
            - ▶ **Run Fair Value strategy (US)**
            - ▶ **Run strategies_run.py** (both sequentially)
            - ▶ **Run Streamlit Dashboard** (this app)
        5. Answer the prompts in the integrated terminal.
        """
    )

    st.subheader("Option B — Command line")
    st.code(
        "# 1. Activate the venv\n"
        "# Windows (PowerShell):\n"
        ".\\venv\\Scripts\\Activate.ps1\n"
        "# macOS / Linux / WSL:\n"
        "source venv/bin/activate\n\n"
        "# 2. Run the full pipeline (both strategies):\n"
        "python -m finviz_us.strategies_run\n\n"
        "# Or run only one strategy:\n"
        "python -m finviz_us.data_tickers_and_strats.strat_basic_fama_french.basic_fam_fre\n"
        "python -m finviz_us.data_tickers_and_strats.strat_broad_FV.strat_run\n",
        language="bash",
    )

    st.subheader("Option C — Interactive cells (the Afonso way)")
    st.markdown(
        """
        The `.py` files use `#%%` cell delimiters — VSCode's Jupyter extension
        recognises them. In any strategy file, click **Run Cell** above a
        `#%%` line to execute just that cell. This is great for exploration.
        """
    )

    st.info(
        "ℹ️ On first run, the script will ask for a **storage directory**. "
        "Pick a folder where the parquet financials will be saved — e.g. "
        "`C:\\\\Users\\\\You\\\\Documents\\\\finviz_data` on Windows, or "
        "`~/finviz_data` on Unix."
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EXPLORE STORED DATA
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "explore":
    st.title("🔍 Explore stored financials")
    st.caption(
        "Point this page at your storage directory (where the script saved "
        "parquet files) and browse what's there — no re-scraping required."
    )

    default_dir = st.session_state.get("storage_dir", "")
    storage_dir = st.text_input(
        "Storage directory (absolute path)",
        value=default_dir,
        placeholder=r"e.g. C:\Users\You\Documents\finviz_data   or   /home/you/finviz_data",
        help="The same path you typed when running the scripts.",
    )
    st.session_state["storage_dir"] = storage_dir

    if not storage_dir:
        st.info("Enter a directory path above to start exploring.")
        st.stop()

    root = Path(storage_dir).expanduser()
    if not root.exists():
        st.error(f"Directory not found: `{root}`")
        st.stop()

    statements = ["bal_sheet", "inc_stat", "stat_cfs"]
    missing = [s for s in statements if not (root / s).exists()]
    if missing:
        st.error(
            f"Directory `{root}` is missing these subfolders: {missing}. "
            "Has the fetch script finished running?"
        )
        st.stop()

    # Collect tickers (files in bal_sheet/*.parquet)
    bs_dir = root / "bal_sheet"
    tickers = sorted(p.stem for p in bs_dir.glob("*.parquet"))

    if not tickers:
        st.warning(f"No parquet files found in `{bs_dir}`.")
        st.stop()

    st.success(f"Found **{len(tickers)}** tickers in `{root}`.")

    col1, col2 = st.columns([1, 3])
    with col1:
        ticker = st.selectbox("Ticker", tickers, index=0)
    with col2:
        statement = st.radio(
            "Statement",
            statements,
            horizontal=True,
            format_func=lambda s: {
                "bal_sheet": "📊 Balance Sheet",
                "inc_stat": "💵 Income Statement",
                "stat_cfs": "🏦 Cash Flows",
            }[s],
        )

    path = root / statement / f"{ticker}.parquet"
    if not path.exists():
        st.warning(f"{statement} not available for {ticker} (file not found).")
        st.stop()

    df = load_parquet_safely(path)
    if df is None:
        st.stop()

    st.subheader(f"{ticker} — {statement}")
    st.dataframe(df, use_container_width=True)

    with st.expander("📥 Download this statement as CSV"):
        csv = df.to_csv(index=True).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv,
            file_name=f"{ticker}_{statement}.csv",
            mime="text/csv",
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HELP / FAQ
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "help":
    st.title("❓ Help & FAQ")

    with st.expander("Why does the first fetch take so long?", expanded=True):
        st.markdown(
            "FinViz throttles requests. Scraping the Balance Sheet + Income "
            "Statement + Cash Flow Statement for ~1,800 tickers with a small "
            "`time.sleep` between calls adds up to 45–60 minutes. "
            "**Good news:** once you've stored the parquet files, subsequent "
            "runs read from disk in seconds."
        )

    with st.expander("I got a timeout or my internet dropped mid-fetch"):
        st.markdown(
            "The comment in `organizing_tickers.py` has the recipe: restart "
            "with `tickers_lst[last_index_printed:]` as input, answering the "
            "same Yes/No prompts as before. Already-stored tickers are skipped "
            "automatically."
        )

    with st.expander("What's the difference between Annual and Quarterly?"):
        st.markdown(
            "The helpers fetch **Annual** (`'A'`) by default because the "
            "strategies need multi-year history. Quarterly is in the code "
            "but not wired into the default pipeline."
        )

    with st.expander("The European (Yahoo) script doesn't work"):
        st.markdown(
            "Correct — `yahoo_finance/yf_provisional.py` is marked "
            "*'IGNORE THIS FILE FOR NOW IT IS NOT WORKING YET'* by the "
            "author. It's a sketch for a future escalation to European "
            "equities via `yfinance`. Skip it for now."
        )

    with st.expander("I get 'No module named finviz_us'"):
        st.markdown(
            "Run the script **from the project root** with `python -m`:\n\n"
            "```bash\n"
            "cd path/to/US_EUR_Financials_Import_Diff_Struc\n"
            "python -m finviz_us.strategies_run\n"
            "```\n\n"
            "The absolute imports (`from finviz_us...`) require the package "
            "root to be on `sys.path`, which `-m` does automatically."
        )

    with st.expander("Is my data sent anywhere?"):
        st.markdown(
            "No. Financial data is downloaded from FinViz/Yahoo Finance and "
            "stored **only on your machine** as parquet files. This dashboard "
            "runs locally on `localhost:8501`."
        )

    st.divider()
    st.markdown(
        "**Need more help?** Open an issue on the project's GitHub repo, "
        "or ping Afonso directly."
    )


