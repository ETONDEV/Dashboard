import streamlit as st
import time
from yfinance import Ticker
from datetime import datetime, timedelta

def is_market_open(market, current_time):
  if market == "korean":
    return korean_market_open <= current_time <= korean_market_close
  elif market == "us":
    return us_market_open <= current_time <= us_market_close
  else:
    raise ValueError("Invalid market specified.")

# Market details
korean_market_open = datetime(hour=9, minute=00)
korean_market_close = datetime(hour=17, minute=30)
us_market_open = datetime(hour=16, minute=00) - timedelta(days=1)  # Account for timezone difference
us_market_close = datetime(hour=4, minute=00)

st.title("Live Clock App")

# Create a container for the clock
clock_container = st.empty()

def update_clock():
  current_time = datetime.now()

  # Update clock display
  clock_container.markdown(f"**Current Time:** {current_time.strftime('%H:%M:%S')}")

  # Check Korean market status
  korean_open = is_market_open("korean", current_time)
  market_status = "Open" if korean_open else "Closed"
  time_remaining = None
  if not korean_open:
    time_remaining = korean_market_open - current_time

  # Check US market status
  us_open = is_market_open("us", current_time)
  market_status += f" (US: {market_status})"

  # Display market status and remaining time
  st.markdown(f"**Korean Market:** {market_status}")
  if time_remaining:
    st.markdown(f"Time until Korean market opens: {time_remaining.strftime('%H:%M:%S')}")

  # Additional logic for US market details (optional)

while True:
  update_clock()
  time.sleep(1)
