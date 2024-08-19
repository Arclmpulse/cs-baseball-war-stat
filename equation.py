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
    
    # Calculate Weighted Kills Above Average (wKAA). This will cap out at around 1.5
    avgKillMap = df['KPR'].mean()
    
    # deprecated but i'll keep it in
    IGL = 0.15 * df['IGL'] * df['KPR']
    
    df['wKAA'] = df['KPR'] - avgKillMap
    dummyOne = 4.3333
    wKAAFactor = ((df['wKAA']) / avgKillMap) * dummyOne
    df['wKAAFactor'] = wKAAFactor
    
    # Calculate Weighted ADR Above Average (wAAA) (balanced around 1.75)
    avgADR = df['ADR'].mean()
    df['wAAA'] = df['ADR'] - avgADR 
    dummyFour = 12.6666
    wAAAFactor = df['wAAA'] / dummyFour
    df['wAAAFactor'] = wAAAFactor
    
    # Calculate KAST/AWP% Adjustment Factor (kAWP) (balanced around 0.25)
    KASTAvg = df['KAST'].mean() 
    wKAST = df['KAST'] - KASTAvg 
    df['kAWP'] = wKAST * df['AWP%']
    dummyTwo = 9.7
    kAWPFactor = df['kAWP'] * dummyTwo
    df['kAWPFactor'] = kAWPFactor
    
    # Calculate Impact/AWP% Adjustment Factor (iAWP) (balanced around 0.75)
    ImpactAvg = df['Impact'].mean() 
    wImpact = df['Impact'] - ImpactAvg
    dummyThree = 6.3333
    df['iAWP'] = wImpact * df['AWP%']
    iAWPFactor = df['iAWP'] * dummyThree
    df['iAWPFactor'] = iAWPFactor
    
    #Calculate Impact/ADR Adjustment Factor (iADR) (balanced around 0.5)
    dummyFive = 0.9
    df['iADR'] = abs(wImpact) * (wAAAFactor)
    iADRFactor = df['iADR'] / dummyFive
    
    # Calculate Win/Loss + Sample Size Adjustment Factor (WL) (balanced around 1.75)
    SampleSize = (df['Loss'] + df['Win']).mean()
    print(SampleSize)
    df['WL'] = ((((df['Win']) / (df['Loss'] + df['Win'])) - 0.5 ) + (((df['Loss'] + df['Win'])/SampleSize) - 1) )
    dummySix = 4.667
    WLFactor = (df['WL'] * 0.19 + df['WL']*df['IGL']*0.05) * dummySix
    df['WLFactor'] = WLFactor
    
    # Calculate SAR
    df['SAR'] = wKAAFactor - kAWPFactor + iAWPFactor + wAAAFactor + iADRFactor + WLFactor + 2
    
    # debug
    #print(df)
    # for reference
    df.to_csv('player_war.csv', index=False)

if __name__ == '__main__':
    main()
