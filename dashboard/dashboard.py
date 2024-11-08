import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
@st.cache
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/bagusangkasawan/data-analysis/refs/heads/main/data/day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/bagusangkasawan/data-analysis/refs/heads/main/data/hour.csv")

    # Clean Data
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar with Logo
st.sidebar.image('https://raw.githubusercontent.com/bagusangkasawan/data-analysis/refs/heads/main/dashboard/bikes-sharing.png', use_column_width=True) 
st.sidebar.header('Bike Sharing Data Analysis')
st.sidebar.text('Select your analysis options below:')

# Select options
analysis_option = st.sidebar.selectbox('Choose Analysis', ['Overview', 'Weather vs Usage', 'Time vs Usage'])

# Header with Logo
st.image('https://raw.githubusercontent.com/bagusangkasawan/data-analysis/refs/heads/main/dashboard/bikes-sharing.png', use_column_width=True) 

# Overview
if analysis_option == 'Overview':
    st.title('Bike Sharing Data Overview')
    st.write('Here is a general overview of the bike sharing data:')
    st.write("### Day Data")
    st.dataframe(day_df.head())
    st.write("### Hour Data")
    st.dataframe(hour_df.head())

# Weather vs Usage
elif analysis_option == 'Weather vs Usage':
    st.title('Weather Impact on Bike Usage')
    weather_df = day_df.groupby('weathersit').agg({'cnt': 'sum'}).reset_index()
    st.write(weather_df)

    fig, ax = plt.subplots()
    sns.barplot(x='weathersit', y='cnt', data=weather_df, ax=ax)
    ax.set_title('Weather Condition vs Total Bike Usage')
    ax.set_xlabel('Weather Condition')
    ax.set_ylabel('Total Usage')
    st.pyplot(fig)

# Time vs Usage
elif analysis_option == 'Time vs Usage':
    st.title('Time of Day Impact on Bike Usage')
    
    hour_df["hr_group"] = hour_df['hr'].apply(lambda x: "Early Morning" if x < 6 else ("Morning" if x < 11 else ("Afternoon" if x < 15 else ("Evening" if x < 18 else "Night"))))
    
    time_df = hour_df.groupby('hr_group').agg({'cnt': 'sum'}).reset_index()
    
    st.write(time_df)
    
    fig, ax = plt.subplots()
    sns.barplot(x='hr_group', y='cnt', data=time_df, ax=ax)
    ax.set_title('Time of Day vs Total Bike Usage')
    ax.set_xlabel('Time of Day')
    ax.set_ylabel('Total Usage')
    st.pyplot(fig)

# Footer
st.sidebar.text('Created by: Bagus Angkasawan Sumantri Putra')
