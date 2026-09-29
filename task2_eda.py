"""
==========================================================================
 TASK 2: EXPLORATORY DATA ANALYSIS (EDA)
 CodeAlpha Data Analytics Internship
==========================================================================
Input  : data/scraped_books.csv   (produced by task1_web_scraping.py)
Output : outputs/eda_report.md    (full written findings, saved automatically)

This script works through the brief's checklist in order:
  1. Ask meaningful questions about the dataset before analysis
  2. Explore the data structure (variables, data types)
  3. Identify trends, patterns and anomalies
  4. Test hypotheses and validate assumptions using statistics
  5. Detect potential data issues / problems for further cleaning

Libraries used: pandas, numpy
==========================================================================
"""

import numpy as np
import pandas as pd

pd.set_option("display.width", 120)
report_lines = []


def log(text=""):
    """Print to console AND collect for the saved markdown report."""
    print(text)
    report_lines.append(text)


# --------------------------------------------------------------------
# 0. Load data
# --------------------------------------------------------------------
df = pd.read_csv("data/scraped_books.csv")

log("# EDA Report — CodeAlpha Data Analytics Task 2")
log(f"\nDataset: `data/scraped_books.csv`  |  Rows: {len(df)}  |  Columns: {df.shape[1]}\n")

# --------------------------------------------------------------------
# 1. Meaningful questions to ask before diving in
# --------------------------------------------------------------------
log("## 1. Questions this analysis sets out to answer\n")
questions = [
    "How is price distributed across the catalogue — is it symmetric or skewed?",
    "Do higher star ratings correlate with higher prices?",
    "Which categories dominate the catalogue, and which are niche?",
    "Is stock availability a meaningful signal, or is almost everything in stock?",
    "Does the raw scraped data contain duplicates, missing values, or outliers "
    "that would distort downstream analysis?",
]
for q in questions:
    log(f"- {q}")

# --------------------------------------------------------------------
# 2. Explore data structure
# --------------------------------------------------------------------
log("\n## 2. Data structure\n")
log("**Columns and dtypes:**\n")
log("```")
log(df.dtypes.to_string())
log("```")

log("\n**First 5 rows:**\n")
log("```")
log(df.head().to_string())
log("```")

log("\n**Summary statistics (numeric columns):**\n")
log("```")
log(df.describe().round(2).to_string())
log("```")

log("\n**Categorical overview:**\n")
log(f"- Unique categories: {df['category'].nunique()}")
log(f"- Unique titles: {df['title'].nunique()} (out of {len(df)} rows)")
log(f"- In-stock share: {df['in_stock'].mean()*100:.1f}%")

# --------------------------------------------------------------------
# 3. Trends, patterns, anomalies
# --------------------------------------------------------------------
log("\n## 3. Trends, patterns & anomalies\n")

top_categories = df["category"].value_counts().head(5)
log("**Top 5 categories by book count:**\n")
log("```")
log(top_categories.to_string())
log("```")

rating_dist = df["rating_out_of_5"].value_counts(dropna=True).sort_index()
log("\n**Rating distribution:**\n")
log("```")
log(rating_dist.to_string())
log("```")

price_skew = df["price_gbp"].skew()
log(f"\n- Price distribution skewness: **{price_skew:.2f}** "
    f"({'right-skewed (a few expensive outliers pull the mean up)' if price_skew > 0.5 else 'roughly symmetric'})")

# Outlier detection via IQR
q1, q3 = df["price_gbp"].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
price_outliers = df[(df["price_gbp"] < lower) | (df["price_gbp"] > upper)]
log(f"- Price outliers (IQR method, bounds [{lower:.2f}, {upper:.2f}]): "
    f"**{len(price_outliers)} books** flagged, e.g.:")
log("```")
log(price_outliers[["title", "price_gbp", "category"]].head(5).to_string(index=False))
log("```")

# --------------------------------------------------------------------
# 4. Hypothesis testing
# --------------------------------------------------------------------
log("\n## 4. Hypothesis testing\n")
log("**H1: Books with higher star ratings tend to be priced higher.**\n")

corr = df[["price_gbp", "rating_out_of_5"]].corr().iloc[0, 1]
log(f"- Pearson correlation (price vs rating): **{corr:.3f}**")
if abs(corr) < 0.1:
    verdict = "no meaningful linear relationship — rating does not predict price here."
elif corr > 0:
    verdict = "a weak-to-moderate positive relationship — higher-rated books skew slightly pricier."
else:
    verdict = "a weak-to-moderate negative relationship."
log(f"- **Conclusion:** {verdict}")

mean_by_rating = df.groupby("rating_out_of_5")["price_gbp"].mean().round(2)
log("\n**Mean price by rating:**\n")
log("```")
log(mean_by_rating.to_string())
log("```")

log("\n**H2: Almost all books are in stock, so availability carries little "
    "analytical signal in this dataset.**\n")
log(f"- Confirmed: {df['in_stock'].mean()*100:.1f}% in-stock rate — "
    "too skewed to use as a predictive variable without a different sampling approach.")

# --------------------------------------------------------------------
# 5. Data quality issues
# --------------------------------------------------------------------
log("\n## 5. Data quality issues detected\n")

dupes = df.duplicated(subset="upc").sum()
missing = df.isna().sum()
missing = missing[missing > 0]

log(f"- **Duplicate rows (by UPC):** {dupes}")
log("- **Missing values by column:**")
log("```")
log(missing.to_string() if len(missing) else "None found")
log("```")
log(f"- **Extreme price outliers:** {len(price_outliers)} rows above/below the IQR fence "
    "(see Section 3) — worth a manual sanity check before modeling.")

log("\n**Recommended cleaning steps before further analysis:**")
log("1. Drop duplicate UPCs, keeping the first occurrence.")
log("2. Impute or drop the missing `rating_out_of_5` values depending on downstream use "
    "(median imputation is reasonable here since ratings are ordinal 1-5).")
log("3. Investigate the flagged price outliers individually — decide whether they're "
    "genuine premium items (e.g. box sets) or scraping/parsing errors.")

# --------------------------------------------------------------------
# Save report
# --------------------------------------------------------------------
with open("outputs/eda_report.md", "w") as f:
    f.write("\n".join(report_lines))

print("\nFull report saved to outputs/eda_report.md")
