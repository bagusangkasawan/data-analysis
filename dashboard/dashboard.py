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
day_df['temp_bin'] = pd.cut(day_df['temp'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0], labels=['Very Cold', 'Cold', 'Mild', 'Warm', 'Hot'])

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
    page_icon="https://raw.githubusercontent.com/bagusangkasawan/data-analysis/main/dashboard/bikes-sharing.png",
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

# Define each tab's content
if analysis_type == "Efek Cuaca":
    st.header("Pengaruh Cuaca pada Penggunaan Sepeda")
    day_type = st.radio("Pilih Hari", ("Hari Kerja", "Hari Libur"))
    
    if day_type == "Hari Kerja":
        weather_workday_df = day_df[day_df["workingday"] == 1].groupby(["weather"]).cnt.sum().reset_index()
        sns.barplot(x="weather", y="cnt", data=weather_workday_df, palette="coolwarm")
        plt.xlabel("Cuaca")
        plt.ylabel("Jumlah Pengguna")
        plt.title("Pengaruh Cuaca pada Penggunaan Sepeda (Hari Kerja)")
        st.pyplot(plt)
        st.write("**Insight**: Jumlah penggunaan sepeda lebih tinggi pada hari kerja saat cuaca cerah (clear) atau berkabut (mist), dan berkurang saat hujan ringan atau salju ringan (light rain/snow).")
    else:
        weather_holiday_df = day_df[day_df["workingday"] == 0].groupby(["weather"]).cnt.sum().reset_index()
        sns.barplot(x="weather", y="cnt", data=weather_holiday_df, palette="coolwarm")
        plt.xlabel("Cuaca")
        plt.ylabel("Jumlah Pengguna")
        plt.title("Pengaruh Cuaca pada Penggunaan Sepeda (Hari Libur)")
        st.pyplot(plt)
        st.write("**Insight**: Pada hari libur, jumlah penggunaan sepeda juga lebih tinggi saat cuaca cerah (clear) atau berkabut (mist), namun penggunaan sepeda cenderung tetap lebih rendah pada kondisi cuaca buruk (light rain/snow).")

elif analysis_type == "Pola Penggunaan":
    st.header("Pola Penggunaan Sepeda")
    st.subheader("Pola Penggunaan Sepanjang Minggu")

    weekday = st.selectbox("Pilih Hari dalam Minggu", ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", "Minggu"])
    weekday_index = ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", "Minggu"].index(weekday)
    usage_by_day = hour_df[hour_df["weekday"] == weekday_index].groupby(["hr"]).cnt.sum().reset_index()

    plt.figure(figsize=(10, 5))
    sns.lineplot(x="hr", y="cnt", data=usage_by_day, palette="viridis")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Pengguna")
    plt.title(f"Pola Penggunaan Sepeda pada hari {weekday}")
    st.pyplot(plt)
    st.write(f"**Insight**: Pola penggunaan sepeda pada hari {weekday} menunjukkan puncak penggunaan pada jam sibuk, seperti pagi dan sore hari, yang mungkin bertepatan dengan jam perjalanan kerja atau sekolah.")

    st.subheader("Pola Penggunaan Sepanjang Jam")
    usage_by_time_df = hour_df.groupby(["weekday", "hr"]).cnt.sum().unstack()
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(usage_by_time_df, cmap="YlGnBu", cbar_kws={'label': 'Total Pengguna Sepeda'})
    plt.xlabel("Jam")
    plt.ylabel("Hari dalam Minggu")
    plt.title("Pola Penggunaan Sepeda Sepanjang Minggu dan Jam")
    plt.yticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", "Minggu"], rotation=0)
    st.pyplot(plt)
    st.write("**Insight**: Heatmap penggunaan sepeda menunjukkan tren penggunaan yang tinggi pada jam-jam tertentu di sepanjang minggu, dengan puncak penggunaan terlihat pada hari kerja saat jam sibuk.")

elif analysis_type == "Clustering":
    st.header("Clustering Pengguna Sepeda")
    combined_df = pd.merge(hour_df, day_df, on='dteday', suffixes=('_hour', '_day'))

    def cluster_group(row):
        if row['season_day'] == 1:
            return 'Winter_Workday' if row['workingday_day'] == 1 else 'Winter_Holiday'
        elif row['season_day'] == 2:
            return 'Spring_Workday' if row['workingday_day'] == 1 else 'Spring_Holiday'
        elif row['season_day'] == 3:
            return 'Summer_Workday' if row['workingday_day'] == 1 else 'Summer_Holiday'
        elif row['season_day'] == 4:
            return 'Fall_Workday' if row['workingday_day'] == 1 else 'Fall_Holiday'

    combined_df['cluster'] = combined_df.apply(cluster_group, axis=1)
    cluster_counts = combined_df.groupby('cluster')[['registered_day', 'casual_day']].sum()

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.35
    ax.barh(cluster_counts.index, cluster_counts['registered_day'], height=bar_width, label='Registered', color='#1f77b4')
    ax.barh(cluster_counts.index, cluster_counts['casual_day'], height=bar_width, label='Casual', color='#ff7f0e', left=cluster_counts['registered_day'])
    ax.set_xlabel('Jumlah Penyewaan', fontsize=14)
    ax.set_ylabel('Cluster', fontsize=14)
    ax.set_title('Total Penyewaan Sepeda Berdasarkan Cluster', fontsize=16)
    ax.legend(title='Tipe Pengguna')
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig)
    st.write("**Insight**: Clustering penggunaan sepeda berdasarkan musim dan hari menunjukkan perbedaan signifikan antara jumlah pengguna terdaftar dan pengguna biasa, dengan variasi berdasarkan musim dan hari kerja/libur. Hal ini dapat membantu dalam perencanaan dan pengelolaan sumber daya sepeda.")

    st.header("Distribusi Binning Suhu")
    temp_bin_counts = day_df['temp_bin'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    sns.countplot(x='temp_bin', data=day_df, palette='coolwarm', order=temp_bin_counts.index)
    plt.title('Distribusi Binning Suhu')
    plt.xlabel('Kelompok Suhu')
    plt.ylabel('Jumlah')
    st.pyplot(plt)
    st.write("**Insight**: Penggunaan sepeda meningkat saat cuaca sedang (mild) dan hangat (warm), sementara penggunaan menurun saat cuaca sangat dingin (very cold) atau panas ekstrem (hot), menunjukkan preferensi pengguna pada kondisi cuaca yang lebih nyaman.")

# Footer
st.sidebar.markdown("Created by Bagus Angkasawan Sumantri Putra")
