import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    file_path = "city_day.csv"  # Change to your actual file path
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
cities = st.sidebar.multiselect("Select Cities", df['City'].unique(), default=df['City'].unique()[:3])
date_range = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])

# Filtered Data
df_filtered = df[(df['City'].isin(cities)) & (df['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))]

st.title("Air Quality Dashboard")
st.write("### Insights from Indian Air Quality Data")

# 1. AQI Trend Over Time
st.subheader("AQI Trend Over Time")
fig1 = px.line(df_filtered, x='Date', y='AQI', color='City', markers=True,
               title='AQI Trends Over Time')
st.plotly_chart(fig1)

# 2. Pollutant Concentrations Comparison
st.subheader("Pollutant Concentrations Across Cities")
pollutants = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3']
selected_pollutant = st.selectbox("Select a Pollutant", pollutants)
fig2 = px.bar(df_filtered, x='City', y=selected_pollutant, color='City',
              title=f'{selected_pollutant} Concentration in Cities')
st.plotly_chart(fig2)

# 3. AQI Category Distribution
st.subheader("AQI Category Distribution")
category_counts = df_filtered['AQI_Bucket'].value_counts().reset_index()
category_counts.columns = ['AQI_Bucket', 'Count']
fig3 = px.pie(category_counts, values='Count', names='AQI_Bucket',
              title='Distribution of AQI Categories')
st.plotly_chart(fig3)

# 4. Correlation Heatmap
st.subheader("Correlation Between Pollutants")
correlation_data = df_filtered[pollutants].corr()
fig, ax = plt.subplots()
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
st.pyplot(fig)


