import streamlit as st
import pandas as pd
import plotly.express as px 
import matplotlib.pyplot as plt
import seaborn as sns 

### Config
st.set_page_config(
    page_title="Getaround delay analysis",
    page_icon="🚗",
    layout="wide"
)

### App
st.title("Getaround delay analysis")


data = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx", sheet_name="rentals_data")

# Create the variable delay 
data["top_delay"] = data.delay_at_checkout_in_minutes.apply(lambda x: 0 if x<=0 else 1)
data["delay"] = data.delay_at_checkout_in_minutes.apply(lambda x:  "No" if x<=0 else "Yes")


st.subheader("Some key metrics")
col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown("Rentals state")
    st.metric(label="% ended", value=round(100*(data.state.value_counts(normalize=True)[0]),2))
    st.metric(label="% canceled", value=round(100*(data.state.value_counts(normalize=True)[1]),2))
with col2:
    st.markdown("Checkout status")
    st.metric(label="% on time", value=round(100*(data.delay.value_counts(normalize=True)[0]),2))
    st.metric(label="% delayed", value=round(100*(data.delay.value_counts(normalize=True)[1]),2))
with col3:
    st.markdown("Delay for mobile rentals")
    st.metric(label="Mean", value=round(data.loc[(data.checkin_type=="mobile") & (data.delay_at_checkout_in_minutes>0), "delay_at_checkout_in_minutes"].mean()))
    st.metric(label="Median", value=round(data.loc[(data.checkin_type=="mobile") & (data.delay_at_checkout_in_minutes>0), "delay_at_checkout_in_minutes"].median()))
with col4:
    st.markdown("Delay for connect rentals")
    st.metric(label="Mean", value=round(data.loc[(data.checkin_type=="connect") &  (data.delay_at_checkout_in_minutes>0), "delay_at_checkout_in_minutes"].mean()))
    st.metric(label="Median", value=round(data.loc[(data.checkin_type=="connect") &  (data.delay_at_checkout_in_minutes>0), "delay_at_checkout_in_minutes"].median()))


st.markdown("---") 


st.markdown("Car rentals per checkin type")
fig = px.histogram(data, x="checkin_type", color="checkin_type")
fig.update_layout(width=800, height=600)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("Proportion of checkin type for the **delayed** checkouts")
    fig = px.pie(data, values=data[data.top_delay==1].checkin_type.value_counts().values, names=data[data.top_delay==1].checkin_type.unique().tolist())
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("Proportion of checkin type for checkouts **on time**")
    fig = px.pie(data, values=data[data.top_delay==0].checkin_type.value_counts().values, names=data[data.top_delay==0].checkin_type.unique().tolist())
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig, use_container_width=True)


data = data[data.delay_at_checkout_in_minutes > 0]
df_mobile_with_thresold = data[data.checkin_type=='mobile']
df_connect_with_thresold = data[data.checkin_type=='connect']


df_threshold = pd.DataFrame(columns = ['checkin_type', 'threshold', 'nb_cancelations'])

for i in range(60, 360, 60):

    df_threshold = df_threshold.append({"checkin_type" : "mobile", 
                         "threshold" : i,
                         "nb_cancelations" : data[(data.checkin_type=="mobile") & (data.top_delay==1) & (data.delay_at_checkout_in_minutes > i)].shape[0]}, ignore_index = True)

    df_threshold = df_threshold.append({"checkin_type" : "connect", 
                         "threshold" : i,
                         "nb_cancelations" : data[(data.checkin_type=="connect") & (data.top_delay==1) & (data.delay_at_checkout_in_minutes > i)].shape[0]}, ignore_index = True)
    

fig = px.line(df_threshold, x="threshold", y="nb_cancelations", color="checkin_type")
st.plotly_chart(fig, use_container_width=True)