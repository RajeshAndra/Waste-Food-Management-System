# Waste Food Management System

The **Waste Food Management System** is a web-based platform designed to help manage the donation and distribution of surplus food. The system involves three primary roles: **Donor**, **Recipient**, and **Admin**. The Donors can donate food, the Recipients can request food, and the Admin can manage the entire process, including generating reports.

---

## Features

- **Donor Role**:
  - Register and login as a donor.
  - Donate available food to recipients.
  - View previously donated food.

- **Recipient Role**:
  - Register and login as a recipient.
  - Browse available donated food.
  - Request donated food.

- **Admin Role**:
  - Administer all operations.
  - Generate reports on donations and requests.
  - Manage donor and recipient accounts.

- **Authentication**:
  - User registration and login based on role (Donor, Recipient, Admin).
  
---

## Installation

### Clone the Repository
```bash
git clone https://github.com/RajeshAndra/Waste-Food-Management-System.git
cd Waste-Food-Management-System
```

### Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### Configure Database
The system uses **SQLite** as the database for storing user data, food donation details, and requests. The database is automatically created when the system runs.

---

## Usage

1. **Start the Application**:
   You can run the website locally by using Streamlit:
   ```bash
   streamlit run app.py
   ```

2. **Role-based Access**:
   - **Donors**: Can donate food and view previous donations.
   - **Recipients**: Can browse donated food and place requests.
   - **Admin**: Can manage users, generate reports, and view all donations and requests.

---

## Key Files

- `app.py`: The main file to run the web application using Streamlit.
- `requirements.txt`: A list of dependencies required to run the project.
- `models.py`: Contains database models for managing users, food donations, and requests.
- `templates/`: Contains the HTML templates for the user interface.

---

## Example Usage

### Donor:
- Donors can log in and donate food by filling out the form with the food details (quantity, type, etc.).
- Donors can also view a history of their donated food.

### Recipient:
- Recipients can log in and browse available donated food.
- Recipients can request food based on availability.

### Admin:
- Admins can generate reports that summarize all food donations and requests.
- Admins can manage both donor and recipient accounts and approve or reject donation requests.

---

