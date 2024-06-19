# %%
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# %%
cases = pd.read_excel(
    r"M:\OneDrive - Danmarks Tekniske Universitet\Main\Project in Statistical Evaluation for Artificial Intelligence and Data\Project\data.xlsx",
    sheet_name="posts",
    header=0,
)  # Assuming headers are in the first row


questions = pd.read_excel(
    r"M:\OneDrive - Danmarks Tekniske Universitet\Main\Project in Statistical Evaluation for Artificial Intelligence and Data\Project\data.xlsx",
    sheet_name="metadata",
    header=0,
    index_col=0,  # Use the first column as the index (row names)
)  # Assuming headers are in the first row

results = pd.read_excel(
    r"M:\OneDrive - Danmarks Tekniske Universitet\Main\Project in Statistical Evaluation for Artificial Intelligence and Data\Project\data.xlsx",
    sheet_name="results",
    header=0,
)  # Assuming headers are in the first row

# results = pd.read_excel("output_new.xlsx", header=0)

r_dict = results.to_dict()


# %%
# Create a DataFrame from the dictionary
l = []
for r in r_dict.keys():
    neutrality = r.split("_")[0]
    perspective = r.split("_")[1]
    for i in range(0, len(r_dict[r])):
        l.append([neutrality, perspective, r_dict[r][i]])

df = pd.DataFrame(l, columns=["neutrality", "perspective", "score"])
df

# %%

# make a boxplot for the 6 different groups with sns
import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(x="neutrality", y="score", hue="perspective", data=df)

plt.show()

# %%
# Perform a Tukey HSD test
from statsmodels.stats.multicomp import MultiComparison

mc = MultiComparison(df["score"], df["neutrality"])
result = mc.tukeyhsd()

print(result)


# %%
df.to_excel("output_new_test.xlsx", index=False)

# %%
results.describe()

# %%
means_table = df.pivot_table(
    index="neutrality",
    columns="perspective",
    values="score",
    aggfunc="mean",
    margins=True,
    margins_name="Average",
)

## print this table with color coding
means_table.style.background_gradient(cmap="Greens", vmin=5, vmax=7.5)

# %%
# make a shapiro test for normality

from scipy.stats import shapiro

for n in df["neutrality"].unique():
    for p in df["perspective"].unique():
        data = df[(df["neutrality"] == n) & (df["perspective"] == p)]["score"]
        stat, p = shapiro(data)
        print(f"Neutrality: {n}, Perspective: {p}, p-value: {p}")

# %%
# because the data is not normally distributed, we will do a pairwise kruskal test

from scipy.stats import kruskal

for n in df["neutrality"].unique():
    for p in df["perspective"].unique():
        data = df[(df["neutrality"] == n) & (df["perspective"] == p)]["score"]
        stat, p = kruskal(data, df["score"])
        print(f"Neutrality: {n}, Perspective: {p}, p-value: {p}")
# %%
import pandas as pd
import numpy as np
from scipy.stats import rankdata, chi2


def scheirer_ray_hare(data, factor1, factor2):
    """
    Perform the Scheirer-Ray-Hare test for a two-way layout.

    :param data: The dependent variable.
    :param factor1: The first factor.
    :param factor2: The second factor.
    :return: A dictionary with the test results.
    """
    # Rank the data
    data["Rank"] = rankdata(data["score"])

    # Compute the sum of ranks for each level of the factors and their interaction
    rank_sum_A = data.groupby(factor1)["Rank"].sum()
    rank_sum_B = data.groupby(factor2)["Rank"].sum()
    rank_sum_AB = data.groupby([factor1, factor2])["Rank"].sum()

    # Number of levels for each factor
    a = data[factor1].nunique()
    b = data[factor2].nunique()
    n = len(data)

    # Compute the H statistics
    H_A = (12 / (n * (n + 1))) * (rank_sum_A**2).sum() / data.groupby(factor1)[
        "Rank"
    ].count() - 3 * (n + 1)
    H_B = (12 / (n * (n + 1))) * (rank_sum_B**2).sum() / data.groupby(factor2)[
        "Rank"
    ].count() - 3 * (n + 1)
    H_AB = (
        (12 / (n * (n + 1)))
        * (rank_sum_AB**2).sum()
        / data.groupby([factor1, factor2])["Rank"].count()
        - 3 * (n + 1)
        - H_A
        - H_B
    )

    # Degrees of freedom
    df_A = a - 1
    df_B = b - 1
    df_AB = df_A * df_B

    # Compute the p-values
    p_A = chi2.sf(H_A, df_A)
    p_B = chi2.sf(H_B, df_B)
    p_AB = chi2.sf(H_AB, df_AB)

    results = {
        "Factor1": {"H": H_A, "df": df_A, "p-value": p_A},
        "Factor2": {"H": H_B, "df": df_B, "p-value": p_B},
        "Interaction": {"H": H_AB, "df": df_AB, "p-value": p_AB},
    }

    return results


# Perform the test
results = scheirer_ray_hare(df, "neutrality", "perspective")
print(results)

# %%

df.to_excel("output_new_test_rows.xlsx", index=False)
