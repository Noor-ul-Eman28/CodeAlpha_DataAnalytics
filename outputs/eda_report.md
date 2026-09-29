# EDA Report — CodeAlpha Data Analytics Task 2

Dataset: `data/scraped_books.csv`  |  Rows: 956  |  Columns: 7

## 1. Questions this analysis sets out to answer

- How is price distributed across the catalogue — is it symmetric or skewed?
- Do higher star ratings correlate with higher prices?
- Which categories dominate the catalogue, and which are niche?
- Is stock availability a meaningful signal, or is almost everything in stock?
- Does the raw scraped data contain duplicates, missing values, or outliers that would distort downstream analysis?

## 2. Data structure

**Columns and dtypes:**

```
title                  str
price_gbp          float64
rating_out_of_5    float64
in_stock              bool
category               str
upc                    str
product_url            str
```

**First 5 rows:**

```
                  title  price_gbp  rating_out_of_5  in_stock           category               upc                                                           product_url
0  Whispers of Time 773      46.33              5.0      True  Christian Fiction  156562c712fc8640  https://books.toscrape.com/catalogue/whispers-of-time-773/index.html
1   Ashes and Roses 545      39.25              2.0      True         Paranormal  e4c65fb918466df1   https://books.toscrape.com/catalogue/ashes-and-roses-545/index.html
2    The Paper Crown 44      59.99              4.0      True      Adult Fiction  c8fb16d1c41fd349    https://books.toscrape.com/catalogue/the-paper-crown-44/index.html
3  Winter's Embrace 161      42.90              4.0      True          Christian  708ed44c7d6a6664  https://books.toscrape.com/catalogue/winter's-embrace-161/index.html
4   The Paper Crown 704      26.69              3.0      True            Default  6144173b63432b26   https://books.toscrape.com/catalogue/the-paper-crown-704/index.html
```

**Summary statistics (numeric columns):**

```
       price_gbp  rating_out_of_5
count     956.00           941.00
mean       36.46             3.27
std        15.60             1.21
min        10.00             1.00
25%        27.00             3.00
50%        35.66             3.00
75%        45.00             4.00
max       203.70             5.00
```

**Categorical overview:**

- Unique categories: 50
- Unique titles: 928 (out of 956 rows)
- In-stock share: 96.7%

## 3. Trends, patterns & anomalies

**Top 5 categories by book count:**

```
category
Mystery       26
Thriller      26
Philosophy    25
Humor         25
Travel        24
```

**Rating distribution:**

```
rating_out_of_5
1.0     97
2.0    136
3.0    287
4.0    258
5.0    163
```

- Price distribution skewness: **3.30** (right-skewed (a few expensive outliers pull the mean up))
- Price outliers (IQR method, bounds [-0.01, 72.02]): **4 books** flagged, e.g.:
```
                 title  price_gbp       category
Echoes in the Dark 922     203.70 Sequential Art
   Ashes and Roses 853     201.45       Thriller
 The Silent Garden 583     147.90        Romance
   Shattered Glass 247     155.60  Adult Fiction
```

## 4. Hypothesis testing

**H1: Books with higher star ratings tend to be priced higher.**

- Pearson correlation (price vs rating): **0.127**
- **Conclusion:** a weak-to-moderate positive relationship — higher-rated books skew slightly pricier.

**Mean price by rating:**

```
rating_out_of_5
1.0    31.36
2.0    35.12
3.0    36.06
4.0    38.65
5.0    38.08
```

**H2: Almost all books are in stock, so availability carries little analytical signal in this dataset.**

- Confirmed: 96.7% in-stock rate — too skewed to use as a predictive variable without a different sampling approach.

## 5. Data quality issues detected

- **Duplicate rows (by UPC):** 6
- **Missing values by column:**
```
rating_out_of_5    15
```
- **Extreme price outliers:** 4 rows above/below the IQR fence (see Section 3) — worth a manual sanity check before modeling.

**Recommended cleaning steps before further analysis:**
1. Drop duplicate UPCs, keeping the first occurrence.
2. Impute or drop the missing `rating_out_of_5` values depending on downstream use (median imputation is reasonable here since ratings are ordinal 1-5).
3. Investigate the flagged price outliers individually — decide whether they're genuine premium items (e.g. box sets) or scraping/parsing errors.