# %%
import pandas as pd

data = pd.read_excel(
    "data/results_untransformed.xlsx",
    sheet_name="Sheet1",
    header=0,
)  # Assuming headers are in the first row
data.head()
# %%

r_dict = data.to_dict()

# Create a DataFrame from the dictionary
l = []
for r in r_dict.keys():
    perspective = r.split("[")[0]
    sentiment = r.split("[")[1].split("]")[0]
    for i in range(0, len(r_dict[r])):
        l.append([i, perspective, sentiment, r_dict[r][i]])

df = pd.DataFrame(l, columns=["post", "perspective", "sentiment", "score"])
df.to_excel("data/results.xlsx", index=False)
df.head()
