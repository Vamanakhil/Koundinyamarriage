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
st.title("🚌 Koundinya's Wedding Bus Boarding Info 💑🎉")

# Navigation
page = st.sidebar.selectbox("📌 Choose a Page", ["🕒 Time Table", "📝 Registration", "🔑 Admin"])

# 🕒 Time Table Page
if page == "🕒 Time Table":
    st.title("🕒 Bus Time Table")
    st.write("- **🚏 Starting Point:** Miyapur")
    st.write("- **🏛️ Ending Point:** Adivelama Function Hall, Malkajgiri")
    st.write("- **⏰ Start Time:** 7:00 AM")
    st.write("- **🕤 Estimated Arrival Time:** 9:30 AM")

    if not data.empty:
        st.dataframe(data[["Pickup Point", "Location URL", "Time Slot"]])
    else:
        st.warning("⚠️ No boarding points available yet.")

# 📝 Registration Page
elif page == "📝 Registration":
    st.title("📝 Bus Boarding Registration")
    st.write("📢 For new boarding points, contact **Shashikanth**")

    name = st.text_input("👤 Name")
    phone = st.text_input("📞 Phone Number")

    if data.empty or "Pickup Point" not in data.columns:
        st.warning("⚠️ No existing pickup points available.")
        pickup_point = st.text_input("Enter New Pickup Point")  
    else:
        pickup_point = st.radio("🚏 Select Pickup Point", data["Pickup Point"].unique())

    location_url = st.text_input("📍 Location URL")
    time_slot = st.time_input("⏰ Preferred Pickup Time", value=datetime.time(7, 0), step=300)
    seats = st.number_input("💺 Number of Seats Needed", min_value=1, step=1)

    if st.button("✅ Submit"):
        if name and phone and pickup_point and time_slot and location_url and seats:
            new_entry = pd.DataFrame([[pickup_point, location_url, time_slot.strftime("%H:%M"), name, phone, seats]],
                                     columns=["Pickup Point", "Location URL", "Time Slot", "Name", "Phone", "Seats"])
            updated_data = pd.concat([data, new_entry], ignore_index=True)
            save_data(updated_data)
            st.success("✅ Your response has been recorded! Thank you.")
            st.rerun()  
        else:
            st.error("⚠️ Please fill in all fields.")

# 🔑 Admin Page
elif page == "🔑 Admin":
    st.title("🔑 Admin Access")

    if not st.session_state.admin_authenticated:
        password = st.text_input("🔒 Enter Admin Password", type="password")
        if st.button("🔓 Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect Password")
    else:
        st.success("✅ Access Granted. You can edit boarding points.")

        # Editable data table
        edited_data = st.data_editor(data, use_container_width=True, num_rows="dynamic")

        # Section to add a new Pickup Point
        with st.expander("➕ Add New Pickup Point"):
            new_pickup = st.text_input("🚏 New Pickup Point Name")
            new_url = st.text_input("📍 Location URL")
            new_time = st.time_input("⏰ Pickup Time", value=datetime.time(7, 0))

            if st.button("✅ Add Pickup Point"):
                if new_pickup and new_url and new_time:
                    new_entry = pd.DataFrame([[new_pickup, new_url, new_time.strftime("%H:%M"), "", "", ""]],
                                             columns=["Pickup Point", "Location URL", "Time Slot", "Name", "Phone", "Seats"])
                    edited_data = pd.concat([edited_data, new_entry], ignore_index=True)
                    save_data(edited_data)
                    st.success("✅ Pickup Point Added Successfully!")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill all fields!")

        # Save Admin Edits
        if st.button("💾 Save Changes"):
            save_data(edited_data)
            st.success("✅ Boarding data updated successfully!")
            st.rerun()

        if st.button("🚪 Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()