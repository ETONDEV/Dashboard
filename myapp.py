import streamlit as st
import time
import datetime
import pytz  # Import pytz for time zone support

#======================def START=========================
def extract_time(remaining_time):
    # Extract hours, minutes, and seconds from the timedelta object
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    remaining_time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return remaining_time_formatted

def market_status(current_utc, market_tz, market_open, market_close, xx_time_zone):
    market_time = current_utc.astimezone(market_tz)

    if not is_weekday(market_time):
        return "Closed - Opens on next weekday"

    # Ensure that market_open and market_close are datetime.time objects
    if not isinstance(market_open, datetime.time) or not isinstance(market_close, datetime.time):
        raise ValueError("market_open and market_close must be datetime.time objects")

    market_open_dt = market_time.replace(hour=market_open.hour, minute=market_open.minute, second=0, microsecond=0)
    market_close_dt = market_time.replace(hour=market_close.hour, minute=market_close.minute, second=0, microsecond=0)

        
    if market_open_dt <= market_time < market_close_dt:
        remaining_time = market_close_dt - market_time
        remaining_time_formatted = extract_time(remaining_time)
        xx_time_zone.markdown(f"[Openned]")
        return f"**Closes** : in {str(remaining_time_formatted)}"
        
    elif market_time < market_open_dt:
        remaining_time = market_open_dt - market_time
        remaining_time_formatted = extract_time(remaining_time)
        xx_time_zone.markdown(f"[Closed]")
        return f"**Opens** : in {str(remaining_time_formatted)}"
    else:
        next_open_dt = (market_open_dt + datetime.timedelta(days=1)).astimezone(pytz.utc)
        remaining_time = next_open_dt - current_utc
        remaining_time_formatted = extract_time(remaining_time)
        xx_time_zone.markdown(f"[Closed]")
        return f"**Opens** : in {str(remaining_time_formatted)}"

def is_weekday(dt):
    return dt.weekday() < 5  # Monday is 0, Sunday is 6

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


col1, col2, col3, col4 = st.columns([4,0.4,2.8,2.8])
with col1:
    selected_time_zone = st.selectbox("Select Time Zone :", time_zones)
    clock_container = st.empty()
with col2:
    st.markdown("") #공백추가 디자인 
with col3:
    #korea_time_zone = st.text_input("Korea [9:00AM ~ 3:30PM (KST)] :", close_open)
    "Korea Market:"
    korea_time_zone = st.empty()
    stock1_container = st.empty()
with col4:
    #us_time_zone = st.text_input("US [11:30PM ~ 6:00AM (KST)] :", close_open)
    "US Market:"
    us_time_zone = st.empty()
    stock2_container = st.empty()
    
def update_clock():
    # Get the current time in UTC
    current_time_utc = datetime.datetime.now(pytz.utc)

    # Convert the time to the selected time zone
    current_time_localized = current_time_utc.astimezone(pytz.timezone(selected_time_zone))

    # Format the time as HH:MM:SS
    current_time_formatted = current_time_localized.strftime("%Y-%m-%d(%a) %H:%M:%S")

    # Display the clock with the time zone label
    clock_container.markdown(f"**Time :** {current_time_formatted}")
    stock1_container.markdown(market_status(current_time_utc, korean_tz, korean_market_open, korean_market_close, korea_time_zone))
    stock2_container.markdown(market_status(current_time_utc, us_tz, us_market_open, us_market_close, us_time_zone))

# Call the update_clock function every second
while True:
    update_clock()
    time.sleep(1)
