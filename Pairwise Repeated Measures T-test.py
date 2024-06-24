# %%
from collections import defaultdict
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import ttest_rel, wilcoxon

# %%
df = pd.read_excel("data/results_untransformed.xlsx")

df.describe()

# %%
p_values_t_test = []
p_values_wilcoxon = []
std = []
mean = []
diffs = []


prompts = df.columns
prompts_names = df.columns
# prompts_names = ["_".join(c.split("_")[:2]) for c in df.columns]
for i, propmt1 in enumerate(prompts):
    for j, prompt2 in enumerate(prompts):
        if i != j:
            # Make a paried t test
            result = ttest_rel(df[propmt1], df[prompt2])
            p_values_t_test.append((prompts_names[i], prompts_names[j], result.pvalue))

            # make a wilcoxon test
            result = wilcoxon(df[propmt1], df[prompt2])
            p_values_wilcoxon.append(
                (prompts_names[i], prompts_names[j], result.pvalue)
            )

            diff = np.array(df[propmt1]) - np.array(df[prompt2])
            # print(f"Prompt 1: {prompts_names[i]}")
            # print(f"Prompt 2: {prompts_names[j]}")
            # plt.hist(diff, bins=20)
            # plt.show()

            diffs.append((prompts_names[i], prompts_names[j], np.mean(diff)))
            std.append((prompts_names[i], prompts_names[j], np.std(diff)))
            mean.append((prompts_names[i], prompts_names[j], np.mean(diff)))


def render(X):
    # Convert the list of tuples into a pandas DataFrame
    t_test = pd.DataFrame(X, columns=["Prompt 1", "Prompt 2", "X"]).round(5)

    # Output the DataFrame
    t_test = (
        t_test.pivot(index="Prompt 1", columns="Prompt 2", values="X")
        .reindex(index=prompts_names, columns=prompts_names)
        .T.dropna(axis=1, how="all")
        .dropna(axis=0, how="all")
    )

    t_test.to_latex("render.tex", float_format="%.4f")
    display(t_test)


# render(p_values_wilcoxon)
render(p_values_t_test)
# render(diffs)
# render(std)
# render(mean)

# %% For making the same analysis for the transformed data, ie.
# grouped by sentiment or perspective
df = pd.read_excel("data/results.xlsx")

# df.describe()

sentiment_dict = defaultdict(list)
perspectivedict = defaultdict(list)

for i, row in df.iterrows():
    sentiment_dict[row["sentiment"]].append(row["score"])
    perspectivedict[row["perspective"]].append(row["score"])

sentiment_df = pd.DataFrame(sentiment_dict)
perspective_df = pd.DataFrame(perspectivedict)

df = sentiment_df
# df = perspective_df
