import streamlit as st
import pandas as pd
import datetime

# Load existing data if available
@st.cache_data
def load_data():
    try:
        return pd.read_csv("boarding_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Phone", "Pickup Point", "Time Slot", "Location URL", "Seats"])

data = load_data()

# Admin authentication
ADMIN_PASSWORD = "admin123"

# Initialize session state for admin login
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "refresh_admin" not in st.session_state:
    st.session_state.refresh_admin = False

# Streamlit UI
st.title("Wedding Bus Boarding Info")

st.write("### Bus Time Table")
st.write("- **Starting Point:** Miyapur")
st.write("- **Ending Point:** Adivelama Function Hall, Malkajgiri")
st.write("- **Start Time:** 7:00 AM")
st.write("- **Estimated Arrival Time:** 9:30 AM")

# Sorting data by time
if not data.empty:
    data["Time Slot"] = pd.to_datetime(data["Time Slot"], errors="coerce").dt.strftime("%H:%M")
    data = data.sort_values(by=["Time Slot"])
    st.write("### Current Boarding Points")
    st.dataframe(data)

# Registration page
def registration_page():
    st.title("Bus Boarding Registration")
    st.write("For new boarding points, contact Shashikanth")

    name = st.text_input("Name")
    phone = st.text_input("Phone Number")

    if data.empty or "Pickup Point" not in data.columns:
        st.warning("No existing pickup points available. Please contact Shashikanth.")
        pickup_point = st.text_input("Enter New Pickup Point")  # Allow manual entry if empty
    else:
        pickup_point = st.radio("Select Pickup Point", data["Pickup Point"].unique())

    location_url = st.text_input("Location URL")
    time_slot = st.time_input("Preferred Pickup Time", value=datetime.time(7, 0), step=300)  # Step = 5 minutes
    seats = st.number_input("Number of Seats Needed", min_value=1, step=1)

    if st.button("Submit"):
        if name and phone and pickup_point and time_slot and location_url and seats:
            new_entry = pd.DataFrame([[name, phone, pickup_point, time_slot.strftime("%H:%M"), location_url, seats]], 
                                     columns=["Name", "Phone", "Pickup Point", "Time Slot", "Location URL", "Seats"])
            updated_data = pd.concat([data, new_entry], ignore_index=True)
            updated_data.to_csv("boarding_data.csv", index=False)
            st.success("Your response has been recorded! Thank you.")
            st.session_state.refresh_admin = True  # Set flag to refresh
            st.rerun()  # <-- Updated from experimental_rerun to rerun
        else:
            st.error("Please fill in all fields.")

# Admin page
def admin_page():
    st.title("Admin Access")

    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.session_state.refresh_admin = True  # Trigger refresh
                st.rerun()  # <-- Updated from experimental_rerun to rerun
            else:
                st.error("Incorrect Password")
    else:
        st.success("Access Granted. You can edit boarding points.")

        # Editable data table
        edited_data = st.data_editor(data, use_container_width=True, num_rows="dynamic")

        # Save changes when admin clicks button
        if st.button("Save Changes"):
            edited_data.to_csv("boarding_data.csv", index=False)
            st.success("Boarding data updated successfully!")
            st.session_state.refresh_admin = True  # Trigger refresh
            st.rerun()  # <-- Updated from experimental_rerun to rerun

        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.session_state.refresh_admin = True  # Trigger refresh
            st.rerun()  # <-- Updated from experimental_rerun to rerun

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
    if not data.empty:
        st.dataframe(data)  # Display sorted pickup data
    else:
        st.warning("No boarding points available yet.")

elif page == "Registration":
    registration_page(data)

elif page == "Admin":
    admin_page()