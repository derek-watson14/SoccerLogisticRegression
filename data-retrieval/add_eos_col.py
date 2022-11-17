import pandas as pd

df = pd.read_csv('./data/table_data.csv')
eos_df = df[df['Final Table'] == True]

def Get_EOS_Position(row):
    if row['Final Table'] == True:
        return row['Position']
    else:
        club, year = row['Club'], row['Year']
        return eos_df[((eos_df['Club'] == club) & (eos_df['Year'] == year))].iloc[0]['Position']

df['EOS Position'] = df.apply(Get_EOS_Position, axis=1)

df.to_csv('./data/table_data.csv', index=False)