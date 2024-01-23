import streamlit as st
import time
import datetime
import pytz  # Import pytz for time zone support
import streamlit_antd_components as sac
import requests
import pandas as pd

#======================def START=========================
#===========Upbit START=============
#종목리스트 가져오기
def get_tickers():
    url = "https://api.upbit.com/v1/market/all"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    tickers = []
    for market in data:
        if market['market'].startswith("KRW"):
            tickers.append(market['market'])
    return tickers

#종목 현재가 가져오기
def get_ticker_price(market):
    url = f"https://api.upbit.com/v1/ticker?markets={market}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

#종목 오더북 가져오기
def get_order_price(market):
    url = f"https://api.upbit.com/v1/orderbook?markets={market}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data
    
#===========Upbit END=============
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

st.set_page_config(page_title="●●Etonboard●●")
st.title("Live Clock")

# Create a list of time zones with their labels
time_zones = ['Asia/Dubai', 'Asia/Seoul', 'America/Chicago']
close_open = ['Closed', 'Opened']


# Create a selectbox for time zone selection
#selected_time_zone = st.selectbox("Select Time Zone:", time_zones)

# Create a container for the clock


col1, col2, col3, col4 = st.columns([4, 1, 2.5, 2.5])
with col1:
    selected_time_zone = st.selectbox("Select Time Zone :", time_zones)
    clock_container = st.empty()
with col2:
    ""
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

coin_array = []
coin_string = ""
coin_data = []

trade_price = [] #현재가

all_coin_list = []

all_coin_list = get_tickers()

tab1, tab2, tab3 = st.tabs(["Main", "Setting1", "Setting2"])

with tab1:
    st.header("Main")
    coin_selected = st.empty()
    coin_selected2 = st.empty()
with tab2:
    coin_array = sac.transfer(items=all_coin_list, label='label', index=[0, 1], titles=['source', 'target'], reload='reload data', color='dark', search=True, pagination=True, use_container_width=True)
    coin_number = len(coin_array)
    #coin_selected.write(coin_number)
    
    #현재가
    for m in range(0,coin_number):
        trade_price.append(coin_data[m]['trade_price'])
    #trade_price = [data[i]['trade_price'] for i in range(0, coin_number)]
    #st.write(trade_price)
    
    coin_df = pd.DataFrame({'Name': coin_array, 'Price': trade_price})
    coin_selected2.dataframe(coin_df)
    coin_string = ','.join(coin_array)    
    coin_data = get_ticker_price(coin_string)
with tab3:
    st.header("An owl")
   #st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
    

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
