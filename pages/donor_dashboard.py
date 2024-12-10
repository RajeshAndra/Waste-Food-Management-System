import streamlit as st
from datetime import date
from database import add_donation, generate_donor_report

def donor_dashboard(user):
    st.header("Donor Dashboard")

    # Logout logic
    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out!")
        st.stop()

    # Initialize session state flags
    if "donation_submitted" not in st.session_state:
        st.session_state.donation_submitted = False
    if "report_generated" not in st.session_state:
        st.session_state.report_generated = False

    # Add a new donation section
    st.subheader("Add a New Donation")
    item_name = st.text_input("Food Item Name", key="item_name")
    quantity = st.number_input("Quantity", min_value=1, key="quantity")
    expiry_date = st.date_input("Expiry Date", key="expiry_date")
    location = st.text_input("Location", key="location")

    # Handle Submit Donation
    if st.button("Submit Donation"):
        try:
            # Check for errors
            if not item_name or not location:
                st.error("Please fill in all required fields.")
            elif expiry_date < date.today():
                st.error("Expiry date cannot be in the past.")
            elif quantity <= 0:
                st.error("Quantity must be greater than zero.")
            else:
                add_donation(user, item_name, quantity, expiry_date, location)
                st.session_state.donation_submitted = True
                st.success("Donation added successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")


    # Generate donation report section
    st.subheader("Generate Donation Report")
    if st.button("Generate Report"):
        try:
            report = generate_donor_report(user)
            if report:
                for record in report:
                    st.write(f"Item: {record[0]}, Quantity: {record[1]}, Expiry Date: {record[2]}, Location: {record[4]}, Status: {record[3]},")
            else:
                st.info("No donation report found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
