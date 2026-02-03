import streamlit as st
import datetime, requests
from plotly import graph_objects as go

st.set_page_config(page_title='Weather Forecast', page_icon=":rainbow:")

st.title("8-DAY WEATHER FORECAST 🌧🌥")

city = st.text_input("ENTER THE NAME OF THE CITY ")

unit = st.selectbox("SELECT TEMPERATURE UNIT ", ["Celsius", "Fahrenheit"])

speed = st.selectbox("SELECT WIND SPEED UNIT ", ["Metre/sec", "Kilometre/hour"])

graph = st.radio("SELECT GRAPH TYPE ", ["Bar Graph", "Line Graph"])

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://wallpaperaccess.com/full/1442216.jpg")
    }
    </style>
    """,
    unsafe_allow_html=True
)

if unit == "Celsius":
    temp_unit = " °C"
else:
    temp_unit = " °F"
    
if speed == "Kilometre/hour":
    wind_unit = " km/h"
else:
    wind_unit = " m/s"

api = "c1b71039567ec4898883cd4e53ba027d"
weather_url = f"https://api.openweathermap.org/data/3.0/weather?q={city}&appid={api}"

if st.button("SUBMIT"):
    try:
        response = requests.get(weather_url)
        if response.status_code == 200:
            city_data = response.json()
            lon = city_data["coord"]["lon"]
            lat = city_data["coord"]["lat"]

            onecall_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={api}"
            forecast_response = requests.get(onecall_url)

            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()

                maxtemp = []
                mintemp = []
                pres = []
                humd = []
                wspeed = []
                desc = []
                cloud = []
                rain = []
                dates = []
                sunrise = []
                sunset = []
                cel = 273.15

                for item in forecast_data["daily"]:
                    if unit == "Celsius":
                        maxtemp.append(round(item["temp"]["max"] - cel, 2))
                        mintemp.append(round(item["temp"]["min"] - cel, 2))
                    else:
                        maxtemp.append(round((((item["temp"]["max"] - cel) * 1.8) + 32), 2))
                        mintemp.append(round((((item["temp"]["min"] - cel) * 1.8) + 32), 2))

                    if wind_unit == "m/s":
                        wspeed.append(str(round(item["wind_speed"], 1)) + wind_unit)
                    else:
                        wspeed.append(str(round(item["wind_speed"] * 3.6, 1)) + wind_unit)

                    pres.append(item["pressure"])
                    humd.append(str(item["humidity"]) + ' %')
                    cloud.append(str(item["clouds"]) + ' %')
                    rain.append(str(int(item["pop"] * 100)) + '%')
                    desc.append(item["weather"][0]["description"].title())

                    d1 = datetime.date.fromtimestamp(item["dt"])
                    dates.append(d1.strftime('%d %b'))

                    sunrise.append(datetime.datetime.utcfromtimestamp(item["sunrise"]).strftime('%H:%M'))
                    sunset.append(datetime.datetime.utcfromtimestamp(item["sunset"]).strftime('%H:%M'))

                def bargraph():
                    fig = go.Figure(data=[
                        go.Bar(name="Maximum", x=dates, y=maxtemp, marker_color='crimson'),
                        go.Bar(name="Minimum", x=dates, y=mintemp, marker_color='navy')
                    ])
                    fig.update_layout(xaxis_title="Dates", yaxis_title="Temperature", barmode='group', margin=dict(l=70, r=10, t=80, b=80), font=dict(color="white"))
                    st.plotly_chart(fig)

                def linegraph():
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=dates, y=mintemp, name='Minimum '))
                    fig.add_trace(go.Scatter(x=dates, y=maxtemp, name='Maximimum ', marker_color='crimson'))
                    fig.update_layout(xaxis_title="Dates", yaxis_title="Temperature", font=dict(color="white"))
                    st.plotly_chart(fig)

                icon = city_data["weather"][0]["icon"]
                current_weather = city_data["weather"][0]["description"].title()

                if unit == "Celsius":
                    temp = str(round(city_data["main"]["temp"] - cel, 2))
                else:
                    temp = str(round((((city_data["main"]["temp"] - cel) * 1.8) + 32), 2))

                col1, col2 = st.columns(2)
                with col1:
                    st.write("## Current Temperature ")
                with col2:
                    st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png", width=70)
                col1.metric("TEMPERATURE", temp + temp_unit)
                col2.metric("WEATHER", current_weather)
                st.subheader(" ")

                if graph == "Bar Graph":
                    bargraph()

                elif graph == "Line Graph":
                    linegraph()

                table1 = go.Figure(data=[go.Table(header=dict(
                    values=[
                        '<b>DATES</b>',
                        '<b>MAX TEMP<br>(in' + temp_unit + ')</b>',
                        '<b>MIN TEMP<br>(in' + temp_unit + ')</b>',
                        '<b>CHANCES OF RAIN</b>',
                        '<b>CLOUD COVERAGE</b>',
                        '<b>HUMIDITY</b>'],
                    line_color='black', fill_color='royalblue', font=dict(color='white', size=14), height=32),
                    cells=dict(values=[dates, maxtemp, mintemp, rain, cloud, humd],
                               line_color='black', fill_color=['paleturquoise', ['palegreen', '#fdbe72'] * 7], font_size=14, height=32
                               ))])

                table1.update_layout(margin=dict(l=10, r=10, b=10, t=10), height=328)
                st.write(table1)

                table2 = go.Figure(data=[go.Table(columnwidth=[1, 2, 1, 1, 1, 1], header=dict(values=['<b>DATES</b>', '<b>WEATHER CONDITION</b>', '<b>WIND SPEED</b>', '<b>PRESSURE<br>(in hPa)</b>', '<b>SUNRISE<br>(in UTC)</b>', '<b>SUNSET<br>(in UTC)</b>']
                                                 , line_color='black', fill_color='royalblue', font=dict(color='white', size=14), height=36),
                    cells=dict(values=[dates, desc, wspeed, pres, sunrise, sunset],
                               line_color='black', fill_color=['paleturquoise', ['palegreen', '#fdbe72'] * 7], font_size=14, height=36))])

                table2.update_layout(margin=dict(l=10, r=10, b=10, t=10), height=360)
                st.write(table2)

                st.header(' ')
                st.header(' ')

            else:
                st.error("Error fetching forecast data.")
        else:
            st.error("Invalid city name or API issue.")
    except KeyError:
        st.error("Invalid city!! Please try again!!")
