import pandas as pd

# DATA IS ACCURATE AS OF 2024/08/02
pd.set_option("display.max_rows", 1500) 

def calculate_war(row):
    TK = row['Total Kills']
    MP = row['Maps Played']
    ADR = row['ADR']
    
    # Calculate average kills per map for this row
    avgKill = TK / MP
    return avgKill

def main():
    df = pd.read_csv('stats.csv')
    
    # Calculate Weighted Kills Above Average (wKAA)
    df['avgKill'] = df.apply(calculate_war, axis=1)
    avgKillMap = df['avgKill'].mean()
    
    # Calculate IGL adjustment factor (IGL)
    IGL = 0.1 * df['IGL'] * df['avgKill']
    df['wKAA'] = df['avgKill'] - avgKillMap
    wKAAFactor = ((df['wKAA'] + IGL) / avgKillMap)
    
    # Calculate KAST/AWP% Adjustment Factor (kAWP)
    KASTAvg = df['KAST'].mean()
    wKAST = df['KAST'] - KASTAvg 
    df['kAWP'] = wKAST * df['AWP%']
    kAWPFactor = df['kAWP'] * 10
    
    # Calculate Impact/AWP% Adjustment Factor (iAWP)
    ImpactAvg = df['Impact'].mean()
    wImpact = df['Impact'] - ImpactAvg
    df['iAWP'] = wImpact * df['AWP%']
    iAWPFactor = df['iAWP'] * 10
    
    # Calculate Weighted ADR Above Average (wAAA)
    avgADR = df['ADR'].mean()
    df['wAAA'] = df['ADR'] - avgADR 
    wAAAFactor = df['wAAA'] / 10
    
    #Calculate Impact/ADR Adjustment Factor (iADR)
    df['iADR'] = abs(wImpact) * (wAAAFactor)
    
    # Calculate Win/Loss + Sample Size Adjustment Factor (WL)
    SampleSize = (df['Loss'] + df['Win']).mean()
    print(SampleSize)
    df['WL'] = ((((df['Win']) / (df['Loss'] + df['Win'])) - 0.5 ) + (((df['Loss'] + df['Win'])/SampleSize) - 1) )
    
    # Calculate SAR
    df['SAR'] = wKAAFactor - kAWPFactor + iAWPFactor + wAAAFactor + df['iADR'] + df['WL']
    
    # debug
    #print(df)
    # for reference
    df.to_csv('player_war.csv', index=False)

if __name__ == '__main__':
    main()
