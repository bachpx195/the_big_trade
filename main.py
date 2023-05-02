import streamlit as st
from hydralit import HydraApp
import hydralit_components as hc
import apps

#Only need to set these here as we are add controls outside of Hydralit, to customise a run Hydralit!
st.set_page_config(page_title='The Big Trade',page_icon="🐙",layout='wide',initial_sidebar_state='auto',)

if __name__ == '__main__':
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
      title='The Big Trade',
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
  app.add_app("Inside And Outside", app=apps.InsideAndOutsideApp(title='Inside And Outside'))
  app.add_app("True Range", app=apps.TrueRangeApp(title='True Range'))
  app.add_app("Hour Data", app=apps.HighestHourInDayApp(title='Hour Data'))
  app.add_app("Diff Data", app=apps.DiffDataApp(title='Diff Data'))
  app.add_app("Data 2h", app=apps.Data2hApp(title='Data 2h'))
  app.add_app("Mid autumn", app=apps.MidAutumnApp(title='mid autumn'))
  app.add_app("Morning session", app=apps.MorningSession(
      title='morning session'))
  app.add_app("Month return", app=apps.MonthReturnApp(
      title='month return'))

  app.add_loader_app(apps.MyLoadingApp(delay=0))


  complex_nav = {
    'Home': ['Home'],
    'Data': ['Data'],
    'Inside And Outside': ['Inside And Outside'],
    'Hour Data': ['Hour Data'],
    'True Range': ['True Range'],
    'Diff Data': ['Diff Data'],
    'Data 2h': ['Data 2h'],
    'Mid autumn': ['Mid autumn'],
    'Morning session': ['Morning session'],
    'Month return': ['Month return']
  }

  app.run(complex_nav)
