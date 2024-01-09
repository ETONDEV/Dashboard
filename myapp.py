import streamlit as st
import time
import datetime
from datetime import datetime
import pytz  # Import pytz for time zone support

#======================def START=========================
def market_status(current_utc, market_tz, market_open, market_close):
    market_time = current_utc.astimezone(market_tz)
    if not is_weekday(market_time):
        return "Closed - Opens on next weekday"

    market_open_dt = market_time.replace(hour=market_open.hour, minute=market_open.minute, second=0, microsecond=0)
    market_close_dt = market_time.replace(hour=market_close.hour, minute=market_close.minute, second=0, microsecond=0)

    if market_open_dt <= market_time < market_close_dt:
        remaining_time = market_close_dt - market_time
        return f"Open - Closes in {str(remaining_time)}"
    elif market_time < market_open_dt:
        remaining_time = market_open_dt - market_time
        return f"Closed - Opens in {str(remaining_time)}"
    else:
        next_open_dt = (market_open_dt + datetime.timedelta(days=1)).astimezone(pytz.utc)
        remaining_time = next_open_dt - current_utc
        return f"Closed - Opens in {str(remaining_time)}"


#======================def END=========================

#======================var START=========================

# Define market timezones and hours
korean_tz = pytz.timezone("Asia/Seoul")
us_tz = pytz.timezone("America/New_York")
korean_market_open = datetime.time(9, 0, 0)  # 9:00 AM KST
korean_market_close = datetime.time(15, 30, 0)  # 3:30 PM KST
us_market_open = datetime.time(9, 30, 0)  # 9:30 AM ET
us_market_close = datetime.time(16, 0, 0)  # 4:00 PM ET

#======================var END=========================

st.set_page_config(page_title="Etonboard")
st.title("Live Clock")

# Create a list of time zones with their labels
time_zones = ['Asia/Dubai', 'Asia/Seoul', 'America/Chicago']
close_open = ['Closed', 'Opened']


# Create a selectbox for time zone selection
#selected_time_zone = st.selectbox("Select Time Zone:", time_zones)

# Create a container for the clock


col1, col2, col3 = st.columns(3)
with col1:
    selected_time_zone = st.selectbox("Select Time Zone:", time_zones)
    clock_container = st.empty()
with col2:
    korea_time_zone = st.selectbox("Korea [9:00AM ~ 3:30PM (KST)]:", close_open)
    stock1_container = st.empty()
with col3:
    korea_time_zone = st.selectbox("US [11:30PM ~ 6:00AM (KST)]:", close_open)
    stock2_container = st.empty()
def update_clock():
    # Get the current time in UTC
    current_time_utc = datetime.now(pytz.utc)

    # Convert the time to the selected time zone
    current_time_localized = current_time_utc.astimezone(pytz.timezone(selected_time_zone))

    # Format the time as HH:MM:SS
    current_time_formatted = current_time_localized.strftime("%Y-%m-%d(%a) %H:%M:%S")

    # Display the clock with the time zone label
    clock_container.markdown(f"**Time :** {current_time_formatted}")

# Call the update_clock function every second
while True:
    update_clock()
    time.sleep(1)
