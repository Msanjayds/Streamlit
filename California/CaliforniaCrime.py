
# This demo to is to explore the crime retae data of Sarcamento city
# in california in the month of Jan 2018. This is built using the streamlit API's.
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
from PIL import Image


def main():
    st.success("**_Crime Rate Analysis_: Sacramento, California - Jan 2018 Data**")

    image = Image.open('sacramento.jpg')
    st.image(image, caption='Sacramento,California (source-wiki)', use_column_width=True)

   # Function to load the data and cache it
    @st.cache
    def load_data():
        data = pd.read_csv('california_crimeinfo.csv')
        return data

    # load data and cache it using Streamlit cache
    crime_data = load_data()

    # Create a Check box to display the raw data.
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        load_state = st.text('Loading Data..')
        st.write(crime_data)
        load_state.text('Loading Completed!')

    # Create a Check box to show few summary details.
    if st.checkbox('Crime Summary'):
        grp_data = crime_data.copy()
        grp_data['Count'] = 1
        st.subheader('Top 50 Crimes in a Month')
        st.write(pd.DataFrame(grp_data.groupby(['C_Descrip'], sort=False)['Count'].count().rename_axis(["Type of Crime"]).nlargest(50)))
        st.subheader('# of Crimes by Day of Month')
        st.write(pd.DataFrame(grp_data.groupby(['C_Day of month'], sort=False)['Count'].count().rename_axis(["Day of Month"])))

    # Bar chart to show the Top 10 cromes using plotly
    st.subheader(" Top 10 Crimes ")
    grp_data = crime_data.copy()
    grp_data['Count'] = 1
    k = pd.DataFrame(grp_data.groupby(['C_Descrip'], sort=False)['C_Address'].count().rename_axis(["Type of Crime"]).nlargest(10))
    Crime = pd.Series(k.index[:])
    Count = list(k['C_Address'][:])
    Crime_Count = pd.DataFrame(list(zip(Crime, Count)),
                               columns=['Crime', 'Count'])
    fig = px.bar(Crime_Count, x='Crime', y='Count', color='Count',
                 labels={'Crime': 'Crime Type', 'Count': 'Crime Count'})
    st.plotly_chart(fig)

   # create a slider to select the required day of month
    st.subheader('Crime Location on Map - Select the day of a Month')
    Day_filter = st.slider('', 1, 31, 5)
    Crime_Filter = crime_data[crime_data['C_Day of month'] == Day_filter]

    # Create a Map to show the physical locations of crime for the selected day.
    midpoint = (np.average(Crime_Filter["lat"]), np.average(Crime_Filter["lon"]))

    st.deck_gl_chart(
        viewport={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 40,
        },
        layers=[
            {
                "type": "HexagonLayer",
                "data": Crime_Filter,
                "radius": 80,
                "elevationScale": 4,
                "elevationRange": [0, 1000],
                "pickable": True,
                "extruded": True,
            }
        ],
    )

    # Histogram to show the no of Crimes by Hour for the selcted day of month.
    hist_values = np.histogram(Crime_Filter['C_Hour'], bins=24, range=(0, 23))[0]
    st.bar_chart(hist_values)
    st.write('--------------------------------- No. of Crimes by Hour in a given day ---------------------------------')
    st.success("     ")

    if st.checkbox('Like Balloons?'):
        st.balloons()


if __name__ == "__main__":
    main()
