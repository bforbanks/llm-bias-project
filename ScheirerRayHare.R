# Loading
if(!require(rcompanion)){install.packages("rcompanion")}
if(!require(FSA)){install.packages("FSA")}

library("readxl")
library(rcompanion)
# xls files
my_data <- read_excel("C:/Users/Benja/dev/dtu/llm-bias-project/output_new_test_rows.xlsx")

# make a scheirerRayHare test
scheirerRayHare(score ~ neutrality + perspective + neutrality:perspective,
                data = my_data)


