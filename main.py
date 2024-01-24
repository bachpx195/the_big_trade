import streamlit as st
from hydralit_custom import HydraApp
import hydralit_components as hc
import apps

if __name__ == '__main__':
  app = HydraApp(
      title='The Big Trade',
  )

  app.add_app("Home", icon="🏠", app=apps.HomeApp(title='Home'),is_home=True)
  app.add_app("Data", app=apps.DataApp(title='Data'))
  # app.add_app("Inside And Outside", app=apps.InsideAndOutsideApp(title='Inside And Outside'))
  # app.add_app("True Range", app=apps.TrueRangeApp(title='True Range'))
  # app.add_app("Hour Data", app=apps.HighestHourInDayApp(title='Hour Data'))
  # app.add_app("Diff Data", app=apps.DiffDataApp(title='Diff Data'))
  # app.add_app("Data 2h", app=apps.Data2hApp(title='Data 2h'))
  # app.add_app("Mid autumn", app=apps.MidAutumnApp(title='mid autumn'))
  # app.add_app("Morning session", app=apps.MorningSession(
  #     title='morning session'))
  app.add_app("Month return", app=apps.MonthReturnApp(
      title='month return'))

  app.add_loader_app(apps.MyLoadingApp(delay=0))

  app.run()
