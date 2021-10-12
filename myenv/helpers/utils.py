# ((col2 - col1) / col1) * 100
def percentage_change(df, col1_index, col2_index):
    return df.apply(lambda row: (row.iloc[col2_index]-row.iloc[col1_index])/row.iloc[col1_index]*100, axis=1)
