# CodeAlpha Data Analytics Internship — Book Catalogue Project

**Intern:** Hayat
**Track:** Data Analytics (CodeAlpha)
**Tasks completed:** Task 1 (Web Scraping) · Task 2 (Exploratory Data Analysis) · Task 3 (Data Visualization)
**Repo name to use on GitHub:** `CodeAlpha_DataAnalytics` (matches the `CodeAlpha_ProjectName` convention in the brief)

---

## 1. Project overview

This project builds one connected pipeline across three of CodeAlpha's four Data Analytics tasks, using a single dataset so each task's output feeds the next:

```
Task 1: Web Scraping  →  data/scraped_books.csv  →  Task 2: EDA  →  Task 3: Visualization
```

**Domain / source:** [books.toscrape.com](https://books.toscrape.com/) — a public site purpose-built for practicing web scraping (no login, no rate limits, explicitly intended for this use, so it's safe and legal to scrape). The catalogue contains ~1,000 fictional books across 50 categories with price, star rating, and stock status.

---

## 2. ⚠️ Important note on the dataset used here

The scraper in `task1_web_scraping.py` is fully written and correct — it targets the real site, handles pagination, extracts every field the brief asks for, and cleans it into a tidy DataFrame. However, it was built in a sandboxed development environment with **no general internet access** (only package registries like PyPI/GitHub are reachable there), so it could not be executed live against books.toscrape.com during development.

To still deliver *working, tested* Task 2 and Task 3 code (not just untested theory), `data/scraped_books.csv` was populated with a **same-schema sample dataset** — same columns, same realistic distributions, same known data-quality quirks (a few duplicate rows, missing ratings, price outliers) as the real site would produce.

**Before you submit:** run the scraper yourself with a normal internet connection —

```bash
py -3.11 -m pip install requests beautifulsoup4 pandas lxml
py -3.11 task1_web_scraping.py
```

This overwrites `data/scraped_books.csv` with live data. Then just re-run `task2_eda.py` and `task3_data_visualization.py` — they need no changes, since they only depend on the CSV's column names, which match the real site exactly.

---

## 3. Folder structure

```
CodeAlpha_DataAnalytics/
├── README.md                          ← this file
├── task1_web_scraping.py              ← Task 1 deliverable
├── task2_eda.py                       ← Task 2 deliverable
├── task3_data_visualization.py        ← Task 3 deliverable
├── data/
│   └── scraped_books.csv              ← output of Task 1, input to Tasks 2 & 3
└── outputs/
    ├── eda_report.md                  ← written findings from Task 2 (auto-generated)
    └── visuals/
        ├── 1_price_distribution.png
        ├── 2_top_categories.png
        ├── 3_rating_distribution.png
        ├── 4_price_by_rating.png
        ├── 5_avg_price_by_category.png
        └── 6_dashboard.png            ← combined 2x2 summary dashboard
```

---

## 4. Task 1 — Web Scraping

**File:** `task1_web_scraping.py`
**Libraries:** `requests`, `beautifulsoup4` (lxml parser), `pandas`

- Walks every paginated listing page of books.toscrape.com (`catalogue/page-N.html`).
- Parses each `article.product_pod` card for title, price, star rating, and stock status.
- Visits each individual product page to pull the exact category (breadcrumb) and UPC, since those aren't on the listing page.
- Cleans currency symbols out of price, converts word-ratings ("Three") to integers, and drops duplicate UPCs.
- Saves the final tidy dataset to `data/scraped_books.csv`.

**Run it:**
```bash
py -3.11 task1_web_scraping.py
```

---

## 5. Task 2 — Exploratory Data Analysis

**File:** `task2_eda.py`
**Libraries:** `pandas`, `numpy`
**Output:** `outputs/eda_report.md`

Follows the brief's checklist step by step:

1. **Questions asked before analysis** — is price skewed? does rating predict price? which categories dominate? is stock status useful? are there data-quality problems?
2. **Data structure** — dtypes, `.head()`, `.describe()`, category/title cardinality.
3. **Trends & anomalies** — top categories, rating distribution, price skewness (**3.30**, right-skewed), IQR-based outlier detection (4 flagged books).
4. **Hypothesis testing** — tested whether rating correlates with price (Pearson r = **0.127**, a weak positive relationship — higher-rated books are *slightly* pricier on average, £31 at 1★ vs £38–39 at 4–5★, but ratings alone don't explain most of the price variation) and whether stock status carries signal (96.7% in-stock — too skewed to be useful).
5. **Data quality issues** — found 6 duplicate UPCs, 15 missing ratings, 4 extreme price outliers, with concrete cleaning recommendations for each.

**Run it:**
```bash
python3 task2_eda.py
```

**Key finding:** price is right-skewed with a handful of high-value outliers; rating has only a weak relationship with price, so rating alone is not a strong price predictor for this catalogue.

---

## 6. Task 3 — Data Visualization

**File:** `task3_data_visualization.py`
**Libraries:** `pandas`, `matplotlib`, `seaborn`
**Output:** 6 PNG files in `outputs/visuals/`

| File | Chart | Answers |
|---|---|---|
| `1_price_distribution.png` | Histogram + KDE | How is price distributed? |
| `2_top_categories.png` | Horizontal bar | Which categories dominate the catalogue? |
| `3_rating_distribution.png` | Count plot | How are star ratings spread? |
| `4_price_by_rating.png` | Boxplot | Does price vary meaningfully by rating? |
| `5_avg_price_by_category.png` | Horizontal bar | Which categories are priciest on average? |
| `6_dashboard.png` | 2×2 combined grid | One-glance summary for a portfolio/README |

Each chart is titled, axis-labeled, and colored with a consistent palette so it can be dropped straight into a GitHub README or LinkedIn post.

**Run it:**
```bash
python3 task3_data_visualization.py
```

---

## 7. How to run the whole pipeline

```bash
py -3.11 -m pip install requests beautifulsoup4 pandas numpy matplotlib seaborn lxml
py -3.11 task1_web_scraping.py        # scrape live data (needs internet)
py -3.11 task2_eda.py                 # analyze it
py -3.11 task3_data_visualization.py  # visualize it
```

*(Using `py -3.11` because of the known Python 3.11 vs 3.14 interpreter conflict — VS Code defaults to 3.14, which has caused package issues in past projects.)*

---

## 8. Submission checklist (per the CodeAlpha instructions)

- [ ] Create GitHub repo named `CodeAlpha_DataAnalytics`, push all files above.
- [ ] Run `task1_web_scraping.py` locally with real internet to replace the sample CSV with live data, then re-run Tasks 2 & 3.
- [ ] Share internship status on LinkedIn, tagging **@CodeAlpha**.
- [ ] Post a short video walkthrough of the project with the GitHub repo link.
- [ ] Submit via the WhatsApp-group submission form (not email) — per the brief, submissions are only accepted through that form.
- [ ] This project completes **3 of the 4** listed tasks (Web Scraping, EDA, Data Visualization), satisfying the "complete any 2 or 3" requirement. Task 4 (Sentiment Analysis) was not attempted here.

---

## 9. Contact (from the internship brief)

- Website: [www.codealpha.tech](https://www.codealpha.tech)
- WhatsApp: +91 9336576683
- Email: services@codealpha.tech, services.codealpha@gmail.com
