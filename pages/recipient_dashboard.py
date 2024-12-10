import streamlit as st
from database import view_available_food, request_food, view_request_history, update_food_quantity
def recipient_dashboard(user):
    st.header("Recipient Dashboard")

    # Logout logic
    if st.button("Logout"):
        st.session_state.clear()
        st.success("You have been logged out!")
        st.stop()

    # Display available food items
    st.subheader("Available Food Items")
    food_items = view_available_food()

    if food_items:
        for item in food_items:
            st.write(f"Item: {item[1]}, Quantity: {item[2]}, Expiry Date: {item[3]}, Location: {item[4]}")

            # Quantity input and validation
            try:
                quantity_requested = st.number_input(
                    f"Quantity to request for {item[1]}",
                    min_value=1,
                    max_value=item[2],
                    key=f"quantity_{item[0]}"
                )

                if st.button(f"Request {item[1]}", key=f"request_{item[0]}"):
                    if quantity_requested > item[2]:
                        st.error(f"Requested quantity exceeds available stock for {item[1]}.")
                    elif quantity_requested <= 0:
                        st.error("Quantity must be greater than zero.")
                    else:
                        request_food(user, item[0], quantity_requested)
                        st.success(f"Requested {quantity_requested} of {item[1]}")

                        # Update availability
                        updated_quantity = item[2] - quantity_requested
                        update_food_quantity(item[0], updated_quantity)

                        # Notify about item removal if quantity is zero
                        if updated_quantity == 0:
                            st.warning(f"{item[1]} is no longer available and has been removed from the list.")

                        st.rerun()  # Refresh page to reflect changes
            except Exception as e:
                st.error(f"An error occurred while requesting food: {e}")
    else:
        st.info("No food items available at the moment.")

    # Button to display user report
    if st.button("View User Report"):
        show_user_request_report(user)  # Function to display detailed report

# Function to show the detailed user request report (separate view)
def show_user_request_report(user_id):
    st.subheader("User's Detailed Request Report")
    try:
        requests = view_request_history(user_id)
        if requests:
            for request in requests:
                st.write(f"Item: {request[0]}, Quantity: {request[1]}, Expiry Date: {request[2]}")
        else:
            st.info("No requests found for this user.")
    except Exception as e:
        st.error(f"An error occurred while retrieving user report: {e}")
