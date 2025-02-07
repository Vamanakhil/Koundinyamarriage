import streamlit as st
import pandas as pd
import datetime

# Load existing data if available
def load_data():
    try:
        return pd.read_csv("boarding_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Phone", "Pickup Point", "Time Slot"])

data = load_data()

# Streamlit UI
st.title("Koundinya Wedding Bus Boarding Registration")
st.write("Please enter your details to help plan the bus route.")

st.write("### Bus Route Information")
st.write("- **Starting Point:** Miyapur")
st.write("- **Ending Point:** Adivelama Function Hall, Malkajgiri")
st.write("- **Start Time:** 7:00 AM")
st.write("- **Estimated Arrival Time:** 9:30 AM")

name = st.text_input("Name")
phone = st.text_input("Phone Number")
pickup_point = st.text_input("Custom Pickup Point (Enter Address or Landmark)")

# Time input with constraints
def time_within_range(selected_time):
    return datetime.time(6, 30) <= selected_time <= datetime.time(9, 30)

time_slot = st.time_input("Preferred Pickup Time", value=datetime.time(7, 0))
if not time_within_range(time_slot):
    st.error("Please select a time between 6:30 AM and 9:30 AM.")

if st.button("Submit"):
    if name and phone and pickup_point and time_within_range(time_slot):
        new_entry = pd.DataFrame([[name, phone, pickup_point, time_slot]], columns=["Name", "Phone", "Pickup Point", "Time Slot"])
        data = pd.concat([data, new_entry], ignore_index=True)
        data.to_csv("boarding_data.csv", index=False)
        st.success("Your response has been recorded! Thank you.")
    else:
        st.error("Please fill in all fields and select a valid time.")

st.write("### Current Responses")
st.dataframe(data)
