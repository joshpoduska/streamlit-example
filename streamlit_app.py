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
import pickle
import time
from matplotlib import pyplot as plt
from  matplotlib.ticker import FuncFormatter
import seaborn as sns
import requests
import eli5
import xgboost as xgb
 
xgc = xgb.Booster(model_file="tune_best.xgb")
 
 
st.set_page_config(layout="wide")
 
 
    
####################
### INTRODUCTION ###
####################
 
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('Credit Application Risk Scores')
with row0_2:
    st.text("")
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("")
    
#################
### SELECTION ###
#################
 
 
st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')
 
### SEASON RANGE ###
st.sidebar.subheader("**Enter the application inputs to view the risk scores.**")
st.sidebar.subheader("")
with st.sidebar.form("my_form"):
    checking_account_A14 = st.checkbox('Has a Checking Account')
    credit_history_A34 = st.checkbox('Full Credit History')
    property_A121 = st.checkbox('Property')
    checking_account_A13 = st.checkbox('Checking Account Balance > 1000')
    other_installments_A143 = st.checkbox('other_installments_A143')
    debtors_guarantors_A103 = st.checkbox('Has Guarantors')
    savings_A65 = st.checkbox('Has Savings Account')
    employment_since_A73 = st.checkbox('Employed for > 5 Years')
    savings_A61 = st.checkbox('Savings > 1000')
    age = st.number_input('Insert applicant age', min_value = 20, max_value = 115)
    scored = st.form_submit_button("Score")
 
# baseline = 'domino/datasets/local/CreditRisk/data/train_data_0.csv'
# df_cr = pd.read_csv(baseline)
 
age_min, age_max = 21, 115
age_std = (age - age_min) / (age_max - age_min)
 
featurenames = ["checking_account_A14", "credit_history_A34", "property_A121", "checking_account_A13", 
                 "other_installments_A143", "debtors_guarantors_A103", "savings_A65", "age", 
                 "employment_since_A73", "savings_A61"]
 
# column_names = ['duration', 'credit_amount', 'installment_rate', 'residence', 'age', 'credits', 'dependents', 
#                 'checking_account_A11', 'checking_account_A12', 'checking_account_A13', 'checking_account_A14', 
#                 'credit_history_A30', 'credit_history_A31', 'credit_history_A32', 'credit_history_A33', 
#                 'credit_history_A34', 'purpose_A40', 'purpose_A41', 'purpose_A410', 'purpose_A42', 'purpose_A43', 
#                 'purpose_A44', 'purpose_A45', 'purpose_A46', 'purpose_A48', 'purpose_A49', 'savings_A61', 
#                 'savings_A62', 'savings_A63', 'savings_A64', 'savings_A65', 'employment_since_A71', 
#                 'employment_since_A72', 'employment_since_A73', 'employment_since_A74', 'employment_since_A75', 
#                 'status_A91', 'status_A92', 'status_A93', 'status_A94', 'debtors_guarantors_A101', 
#                 'debtors_guarantors_A102', 'debtors_guarantors_A103', 'property_A121', 'property_A122', 
#                 'property_A123', 'property_A124', 'other_installments_A141', 'other_installments_A142', 
#                 'other_installments_A143', 'housing_A151', 'housing_A152', 'housing_A153', 'job_A171', 'job_A172', 
#                 'job_A173', 'job_A174', 'telephone_A191', 'telephone_A192', 'foreign_worker_A201', 'foreign_worker_A202']
    
# # Set some default values
# sample_data = [[0.4705882352941176, 0.3685484758446132, 0.3333333333333333, 0.3333333333333333, 
#                 0.2857142857142857, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 
#                 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
#                 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 
#                 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0]]
 
# df = pd.DataFrame(sample_data, columns=column_names)
 
# # Override the values with what was passed to the scoring function
# df[["checking_account_A14"]] = checking_account_A14
# df[["credit_history_A34"]] = credit_history_A34
# df[["property_A121"]] = property_A121
# df[["checking_account_A13"]] = checking_account_A13
# df[["other_installments_A143"]] = other_installments_A143
# df[["debtors_guarantors_A103"]] = debtors_guarantors_A103
# df[["savings_A65"]] = savings_A65
# df[["age"]] = age
# df[["employment_since_A73"]] = employment_since_A73
# df[["savings_A61"]] = savings_A61
 
df = pd.DataFrame(columns=["checking_account_A14", "credit_history_A34", "property_A121", "checking_account_A13", 
                 "other_installments_A143", "debtors_guarantors_A103", "savings_A65", "age", 
                 "employment_since_A73", "savings_A61"], 
                      data=[[checking_account_A14, credit_history_A34, property_A121, checking_account_A13,
                             other_installments_A143, debtors_guarantors_A103, savings_A65, age_std, 
                             employment_since_A73, savings_A61]])
 
setup_dict = {}
scoring_request = {}
results = list()
 
for n in range(df.shape[0]):
    for i in list(df.columns):
        setup_dict.update({i :list(df[n:n+1].to_dict().get(i).values())[0]})
        scoring_request = {'data' : setup_dict}
        
        
        response = requests.post("https://demo2.dominodatalab.com:443/models/63f889a99fb0fd477f3a599e/latest/model",
    auth=(
        "B0HjcRkGR9YqicRzxRIN08rc2hor1vsZdPoR5mFF1BvvbR1iFRZZKRBgb8RWvGNv",
        "B0HjcRkGR9YqicRzxRIN08rc2hor1vsZdPoR5mFF1BvvbR1iFRZZKRBgb8RWvGNv"
    ),
        json=scoring_request
    )
    results.append(response.json().get('result'))
 
 
### Results ###
 
probability = results[0]["score"]

if results[0]["class"] == 1:
    result_text = ":green[APPROVED]"
else:
    result_text = ":red[DENIED]"
  
  
import plotly.graph_objects as go
import plotly.express as px

# fig = go.Figure(go.Indicator(
#     mode = "gauge+number",
#     value = probability,
#     domain = {'x': [0, 1], 'y': [0, 1]},
#     title = {'text': "Probability to Repay"}))

fig = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = probability,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Probability to Repay", 'font': {'size': 24}},
    gauge = {
        'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "white"},
        'bar': {'color': "white"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "white",
        'steps': [
            {'range': [0, 0.4], 'color': px.colors.qualitative.Plotly[1]},
            {'range': [0.4, 0.6], 'color': px.colors.qualitative.Plotly[9]},         
            {'range': [0.6, 1], 'color': px.colors.qualitative.Plotly[2]}]
        }))

fig.update_layout(paper_bgcolor = px.colors.qualitative.Dark24[5], font = {'color': "white", 'family': "Arial"})


 
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.subheader('After scoring this application, the model suggests that the application be:')
    st.subheader(' ')
    st.subheader(result_text)
    st.subheader(' ')
    st.plotly_chart(fig, use_container_width=True)
    
    
#     html_object = eli5.show_weights(xgc)
#     raw_html = html_object._repr_html_()
#     components.v1.html(raw_html)



#     st.markdown('The following table shows the impact each application characteristic had on the prediction.')
# #     print(eli5.format_as_text(eli5.explain_weights(xgc)))
#     st.markdown(print(eli5.format_as_text(eli5.show_prediction(xgc, df, feature_names=list(df.columns), show_feature_values=True))))
