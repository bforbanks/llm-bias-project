# %%
import pandas as pd

data = pd.read_excel(
    "data_untransformed.xlsx",
    sheet_name="Sheet1",
    header=0,
)  # Assuming headers are in the first row
data.head()
# %%

r_dict = data.to_dict()

# Create a DataFrame from the dictionary
l = []
for r in r_dict.keys():
    neutrality = r.split("_")[0]
    perspective = r.split("_")[1]
    for i in range(0, len(r_dict[r])):
        l.append([neutrality, perspective, r_dict[r][i]])

df = pd.DataFrame(l, columns=["neutrality", "perspective", "score"])
# df.to_excel("results.xlsx")
df.head()
