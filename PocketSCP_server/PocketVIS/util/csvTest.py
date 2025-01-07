import pandas as pd
df = pd.DataFrame({'A': range(1, 6),
                   'B': range(10, 0, -2),
                   'C C': range(10, 5, -1)})
df2 = pd.DataFrame({'A': range(1, 6),
                   'B': range(20, -1, -5),
                   'C C': range(10, 5, -1)})
print(df)
print(df2)


a = df.query('A==1')['B'].iloc[0]
df2.loc[0,'B'] = a
print('=====================')
print(df2)