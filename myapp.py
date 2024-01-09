# myapp.py
import streamlit as st
import datetime
import pytz

def market_status(current_time, market_open, market_close):
    if market_open <= current_time.time() < market_close:
        remaining_time = datetime.datetime.combine(datetime.date.today(), market_close) - current_time
        return f"Open - Closes in {str(remaining_time)}"
    else:
        next_open = datetime.datetime.combine(datetime.date.today(), market_open)
        if current_time.time() > market_close:
            next_open += datetime.timedelta(days=1)
        remaining_time = next_open - current_time
        return f"Closed - Opens in {str(remaining_time)}"

def main():
    st.title('Real-time Clock with Market Status')

    # Default timezone
    default_tz = 'Asia/Dubai'
    selected_tz = st.text_input('Enter Time Zone', default_tz)
    
    # Try to set the timezone, revert to default if invalid
    try:
        current_tz = pytz.timezone(selected_tz)
    except:
        current_tz = pytz.timezone(default_tz)
        st.error('Invalid Time Zone. Showing default.')

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

    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown("**Korean Market**")
        st.text(market_status(now, korean_market_open, korean_market_close))

    with col2:
        st.markdown("**US Market**")
        st.text(market_status(now, us_market_open, us_market_close))

if __name__ == "__main__":
    main()
