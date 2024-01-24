import streamlit as st
import time
import datetime
import pytz  # Import pytz for time zone support
import streamlit_antd_components as sac
import requests
import pandas as pd

#주식관련
#import requests
import bs4 as bs
import urllib3
import ast

#======================def START=========================
#===========Upbit START=============
#코인 리스트 가져오기
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

#코인 현재가 가져오기
def get_ticker_price(market):
    url = f"https://api.upbit.com/v1/ticker?markets={market}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

#코인 오더북 가져오기
def get_order_price(market):
    url = f"https://api.upbit.com/v1/orderbook?markets={market}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

#코인 메인 표
def update_coin_data():
    #global coin_array, trade_price, coin_string, coin_number, coin_array_noKRW, signed_change_rate, signed_change_price, up_down, sum_ask_size, sum_bid_size
    global coin_array, coin_string, coin_number, coin_array_noKRW
    coin_data = get_ticker_price(coin_string) #선택된 코인 data 가져오기
    coin_orderbook = get_order_price(coin_string)

    trade_price = [] #현재가
    up_down = [] #전일대비 업다운
    signed_change_rate = [] #전일대비 퍼센트
    signed_change_price = [] #전일대비 금액
    sum_ask_size = []
    sum_bid_size = []
    sum_ask_bid_rate = []
    compare = []

    #코인 data 가공
    #현재가
    trade_price = [coin_data[i]['trade_price'] for i in range(coin_number)]
    #전일대비 퍼센트
    signed_change_rate = ["{0:6.2f}%".format(float(coin_data[i]['signed_change_rate']*100)) for i in range(coin_number)]
    #전일대비 금액
    signed_change_price = [coin_data[i]['signed_change_price'] for i in range(coin_number)]
    #전일대비 업다운
    change_symbols = {"FALL": "▽", "EVEN": "〓", "RISE": "▲"}
    up_down = [change_symbols.get(coin_data[m]['change'], "") for m in range(coin_number)]
    #매수/매도값 산
    for j in range(coin_number):
        units = coin_orderbook[j]['orderbook_units']
        sum_ask_size.append(int(sum(u['ask_size'] * u['ask_price'] for u in units[:15])))
        sum_bid_size.append(int(sum(u['bid_size'] * u['bid_price'] for u in units[:15])))
    #매수/매도값 산
    for m in range(0,coin_number):
        if sum_ask_size[m] > sum_bid_size[m]:
            sum_ask_bid_tmp = "{0:6.1f}".format(float(sum_ask_size[m]/sum_bid_size[m]))
            compare_tmp = "▶"
        else:
            sum_ask_bid_tmp = "{0:6.1f}".format(float(-sum_bid_size[m]/sum_ask_size[m]))
            compare_tmp = "◁"
        sum_ask_bid_rate.append(sum_ask_bid_tmp)
        compare.append(compare_tmp)
    
    #Dataframe 뿌려주기(초기값)
    coin_df = pd.DataFrame({'Name': coin_array_noKRW, 'Price': trade_price, 'Trd': up_down, '%': signed_change_rate, 'Change': signed_change_price, 'A/B': sum_ask_bid_rate, 'Ask': sum_ask_size, 'Cmpr': compare, 'Bid': sum_bid_size})
    coin_df_sorted = coin_df.sort_values(by=['Price'], ascending=False)
    coin_dataframe.dataframe(coin_df_sorted) 
    
#===========Upbit END=============


#===========Stock START=============
# 1. 종목 데이터 가져오기
def get_all_info(company_code):
    html = connect_finance_page(company_code)
    current_info = html.find("dl", {"class": "blind"})
    current_info = change_info_format(current_info.find_all("dd"))  # dict 형태로 변경
    return current_info

# 1-1. url 연결
def connect_finance_page(company_code):
    url = "https://finance.naver.com/item/main.nhn?code=" + company_code
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, "html.parser")
    return soup

# 1-2. 종목 데이터 리스트 -> 사전 형태로 변경
def change_info_format(current_info):
    info_dictionary = {"Date": current_info[0].get_text()}
    current_info.remove(current_info[0])
    for i, item in enumerate(current_info):
        current_info[i] = item.get_text().split()
    for i, item in enumerate(current_info):
        info_dictionary[item[0]] = item[1]
    return info_dictionary

#주식 메인 표
def update_stock_data():
    #global stock_array
    stock_input = "005930, 035720, 035420" #★★★★★★★★★★★★★종목입력★★★★★★★★★★★★★
    stock_input_tmp = stock_input.replace(" ", "")
    stock_array = stock_input_tmp.split(",") #string to Array
    stock_number = len(stock_array)    

    for code in stock_array:
        info = get_all_info(code)
    #stock_test.write(info)
    stock_test.text_input("output", info)

#===========Stock END=============
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

st.set_page_config(page_title="♣Etonboard♣")
#st.title("Live Clock")

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



all_coin_list = []

# 코인 전체목록 불러오기
all_coin_list = get_tickers()

# 초기 코인선택 대상 설정
text_values = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-VET","KRW-STEEM", "KRW-ETC", "KRW-SAND", "KRW-XEC"]
indices = [all_coin_list.index(text) for text in text_values if text in all_coin_list]

tab1, tab2, tab3 = st.tabs(["Main", "Setting1", "Setting2"])
with tab1:
    #st.header("Main")
    #coin_selected = st.empty()
    coin_dataframe = st.empty()
    stock_test = st.empty()
with tab2:
    coin_array = sac.transfer(items=all_coin_list, label='label', index=indices, titles=['source', 'target'], reload='reload data', color='dark', search=True, pagination=True, use_container_width=True)
    coin_array_noKRW = [coin.replace('KRW-', '') for coin in coin_array]
    coin_number = len(coin_array)
    coin_string = ','.join(coin_array)    
    update_coin_data() #코인 표 만들기
    update_stock_data()
    
    #stock_test.write
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
    update_coin_data()
    time.sleep(1)
