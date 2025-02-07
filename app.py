import streamlit as st
import pandas as pd
import datetime

# Function to load data
def load_data():
    try:
        return pd.read_csv("boarding_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Pickup Point", "Location URL", "Time Slot", "Name", "Phone", "Seats"])

# Function to save data
def save_data(data):
    data.to_csv("boarding_data.csv", index=False)

# Load existing data
data = load_data()

# Admin authentication
ADMIN_PASSWORD = "allwin@1122"

# Initialize session state for admin login
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

# Streamlit UI
st.title("Koundinya's Wedding Bus Boarding Info")



# Sorting data by time (if available)
#if not data.empty and "Time Slot" in data.columns:
  #  data["Time Slot"] = pd.to_datetime(data["Time Slot"], errors="coerce").dt.strftime("%H:%M")
  #  data = data.sort_values(by=["Time Slot"])
  #  st.write("### Current Boarding Points")
   # st.dataframe(data[["Pickup Point", "Location URL", "Time Slot"]])  # Show only relevant columns

# Registration Page
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
    time_slot = st.time_input("Preferred Pickup Time", value=datetime.time(7, 0), step=300)  # 5 min step
    seats = st.number_input("Number of Seats Needed", min_value=1, step=1)

    if st.button("Submit"):
        if name and phone and pickup_point and time_slot and location_url and seats:
            new_entry = pd.DataFrame([[pickup_point, location_url, time_slot.strftime("%H:%M"), name, phone, seats]],
                                     columns=["Pickup Point", "Location URL", "Time Slot", "Name", "Phone", "Seats"])
            updated_data = pd.concat([data, new_entry], ignore_index=True)
            save_data(updated_data)  # Save to CSV
            st.success("Your response has been recorded! Thank you.")
            st.rerun()  # Refresh page to reflect updates
        else:
            st.error("Please fill in all fields.")

# Admin Page
def admin_page():
    st.title("Admin Access")

    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()  # Refresh page after login
            else:
                st.error("Incorrect Password")
    else:
        st.success("Access Granted. You can edit boarding points.")

        # Editable data table
        edited_data = st.data_editor(data, use_container_width=True, num_rows="dynamic")

        if st.button("Save Changes"):
            save_data(edited_data)  # Save changes to CSV
            st.success("Boarding data updated successfully!")
            st.rerun()  # Refresh page to reflect updates

        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()  # Refresh page after logout

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
        st.dataframe(data[["Pickup Point", "Location URL", "Time Slot"]])  # Show sorted pickup points
    else:
        st.warning("No boarding points available yet.")

elif page == "Registration":
    registration_page()

elif page == "Admin":
    admin_page()