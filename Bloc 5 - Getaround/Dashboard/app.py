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


# threshold = st.selectbox("Select delay betweew two rentals", range(60, 360, 60))

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



    # df_threshold.append()
    # count = df_mobile_with_thresold[df_mobile_with_thresold.delay_at_checkout_in_minutes > i].shape[0]
    # impacted_mobile_count.append(count)
    # impacted_mobile_percentage.append((count / df_mobile_with_thresold.shape[0])*100)
    # count = df_connect_with_thresold[df_connect_with_thresold.delay_at_checkout_in_minutes > i].shape[0]
    # impacted_connect_count.append(count)
    # impacted_connect_percentage.append((count / df_connect_with_thresold.shape[0])*100)



# fig, ax1 = plt.subplots(1, 1)    
# st.subheader("Count of impacted rentals following a threshold on allowed checkout delay")
# ax1.plot(arange, impacted_connect_count)
# ax1.plot(arange, impacted_mobile_count)
# ax1.legend(['connect', 'mobile'], labelcolor="black")
# ax1.set_xlabel('Threshold of checkout delay', fontsize="large")
# ax1.xaxis.label.set_color('white')
# st.plotly_chart(fig, use_container_width=True)

# col1, col2 = st.columns(2)
# with col1:
#     fig, ax1 = plt.subplots(1, 1)    
#     st.subheader("Count of impacted rentals following a threshold on allowed checkout delay")
#     ax1.plot(arange, impacted_connect_count)
#     ax1.plot(arange, impacted_mobile_count)
#     ax1.legend(['connect', 'mobile'], labelcolor="white", fontsize="large")
#     ax1.set_xlabel('Threshold of checkout delay', fontsize="large")
#     ax1.xaxis.label.set_color('white')
#     st.plotly_chart(fig, use_container_width=True)
    
# with col2:
#     fig, ax1 = plt.subplots(1, 1)     
#     st.subheader("Percentage of impacted rentals following a threshold on allowed checkout delay")
#     ax1.plot(arange, impacted_connect_percentage)
#     ax1.plot(arange, impacted_mobile_percentage)
#     ax1.legend(['connect', 'mobile'], labelcolor="white", fontsize="large")
#     ax1.set_xlabel('Threshold of checkout delay', fontsize="large")
#     ax1.xaxis.label.set_color('white')
#     st.plotly_chart(fig, use_container_width=True)


# new_data = data[(data.delay_at_checkout_in_minutes > 0) & (data.delay_at_checkout_in_minutes < threshold)]

# fig, ax = plt.subplots(figsize=(8, 4))
# ax = sns.countplot(data=new_data[new_data.delay=="Yes"], x="state")
# lab_val = (new_data['state'].value_counts(sort=False).values / new_data.shape[0])
# lab_pct = [f'{p:2.2%}' for p in lab_val]
# ax.bar_label(container=ax.containers[0], labels=lab_pct);
# st.pyplot(fig)

# ## Simple bar chart
# st.subheader("Simple bar chart built directly with Streamlit")
# st.markdown("""
#     You can build simple chart directly with streamlit using:

#     * [`st.bar_chart`](https://docs.streamlit.io/library/api-reference/charts/st.bar_chart)
#     * [`st.line_chart`](https://docs.streamlit.io/library/api-reference/charts/st.line_chart)
#     * [`st.area_chart`](https://docs.streamlit.io/library/api-reference/charts/st.area_chart)

#     Eventhough it doesn't offer great flexibility, it is still a very simple way to create graphs quickly since 
#     streamlit since these methods accepts a pandas DataFrame or Numpy array as input.

# """)
# currency_per_country = data.set_index("country")["currency"]
# st.bar_chart(currency_per_country)

# ## Bar chart built with plotly 
# st.subheader("Simple bar chart built with Plotly")
# st.markdown("""
#     Now, the best thing about `streamlit` is its compatibility with other libraries. For example, you
#     don't need to actually use built-in charts to create your dashboard, you can use :
    
#     * [`plotly`](https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart) 
#     * [`matplotlib`](https://docs.streamlit.io/library/api-reference/charts/st.pyplot)
#     * [`bokeh`](https://docs.streamlit.io/library/api-reference/charts/st.bokeh_chart)
#     * ...

#     This way, you have all the flexibility you need to build awesome dashboards. 🥰

# """)
# fig = px.histogram(data.sort_values("country"), x="country", y="currency", barmode="group")
# st.plotly_chart(fig, use_container_width=True)


# ### Input data 
# st.subheader("Input data")
# st.markdown("""
#     As a final note, you can use data that a user will insert when he/she interacts with your app.
#     This is called *input data*. To collect these, you can do two things:
#     * [Use any of the input widget](https://docs.streamlit.io/library/api-reference/widgets)
#     * [Build a form](https://docs.streamlit.io/library/api-reference/control-flow/st.form)

#     Depending on what you need to do, you will prefer one or the other. With a `form`, you actually group
#     input widgets together and send the data right away, which can be useful when you need to filter
#     by several variables.

# """)

# #### Create two columns
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("**1️⃣ Example of input widget**")
#     country = st.selectbox("Select a country you want to see all time sales", data["country"].sort_values().unique())
    
#     country_sales = data[data["country"]==country]
#     fig = px.histogram(country_sales, x="Date", y="currency")
#     fig.update_layout(bargap=0.2)
#     st.plotly_chart(fig, use_container_width=True)

# with col2:
#     st.markdown("**2️⃣ Example of input form**")

#     with st.form("average_sales_per_country"):
#         country = st.selectbox("Select a country you want to see sales", data["country"].sort_values().unique())
#         start_period = st.date_input("Select a start date you want to see your metric")
#         end_period = st.date_input("Select an end date you want to see your metric")
#         submit = st.form_submit_button("submit")

#         if submit:
#             avg_period_country_sales = data[(data["country"]==country)]
#             start_period, end_period = pd.to_datetime(start_period), pd.to_datetime(end_period)
#             mask = (avg_period_country_sales["Date"] > start_period) & (avg_period_country_sales["Date"] < end_period)
#             avg_period_country_sales = avg_period_country_sales[mask].mean()
#             st.metric("Average sales during selected period (in $)", np.round(avg_period_country_sales, 2))


# ### Side bar 
# st.sidebar.header("Build dashboards with Streamlit")
# st.sidebar.markdown("""
#     * [Load and showcase data](#load-and-showcase-data)
#     * [Charts directly built with Streamlit](#simple-bar-chart-built-directly-with-streamlit)
#     * [Charts built with Plotly](#simple-bar-chart-built-with-plotly)
#     * [Input Data](#input-data)
# """)
# e = st.sidebar.empty()
# e.write("")
# st.sidebar.write("Made with 💖 by [Jedha](https://jedha.co)")



# ### Footer 
# empty_space, footer = st.columns([1, 2])

# with empty_space:
#     st.write("")

# with footer:
#     st.markdown("""
#         🍇
#         If you want to learn more, check out [streamlit's documentation](https://docs.streamlit.io/) 📖
#     """)