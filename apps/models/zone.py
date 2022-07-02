# Hệ số cho chiều cao vùng trung bình. Càng lớn, các khu càng thấp
AVERAGE_WEIGHT = 1.0
# Số nến liên tiếp trong 1 vùng
MIN_ZONE_WIDTH = 2
# Dung sai trong các điểm trên mức thấp/cao của một nến
TOLERANCE_RATE = 20

class Zone:
  def __init__(self, start, end, high, low):
    self.start = start
    self.end = end
    self.high = high
    self.low = low

  @classmethod
  def calculate_sideway_zone(cls, df):
    # Nghịch đảo dataframe
    df = df.iloc[::-1]

    avg_zone_height = 0
    num_bars = len(df)
    zone_start = 0
    zones_counter = 0
    zones = []

    for i in range(0, num_bars - 2):
      is_in_range = False
      if zones:
        for zone in zones:
          if i >= zone.start and i <= zone.end - 1:
            is_in_range = True
            break
      if is_in_range:
        continue

      zone_start = i
      current_height = abs(df.iloc[i].high - df.iloc[i].low)
      tolerance = current_height/TOLERANCE_RATE
      range_high = df.iloc[i].high + tolerance
      range_low = df.iloc[i].low - tolerance
      zones_counter = zone_start
      avg_zone_height = abs(range_high - range_low)

      while cls.not_break_zone(df, zones_counter, zone_start, num_bars, range_high, range_low, current_height, avg_zone_height):
        if cls.can_change_range_height(df, zone_start, zones_counter, range_high, range_low):
          if df.iloc[zones_counter].high > range_high:
            range_high = df.iloc[zones_counter].high + tolerance
          if df.iloc[zones_counter].low < range_low:
            range_low = df.iloc[zones_counter].low - tolerance
        avg_zone_height = abs(range_high - range_low)
        zones_counter = zones_counter + 1
        current_height = abs(df.iloc[zones_counter].high - df.iloc[zones_counter].low)
        tolerance = avg_zone_height/TOLERANCE_RATE

      if zones_counter - zone_start > 3:
        start = zone_start - 1
        if zone_start == 0:
          start = 0
        zones.append(Zone(start, zones_counter, range_low, range_high))

    return zones

  @staticmethod
  def not_break_zone(df, counter, zone_start, num_bars, range_high, range_low, current_height, avg_zone_height):
    valid_df_range = (counter < num_bars - 1)
    valid_zone_size = (counter - zone_start) < MIN_ZONE_WIDTH
    valid_zone_height = current_height > avg_zone_height/2 or (counter - zone_start) > 3
    is_in_zone = df.iloc[counter].open <= range_high and \
      df.iloc[counter].open >= range_low and \
      df.iloc[counter].close <= range_high and \
      df.iloc[counter].close > range_low

    return valid_df_range and (valid_zone_size or (is_in_zone and valid_zone_height))

  @staticmethod
  def can_change_range_height(df, zone_start, counter, range_high, range_low):
    zone_height = abs(range_high - range_low)
    valid_zone_size = zone_start != counter
    valid_high = df.iloc[counter].high <= range_high or abs(df.iloc[counter].high - range_high) < zone_height/(TOLERANCE_RATE/2)
    valid_low = df.iloc[counter].low >= range_low or abs(range_low - df.iloc[counter].low) < zone_height/(TOLERANCE_RATE/2)

    return valid_zone_size and valid_high and valid_low
