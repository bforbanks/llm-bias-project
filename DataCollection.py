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
def extract_score(text):
    # Regular expression to find [[<number>]] pattern
    match = re.search(r"\[\[(\d+)\]\]", text)
    if match:
        # Extract and return the score as an integer
        return int(match.group(1))
    else:
        # Return None if the pattern is not found
        return None


# %%
set_debug(False)

agentPrompt = ChatPromptTemplate.from_messages(
    [
        ("user", "{user_string}"),
        (
            "system",
            "Reason about this, and at last, output your final score as a single number in double square brackets. Like this [[x]]",
        ),
    ]
)

model = ChatOpenAI(temperature=0, model="gpt-4o", verbose=True)


def chain(question, case):
    user_string = question + ' \n\n"' + case + '"'

    # display_markdown(user_string, raw=True)

    chain = agentPrompt | model | StrOutputParser()
    response = chain.invoke(
        {
            "user_string": user_string,
        }
    )
    return response


# %%
display_markdown(
    chain(questions["positive"]["first_person"], cases["cases"][0]), raw=True
)

# %%
# Create a defaultdict with an empty list as the default value
data = defaultdict(list)

perspective = ["first_person", "third_person"]
neutrality = ["positive", "neutral", "negative"]

for case in tqdm(range(1)):
    for perspective in range(2):
        for question in range(3):
            id = questions.columns[question] + "_" + perspective[perspective]
            answer = chain(
                questions[neutrality[question]][perspective[perspective]],
                cases["cases"][case],
            )
            data[id].append(answer)
df = pd.DataFrame(data)
df.to_excel("output_new.xlsx", index=False)
df
# %%
questions[neutrality[1]][perspective[1]]

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

# %%
import pandas as pd

# Convert the dictionary of lists to a DataFrame
df = pd.DataFrame.from_dict(data, orient="index").transpose()

# Display the DataFrame
df

# Save the DataFrame to a CSV file
df.to_csv("output.csv", index=False)

# %%


for case in range(1):
    for perspective in range(2):
        for question in range(3):
            id = questions.columns[question] + "_" + perspective[perspective]
            answer = chain(
                questions[neutrality[question]][perspective[perspective]],
                cases["cases"][case],
            )
            print(answer)
            data[id].append(answer)
