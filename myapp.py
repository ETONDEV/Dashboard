import streamlit as st
import time
import datetime
from datetime import datetime
import pytz  # Import pytz for time zone support

def get_timezone_display_name(tz_name):
    tz = pytz.timezone(tz_name)
    now = datetime.datetime.now(tz)
    offset = tz.utcoffset(now)
    hours_offset = int(offset.total_seconds() / 3600)
    return f"{tz_name} (GMT {'+' if hours_offset >= 0 else ''}{hours_offset})"

st.title("Live Clock")

# Create a list of time zones with their labels
time_zones = ['Asia/Dubai', 'Asia/Seoul', 'America/Chicago']
]

# Create a selectbox for time zone selection
selected_time_zone = st.selectbox("Select Time Zone:", time_zones)

# Create a container for the clock
clock_container = st.empty()

def update_clock():
    # Get the current time in UTC
    current_time_utc = datetime.now(pytz.utc)

    # Convert the time to the selected time zone
    current_time_localized = current_time_utc.astimezone(pytz.timezone(selected_time_zone[0]))

    # Format the time as HH:MM:SS
    current_time_formatted = current_time_localized.strftime("%H:%M:%S")

    # Display the clock with the time zone label
    clock_container.markdown(f"**Current Time :** {current_time_formatted}")

# Call the update_clock function every second
while True:
    update_clock()
    time.sleep(1)
