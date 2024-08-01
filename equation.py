import pandas as pd

pd.set_option("display.max_rows", 1500) 

def calculate_war(row):
    # Extract values from the row
    TK = row['Total Kills']
    MP = row['Maps Played']
    ADR = row['ADR']
    
    # Calculate average kills per map for this row
    avgKill = TK / MP
    
    return avgKill

def main():
    # Load the data from CSV
    df = pd.read_csv('stats.csv')
    
    # Calculate average kills per map for each player and store in a new column
    df['avgKill'] = df.apply(calculate_war, axis=1)
    
    # Calculate the average of avgKill across all players
    avgKillMap = df['avgKill'].mean()
    
    # Calculate Weighted Kills Above Average (wKAA)
    df['wKAA'] = df['avgKill'] - avgKillMap
    
    # Calculate the average ADR
    avgADR = df['ADR'].mean()
    
    # Calculate Weighted ADR Above Average (wAAA)
    df['wAAA'] = df['ADR'] - avgADR
    
    # Print the DataFrame to check the new columns
    print(df)
    
    # Example of further processing (WAR calculation or saving to file)
    # df.to_csv('player_war.csv', index=False)
    # print("WAR calculations saved to 'player_war.csv'")

if __name__ == '__main__':
    main()
