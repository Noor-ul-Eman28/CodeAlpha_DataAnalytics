# CodeAlpha Data Analytics Internship — Book Catalogue Project

**Intern:** Noor-ul-Eman
**Track:** Data Analytics  
**Tasks:** Web Scraping, Exploratory Data Analysis, and Data Visualization

## Project overview

This project uses one book catalogue dataset across three data analytics tasks. The data is collected through web scraping, then analyzed and visualized.

```text
Web scraping → scraped_books.csv → exploratory analysis → visualizations
```

The source is [Books to Scrape](https://books.toscrape.com/), a practice website containing roughly 1,000 fictional books. The catalogue includes information such as title, category, price, star rating, and stock status.

## Dataset note

The scraper in `task1_web_scraping.py` is designed to collect the live catalogue data, but the CSV included in this repository is a same-schema sample dataset created during development. It should be replaced with fresh data before the project is submitted.

To collect the live data, install the dependencies and run:

```bash
python -m pip install requests beautifulsoup4 pandas lxml
python task1_web_scraping.py
```

The scraper will save the result to `data/scraped_books.csv`. The analysis and visualization scripts use the same column names, so they can then be run without further changes.

## Repository structure

```text
CodeAlpha_DataAnalytics/
├── README.md
├── task1_web_scraping.py
├── task2_eda.py
├── task3_data_visualization.py
├── data/
│   └── scraped_books.csv
└── outputs/
    ├── eda_report.md
    └── visuals/
        ├── 1_price_distribution.png
        ├── 2_top_categories.png
        ├── 3_rating_distribution.png
        ├── 4_price_by_rating.png
        ├── 5_avg_price_by_category.png
        └── 6_dashboard.png
```

## Task 1: Web scraping

**File:** `task1_web_scraping.py`

The scraper:

- visits the catalogue pages and handles pagination;
- extracts each book's title, price, rating, and stock status;
- visits individual product pages to obtain the category and UPC;
- converts prices and star ratings into usable numeric values; and
- removes duplicate UPCs before saving the CSV file.

Run it with:

```bash
python task1_web_scraping.py
```

## Task 2: Exploratory data analysis

**File:** `task2_eda.py`  
**Output:** `outputs/eda_report.md`

The analysis covers the structure of the dataset, category and rating distributions, price trends, possible outliers, and data-quality issues. It also checks whether rating and stock status provide useful information about price.

The main observations from the current dataset are:

- prices are right-skewed, with a small number of high-value books;
- the relationship between rating and price is weak;
- stock status has limited analytical value because most books are in stock; and
- duplicate UPCs, missing ratings, and unusually high prices should be checked before using the data for further analysis.

Run it with:

```bash
python task2_eda.py
```

## Task 3: Data visualization

**File:** `task3_data_visualization.py`  
**Output:** six PNG files in `outputs/visuals/`

The script creates visualizations for:

| File | Visualization | Purpose |
|---|---|---|
| `1_price_distribution.png` | Histogram and KDE plot | Show the distribution of prices |
| `2_top_categories.png` | Horizontal bar chart | Compare the largest categories |
| `3_rating_distribution.png` | Count plot | Show the distribution of star ratings |
| `4_price_by_rating.png` | Boxplot | Compare prices across ratings |
| `5_avg_price_by_category.png` | Horizontal bar chart | Compare average prices by category |
| `6_dashboard.png` | Combined 2×2 dashboard | Summarize the main patterns |

Run it with:

```bash
python task3_data_visualization.py
```

## Running the full project

```bash
python -m pip install requests beautifulsoup4 pandas numpy matplotlib seaborn lxml
python task1_web_scraping.py
python task2_eda.py
python task3_data_visualization.py
```

## Notes for submission

Before submitting the project, replace the sample CSV with the output from a live scrape and regenerate the analysis report and visualizations. The repository contains three completed tasks: web scraping, exploratory data analysis, and data visualization.

## Source

- [Books to Scrape](https://books.toscrape.com/)
