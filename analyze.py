import pandas as pd
if __name__ == '__main__':
    pd.set_option('display.max_rows', 50)
    df = pd.read_csv('dater.csv')
    df = df[df['playlist']=='Kchill']
    l = df.groupby(by='Artist').count().sort_values(by='playlist', ascending=False)
    print(l.head(50))
    print(l.describe())