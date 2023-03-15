###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################

import streamlit as st
from streamlit import components
import numpy as np
import pandas as pd
# import pickle
# import time
# from matplotlib import pyplot as plt
# from  matplotlib.ticker import FuncFormatter
# import seaborn as sns
import requests
# import eli5
# import xgboost as xgb
# import seaborn as sns

# xgc = xgb.Booster(model_file="tune_best.xgb")


st.set_page_config(layout="wide")


    
####################
### INTRODUCTION ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('Financial News Sentiment Analysis')
with row0_2:
    st.text("")
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.subheader("Enter financial news text and click score to determine the sentiment of the text.")
    st.markdown("")
    
#################
### SELECTION ###
#################

with st.form("my_form"):
    fintext = st.text_input('Input text', 'there is a shortage of capital, and we need extra financing')
    scored = st.form_submit_button("Score")

setup_dict = {}
scoring_request = {}
results = list()
    
response = requests.post("https://prod-field.cs.domino.tech:443/models/640b3dcd46197615f41ce5f6/latest/model",
    auth=(
        "qJst3g61jZrQqHPtcIknbOPhmbgrjdY0sJqjadkVUMBupjMvvDh084z0MIc6BfUc",
        "qJst3g61jZrQqHPtcIknbOPhmbgrjdY0sJqjadkVUMBupjMvvDh084z0MIc6BfUc"
    ),
    json={
  "data": {
    "sentence": fintext
  }
})
results.append(response.json().get('result'))

### Results ###
 
probability = results[0]["score"]
result_text = results[0]["label"]
  
  
import plotly.graph_objects as go
import plotly.express as px

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = probability,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Probability to Repay", 'font': {'size': 28}},
    gauge = {
        'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "white"},
        'bar': {'color': "white"},
        'bgcolor': "red",
        'borderwidth': 2,
        'bordercolor': "white",
        'steps': [
            {'range': [0, 0.4], 'color': px.colors.qualitative.Plotly[1]},
            {'range': [0.4, 0.6], 'color': px.colors.qualitative.Plotly[9]},         
            {'range': [0.6, 1], 'color': px.colors.qualitative.Plotly[2]}]
        }))

fig.update_layout(paper_bgcolor = "#0e1117", font = {'color': "white", 'family': "Arial"})

 
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:    
    st.subheader('The sentiment of this financial text is:')
    st.subheader("")
    st.subheader(result_text)
    st.subheader(' ')
    st.plotly_chart(fig, use_container_width=True)
