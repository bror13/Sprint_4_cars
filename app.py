import pandas as pd
import streamlit as st
import plotly.express as px
#import altair as at

st.header('Analysis of Used Vehicle Markets')
st.write('Filter by vehicle make in the drop down below')

df = pd.read_csv('vehicles_us.csv')


#separate the make and model strings into new columns
df[['make','model']] = df['model'].str.split(" ", n=1, expand=True)



make_options = df['make'].unique()

selected_menu = st.selectbox('Select a make', make_options)