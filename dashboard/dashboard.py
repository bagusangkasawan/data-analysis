import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/bagusangkasawan/data-analysis/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/bagusangkasawan/data-analysis/refs/heads/main/data/hour.csv")

# Data preprocessing
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['weekday'] = hour_df['dteday'].dt.dayofweek

# Define weather condition mappings
weather_conditions = {
    1: "Clear",
    2: "Mist",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}

day_df['weather'] = day_df['weathersit'].map(weather_conditions)
hour_df['weather'] = hour_df['weathersit'].map(weather_conditions)

# Set up Streamlit app
st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    page_icon="\U0001F6B2",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Display logo
st.sidebar.image("https://raw.githubusercontent.com/bagusangkasawan/data-analysis/main/dashboard/bikes-sharing.png", use_column_width=True)
st.title('Bike Sharing Analysis Dashboard')

# Date filter
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [day_df['dteday'].min(), day_df['dteday'].max()])
if len(date_range) == 2:
    start_date, end_date = date_range
    day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
    hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

# Sidebar for user input
analysis_type = st.sidebar.selectbox("Pilih Jenis Analisis", ["Efek Cuaca", "Pola Penggunaan", "Clustering"])

if analysis_type == "Efek Cuaca":
    st.header("Pengaruh Cuaca pada Penggunaan Sepeda")
    day_type = st.radio("Pilih Hari", ("Hari Kerja", "Hari Libur"))
    
    if day_type == "Hari Kerja":
        weather_workday_df = day_df[day_df["workingday"] == 1].groupby("weather")["cnt"].sum().reset_index()
    else:
        weather_workday_df = day_df[day_df["workingday"] == 0].groupby("weather")["cnt"].sum().reset_index()
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x="weather", y="cnt", data=weather_workday_df, palette="coolwarm")
    plt.xlabel("Cuaca")
    plt.ylabel("Jumlah Pengguna")
    plt.title(f"Pengaruh Cuaca pada Penggunaan Sepeda ({day_type})")
    st.pyplot(plt)

elif analysis_type == "Pola Penggunaan":
    st.header("Pola Penggunaan Sepeda")
    weekday = st.selectbox("Pilih Hari dalam Minggu", ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", "Minggu"])
    weekday_index = ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", "Minggu"].index(weekday)
    usage_by_day = hour_df[hour_df["weekday"] == weekday_index].groupby("hr")["cnt"].sum().reset_index()
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(x="hr", y="cnt", data=usage_by_day, palette="viridis")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Pengguna")
    plt.title(f"Pola Penggunaan Sepeda pada {weekday}")
    st.pyplot(plt)

elif analysis_type == "Clustering":
    st.header("Clustering Pengguna Sepeda")
    cluster_df = day_df.copy()
    cluster_df["cluster"] = cluster_df.apply(lambda row: f"Season-{row['season']}_Workday-{row['workingday']}", axis=1)
    cluster_counts = cluster_df.groupby("cluster")["cnt"].sum().reset_index()
    
    plt.figure(figsize=(10, 5))
    sns.barplot(y="cluster", x="cnt", data=cluster_counts, palette="magma")
    plt.xlabel("Jumlah Penyewaan")
    plt.ylabel("Cluster")
    plt.title("Total Penyewaan Sepeda Berdasarkan Cluster")
    st.pyplot(plt)

# Footer
st.sidebar.markdown("Created by Bagus Angkasawan Sumantri Putra")
