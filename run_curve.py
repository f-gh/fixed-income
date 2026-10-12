import pandas as pd
from fixed_income.curve import construct_curve 

df = pd.read_csv("data/synthetic/par_yields.csv")

df_1, df_2, df_3 = construct_curve(df)

print("1Y discount factor:", df_1)
print("2Y discount factor:", df_2)
print("3Y discount factor:", df_3)
