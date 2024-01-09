import streamlit as st
import time
import datetime
from datetime import datetime
import pytz  # Import pytz for time zone support

st.title("Live Clock")

# Create a list of time zones with their labels
time_zones = ['Asia/Dubai', 'Asia/Seoul', 'America/Chicago']


# Create a selectbox for time zone selection
selected_time_zone = st.selectbox("Select Time Zone:", time_zones)

# Create a container for the clock
clock_container = st.empty()

def update_clock():
    # Get the current time in UTC
    current_time_utc = datetime.now(pytz.utc)

    # Convert the time to the selected time zone
    current_time_localized = current_time_utc.astimezone(pytz.timezone(selected_time_zone))

    # Format the time as HH:MM:SS
    current_time_formatted = current_time_localized.strftime("%Y-%m-%d(%a) %H:%M:%S")

    # Display the clock with the time zone label
    clock_container.markdown(f"**Current Time :** {current_time_formatted}")

# Call the update_clock function every second
while True:
    update_clock()
    time.sleep(1)
