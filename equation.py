import pandas as pd
import numpy as np

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
    
    # Calculate Weighted Kills Above Average (wKAA). This will cap out at around 1.5
    avgKillMap = df['KPR'].mean()
    
    # deprecated but i'll keep it in
    IGL = 0.15 * df['IGL'] * df['KPR']
    
    df['wKAA'] = df['KPR'] - avgKillMap
    dummyOne = 5.5000
    df['wKAAFactor']  = ((df['wKAA']) / avgKillMap) * dummyOne
    
    # Calculate Weighted ADR Above Average (wAAA) (balanced around 1.75)
    avgADR = df['ADR'].mean()
    df['wAAA'] = df['ADR'] - avgADR 
    dummyFour = 8.6667
    df['wAAAFactor'] = (df['wAAA']/avgADR) * dummyFour
    
    # Calculate KAST/AWP% Adjustment Factor (kAWP) (balanced around 0.25)
    KASTAvg = df['KAST'].mean() 
    wKAST = df['KAST'] - KASTAvg 
    df['kAWP'] = wKAST * df['AWP%'] * df['AWP']
    dummyTwo = 4.8500
    dummyTwoTwo = 0.125
    df['kAWPFactor'] = np.where(df['kAWP'] != 0, (df['kAWP'] * dummyTwo) + dummyTwoTwo, 0)

    # Calculate Impact/AWP% Adjustment Factor (iAWP) (balanced around 0.75)
    ImpactAvg = df['Impact'].mean() 
    wImpact = df['Impact'] - ImpactAvg
    dummyThree = 3.1667
    dummyThreeTwo = 0.3750
    df['iAWP'] = wImpact * df['AWP%'] * df['AWP']
    df['iAWPFactor'] = np.where(df['iAWP'] != 0, (df['iAWP'] * dummyThree) + dummyThreeTwo, 0)

    
    #Calculate Impact/ADR Adjustment Factor (iADR) (balanced around 0.5)
    dummyFive = 0.8250
    df['iADRFactor'] = (abs(wImpact) * df['wAAAFactor']) / dummyFive
    
    # Calculate Win/Loss + Sample Size Adjustment Factor (WL) (balanced around 1.75)
    SampleSize = (df['Loss'] + df['Win']).mean()
    print(SampleSize)
    df['WL'] = ((((df['Win']) / (df['Loss'] + df['Win'])) - 0.5 ) + (((df['Loss'] + df['Win'])/SampleSize) - 1) )
    dummySix = 5.7500
    df['WLFactor']= (df['WL'] * 0.19 + df['WL']*df['IGL']*0.05) * dummySix
    
    # Calculate SAR
    df['RAR'] = df ['wKAAFactor']+ df['wAAAFactor'] - df['kAWPFactor'] + df['iAWPFactor'] + df['iADRFactor'] + df['WLFactor']+ 2
    
    # debug
    #print(df)
    # for reference
    df.to_csv('player_war.csv', index=False)

if __name__ == '__main__':
    main()
