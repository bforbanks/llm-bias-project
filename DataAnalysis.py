# %%
import pandas as pd

# %%
df = pd.read_excel("results.xlsx")

# %%
df.describe()
# %%
# make a boxplot for the 6 different groups with sns
import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(x="neutrality", y="score", hue="perspective", data=df)

plt.show()
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
## data is not normally distributed
# %%
# because the data is not normally distributed, we will do a pairwise kruskal test
from scipy.stats import kruskal

for n in df["neutrality"].unique():
    for p in df["perspective"].unique():
        data = df[(df["neutrality"] == n) & (df["perspective"] == p)]["score"]
        stat, p = kruskal(data, df["score"])
        print(f"Neutrality: {n}, Perspective: {p}, p-value: {p}")
