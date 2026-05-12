# 📈 Tickers Financials Fetching & Analysis

# 🤖 README.md was built using AI in the vast majority. EVERYTHING RELATED TO Shell & PowerShell was built using AI.

> Quantitative stock screener for US (and, eventually, European) equities —
> scrapes 3 financial statements, stores them locally, and ranks tickers with
> two peer-reviewed investing frameworks.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

---

## 📚 Table of contents

1. [What is this?](#-what-is-this)
2. [Prerequisites](#-prerequisites)
3. [🏦🧺📈 Storaging/Caching of ETFs](#-Storaging/Caching-of-ETFs)
4. [🚀 Quickstart — from zero to running](#-quickstart--from-zero-to-running)
5. [Project layout](#-project-layout)
6. [Running the strategies](#%EF%B8%8F-running-the-strategies)
7. [Optional: the friendly dashboard](#-optional-the-friendly-dashboard)
8. [Troubleshooting](#-troubleshooting)
9. [For developers](#-for-developers)
10. [License](#-license)

---

## ❓ What is this?

Picking stocks usually means drowning in opinions, tweets and hot takes. This
project takes the opposite approach: it looks **only at the numbers** a
company publishes and asks one cold question — _"Based on the balance sheet,
income statement and cash-flow statement, is this stock attractive right
now?"_

It works in four steps:

1. 🔍 **Scrapes** the 3 financial statements for each ticker from
   [FinViz](https://finviz.com/) (free tier) and yfinance.
2. 💾 **Stores** them locally as Parquet files so you only pay the
   scraping cost once (~1 hour for ~1,800 US tickers,using FinViz).
   yfinance tends to take longer as it uses ETF tickers to then use yf (~2 hour for ~1000 tickers as the number of requests is much higher than FinViz)
3. 📊 **Scores** each company using two frameworks:
    - **Fama-French 5-Factor** — value, profitability, beta, momentum,
      investment discipline.
    - **Fair Value by Persistence** — 5+ year consistency in revenue / EPS
      growth, margin stability, debt coverage, followed by a 3-scenario DCF.
4. 🏆 **Ranks** tickers so you can focus on the top candidates.

> ⚠️ **This is not investment advice.** It's a learning tool and a way to
> reduce screening noise. Any decisions are yours.

---

## ✅ Prerequisites

You'll need **three** things installed before you start. If you already have
them, skip to the [Quickstart](#-quickstart--from-zero-to-running).

### 1. Python 3.11 or newer

- **Windows / macOS:** [python.org/downloads](https://www.python.org/downloads/)
  → during install, **tick the "Add python.exe to PATH" box**.
- **Linux:** `sudo apt install python3 python3-venv` (Ubuntu/Debian) or the
  equivalent for your distro.

Verify in a terminal:

```bash
python --version        # should print Python 3.11.x or newer
```

### 2. Git

- [git-scm.com/downloads](https://git-scm.com/downloads)
- On macOS, running `git` once triggers the Xcode tools installer.

Verify:

```bash
git --version
```

### 3. Visual Studio Code

- Download: [code.visualstudio.com](https://code.visualstudio.com/)
- Once installed, open VSCode. When you open this project it will prompt you
  to install the **recommended extensions** (Python, Pylance, Jupyter, Ruff).
  **Click "Install all".** This repo ships with the list in
  `.vscode/extensions.json`.

---

## 🏦🧺📈 Storaging/Caching of ETFs


#### Step 1 · Seek ETFs Providers

The program is prepared to **ONLY** handle ETFs from **iShares** (BlackRock Branch)
& **StateStreet** as one saw them as the most well known ETF providers that
provided some sort of info through excel files on their holdings.

Donwload the ETFs into a directory of your choice in your device.

#### Step 2 - Transform the ETF Data

**2.1 - iShares ETF - CURRENTLY EUROPEAN TICKERS ONLY**

Whenever you download an ETF from this providers with European tickers,
you will get .csv files. So this steps must be followed to ensure the program
reads the ETF

**2.1.1 - TRANSFORM THE CSV FILES TO PRESENT THAT DATA IN EACH CELLS**

**2.1.2 - FIGURE OUT THE DATA RANGE THAT HAS THE TICKERS INFO**

**2.1.3 - ERASE ANYTHING THAT IS OUTSIDE THE SCOPE OF THE RANGE WHERE THERE IS TICKER INFO**

**2.1.4 - AFTER ERASING EVERYTHING, SELECT THE ENTIRE RANGE AND MOVE IT TO CELL A1**

**2.1.5 - MAKE SURE TICKERS ON TICKER COLUMN THAT HAVE LETTERS AND NUMBERS ARE NOT IN FORM OF DATES, FOR EXAMPLE 'JUN3' APPEARS IN DATE AND NOT IN TICKER FORM**

**AFTER THIS SAVE THE ETF BY KEEPING THE CSV FORMAT WHEN SAVING AND IT IS READY TO BE WORKED**

**2.2 - StateStreet ETFs**

Whenever you download an ETF from this providers with tickers,
you will get .xlsx files. So this steps must be followed to ensure the program
reads the ETF.

**2.2.1 - FIGURE OUT THE DATA RANGE THAT HAS THE TICKERS INFO**

**2.2.2 - ERASE ANYTHING THAT IS OUTSIDE THE SCOPE OF THE RANGE WHERE THERE IS TICKER INFO**

**2.2.3 - AFTER ERASING EVERYTHING, SELECT THE ENTIRE RANGE AND MOVE IT TO CELL A1**

**2.2.4 - MAKE SURE TICKERS ON TICKER COLUMN THAT HAVE LETTERS AND NUMBERS ARE NOT IN FORM OF DATES, FOR EXAMPLE 'JUN3' APPEARS IN DATE AND NOT IN TICKER FORM**

**AFTER THIS SAVE THE ETF BY KEEPING THE CSV FORMAT WHEN SAVING AND IT IS READY TO BE WORKED**

---

## 🚀 Quickstart — from zero to running

The short version, for copy-pasters:

### Windows (PowerShell)

```powershell

# 1. Set Directory to clone the project
cd Wanted_Directory

# 2. Clone the repo
git clone <REPO_URL>
cd Tickers_Financials_Fetching_And_Analysis

# 3. One-click setup (creates venv + installs everything)
powershell -ExecutionPolicy Bypass -File    Wanted_Directory\Tickers_Financials_Fetching_And_Analysis
\setup.ps1

# 4. Open in VSCode — accept the "Install recommended extensions" prompt
code .

# 5. Run the friendly dashboard - OPTIONAL, NO NEED UF YOU RUN AT THE IDE
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

### macOS / Linux / WSL (bash)

```bash

# 0. NOTE: I DID NOT TRY THIS PROCEDURE IN THIS OPERATING SYSTEM.

# 1. Clone the repo
git clone <REPO_URL>
cd Tickers_Financials_Fetching_And_Analysis

# 2. One-click setup
chmod +x setup.sh
./setup.sh

# 3. Open in VSCode — accept the "Install recommended extensions" prompt
code .

# 4. Run the friendly dashboard
source venv/bin/activate
streamlit run app.py
```

Your browser should open at <http://localhost:8501> showing the dashboard. 🎉

---

### Step-by-step (first-timers version)

If the block above felt like magic, here is the same flow broken down:

<details>
<summary><b>Click to expand the detailed walkthrough</b></summary>

#### Step 1 · Clone the repository

Open a terminal (PowerShell on Windows, Terminal on macOS, anything on
Linux) and navigate to where you keep your projects. Then:

```bash
git clone <REPO_URL>
```

This downloads the whole project into a folder of the same name.
Move into it:

```bash
cd Tickers_Financials_Fetching_And_Analysis
```

#### Step 2 · Create a virtual environment

A **venv** is a sandboxed copy of Python just for this project, so you don't
pollute your system installation.

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS / Linux / WSL:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Your prompt should now show `(venv)` at the start. **Leave this terminal
open** — every command below runs inside it.

#### Step 3 · Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This pulls in pandas, finvizfinance, yfinance, streamlit and the rest.
Takes ~2 minutes on a decent connection.

#### Step 4 · Open in VSCode

```bash
code .
```

On the bottom-right, VSCode will ask if you want to install the recommended
extensions. **Click "Install all"** — this repo ships with the list.

On the bottom-left status bar, confirm that the Python interpreter shown is
`Python 3.X.X ('venv': venv)`. If not, click it and pick the one inside
`./venv`.

#### Step 5 · Launch the dashboard (optional but recommended)

```bash
streamlit run app.py
```

Your browser opens at <http://localhost:8501>. The dashboard has:

- 🏠 **Home** — what the project does, in plain language.
- 📚 **Strategies explained** — Fama-French + Fair Value without jargon.
- 🛠️ **Setup check** — confirms your Python/venv/packages are all good.
- ▶️ **Run scripts** — the commands to trigger the actual scraping.
- 🔍 **Explore stored data** — browse parquet files without re-scraping.

Stop the dashboard with **Ctrl+C** in the terminal.

#### Step 6 · Run the strategy (finally)

Inside the same venv-activated terminal:

```bash
python -m run.py
```

The script will ask a series of questions — directory for storage, list of
tickers, number of years for averages, etc. Answer them and wait.
On first run with ~1,800 tickers for FinViz, expect **45 – 60 minutes**.
For yfinance depending on the numbers of tickers you use, either individually
or scrapping from ETF time varies. If no previous storage and ETF has a large
number of tickers, yfinance can take up to **2-3 hours** in the first run and
every time you decide to update a storage of yours.(assuming you already have
a large number or cached tickers)

</details>

---

## 🗂 Project layout

```
Tickers_Financials/
├── app.py                              # Streamlit dashboard (friendly UI)
├── run.py                              # Runs the strategies created
├── setup.ps1                           # Windows one-click setup
├── setup.sh                            # Unix one-click setup
├── requirements.txt                    # Python dependencies
├── README.md                           # You are here
│
├── .vscode/
│   ├── settings.json                   # Points Python to ./venv
│   ├── extensions.json                 # Recommended extensions
│   ├── launch.json                     # Press F5 to debug/run strategies
│   └── tasks.json                      # Predefined tasks
│
├── finviz_us/                          # US screener (FinViz-based)
│   ├── helpers_file_root               # Folder with file with functions used in run.py
│   │   ├──  helpers_root.py            # File with functions that will be used in run.py
│   ├── organize_tickers/               # Folder with file responsible fetching and handling tickers info
│   │   ├──  helpers_finviz/            # Contains the file with functions used at "organizing_tickers.py"
│   │   │    ├──  helpers_func.py       # File with helper functions for data organization
│   │   ├──  organizing_tickers.py      # File which runs code from functions to fetch tickers' data
│   ├── strategies/                     # Contains all strategies
│   │   ├── miscellaneous/              # Contains all the stuff that is unused but might be important
│   │   │  ├──  help_func/              # Folder with file with helpers
│   │   │  │ ├──  help_func.py          # File with helpers with ratios not used for now.
│   │   │  ├── strat_to_build.py        # Nothing build yet.
│   │   ├── strat_basic_fama_french/    # 5-Factor model related content
│   │   │  ├──  fama_french_helpers/    # Folder with file with helpers for factor calculation
│   │   │  │ ├──  ff_helpers.py         # File with five factor functions
│   │   │  ├── basic_fam_fre.py         # File with strategy run on a cell basis. Able to see inputs step-by-step.
│   │   │  ├── func_strat_run.py        # File with function created with the entire strategy
│   │   ├── strat_broad_FV/             # Fair Value by persistence
│   │   │  ├──  helpers_func/           # Folder with file with helpers for FV Calculation for tickers.
│   │   │  │ ├──  helpers.py            # File with FV functions based on 3 statements.
│   │   │  ├── func_strat_run.py        # File with function created with the entire strategy
│   │   │  ├── strat_run.py             # File with strategy run on a cell basis. Able to see inputs step-by-step.
│
│
|   🚧🚧🚧Yahoo Finance Script currently being built 🚧🚧🚧
|
|
|── yahoo_finance/                      # Rest of the world screener (YahooFinance-based)
│   ├── helpers_file_root               # Folder with file with functions used in run.py NOT CREATED YET
│   │   ├──  helpers_root.py            # File with functions that will be used in run.py NOT CREATED YET
│   ├── organize_tickers/               # Folder with file responsible fetching and handling tickers info
│   │   ├──  helpers_org/               # Contains the file with functions used at "organizing_tickers.py"
│   │   │    ├──  helpers.py            # File with helper functions for data organization of 'yfinance'
│   │   ├──  organizing_tickers.py      # File which runs code from functions to fetch tickers' data
│   ├── strategies/                     # Contains all strategies
│   │   ├── miscellaneous/              # Contains all the stuff that is unused but might be important
│   │   │  ├──  help_func/              # Folder with file with helpers
│   │   │  │ ├──  help_func.py          # File with helpers with ratios not used for now.
│   │   │  ├── strat_to_build.py        # Nothing build yet.
│   │   ├── strat_basic_fama_french/    # 5-Factor model related content
│   │   │  ├──  fama_french_helpers/    # Folder with file with helpers for factor calculation
│   │   │  │ ├──  ff_helpers.py         # File with five factor functions
│   │   │  ├── basic_fam_fre.py         # File with strategy run on a cell basis. Able to see inputs step-by-step.
│   │   │  ├── func_strat_run.py        # File with function created with the entire strategy
│   │   ├── strat_broad_FV/             # Fair Value by persistence
│   │   │  ├──  helpers_func/           # Folder with file with helpers for FV Calculation for tickers.
│   │   │  │ ├──  helpers.py            # File with FV functions based on 3 statements.
│   │   │  ├── func_strat_run.py        # File with function created with the entire strategy
│   │   │  ├── strat_run.py             # File with strategy run on a cell basis. Able to see inputs step-by-step.
```

---

## ▶️ Running the strategies

There are **three** ways to run the actual strategy scripts — pick the one
that feels natural.

### ① From VSCode (F5 — easiest)

With the project open in VSCode:

1. Press **Ctrl+Shift+D** (or click the **Run and Debug** icon).
2. Pick one of the configurations from the dropdown:
    - `▶ Run Fama-French strategy (US)`
    - `▶ Run Fair Value strategy (US)`
    - `▶ Run strategies_run.py` (both sequentially)
    - `▶ Run Streamlit Dashboard`
3. Press **F5**. Answer the prompts in the integrated terminal.

### ② From the command line

```bash
# Activate the venv first (every new terminal)
source venv/bin/activate              # Unix
.\venv\Scripts\Activate.ps1           # Windows

# Then:
python -m finviz_us.strategies_run    # both strategies
python -m finviz_us.data_tickers_and_strats.strat_basic_fama_french.basic_fam_fre
python -m finviz_us.data_tickers_and_strats.strat_broad_FV.strat_run
```

> 💡 **Always use `python -m`**, not `python path/to/file.py`. The project
> uses absolute imports (`from finviz_us...`) which need the package root on
> `sys.path` — `python -m` handles this automatically.

### ③ Interactively, cell-by-cell (Afonso's way)

The `.py` files contain `#%%` cell delimiters. In VSCode, with the Jupyter
extension installed, you'll see **▷ Run Cell** / **▷ Run Below** buttons
above every `#%%` line. This is the best mode for exploration and
experimentation.

---

## 🎛 Optional: the friendly dashboard

For non-technical users (or when you just want to explore results), run:

```bash
streamlit run app.py
```

The dashboard won't run the interactive fetch pipeline for you (the scripts
use `input()` prompts that Streamlit can't drive), but it **will**:

- Explain everything the project does in plain language.
- Check that your Python version, venv and packages are all correct.
- Show the exact commands to run the strategies.
- **Browse the stored Parquet files** after a fetch — pick a ticker and
  see its Balance Sheet / Income Statement / Cash Flows without having to
  rescrape anything.

---

## 🧰 Troubleshooting

<details>
<summary><b><code>ModuleNotFoundError: No module named 'finviz_us'</code></b></summary>

Run from the **project root** using `python -m`:

```bash
cd path/to/Tickers_Financials
python -m finviz_us.strategies_run
```

Don't run `python finviz_us/strategies_run.py` — that bypasses the package
mechanism.

</details>

<details>
<summary><b>PowerShell: <code>cannot be loaded because running scripts is disabled</code></b></summary>

Run once in an elevated PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try `.\venv\Scripts\Activate.ps1` again.

</details>

<details>
<summary><b><code>pip install</code> fails with SSL / certificate errors</b></summary>

Upgrade pip first:

```bash
python -m pip install --upgrade pip
```

If you're behind a corporate proxy, set `HTTPS_PROXY` in your environment.

</details>

<details>
<summary><b>FinViz scraping is slow or timing out</b></summary>

FinViz rate-limits. The scripts already sleep between requests, but if you
get timeouts:

1. Note the **last ticker index printed** in the console.
2. Restart the script.
3. Answer the same Yes/No prompts as before.
4. When asked for tickers, pass `tickers_lst[last_index:]`.

Already-stored tickers are skipped automatically via the parquet cache.

</details>

<details>
<summary><b>The Yahoo Finance (European) script doesn't work</b></summary>

Correct. `yahoo_finance/yf_provisional.py` is marked
*"IGNORE THIS FILE FOR NOW IT IS NOT WORKING YET"* by the author — it's a
sketch for a future escalation to European equities. Skip it for now.

</details>

<details>
<summary><b>VSCode is using the wrong Python interpreter</b></summary>

Bottom-left status bar → click the Python version → pick the one inside
`./venv`. The shipped `.vscode/settings.json` points to this automatically
on most setups.

</details>

---

## 👨‍💻 For developers

### Package the project

The project uses absolute imports (`from finviz_us...`). If you want to
`pip install` it as a package, add a minimal `pyproject.toml`:

```toml
[project]
name = "tickers-financials"
version = "0.1.0"
requires-python = ">=3.11"
```

### Run a single cell from a script

VSCode's Python extension recognises `#%%` as a cell boundary. Place your
cursor inside a cell and press **Shift+Enter** to send it to an interactive
window — great for debugging one factor at a time.

### Where to add a new strategy

Drop a new module into `finviz_us/data_tickers_and_strats/` following the
pattern of `strat_basic_fama_french/`:

```
strat_your_name/
├── __init__.py
├── your_main.py
└── your_helpers/
    ├── __init__.py
    └── helpers.py
```

Then wire it into `strategies_run.py` or call it directly.

---

## 📄 License

MIT — do whatever you want, just don't sue the author if your stock picks
go south. Not investment advice.
