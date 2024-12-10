import streamlit as st
from database import view_donations_report, view_request_report, view_available_food

def admin_dashboard():
    st.header("Admin Dashboard")

    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out!")
        st.stop()

    # Donations Report
    st.subheader("Donations Report")
    donations = view_donations_report()
    if donations:
        for donation in donations:
            st.write(f"Donor: {donation[1]}, Item: {donation[2]}, Quantity: {donation[3]}, Date: {donation[4]}, Location: {donation[5]}")
    else:
        st.info("No donations available.")

    # Requests Report
    st.subheader("Requests Report")
    requests = view_request_report()
    if requests:
        for request in requests:
            st.write(f"Donor: {request[6]}, Recipient: {request[1]}, Item: {request[7]}, Quantity: {request[3]}")
    else:
        st.info("No requests available.")

    # Available Food Inventory
    st.subheader("Available Food Inventory")
    inventory = view_available_food()
    if inventory:
        for item in inventory:
            st.write(f"Item: {item[1]}, Quantity: {item[2]}, Expiry Date: {item[3]}, Location: {item[4]}")
    else:
        st.info("No food items in stock.")
