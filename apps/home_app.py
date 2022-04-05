import os
import streamlit as st
from hydralit import HydraHeadApp

MENU_LAYOUT = [1,1,1,7,2]

class HomeApp(HydraHeadApp):


   def __init__(self, title = 'Hydralit Explorer', **kwargs):
      self.__dict__.update(kwargs)
      self.title = title


   #This one method that must be implemented in order to be used in a Hydralit application.
   #The application must also inherit from the hydrapp class in order to correctly work within Hydralit.
   def run(self):
      st.write('HI, IM A TRADER!')
