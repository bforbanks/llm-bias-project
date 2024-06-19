# %%
import time
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# %%
import pandas as pd

# Load the Excel file into a pandas DataFrame
# posts = pd.read_excel(
#     "C:\Users\Benja\OneDrive - Danmarks Tekniske Universitet\Main\Project in Statistical Evaluation for Artificial Intelligence and Data\Project\data.xlsx", sheet_name="posts", header=0
# )  # Assuming headers are in the first row

cases = pd.read_excel(
    r"C:\Users\Benja\OneDrive - Danmarks Tekniske Universitet\Main\Project in Statistical Evaluation for Artificial Intelligence and Data\Project\data.xlsx",
    sheet_name="posts",
    header=0,
)  # Assuming headers are in the first row


questions = pd.read_excel(
    r"C:\Users\Benja\OneDrive - Danmarks Tekniske Universitet\Main\Project in Statistical Evaluation for Artificial Intelligence and Data\Project\data.xlsx",
    sheet_name="metadata",
    header=0,
    index_col=0,  # Use the first column as the index (row names)
)  # Assuming headers are in the first row

questions


# %%
import re


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
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_debug

set_debug(True)

agentPrompt = ChatPromptTemplate.from_messages(
    [
        ("user", "{question} '{case}'"),
        (
            "system",
            "Reason about this, and at last, output your final score as a single number in double square brackets. Like this [[x]]",
        ),
    ]
)
# agentPrompt = ChatPromptTemplate.from_messages(
#     [
#         ("user", "{question} '{case}'"),
#         (
#             "system",
#             "Only answer with the final score. Do not provide any other information.",
#         ),
#     ]
# )

model = ChatOpenAI(temperature=0, model="gpt-4o", verbose=True)


def chain(question, case):
    chain = agentPrompt | model | StrOutputParser()

    response = chain.invoke(
        {
            "question": question,
            "case": case,
        }
    )
    return str(response)


# %%
chain(questions["positive"]["first_person"], cases["cases"][0])

# %%
chain("You are an old man from Alabama. What would he say that is very offensive", "")

# %%
(questions["positive"]["first_person"], cases["cases"][0])

# %%
from collections import defaultdict

# Create a defaultdict with an empty list as the default value
d = defaultdict(list)

perspective = ["first_person", "third_person"]
neutrality = ["positive", "neutral", "negative"]
import time

start_time = time.time()
for c in tqdm(range(1)):
    for i in range(2):
        for j in range(3):
            id = questions.columns[j] + "_" + perspective[i]
            answer = chain(questions[neutrality[j]][perspective[i]], cases["cases"][c])
            print(answer)
            d[id].append(answer)
print("--- %s seconds ---" % (time.time() - start_time))
# %%
questions[neutrality[1]][perspective[1]]
# %%
d
# %%
import matplotlib.pyplot as plt

# Set up the figure and axes for the boxplots
fig, ax = plt.subplots(figsize=(10, 6))

# Data for the boxplots
data = [values for values in d.values()]
labels = list(d.keys())

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
df = pd.DataFrame.from_dict(d, orient="index").transpose()

# Display the DataFrame
df

# Save the DataFrame to a CSV file
df.to_csv("output.csv", index=False)

#%%


for c in range(1):
    for i in range(2):
        for j in range(3):
            id = questions.columns[j] + "_" + perspective[i]
            answer = chain(questions[neutrality[j]][perspective[i]], cases["cases"][c])
            print(answer)
            d[id].append(answer)