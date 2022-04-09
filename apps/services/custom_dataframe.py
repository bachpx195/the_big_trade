import pandas as pd
from apps.helpers.utils import unique_list

#             highest_in_day  highest_return
# 2022-04-08               8        1.035503
# 2022-04-07               8        2.400409
def custom_highest_hour_dataframe(origin_df):
  day_list = unique_list(origin_df['day'].tolist())
  highest_hour_list = []
  highest_return_list = []
  for day in day_list:
    max_value = origin_df[origin_df['day'] == day].hour_return.max()
    min_value = origin_df[origin_df['day'] == day].hour_return.min()

    highest_return = max_value if max_value > abs(min_value) else min_value
    highest_return_list.append(highest_return)
    highest_hour_list.append(origin_df[origin_df['hour_return'] == highest_return].hour.values[0])

  data = {
      'highest_in_day': highest_hour_list,
      'highest_return': highest_return_list
  }

  df = pd.DataFrame(data, index=day_list)

  return df
