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
import re
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
    for item in current_info:
        text = item.get_text()
        # '종목명'에 해당하는 경우, 전체 문자열을 저장
        if '종목명' in text:
            info_dictionary['종목명'] = text.replace('종목명', '').strip()
        else:
            # 다른 항목들에 대해서는 원래 코드를 유지
            split_text = text.split()
            if len(split_text) > 1:
                info_dictionary[split_text[0]] = split_text[1]
    return info_dictionary

#주식 메인 표
def update_stock_data():
    global stock_data
    #global stock_array
    stock_input = "005930, 305720, 305540, 174360, 448330, 003620, 133690" #★★★★★★★★★★★★★종목입력★★★★★★★★★★★★★
    stock_input_tmp = stock_input.replace(" ", "")
    stock_array = stock_input_tmp.split(",") #string to Array
    stock_number = len(stock_array)    

    for code in stock_array:    
        stock_data.append(get_all_info(code))

    st_trade_name = []
    st_trade_price = []
    st_signed_change_price = []
    st_signed_change_rate = []
    st_up_down = []
    st_trade_time = []
    st_trade_time_status = []
    
    #현재가
    st_trade_name = [stock_data[i]['종목명'] for i in range(stock_number)]
    st_trade_price = [int(stock_data[i]['현재가'].replace(',', '')) for i in range(stock_number)]
    st_signed_change_price = [int(stock_data[i]['현재가'].replace(',', '')) - int(stock_data[i]['전일가'].replace(',', '')) for i in range(stock_number)]
    st_signed_change_rate = ["{:.2f}%".format((float(stock_data[i]['현재가'].replace(',', '')) - float(stock_data[i]['전일가'].replace(',', '')))/float(stock_data[i]['전일가'].replace(',', '')) * 100) for i in range(stock_number)]
    
    #for문 같이 씀
    for i in range(stock_number):
        #업 다운
        if st_signed_change_price[i] > 0:
            st_up_down_tmp = "▲"
        elif st_signed_change_price[i] < 0:
            st_up_down_tmp = "▽"
        else:
            st_up_down_tmp = "〓"
        st_up_down.append(st_up_down_tmp)
        
        #거래시간
        # stock_number 만큼 반복
        data = stock_data[i]['Date']
        # 정규 표현식을 사용하여 날짜와 시간, 상태 추출
        match = re.search(r'(\d{4})년 (\d{2})월 (\d{2})일 (\d{2})시 (\d{2})분 기준 (\S+)', data)
        if match:
            year, month, day, hour, minute, status = match.groups()
    
            # 날짜 객체 생성
            date_obj = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
    
            # 날짜와 요일을 포맷팅
            var1 = date_obj.strftime('%Y-%m-%d(%a) %H:%M')
            var2 = status
    
            # 추출한 값을 리스트에 추가
            st_trade_time.append(var1)
            st_trade_time_status.append(var2)
            
        
    #change_symbols = {"FALL": "▽", "EVEN": "〓", "RISE": "▲"}
    #up_down = [change_symbols.get(coin_data[m]['change'], "") for m in range(coin_number)]    
    #st_signed_change_rate = [(float(stock_data[i]['현재가'].replace(',', '')) - float(stock_data[i]['전일가'].replace(',', '')))/float(stock_data[i]['전일가'].replace(',', '')) for i in range(stock_number)]
    #coin_df = pd.DataFrame({'Name': coin_array_noKRW, 'Price': trade_price, 'Trd': up_down, '%': signed_change_rate, 'Change': signed_change_price, 'A/B': sum_ask_bid_rate, 'Ask': sum_ask_size, 'Cmpr': compare, 'Bid': sum_bid_size})
    
    #stock_test.text_input("output", stock_data)
    #stock_test2.text_input("output", stock_data[0]['종목명'])

    #Dataframe 뿌려주기(초기값)
    stock_df = pd.DataFrame({'Name': st_trade_name, 'Price': st_trade_price, 'Trd': st_up_down, '%': st_signed_change_rate, 'Change': st_signed_change_price, 'Tr. Time': st_trade_time, 'Status': st_trade_time_status})
    stock_df_sorted = stock_df.sort_values(by=['Price'], ascending=False)
    stock_dataframe.dataframe(stock_df_sorted)

#===========Stock END=============

#===========환율 START=============
def exchange_rate():
    address = 'https://finance.naver.com'
    addition = '/marketindex/?tabSel=exchange#tab_section'
    res = requests.get(address + addition)
    soup = bs.BeautifulSoup(res.content, 'html.parser')

    frame = soup.find('iframe', id="frame_ex1")
    frameaddr = address + frame['src']

    res1 = requests.get(frameaddr)
    frame_soup = bs.BeautifulSoup(res1.content, 'html.parser')
    items = frame_soup.select('body > div > table > tbody > tr')

    exchange_rate_array = []
    # 출력하고자 하는 국가 정보를 리스트로 정의
    desired_countries = ["미국 USD", "유럽연합 EUR", "일본 JPY (100엔)", "아랍에미리트 AED"]

    for item in items:
        name = item.select('td')[0].text.replace("\n", "").replace("\t", "")
        if name in desired_countries:
            exchange_rate_array.append(item.select('td')[1].text)
        
    usd_rate.markdown(exchange_rate_array)
            #print(name + "\t" + item.select('td')[1].text)
            #usd_rate.markdown(name + "\t" + item.select('td')[1].text)

#===========환율 END=============
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
        if "Seoul" in str(market_tz):
            kor_market_open_flag = 1
            stock_test.markdown(f"오픈 - {kor_market_open_flag}")
        #else:
        #    stock_test.markdown(market_tz)
        return f"**Closes** : in {str(remaining_time_formatted)}"
        
    elif market_time < market_open_dt:
        remaining_time = market_open_dt - market_time
        remaining_time_formatted = extract_time(remaining_time)
        xx_time_zone.markdown(f"[Closed]")
        if "Seoul" in str(market_tz):
            kor_market_open_flag = 0
            stock_test.markdown(f"닫음1 - {kor_market_open_flag}")
        #else:
        #    stock_test.markdown(market_tz)            
        return f"**Opens** : in {str(remaining_time_formatted)}"
    else:
        next_open_dt = (market_open_dt + datetime.timedelta(days=1)).astimezone(pytz.utc)
        remaining_time = next_open_dt - current_utc
        remaining_time_formatted = extract_time(remaining_time)
        xx_time_zone.markdown(f"[Closed]")
        if "Seoul" in str(market_tz):
            kor_market_open_flag = 0
            stock_test.markdown(f"닫음2 - {kor_market_open_flag}")
        #else:
        #    stock_test.markdown(market_tz)            
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
kor_market_open_flag = 0
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

f_col1, f_col2, f_col3, f_col4 = st.columns(4)
with f_col1:
    usd_rate = st.empty()
with f_col2:
    eur_rate = st.empty()
with f_col3:
    aed_rate = st.empty()
with f_col4:
    jpy_rate = st.empty()

# 코인 전체목록 불러오기
coin_array = []
coin_string = ""
coin_data = []
all_coin_list = []
all_coin_list = get_tickers()

# 주식 관련
stock_data = []

# 초기 코인선택 대상 설정
text_values = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-VET","KRW-STEEM", "KRW-ETC", "KRW-SAND", "KRW-XEC"]
indices = [all_coin_list.index(text) for text in text_values if text in all_coin_list]

tab1, tab2, tab3 = st.tabs(["Main", "Setting1", "Setting2"])
with tab1:
    #st.header("Main")
    #coin_selected = st.empty()
    coin_dataframe = st.empty()
    stock_dataframe = st.empty()
    stock_test = st.empty()
    stock_test2 = st.empty()
with tab2:
    coin_array = sac.transfer(items=all_coin_list, label='label', index=indices, titles=['source', 'target'], reload='reload data', color='dark', search=True, pagination=True, use_container_width=True)
    coin_array_noKRW = [coin.replace('KRW-', '') for coin in coin_array]
    coin_number = len(coin_array)
    coin_string = ','.join(coin_array)    
    
    exchange_rate()
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
    
    stock2_container.markdown(market_status(current_time_utc, us_tz, us_market_open, us_market_close, us_time_zone))
    stock1_container.markdown(market_status(current_time_utc, korean_tz, korean_market_open, korean_market_close, korea_time_zone))

counter = 0
# Call the update_clock function every second
while True:
    update_clock()
    update_coin_data()
    #장오픈중일때만 if 추가
    if counter % 10 == 0 and kor_market_open_flag == 1:
        update_stock_data()
        counter = 0
    time.sleep(1)
    counter += 1
