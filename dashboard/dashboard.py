import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_weather_workday_df(df, isWorkdaybyInt):
    weather_workday_df = df[df["workingday"] == isWorkdaybyInt].groupby(["weathersit"]).cnt.sum().sort_values(ascending=False).reset_index()
    # karena tidak ada cuaca 4 maka akan kita tambahkan cuaca 4 dengan cnt bernilai 0.
    if not (weather_workday_df['weathersit'] == 4).any():
        new_row = pd.DataFrame({"weathersit": [4], "cnt": [0]})
        weather_workday_df = pd.concat([weather_workday_df, new_row], ignore_index=True)

    weather_workday_df.rename(columns={
        "weathersit": "weather_index",
        "cnt": "users_count"
    }, inplace=True)
    
    return weather_workday_df

def create_byHourGroup_df(df):
    df["hr_group"] = df.hr.apply(
        lambda x: "Dini Hari" if x>=0 and x<6 
        else ("Pagi" if x>=6 and x<11 
              else ("Siang" if x>=11 and x<15 
                    else "Sore" if x>=15 and x<18 else "Malam")
        )
    )


    byHourGroup_df = df.groupby(by="hr_group").cnt.sum().reset_index()
    byHourGroup_df.rename(columns={
        "hr_group": "hour_group",
        "cnt": "users_count"
    }, inplace=True)
    
    return byHourGroup_df


day_df = pd.read_csv(r'https://raw.githubusercontent.com/KawaiSeigiDesu/Belajar-Analisis-Data-dengan-Python/refs/heads/main/data/day.csv')
hour_df = pd.read_csv(r'https://raw.githubusercontent.com/KawaiSeigiDesu/Belajar-Analisis-Data-dengan-Python/refs/heads/main/data/hour.csv')

column = "dteday"
day_df.sort_values(by=column, inplace=True)
day_df.reset_index(inplace=True)
hour_df.sort_values(by=column, inplace=True)
hour_df.reset_index(inplace=True)

day_df[column] = pd.to_datetime(day_df[column])
hour_df[column] = pd.to_datetime(day_df[column])


min_date = day_df[column].min()
max_date = day_df[column].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/KawaiSeigiDesu/Belajar-Analisis-Data-dengan-Python/db8229b9710c7217ca10bc75db15ab52efa977f7/dashboard/bike-sharing-image.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df[column] >= str(start_date)) & 
                (day_df[column] <= str(end_date))]
second_df = hour_df[(hour_df[column] >= str(start_date)) & 
                (hour_df[column] <= str(end_date))]

weather_NOTworkday_df = create_weather_workday_df(main_df, 0)
weather_workday_df = create_weather_workday_df(main_df, 1)
byHourGroup_df = create_byHourGroup_df(second_df)

########################
st.header('Dicoding Bike Sharing Dashboard :sparkles:')

st.subheader("Workdays")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots()
    labels_detail = [
        'Clear or Partly cloudy', 
        'Mist and/or Cloudy', 
        'Light Rain and/or Thunderstorm or Light Snow', 
        'Heavy Rain or Snow and Fog'
    ]
    size = weather_workday_df["users_count"]
    pie = plt.pie(size, startangle=0)
    title = plt.title("Jumlah Total Pengguna di Tiap Cuaca\nPada Hari Bekerja (2011-2012)", fontsize=20)
    title.set_ha("center")
    plt.legend(
        pie[0], 
        labels_detail, 
        bbox_to_anchor=(0.65,-0.05), 
        loc="lower right", 
        bbox_transform=plt.gcf().transFigure
    )
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots()
    labels_detail = [
        'Clear or Partly cloudy', 
        'Mist and/or Cloudy', 
        'Light Rain and/or Thunderstorm or Light Snow', 
        'Heavy Rain or Snow and Fog'
    ]
    size = weather_NOTworkday_df["users_count"]
    pie = plt.pie(size, startangle=0)
    title = plt.title("Jumlah Total Pengguna di Tiap Cuaca\nPada Hari Libur (2011-2012)", fontsize=20)
    title.set_ha("center")
    plt.legend(
        pie[0], 
        labels_detail, 
        bbox_to_anchor=(0.65,-0.05), 
        loc="lower right", 
        bbox_transform=plt.gcf().transFigure
    )
    st.pyplot(fig)
########################

########################
st.subheader("Time of Day")
 
fig = plt.figure(figsize=(10, 5))
 
sns.barplot(
    y="users_count", 
    x="hour_group",
    hue="hour_group",
    data=byHourGroup_df.sort_values(by="users_count", ascending=False),
    legend=False
)
plt.title("Jumlah Total Pengguna di Tiap Kelompok Jam", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
st.pyplot(fig)
