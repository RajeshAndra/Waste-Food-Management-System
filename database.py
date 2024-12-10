import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def init_db():
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiry_date TEXT NOT NULL,
            location TEXT,
            status TEXT DEFAULT 'Available',
            FOREIGN KEY(donor_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER,
            item_name TEXT NOT NULL,
            original_quantity INTEGER NOT NULL,
            expiry_date TEXT NOT NULL,
            location TEXT,
            FOREIGN KEY(donor_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_id INTEGER,
            item_id INTEGER,
            quantity INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(recipient_id) REFERENCES users(id),
            FOREIGN KEY(item_id) REFERENCES donations(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, password, role):
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()
    
    try:
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed_password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        stored_password = result[0]
        return check_password_hash(stored_password, password)
    return False


def check_user_role(username):
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0]
    return None

def is_username_unique(username):
    
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0


def view_donation_history(donor_id):
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT item_name, quantity, expiry_date, status FROM donations WHERE donor_id = ?", (donor_id,))
    history = cursor.fetchall()
    
    conn.close()
    
    return history

def add_donation(donor_id, item_name, quantity, expiry_date, location):
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO donations (donor_id, item_name, quantity, expiry_date, location)
        VALUES (?, ?, ?, ?, ?)
    ''', (donor_id, item_name, quantity, expiry_date, location))

    cursor.execute('''
        INSERT INTO donations_history (donor_id, item_name, original_quantity, expiry_date, location)
        VALUES (?, ?, ?, ?, ?)
    ''', (donor_id, item_name, quantity, expiry_date, location))

    conn.commit()
    conn.close()


def generate_donor_report(donor_id):
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT item_name, quantity, expiry_date, status, location 
        FROM donations 
        WHERE donor_id = ?
    ''', (donor_id,))
    
    report = cursor.fetchall()
    conn.close()
    return report

def update_food_quantity(food_id, new_quantity):

    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()

    if new_quantity > 0:
        cursor.execute("UPDATE donations SET quantity = ? WHERE id = ?", (new_quantity, food_id))
    else:
        cursor.execute("DELETE FROM donations WHERE id = ?", (food_id,))

    conn.commit()
    conn.close()

def get_food_item_by_id(food_item_id):
    try:
        conn = sqlite3.connect("fms.db")
        cursor = conn.cursor()
        query = "SELECT id, name FROM food_items WHERE id = %s"
        cursor.execute(query, (food_item_id,))
        result = cursor.fetchone()

        if result:
            
            return {"id": result[0], "name": result[1]}
        else:
            return None
    except Exception as e:
        print(f"Error in fetching food item by ID: {e}")
        return None


def get_user_request_summary(user_id):
    try:
        conn = sqlite3.connect("fms.db")
        cursor = conn.cursor()
        query = "SELECT food_item_id, SUM(quantity) AS total_requested FROM food_requests WHERE user_id = %s AND status = 'Accepted' GROUP BY food_item_id"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        request_summary = {}
        for row in result:
            
            food_item = get_food_item_by_id(row[0])
            if food_item:  
                request_summary[food_item['name']] = row[1]  

        return request_summary
    except Exception as e:
        print(f"Error in fetching request summary: {e}")
        return {}

def view_available_food():
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()

    
    cursor.execute("SELECT id, item_name, quantity, expiry_date, location FROM donations WHERE status = 'Available'")
    available_food = cursor.fetchall()

    conn.close()

    return available_food



def request_food(recipient_id, item_id, quantity_requested):
    
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()

    try:
        
        cursor.execute("SELECT quantity FROM donations WHERE id = ?", (item_id,))
        available_quantity = cursor.fetchone()

        if not available_quantity:
            print("Error: Food item not found.")
            return "Item not found."
        
        available_quantity = available_quantity[0]

        if available_quantity < quantity_requested:
            return "Not enough quantity available."

        
        new_quantity = available_quantity - quantity_requested
        if new_quantity == 0:
            cursor.execute("UPDATE donations SET status = 'Unavailable', quantity = 0 WHERE id = ?", (item_id,))
        else:
            cursor.execute("UPDATE donations SET quantity = ? WHERE id = ?", (new_quantity, item_id))

        
        cursor.execute("INSERT INTO requests (recipient_id, item_id, quantity, status) VALUES (?, ?, ?, 'Accepted')",
                       (recipient_id, item_id, quantity_requested))
        conn.commit()
        return "Request successful."
    except Exception as e:
        print(f"Error in requesting food: {e}")
        return "Error occurred."
    finally:
        conn.close()


def view_request_history(recipient_id):
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT donations.item_name, requests.quantity, donations.expiry_date, requests.status 
        FROM requests
        JOIN donations ON requests.item_id = donations.id
        WHERE requests.recipient_id = ?
    ''', (recipient_id,))
    
    history = cursor.fetchall()
    conn.close()
    return history

def view_donation_history(donor_id):
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT item_name, quantity, expiry_date, status 
        FROM donations
        WHERE donor_id = ?
    ''', (donor_id,))
    
    history = cursor.fetchall()
    conn.close()
    return history



def get_donation_report():
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT username, item_name, quantity, expiry_date, location, status FROM donations JOIN users ON donations.donor_id = users.id")
    donation_report = cursor.fetchall()
    
    conn.close()
    
    return donation_report

def get_consumer_report():
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT username, item_name, quantity, status FROM requests JOIN users ON requests.recipient_id = users.id JOIN donations ON requests.item_id = donations.id")
    consumer_report = cursor.fetchall()
    
    conn.close()
    
    return consumer_report

def view_donations_report():
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * from donations_history;
    ''')

    actual_donations_report = cursor.fetchall()
    conn.close()
    
    return actual_donations_report


def view_request_report():
    conn = sqlite3.connect("fms.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM requests
        JOIN donations ON requests.item_id = donations.id
    ''')

    requests_report = cursor.fetchall()
    conn.close()
    
    return requests_report

init_db()
