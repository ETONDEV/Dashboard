import streamlit as st
import time
import datetime
from datetime import datetime, timedelta  # Import datetime for tz-aware datetime
from pytz import timezone

now_utc = datetime.datetime.now(timezone.utc)
now_korea = now_utc.astimezone(timezone("Asia/Seoul"))



# Function to determine market status and time to open/close
def get_market_status(market_timezone, market_open_time, market_close_time):
    current_time = datetime.now(timezone.utc).astimezone(timezone(market_timezone))  # Get tz-aware current time
    current_time_str = current_time.strftime("%H:%M")  # Extract time string

    market_open_time_tz = timezone(market_timezone).localize(time.strptime(market_open_time, "%H:%M")).astimezone(tz=None)
    market_close_time_tz = timezone(market_timezone).localize(time.strptime(market_close_time, "%H:%M")).astimezone(tz=None)

    if market_open_time_tz <= current_time_tz <= market_close_time_tz:
        status = "Open"
        time_to_close = market_close_time_tz - current_time_tz
    else:
        status = "Closed"
        if current_time_tz < market_open_time_tz:
            time_to_open = market_open_time_tz - current_time_tz
        else:
            time_to_open = market_open_time_tz + timedelta(days=1) - current_time_tz

    return status, time_to_open or time_to_close

# Main app logic
st.title("Market Clock App")

selected_timezone = st.text_input("Select Time Zone", "Asia/Dubai")

st.markdown("<h2 id='clock'>Current Time:</h2>", unsafe_allow_html=True)
st.markdown(f"<p id='time-display'>Loading...</p>", unsafe_allow_html=True)

# Define market hours (adjust as needed)
korean_market_timezone = "Asia/Seoul"
korean_market_open_time = "09:00"
korean_market_close_time = "15:30"

us_market_timezone = "America/New_York"
us_market_open_time = "09:30"
us_market_close_time = "16:00"

# Display market information
st.markdown("<h2>Market Status</h2>")

korean_market_status, korean_market_time = get_market_status(
    korean_market_timezone, korean_market_open_time, korean_market_close_time
)
st.write(
    f"Korean Market: {korean_market_status} ({korean_market_time.strftime('%H:%M:%S')} remaining)"
)

us_market_status, us_market_time = get_market_status(
    us_market_timezone, us_market_open_time, us_market_close_time
)
st.write(
    f"US Market: {us_market_status} ({us_market_time.strftime('%H:%M:%S')} remaining)"
)

# Include JavaScript for clock updates
st.markdown("<script src='myjs.js'></script>", unsafe_allow_html=True)
