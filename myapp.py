import streamlit as st
import time

st.title("Live Clock App")

# Create a container for the clock
clock_container = st.empty()

def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_container.markdown(f"**Current Time:** {current_time}")

# Call the update_clock function every second
while True:
    update_clock()
    time.sleep(1)
