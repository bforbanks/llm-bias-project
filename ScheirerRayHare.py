# %% [markdown]
# # Scheirer-Ray-Hare Test
#
# This script performs the Scheirer-Ray-Hare Test on the exercise from 'Real Statistics Using Excel'
#
# http://www.real-statistics.com/two-way-anova/scheirer-ray-hare-test/
#
# The data should be in a dataframe with three columns:
# 1. Factor 1 (Fertilizer)
# 2. Factor 2 (Crop)
# 3. Measurement
#
# In this example I created a file with the data from the original exercise.
# However, the code should be adaptable to any dataset provided the assumptions for the test, and the formats are the same.
#
# For more information on this parametric test visit:
#
# https://www.youtube.com/watch?v=N729aMGIUOk
#
# http://rcompanion.org/handbook/F_14.html

# %%
# Importing the libraries.
# pandas is necesary for the calculations
# scipy allows to estimate the p-value using the Chi-Square distribution
import pandas as pd
from scipy import stats


# %%
data = pd.read_excel("data/results.xlsx")
data.head()

# %% [markdown]
# This dataframe has three columns: Factor 1 (Fertilizer), Factor 2 (Crop), and measurement (Measure)
#
# ### Calculating the ranks
#
# Ranks are calculated for each measurement. This step is performed on the sorted measurements regardless of the factors

# %%
data["rank"] = data.score.sort_values().rank(numeric_only=float)
data.head()

# %% [markdown]
# ### Calculating the sum of the squares

# %%
rows = (
    data.groupby(["bias"], as_index=False)
    .agg({"rank": ["count", "mean", "var"]})
    .rename(columns={"rank": "row"})
)
rows.columns = ["_".join(col) for col in rows.columns]
rows.columns = rows.columns.str.replace(r"_$", "")
rows["row_mean_rows"] = rows.row_mean.mean()
rows["sqdev"] = (rows.row_mean - rows.row_mean_rows) ** 2
rows

# %%
cols = (
    data.groupby(["perspective"], as_index=False)
    .agg({"rank": ["count", "mean", "var"]})
    .rename(columns={"rank": "col"})
)
cols.columns = ["_".join(col) for col in cols.columns]
cols.columns = cols.columns.str.replace(r"_$", "")
cols["col_mean_cols"] = cols.col_mean.mean()
cols["sqdev"] = (cols.col_mean - cols.col_mean_cols) ** 2
cols

# %%
data_sum = data.groupby(["bias", "perspective"], as_index=False).agg(
    {"rank": ["count", "mean", "var"]}
)
data_sum.columns = ["_".join(col) for col in data_sum.columns]
data_sum.columns = data_sum.columns.str.replace(r"_$", "")

# %%
nobs_row = rows.row_count.mean()
nobs_total = rows.row_count.sum()
nobs_col = cols.col_count.mean()

# %%
Columns_SS = cols.sqdev.sum() * nobs_col
Rows_SS = rows.sqdev.sum() * nobs_row
Within_SS = data_sum.rank_var.sum() * (data_sum.rank_count.min() - 1)
MS = data["rank"].var()
TOTAL_SS = MS * (nobs_total - 1)
Inter_SS = TOTAL_SS - Within_SS - Rows_SS - Columns_SS

# %% [markdown]
# ### Calculating the H-statistics and degrees of freedom

# %%
H_rows = Rows_SS / MS
H_cols = Columns_SS / MS
H_int = Inter_SS / MS

# %%
df_rows = len(rows) - 1
df_cols = len(cols) - 1
df_int = df_rows * df_cols
df_total = len(data) - 1
df_within = df_total - df_int - df_cols - df_rows

# %% [markdown]
# ### Calculating the p-values

# %%
p_rows = round(1 - stats.chi2.cdf(H_rows, df_rows), 4)
p_cols = round(1 - stats.chi2.cdf(H_cols, df_cols), 4)
p_inter = round(1 - stats.chi2.cdf(H_int, df_int), 4)

# %%
print(p_rows, p_cols, p_inter)

# %% check if the ranks are normally distributed
from scipy.stats import shapiro

for n in data["sentiment"].unique():
    for p in data["perspective"].unique():
        d = data[(data["sentiment"] == n) & (data["perspective"] == p)]["rank"]
        stat, p = shapiro(d)
        print(f"Neutrality: {n}, Perspective: {p}, p-value: {p}")
