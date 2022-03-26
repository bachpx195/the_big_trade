from myenv.models.candlestick import Candlestick
from myenv.helpers.constants import HIGH_INDEX, LOW_INDEX, OPEN_INDEX, CLOSE_INDEX
from myenv.models.merchandise_rate import MerchandiseRate
from myenv.helpers.utils import percentage_change, candlestick_type, type_continuous
import streamlit as st


# Add title and subtitle of the map.
st.title("Accidents in United Kingdom")
st.markdown("This app analyzes accident data in United Kingdom from 2012-2014")

"""
Here, we define load_data function,
to prevent loading the data everytime we made some changes in the dataset.
We use streamlit's cache notation.
"""

merchandise_rate = MerchandiseRate()
merchandise_rate_id = merchandise_rate.find_by_slug('LTCUSDT')
candlestick = Candlestick(merchandise_rate_id, 'week', 100, "DESC")
data_prices = candlestick.to_df()

data_prices['week_return'] = percentage_change(data_prices,OPEN_INDEX, CLOSE_INDEX)
data_prices['month'] = data_prices[['open']].apply(
    lambda x: x.name.month, axis=1)
data_prices['year'] = data_prices[['open']].apply(
    lambda x: x.name.year, axis=1)

total = data_prices.iloc[:, 0].count()
last_date = data_prices.iloc[0].name.date()
first_date = data_prices.iloc[-1].name.date()

print(f"Thông tin: {total} hàng từ ngày {first_date} đến {last_date}")
print(data_prices)

data_prices['type'] = candlestick_type(data_prices)

data_prices['type_continuous'] = type_continuous(data_prices, "ASC")

st.bar_chart(data_prices['week_return'])


# # Plot : 1
# # plot a streamlit map for accident locations.
# st.header("Where are the most people casualties in accidents in UK?")
# # plot the slider that selects number of person died
# casualties = st.slider("Number of persons died", 1, int(data["open"].max()))
# st.map(data.query("number_of_casualties >= @casualties")[["latitude", "longitude"]].dropna(how ="any"))

# # Plot : 2
# # plot a pydeck 3D map for the number of accident's happen between an hour interval
# st.header("How many accidents occur during a given time of day?")
# hour = st.slider("Hour to look at", 0, 23)
# original_data = data
# data = data[data['date / time'].dt.hour == hour]

# st.markdown("Vehicle collisions between % i:00 and % i:00" % (hour, (hour + 1) % 24))
# midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

# st.write(pdk.Deck(
#     map_style ="mapbox://styles / mapbox / light-v9",
#     initial_view_state ={
#         "latitude": midpoint[0],
#         "longitude": midpoint[1],
#         "zoom": 11,
#         "pitch": 50,
#     },
#     layers =[
#         pdk.Layer(
#         "HexagonLayer",
#         data = data[['date / time', 'latitude', 'longitude']],
#         get_position =["longitude", "latitude"],
#         auto_highlight = True,
#         radius = 100,
#         extruded = True,
#         pickable = True,
#         elevation_scale = 4,
#         elevation_range =[0, 1000],
#         ),
#     ],
# ))

# # Plot : 3
# # plot a histogram for minute of the hour atwhich accident happen
# st.subheader("Breakdown by minute between % i:00 and % i:00" % (hour, (hour + 1) % 24))
# filtered = data[
#     (data['date / time'].dt.hour >= hour) & (data['date / time'].dt.hour < (hour + 1))
# ]
# hist = np.histogram(filtered['date / time'].dt.minute, bins = 60, range =(0, 60))[0]
# chart_data = pd.DataFrame({"minute": range(60), "Accidents": hist})
# fig = px.bar(chart_data, x ='minute', y ='Accidents', hover_data =['minute', 'Accidents'], height = 400)
# st.write(fig)

# # The code below uses checkbox to show raw data
# st.header("Condition of Road at the time of Accidents")
# select = st.selectbox('Weather ', ['Dry', 'Wet / Damp', 'Frost / ice', 'Snow', 'Flood (Over 3cm of water)'])

# if select == 'Dry':
#     st.write(original_data[original_data['road_surface_conditions']=="Dry"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))

# elif select == 'Wet / Damp':
#     st.write(original_data[original_data['road_surface_conditions']=="Wet / Damp"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))
# elif select == 'Frost / ice':
#     st.write(original_data[original_data['road_surface_conditions']=="Frost / ice"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))

# elif select == 'Snow':
#     st.write(original_data[original_data['road_surface_conditions']=="Snow"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))

# else:
#     st.write(original_data[original_data['road_surface_conditions']=="Flood (Over 3cm of water)"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))


# if st.checkbox("Show Raw Data", False):
#     st.subheader('Raw Data')
#     st.write(data)
