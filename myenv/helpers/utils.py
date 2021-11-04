from .constants import OPEN_INDEX, CLOSE_INDEX

# ((col2 - col1) / col1) * 100

def percentage_change(df, col1_index, col2_index):
    return df.apply(lambda row: (row.iloc[col2_index]-row.iloc[col1_index])/row.iloc[col1_index]*100, axis=1)


def candlestick_type(df):
    return df.apply(lambda row: 'down' if row.iloc[OPEN_INDEX] > row.iloc[CLOSE_INDEX] else 'up', axis=1)

def type_continuous(df, sort_type='DESC'):
    return df.apply(lambda row: count_continuous(df, row, sort_type), axis=1)

def count_continuous(df, row, sort_type='DESC'):
    count = 0
    while True:
        shift_number = -(count + 1) if sort_type == 'ASC' else count + 1
        if df.shift(shift_number).loc[row.name].type != row.type:
            break
        count = count + 1
    return count if count == 0 else count + 1
