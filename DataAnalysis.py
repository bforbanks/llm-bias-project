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
    x="sentiment",
    y="score",
    hue="perspective",
    data=df,
    # palette="viridis",
    showmeans=True,
    meanline=True,
    meanprops={"linestyle": "--", "linewidth": 2, "color": "black"},
)

# plt.legend(loc='upper right')

plt.rcParams.update({"font.size": 14})  # Adjust the number to your preference
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))

# save the plot as a png file with god resolution and transparent background
plt.savefig("boxplot.png", dpi=300, transparent=True, bbox_inches="tight")

plt.savefig("boxplot.png", dpi=300, transparent=True, bbox_inches="tight")

plt.show()
# %%
means_table = df.pivot_table(
    index="sentiment",
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
std_table = df.pivot_table(
    index="sentiment",
    columns="perspective",
    values="score",
    aggfunc="std",
    # margins=True,
    margins_name="Average",
)

std_table.to_latex("render.tex", float_format="%.4f")

## print this table with color coding
std_table.style.background_gradient(cmap="Greens", vmin=1.88, vmax=2.26)
# %%
# make a shapiro test for normality
from scipy.stats import shapiro

# %%
# make a shapiro test for normality
from scipy.stats import shapiro

for sentiment in df["sentiment"].unique():
    for perspective in df["perspective"].unique():
        data = df[(df["sentiment"] == sentiment) & (df["perspective"] == perspective)][
            "score"
        ]
        stat, p = shapiro(data)
        print(f"{sentiment}[{perspective}] p-value: {p}")
