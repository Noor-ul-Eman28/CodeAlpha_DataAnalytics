"""
==========================================================================
 TASK 3: DATA VISUALIZATION
 CodeAlpha Data Analytics Internship
==========================================================================
Input  : data/scraped_books.csv
Output : outputs/visuals/*.png  (5 individual charts + 1 combined dashboard)

Design choices, tied to the brief:
  - "Transform raw data into visual formats like charts, graphs, dashboards"
        -> 5 chart types + 1 multi-panel dashboard image
  - "Use tools like Matplotlib, Seaborn"
        -> both used together (seaborn styling on matplotlib figures)
  - "Design visuals that enhance understanding and reveal insights clearly"
        -> titles, axis labels, annotations, consistent color palette
  - "Craft compelling data stories that support decision-making"
        -> each chart answers one specific question from the EDA
  - "Build a strong portfolio with impactful, well-designed visualizations"
        -> saved as high-res PNGs suitable for a GitHub README / LinkedIn post

Libraries used: pandas, matplotlib, seaborn
==========================================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 120
OUT = "outputs/visuals/"

df = pd.read_csv("data/scraped_books.csv")
# light cleaning consistent with Task 2's recommendations, applied only
# for visualization purposes (raw file is left untouched for reproducibility)
df_clean = df.drop_duplicates(subset="upc").copy()

ACCENT = "#4C72B0"


# --------------------------------------------------------------------
# 1. Price distribution — histogram + KDE
# --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df_clean["price_gbp"], bins=30, kde=True, color=ACCENT, ax=ax)
ax.set_title("Distribution of Book Prices", fontsize=14, weight="bold")
ax.set_xlabel("Price (GBP)")
ax.set_ylabel("Number of Books")
ax.axvline(df_clean["price_gbp"].median(), color="crimson", linestyle="--",
           label=f"Median = £{df_clean['price_gbp'].median():.2f}")
ax.legend()
fig.tight_layout()
fig.savefig(OUT + "1_price_distribution.png")
plt.close(fig)


# --------------------------------------------------------------------
# 2. Top 10 categories by book count — bar chart
# --------------------------------------------------------------------
top10 = df_clean["category"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=top10.values, y=top10.index, hue=top10.index, palette="Blues_r",
            legend=False, ax=ax)
ax.set_title("Top 10 Categories by Number of Books", fontsize=14, weight="bold")
ax.set_xlabel("Book Count")
ax.set_ylabel("Category")
for i, v in enumerate(top10.values):
    ax.text(v + 0.3, i, str(v), va="center", fontsize=9)
fig.tight_layout()
fig.savefig(OUT + "2_top_categories.png")
plt.close(fig)


# --------------------------------------------------------------------
# 3. Rating distribution — count plot
# --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
sns.countplot(x="rating_out_of_5", data=df_clean, hue="rating_out_of_5",
              palette="viridis", legend=False, ax=ax)
ax.set_title("Star Rating Distribution", fontsize=14, weight="bold")
ax.set_xlabel("Rating (out of 5 stars)")
ax.set_ylabel("Number of Books")
fig.tight_layout()
fig.savefig(OUT + "3_rating_distribution.png")
plt.close(fig)


# --------------------------------------------------------------------
# 4. Price vs. Rating — boxplot (reveals the weak-positive trend from EDA)
# --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="rating_out_of_5", y="price_gbp", data=df_clean,
            hue="rating_out_of_5", palette="coolwarm", legend=False, ax=ax)
ax.set_title("Price by Star Rating", fontsize=14, weight="bold")
ax.set_xlabel("Rating (out of 5 stars)")
ax.set_ylabel("Price (GBP)")
fig.tight_layout()
fig.savefig(OUT + "4_price_by_rating.png")
plt.close(fig)


# --------------------------------------------------------------------
# 5. Average price by category (top 10 priciest categories, min 5 books)
# --------------------------------------------------------------------
avg_price = (df_clean.groupby("category")["price_gbp"]
             .agg(["mean", "count"])
             .query("count >= 5")
             .sort_values("mean", ascending=False)
             .head(10))
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=avg_price["mean"], y=avg_price.index, hue=avg_price.index,
            palette="magma", legend=False, ax=ax)
ax.set_title("Top 10 Highest-Priced Categories (avg, min. 5 books)", fontsize=13, weight="bold")
ax.set_xlabel("Average Price (GBP)")
ax.set_ylabel("Category")
fig.tight_layout()
fig.savefig(OUT + "5_avg_price_by_category.png")
plt.close(fig)


# --------------------------------------------------------------------
# 6. Combined dashboard — 2x2 grid summarizing the whole story
# --------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("CodeAlpha Data Analytics — Book Catalogue Dashboard",
             fontsize=16, weight="bold")

sns.histplot(df_clean["price_gbp"], bins=25, kde=True, color=ACCENT, ax=axes[0, 0])
axes[0, 0].set_title("Price Distribution")
axes[0, 0].set_xlabel("Price (GBP)")

sns.barplot(x=top10.values[:6], y=top10.index[:6], hue=top10.index[:6],
            palette="Blues_r", legend=False, ax=axes[0, 1])
axes[0, 1].set_title("Top 6 Categories")
axes[0, 1].set_xlabel("Book Count")

sns.countplot(x="rating_out_of_5", data=df_clean, hue="rating_out_of_5",
              palette="viridis", legend=False, ax=axes[1, 0])
axes[1, 0].set_title("Rating Distribution")
axes[1, 0].set_xlabel("Rating")

sns.boxplot(x="rating_out_of_5", y="price_gbp", data=df_clean,
            hue="rating_out_of_5", palette="coolwarm", legend=False, ax=axes[1, 1])
axes[1, 1].set_title("Price by Rating")
axes[1, 1].set_xlabel("Rating")

fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(OUT + "6_dashboard.png")
plt.close(fig)

print("All 6 visualizations saved to outputs/visuals/")
for f in sorted(pd.Series(__import__("os").listdir(OUT))):
    print(" -", f)
