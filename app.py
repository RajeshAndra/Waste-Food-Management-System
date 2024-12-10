import streamlit as st
from database import create_user, authenticate_user, check_user_role, is_username_unique
from pages.donor_dashboard import donor_dashboard
from pages.recipient_dashboard import recipient_dashboard
from pages.admin_dashboard import admin_dashboard

def main():
    st.title("Food Waste Management System (FMS)")

    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = None

    menu = ["Home", "Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the Food Waste Management System!")
        st.write("Please login or register to continue.")

    elif choice == "Login":
        st.subheader("Login")

        if st.session_state.user and st.session_state.role:
            st.success(f"Welcome back, {st.session_state.user}!")
            load_dashboard()
        else:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = username
                    st.session_state.role = check_user_role(username)
                    st.success(f"Welcome, {username}!")
                    load_dashboard()
                else:
                    st.error("Incorrect Username or Password.")

    elif choice == "Register":
        st.subheader("Create a New Account")

        
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Donor", "Recipient", "Admin"])

        if st.button("Register"):
            
            if not new_username or not new_password:
                st.error("Please fill all the fields.")
            
            elif not is_username_unique(new_username):
                st.error("This username is already taken. Please choose a different one.")
            else:
                create_user(new_username, new_password, role)
                st.success(f"Account created successfully for {role}!")
                st.info("Please go to the Login menu to access your account.")


def load_dashboard():
    if st.session_state.role == "Donor":
        donor_dashboard(st.session_state.user)
    elif st.session_state.role == "Recipient":
        recipient_dashboard(st.session_state.user)
    elif st.session_state.role == "Admin":
        admin_dashboard()


if __name__ == "__main__":
    main()
