# %%
import pandas as pd

# %%
df = pd.read_excel("data/results.xlsx")

# %%
df.describe()
# %%
# make a boxplot for the 6 different groups with sns
import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(
    x="bias",
    y="score",
    hue="perspective",
    data=df,
    # palette="viridis",
    showmeans=True,
    meanline=True,
    meanprops={"linestyle": "--", "linewidth": 2, "color": "black"},
)

# plt.legend(loc='upper right')

plt.legend(loc="upper left", bbox_to_anchor=(1, 1))

# save the plot as a png file with god resolution and transparent background
plt.savefig("boxplot.png", dpi=300, transparent=True, bbox_inches="tight")


plt.show()
# %%
means_table = df.pivot_table(
    index="bias",
    columns="perspective",
    values="score",
    aggfunc="mean",
    # margins=True,
    margins_name="Average",
)

means_table.to_latex("render.tex", float_format="%.4f")

## print this table with color coding
means_table.style.background_gradient(cmap="Greens", vmin=5, vmax=7.5)

# %%
means_table = df.pivot_table(
    index="bias",
    columns="perspective",
    values="score",
    aggfunc="std",
    # margins=True,
    margins_name="Average",
)

means_table.to_latex("render.tex", float_format="%.4f")

## print this table with color coding
means_table.style.background_gradient(cmap="Greens", vmin=1.88, vmax=2.26)
# %%
# make a shapiro test for normality
from scipy.stats import shapiro

models = []
models_data = []


# Initialize an empty DataFrame to store Shapiro test results
shapiro_results = pd.DataFrame(columns=["bias", "perspective", "p-value"])

# Loop through each combination of bias and perspective to perform Shapiro tests
for n in df["bias"].unique():
    for p in df["perspective"].unique():
        data = df[(df["bias"] == n) & (df["perspective"] == p)]["score"]
        stat, p_value = shapiro(data)
        # Correctly append the results to the DataFrame
        new_row = {"bias": n, "perspective": p, "p-value": p_value}
        shapiro_results = shapiro_results.append(new_row, ignore_index=True)
# Pivot the results to match the format of the previous pivot tables
shapiro_pivot = shapiro_results.pivot(
    index="bias", columns="perspective", values="p-value"
)

# Apply color coding to the pivot table
styled_shapiro_pivot = shapiro_pivot.style.background_gradient(
    cmap="Greens", vmin=0, vmax=0.05
)  # Adjust vmin and vmax based on expected p-value range
## data is not normally distributed
# %%
