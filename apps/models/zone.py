# Hệ số cho chiều cao vùng trung bình. Càng lớn, các khu càng thấp
AVERAGE_WEIGHT = 1.0
# Số nến liên tiếp trong 1 vùng
MIN_ZONE_WIDTH = 3
# Dung sai trong các điểm trên mức thấp/cao của một nến
TOLERANCE = 20

class Zone:
  def __init__(self, start, end, high, low):
    self.start = start
    self.end = end
    self.high = high
    self.low = low

  @classmethod
  def calculate_sideway_zone(cls, df, tolerance):
    # Nghịch đảo dataframe
    df = df.iloc[::-1]

    avg_zone_height = 0
    num_bars = len(df)
    has_broken_range = False
    zone_start = num_bars - 1
    zone_end = 0
    zone_size = 0
    zones_counter = 0
    zones = []

    range_high = df.iloc[num_bars - 1].high + tolerance
    range_low = df.iloc[num_bars - 1].low + tolerance

    # ==========Vòng lặp thứ nhất==========
    # Lấy chiều cao trung bình của khu vực để lọc các chuyển động lớn khi bắt đầu
    for i in range(num_bars - 2, -1, -1):
      zone_size = zone_start - i
      zone_end = i
      if df.iloc[i].open > range_high or df.iloc[i].open < range_low or df.iloc[i].close > range_high or df.iloc[i].close < range_low:
        if zone_size >= MIN_ZONE_WIDTH:
          avg_zone_height += abs(range_high - range_low)
          zones_counter = zones_counter + 1

        has_broken_range = True
        zone_start = i
        range_high = df.iloc[i].high + tolerance
        range_low = df.iloc[i].low + tolerance
      else:
        has_broken_range = False

    avg_zone_height /= zones_counter * AVERAGE_WEIGHT
    # ==========Kết thúc vòng lặp thứ nhất==========

    for i in range(num_bars - 2,-1,-1):
      zone_size = zone_start - i
      zone_end = i
      if df.iloc[i].open > range_high or df.iloc[i].open < range_low or df.iloc[i].close > range_high or df.iloc[i].close < range_low:
        if zone_size >= MIN_ZONE_WIDTH:
          zones.append(Zone(zone_start, zone_end + 1, range_low, range_high))
          zones_counter = zones_counter + 1

        has_broken_range = True
        zone_start = i
        range_high = df.iloc[i].high + tolerance
        range_low = df.iloc[i].low + tolerance

        if abs(df.iloc[i].high - df.iloc[i].low) >= avg_zone_height:
          zone_start = -1
          range_high = 0
          range_low = 0
          continue

      else:
        has_broken_range = False

    if has_broken_range == False and zone_size >= MIN_ZONE_WIDTH:
      zones.append(Zone(zone_start, 0, range_low, range_high))

    return zones
