import streamlit as st
import pandas as pd
import datetime

# Load existing data if available
def load_data():
    try:
        return pd.read_csv("boarding_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Phone", "Pickup Point", "Time Slot", "Location URL", "Seats"])

data = load_data()

# Admin authentication
ADMIN_PASSWORD = "admin123"

# Streamlit UI
st.title("Wedding Bus Boarding Info")

st.write("### Bus Time Table")
st.write("- **Starting Point:** Miyapur")
st.write("- **Ending Point:** Adivelama Function Hall, Malkajgiri")
st.write("- **Start Time:** 7:00 AM")
st.write("- **Estimated Arrival Time:** 9:30 AM")

# Sorting data by time
data = data.sort_values(by=["Time Slot"])
st.write("### Current Boarding Points")
st.dataframe(data)

# Registration page
def registration_page():
    st.title("Bus Boarding Registration")
    st.write("For new boarding points, contact Shashikanth")

    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    pickup_point = st.radio("Select Pickup Point", data["Pickup Point"].unique(), index=0)
    location_url = st.text_input("Location URL")
    time_slot = st.time_input("Preferred Pickup Time", value=datetime.time(7, 0))
    seats = st.number_input("Number of Seats Needed", min_value=1, step=1)
    
    if st.button("Submit"):
        if name and phone and pickup_point and time_slot and location_url and seats:
            new_entry = pd.DataFrame([[name, phone, pickup_point, time_slot, location_url, seats]], 
                                     columns=["Name", "Phone", "Pickup Point", "Time Slot", "Location URL", "Seats"])
            data = pd.concat([data, new_entry], ignore_index=True)
            data.to_csv("boarding_data.csv", index=False)
            st.success("Your response has been recorded! Thank you.")
        else:
            st.error("Please fill in all fields.")

# Admin page
def admin_page():
    st.title("Admin Access")
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.success("Access Granted. You can edit boarding points.")
            st.data_editor(data, use_container_width=True)
            data.to_csv("boarding_data.csv", index=False)
        else:
            st.error("Incorrect Password")

# Navigation
page = st.sidebar.selectbox("Choose a Page", ["Time Table", "Registration", "Admin"])

if page == "Time Table":
    st.title("Bus Time Table")
    st.write("### Bus Route Information")
    st.write("- **Starting Point:** Miyapur")
    st.write("- **Ending Point:** Adivelama Function Hall, Malkajgiri")
    st.write("- **Start Time:** 7:00 AM")
    st.write("- **Estimated Arrival Time:** 9:30 AM")
    st.write("### Current Boarding Points")
    st.dataframe(data)  # Display the sorted pickup data

elif page == "Registration":
    registration_page()

elif page == "Admin":
    admin_page()