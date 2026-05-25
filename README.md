# Live Top 20 Corporate Trend Analytics Dashboard

A lightweight, high-performance Python data pipeline that monitors financial media in real-time. The system orchestrates raw data ingestion from NewsAPI, filters text blocks using case-normalization, strips messy trailing punctuation, maps market colloquialisms via an optimized dictionary lookup, and ranks corporate mentions instantly using an algorithmic frequency counter.

## Key Features
- **Dynamic Parameter Engineering:** Automatically constructs compact API search query parameters using ticker verification (`.isupper()`) to stay cleanly under standard character boundaries.
- **Robust Text Normalization:** Lowercases sentences and strips punctuation (`,.!?"\'`) to match slang variants effortlessly (e.g., `"apple"`, `"AAPL"`, and `"Apple,"` all resolve to `"Apple Inc."`).
- **High-Performance Lookups:** Utilizes a decoupled $O(1)$ inverted hash dictionary for near-instant classification and tracking.
- **Fail-Safe Pipeline Core:** Implements aggressive connection guardrails (`raise_for_status()`) and structural data padding to ensure a clean 20-company leaderboard layout under any news cycle volume.

---

## Technical Architecture Flow

Below is the design of the decoupled data processing pipeline:

```text
  ┌───────────────────┐      Real-Time Text Stream       ┌───────────────────┐
  │  data_ingestor.py │ ───────────────────────────────> │  nlp_processor.py │
  └───────────────────┘                                  └───────────────────┘
            │                                                      │
    Pulls 100 Highly                                        Strips Punctuation,
   Relevant Articles                                         Normalizes Case, &
            │                                               Maps Slang to Names
            ▼                                                      ▼
  ┌───────────────────┐                                  ┌───────────────────┐
  │     NewsAPI       │                                  │ collections.Value │
  │    Endpoints      │                                  │   Counter Core    │
  └───────────────────┘                                  └───────────────────┘
            │                                                      │
            │          Aggregated Metric Leaderboard Chart         │
            └──────────────────────────────────────────────────────┘
                                       │
                                       ▼
                             ┌───────────────────┐
                             │      main.py      │
                             │ (Terminal Output) │
                             └───────────────────┘
```

---

## Step-by-Step Setup and Execution Guide

Follow these sequential steps to install Python, configure your working environment, and ignite the dashboard.

### Step 1: Install the Latest Version of Python
To execute this modern script safely, you must have the latest stable release of Python 3 installed.

#### On Windows:
1. Navigate to the official download portal: [python.org/downloads](https://www.python.org/downloads/).
2. Click the **Download Python 3.x.x** button to download the executable installer.
3. **CRITICAL:** Launch the downloaded installer and check the box at the bottom that reads: **"Add python.exe to PATH"**. If you skip this, your terminal will not recognize Python commands.
4. Click **Install Now** and wait for completion.

#### On macOS:
1. Download the macOS 64-bit universal installer from [python.org/downloads](https://www.python.org/downloads/).
2. Open the package installer and step through the standard installation wizard.
3. *Alternative (Recommended for developers):* If you use Homebrew, open your Terminal and execute:
   ```bash
   brew install python
   ```

#### Verify the Installation:
Open your system command prompt or terminal and type the following command to verify your version:
```bash
python --version
```
*(On macOS/Linux, if `python` points to a default legacy version, use `python3 --version` instead).*

---

### Step 2: Open Terminal & Navigate to Your Project Folder
Your system terminal operates relative to a specific directory path. You must explicitly point your terminal into your local repository to run your script files.

1. Open your terminal application (**Command Prompt/PowerShell** on Windows, or **Terminal** on macOS).
2. Use the Change Directory (`cd`) command followed by the absolute or relative path to where your project folder lives. For example:

   **On macOS:**
   ```bash
   cd /Users/Yourusername/top-20-most-talked-about-companies
   ```

   **On Windows:**
   ```cmd
   cd C:\Users\YourUsername\top-20-most-talked-about-companies
   ```

3. Confirm you are in the right folder by listing the contents of the directory:
   - **macOS/Linux command:** `ls`
   - **Windows command:** `dir`
   
   Ensure you see `main.py`, `config.py`, `data_ingestor.py`, and `nlp_processor.py` listed on the screen.

---

### Step 3: Configure Environment Variables
The ingestion layer depends on secure API keys. Ensure you have a `.env` file placed directly in the **root folder** of your project matching this layout:

```env
NEWS_API_KEY=your_actual_news_api_key_here
SCRAPINGBEE_API_KEY=your_actual_scrapingbee_key_here
```

---

### Step 4: Install Dependencies
Before firing the application engine, install the required packages within your project directory:

```bash
pip install requests python-dotenv
```
*(Use `pip3 install requests python-dotenv` on macOS if necessary).*

---

### Step 5: Execute the Engine
With your terminal accurately sitting inside your root directory and dependencies successfully locked, ignite the pipeline runner by typing:

```bash
python main.py
```
*(Use `python3 main.py` on macOS if required).*

#### Expected Console Output Sequence:
```text
Fetching news articles...
Processing news articles...
Displaying results...

=== TOP 20 MOST TALKED ABOUT COMPANIES ===
1. NVIDIA Corp. — Mentioned 43 times
2. Apple Inc. — Mentioned 31 times
3. Microsoft Corp. — Mentioned 18 times
...
20. Visa Inc. — Mentioned 0 times
```

---

## Clean Architecture Directory Layout
```text
top-20-most-talked-about-companies/
│
├── .env                  # Secure local API key configuration file
├── config.py             # Global constants, lookup matrices, & validation checks
├── data_ingestor.py      # Network fetching pump with parameterized query handling
├── nlp_processor.py      # Text tokenization, cleaning, and tracking metrics core
└── main.py               # Central execution pipeline orchestrator
```