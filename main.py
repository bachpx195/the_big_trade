import streamlit as st
from hydralit import HydraApp
import hydralit_components as hc
import apps
from apps.services.update_data import update_data


#Only need to set these here as we are add controls outside of Hydralit, to customise a run Hydralit!
st.set_page_config(page_title='Secure Hydralit Data Explorer',page_icon="🐙",layout='wide',initial_sidebar_state='auto',)

if __name__ == '__main__':
  if st.button('Cập nhật data'):
    is_updated = update_data()
    if is_updated:
      st.write("Cập nhật thành công")


  #---ONLY HERE TO SHOW OPTIONS WITH HYDRALIT - NOT REQUIRED, use Hydralit constructor parameters.
  # st.write('Viết gì đó...')
  # c1,c2,c3,c4,_ = st.columns([2,2,2,2,8])
  # hydralit_navbar = c1.checkbox('Use Hydralit Navbar',True)
  # sticky_navbar = c2.checkbox('Use Sticky Navbar',False)
  # animate_navbar = c3.checkbox('Use Animated Navbar',True)
  # hide_st = c4.checkbox('Hide Streamlit Markers',True)

  over_theme = {'txc_inactive': '#FFFFFF'}
  #this is the host application, we add children to it and that's it!
  app = HydraApp(
      title='Secure Hydralit Data Explorer',
      favicon="🐙",
      hide_streamlit_markers=True,
      #add a nice banner, this banner has been defined as 5 sections with spacing defined by the banner_spacing array below.
      banner_spacing=[5,30,60,30,5],
      use_navbar=True,
      navbar_sticky=True,
      navbar_animation=False,
      navbar_theme=over_theme
  )

  #Home button will be in the middle of the nav list now
  app.add_app("Home", icon="🏠", app=apps.HomeApp(title='Home'),is_home=True)
  app.add_app("Data", app=apps.DataApp(title='Data'))
  app.add_app("True Range", app=apps.TrueRangeApp(title='True Range'))

  app.add_loader_app(apps.MyLoadingApp(delay=0))


  complex_nav = {
    'Home': ['Home'],
    'Data': ['Data'],
    'True Range': ['True Range']
  }

  app.run(complex_nav)



  #add all your application classes here
  # app.add_app("Cheat Sheet", icon="📚", app=apps.CheatApp(title="Cheat Sheet"))
  # app.add_app("Sequency Denoising",icon="🔊", app=apps.WalshApp(title="Sequency Denoising"))
  # app.add_app("Sequency (Secure)",icon="🔊🔒", app=apps.WalshAppSecure(title="Sequency (Secure)"))
  # app.add_app("Solar Mach", icon="🛰️", app=apps.SolarMach(title="Solar Mach"))
  # app.add_app("Spacy NLP", icon="⌨️", app=apps.SpacyNLP(title="Spacy NLP"))
  # app.add_app("Uber Pickups", icon="🚖", app=apps.UberNYC(title="Uber Pickups"))
  # app.add_app("Solar Mach", icon="🛰️", app=apps.SolarMach(title="Solar Mach"))
  # app.add_app("Loader Playground", icon="⏲️", app=apps.LoaderTestApp(title="Loader Playground"))
  # app.add_app("Cookie Cutter", icon="🍪", app=apps.CookieCutterApp(title="Cookie Cutter"))

  #we have added a sign-up app to demonstrate the ability to run an unsecure app
  #only 1 unsecure app is allowed
  # app.add_app("Signup", icon="🛰️", app=apps.SignUpApp(title='Signup'), is_unsecure=True)

  #we want to have secure access for this HydraApp, so we provide a login application
  #optional logout label, can be blank for something nicer!
  # app.add_app("Login", apps.LoginApp(title='Login'),is_login=True)

  #specify a custom loading app for a custom transition between apps, this includes a nice custom spinner
  # app.add_loader_app(apps.MyLoadingApp(delay=0))

  #we can inject a method to be called everytime a user logs out
  #---------------------------------------------------------------------
  # @app.logout_callback
  # def mylogout_cb():
  #     print('I was called from Hydralit at logout!')
  #---------------------------------------------------------------------

  #we can inject a method to be called everytime a user logs in
  #---------------------------------------------------------------------
  # @app.login_callback
  # def mylogin_cb():
  #     print('I was called from Hydralit at login!')
  #---------------------------------------------------------------------

  #if we want to auto login a guest but still have a secure app, we can assign a guest account and go straight in
  # app.enable_guest_access()

  #check user access level to determine what should be shown on the menu
  # user_access_level, username = app.check_access()

  # If the menu is cluttered, just rearrange it into sections!
  # completely optional, but if you have too many entries, you can make it nicer by using accordian menus
  # if user_access_level > 1:
  #     complex_nav = {
  #         'Home': ['Home'],
  #         'Loader Playground': ['Loader Playground'],
  #         'Intro 🏆': ['Cheat Sheet',"Solar Mach"],
  #         'Hotstepper 🔥': ["Sequency Denoising","Sequency (Secure)"],
  #         'Clustering': ["Uber Pickups"],
  #         'NLP': ["Spacy NLP"],
  #         'Cookie Cutter': ['Cookie Cutter']
  #     }
  # elif user_access_level == 1:
  #     complex_nav = {
  #         'Home': ['Home'],
  #         'Loader Playground': ['Loader Playground'],
  #         'Intro 🏆': ['Cheat Sheet',"Solar Mach"],
  #         'Hotstepper 🔥': ["Sequency Denoising"],
  #         'Clustering': ["Uber Pickups"],
  #         'NLP': ["Spacy NLP"],
  #         'Cookie Cutter': ['Cookie Cutter']
  #     }
  # else:
  #     complex_nav = {
  #         'Home': ['Home'],
  #     }


  #and finally just the entire app and all the children.
  # app.run(complex_nav)


  #print user movements and current login details used by Hydralit
  #---------------------------------------------------------------------
  # user_access_level, username = app.check_access()
  # prev_app, curr_app = app.get_nav_transition()
  # print(prev_app,'- >', curr_app)
  # print(int(user_access_level),'- >', username)
  # print('Other Nav after: ',app.session_state.other_nav_app)
  #---------------------------------------------------------------------
























# merchandise_rate = MerchandiseRate()
# merchandise_rate_id = merchandise_rate.find_by_slug('LTCUSDT')
# candlestick = Candlestick(merchandise_rate_id, 'week', 100, "DESC")
# data_prices = candlestick.to_df()

# data_prices['week_return'] = percentage_change(data_prices,OPEN_INDEX, CLOSE_INDEX)
# data_prices['month'] = data_prices[['open']].apply(
#     lambda x: x.name.month, axis=1)
# data_prices['year'] = data_prices[['open']].apply(
#     lambda x: x.name.year, axis=1)

# total = data_prices.iloc[:, 0].count()
# last_date = data_prices.iloc[0].name.date()
# first_date = data_prices.iloc[-1].name.date()

# print(f"Thông tin: {total} hàng từ ngày {first_date} đến {last_date}")
# print(data_prices)

# data_prices['type'] = candlestick_type(data_prices)

# data_prices['type_continuous'] = type_continuous(data_prices, "ASC")

# st.bar_chart(data_prices['week_return'])


# # # Plot : 1
# # # plot a streamlit map for accident locations.
# # st.header("Where are the most people casualties in accidents in UK?")
# # # plot the slider that selects number of person died
# # casualties = st.slider("Number of persons died", 1, int(data["open"].max()))
# # st.map(data.query("number_of_casualties >= @casualties")[["latitude", "longitude"]].dropna(how ="any"))

# # # Plot : 2
# # # plot a pydeck 3D map for the number of accident's happen between an hour interval
# # st.header("How many accidents occur during a given time of day?")
# # hour = st.slider("Hour to look at", 0, 23)
# # original_data = data
# # data = data[data['date / time'].dt.hour == hour]

# # st.markdown("Vehicle collisions between % i:00 and % i:00" % (hour, (hour + 1) % 24))
# # midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

# # st.write(pdk.Deck(
# #     map_style ="mapbox://styles / mapbox / light-v9",
# #     initial_view_state ={
# #         "latitude": midpoint[0],
# #         "longitude": midpoint[1],
# #         "zoom": 11,
# #         "pitch": 50,
# #     },
# #     layers =[
# #         pdk.Layer(
# #         "HexagonLayer",
# #         data = data[['date / time', 'latitude', 'longitude']],
# #         get_position =["longitude", "latitude"],
# #         auto_highlight = True,
# #         radius = 100,
# #         extruded = True,
# #         pickable = True,
# #         elevation_scale = 4,
# #         elevation_range =[0, 1000],
# #         ),
# #     ],
# # ))

# # # Plot : 3
# # # plot a histogram for minute of the hour atwhich accident happen
# # st.subheader("Breakdown by minute between % i:00 and % i:00" % (hour, (hour + 1) % 24))
# # filtered = data[
# #     (data['date / time'].dt.hour >= hour) & (data['date / time'].dt.hour < (hour + 1))
# # ]
# # hist = np.histogram(filtered['date / time'].dt.minute, bins = 60, range =(0, 60))[0]
# # chart_data = pd.DataFrame({"minute": range(60), "Accidents": hist})
# # fig = px.bar(chart_data, x ='minute', y ='Accidents', hover_data =['minute', 'Accidents'], height = 400)
# # st.write(fig)

# # # The code below uses checkbox to show raw data
# # st.header("Condition of Road at the time of Accidents")
# # select = st.selectbox('Weather ', ['Dry', 'Wet / Damp', 'Frost / ice', 'Snow', 'Flood (Over 3cm of water)'])

# # if select == 'Dry':
# #     st.write(original_data[original_data['road_surface_conditions']=="Dry"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))

# # elif select == 'Wet / Damp':
# #     st.write(original_data[original_data['road_surface_conditions']=="Wet / Damp"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))
# # elif select == 'Frost / ice':
# #     st.write(original_data[original_data['road_surface_conditions']=="Frost / ice"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))

# # elif select == 'Snow':
# #     st.write(original_data[original_data['road_surface_conditions']=="Snow"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))

# # else:
# #     st.write(original_data[original_data['road_surface_conditions']=="Flood (Over 3cm of water)"][["weather_conditions", "light_conditions", "speed_limit", "number_of_casualties"]].sort_values(by =['number_of_casualties'], ascending = False).dropna(how ="any"))


# # if st.checkbox("Show Raw Data", False):
# #     st.subheader('Raw Data')
# #     st.write(data)
