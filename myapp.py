# myapp.py
import streamlit as st
import datetime
import pytz

def get_timezone_display_name(tz_name):
    tz = pytz.timezone(tz_name)
    now = datetime.datetime.now(tz)
    offset = tz.utcoffset(now)
    hours_offset = int(offset.total_seconds() / 3600)
    return f"{tz_name} (GMT {'+' if hours_offset >= 0 else ''}{hours_offset})"

def market_status(current_time, market_open, market_close):
    market_open_datetime = datetime.datetime.combine(current_time.date(), market_open, tzinfo=current_time.tzinfo)
    market_close_datetime = datetime.datetime.combine(current_time.date(), market_close, tzinfo=current_time.tzinfo)

    if market_open_datetime <= current_time < market_close_datetime:
        remaining_time = market_close_datetime - current_time
        return f"Open - Closes in {str(remaining_time)}"
    else:
        if current_time.time() > market_close:
            market_open_datetime += datetime.timedelta(days=1)
        remaining_time = market_open_datetime - current_time
        return f"Closed - Opens in {str(remaining_time)}"

def main():
    st.title('Real-time Clock with Market Status')

    # Get list of all time zones with GMT offsets
    time_zones = [get_timezone_display_name(tz) for tz in pytz.all_timezones]

    # Time zone selection
    selected_tz_display = st.selectbox('Select Time Zone', time_zones, index=time_zones.index(get_timezone_display_name('Asia/Dubai')))
    selected_tz = selected_tz_display.split(' ')[0]  # Extract just the timezone name
    current_tz = pytz.timezone(selected_tz)

    # JavaScript to update the time every second
    st.markdown("""
        <script src="/static/myjs.js"></script>
        <div id="current-time"></div>
    """, unsafe_allow_html=True)

    # Display market status
    korean_market_open = datetime.time(9, 0, 0)  # 9:00 AM
    korean_market_close = datetime.time(15, 30, 0)  # 3:30 PM
    us_market_open = datetime.time(9, 30, 0)  # 9:30 AM ET
    us_market_close = datetime.time(16, 0, 0)  # 4:00 PM ET

    now = datetime.datetime.now(current_tz)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Korean Market**")
        st.text(market_status(now, korean_market_open, korean_market_close))

    with col2:
        st.markdown("**US Market**")
        st.text(market_status(now, us_market_open, us_market_close))

if __name__ == "__main__":
    main()
