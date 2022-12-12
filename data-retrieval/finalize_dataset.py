import pandas as pd
import time
from webscraper.webscraper.helpers import seasons

# Add End of Season Position to each row
# Run this with assumption table_parser has just finished running

def Get_EOS_Position(row, eos_df):
    if row['Final Table'] == True:
        return row['Position']
    else:
        club, year = row['Club'], row['Year']
        return eos_df[((eos_df['Club'] == club) & (eos_df['Year'] == year))].iloc[0]['Position']


def Add_EOS_Column(df):
    eos_df = df[df['Final Table'] == True]
    df['EOS Position'] = df.apply(lambda row: Get_EOS_Position(row, eos_df), axis=1)
    return df


def Get_Capacity(row, stadium_df):
    club = row['Club']
    year = row['Year']
    cap = int(stadium_df[(stadium_df["Club"] == club) & (stadium_df["Year"] == year)]['Stadium Capacity'])
    return cap


def Add_Stadium_Capacity(df, stadium_df):
    df['Stadium Capacity'] = df.apply(lambda row: Get_Capacity(row, stadium_df), axis=1)
    return df


def Add_Appearances(df):
    # Calculate number of times in league from 2004-2021
    apps = df[df['Final Table'] == True][['Year', 'Club']].groupby('Club')
    df['Appearances'] = df.apply(lambda row: len(apps.get_group(row['Club'])), axis=1)
    return df


def main():
    table_df = pd.read_csv('./data/table_data.csv')
    stadium_df = pd.read_csv('./data/stadium_data.csv')
    
    print("Adding EOS Position...")
    start = time.time()
    combined_df = Add_EOS_Column(table_df)
    end = time.time()
    print(f"Added EOS Position in {end-start} seconds!")
    print("--------------------------------------------")

    print("Adding Stadium Capacities")
    start = time.time()
    combined_df = Add_Stadium_Capacity(combined_df, stadium_df)
    end = time.time()
    print(f"Added Stadium Capacity in {end-start} seconds!")
    print("--------------------------------------------")

    print("Adding Appearance Count")
    start = time.time()
    combined_df = Add_Appearances(table_df)
    end = time.time()
    print(f"Added Appearance Count in {end-start} seconds!")
    print("--------------------------------------------")

    print(combined_df.head())

    combined_df.to_csv('./data/combined_data.csv', index=False)

if __name__ == "__main__":
    main()