# Loading
library("readxl")
library(ARTool)

# import data
my_data <- read_excel("C:/Users/Benja/dev/dtu/llm-bias-project/data/results.xlsx")
my_data$sentiment <- as.factor(my_data$sentiment)
my_data$perspective <- as.factor(my_data$perspective)
my_data$post <- as.factor(my_data$post)

# check the data
str(my_data)

# make the model
model = art(score ~ sentiment * perspective + Error(post),
  data = my_data)

# Check model
model

# Get results
anova(model)
