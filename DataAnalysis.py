# %%
from dotenv import load_dotenv

load_dotenv()

from tqdm import tqdm
import pandas as pd
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_debug
from IPython.display import display_markdown
from collections import defaultdict
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
    sheet_name="metadata_2",
    header=0,
    index_col=0,  # Use the first column as the index (row names)
)  # Assuming headers are in the first row


# %%
results = pd.read_excel(
    r"M:\OneDrive - Danmarks Tekniske Universitet\Main\Project in Statistical Evaluation for Artificial Intelligence and Data\Project\data.xlsx",
    sheet_name="results_api",
    header=0,
)  # Assuming headers are in the first row
results

# %%
## make an two way anova

# Create a DataFrame from the dictionary
df = pd.DataFrame()

df.columns = ["neutrality", "perspective", "values"]

# Perform two-way ANOVA
model = ols(
    "values ~ C(neutrality) + C(perspective) + C(neutrality):C(perspective)", data=df
).fit()

# Print the ANOVA table
sm.stats.anova_lm(model, typ=2)

# %%

# %%
import matplotlib.pyplot as plt

# Set up the figure and axes for the boxplots
fig, ax = plt.subplots(figsize=(10, 6))

# Data for the boxplots
data = [values for values in data.values()]
labels = list(data.keys())

# Create the boxplot
ax.boxplot(data, labels=labels, patch_artist=True)

# Set the title and labels
ax.set_title("Boxplot for Each Key")
ax.set_xlabel("Key")
ax.set_ylabel("Values")

# Show the plot
plt.xticks(rotation=45)  # Rotate labels to avoid overlap
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
plt.show()
