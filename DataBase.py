import sqlite3
import os.path

DB_FILE = 'event_planner.db'
def connect_db():
    return sqlite3.connect(DB_FILE)

#checking if database file exists in my project folder
if not os.path.isfile(DB_FILE):
    #executing thi block if the database in my folder does not exist by creating a new one
    conn = sqlite3.connect('event_planner.db') #Connecting to database and creating it, if it is not created
    cursor = conn.cursor()

#creating tables in our database
#creating an event table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events(
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            event_date TEXT,
            event_time TEXT,
            event_location TEXT,
            event_description TEXT
        )
    ''')
    #creating a task table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER,
            event_id INTEGER,
            task_name TEXT,
            task_description TEXT,
            task_due_date TEXT,
            task_status TEXT,
            FOREIGN KEY (event_id) REFERENCES events (event_id)
        )
    ''')
    #creating the guest table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guest(
            guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            guest_name TEXT,
            guest_email TEXT,
            guest_phone TEXT,
            rsvp_status TEXT,
            FOREIGN KEY (event_id) REFERENCES events (event_id)
        )
    ''')
    #creating the budgets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets(
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            category TEXT,
            amount REAL,
            description TEXT,
            FOREIGN KEY (event_id) REFERENCES events (event_id)
        )
    ''')
    #craeting a vendor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendor(
            vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_name TEXT,
            vendor_contact TEXT,
            vendor_email TEXT,
            vendor_type TEXT,
            event_id INTEGER,
            FOREIGN KEY (event_id) REFERENCES events (event_id)
        )
    ''')

    #commiting the changes and close the connection
    conn.commit()
    conn.close()

    print("YAY!😊 Database and tables created successfully!👌 ")

else:
    print("Database already exists.!😊😊")

#Creating the CRUD (Create,Read,Update, and Delete) operations for events table in my database
def create_event(event_name, event_date, event_time, event_location, event_description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO events (event_name, event_date, event_time, event_location,event_description)
    VALUES (?, ?, ?, ?, ?)
    ''', (event_name, event_date, event_time, event_location, event_description))
    conn.commit()
    conn.close()
#This is my function to read from events table
def read_events():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return events
#this is a fuction similar to above function but is used to read a selected event
def read_event(event_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE event_id = ?', (event_id,))
    event = cursor.fetchone()
    conn.close()
    return event
#this is the fuction to update data in the events table
def update_event(event_id, event_name, event_date, event_time, event_location, event_description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE events
    SET event_name = ?, event_date = ?, event_time = ?, event_location = ?, event_description = ?
    WHERE event_id = ?
    ''', (event_name, event_date, event_time, event_location, event_description, event_id))
    conn.commit()
    conn.close()
def delete_event(event_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE event_id = ?', (event_id,))
    conn.commit()
    conn.close()
#this is a function that will be used in creating a vendor
def create_vendor(vendor_name, vendor_contact, vendor_email, vendor_type, event_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO vendors (vendor_name, vendor_contact, vendor_email, vendor_type, event_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (vendor_name, vendor_contact, vendor_email, vendor_type, event_id))
    conn.commit()
    conn.close()
#this is the function that will be used to create a vendor information into our database
def read_vendors(event_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vendors WHERE event_id = ?', (event_id,))
    vendors = cursor.fetchall()
    conn.close()
    return vendors
#this function will be used to update a vendor's  information in our database
def update_vendors(vendor_id, vendor_name, vendor_contact, vendor_email, vendor_type):
    conn = connect_db()
    cursor =  conn.cursor()
    cursor.execute('''
    UPDATE vendors
    SET vendor_name = ?, vendor_contact = ?, vendor_email = ?, vendor_type = ?
    WHERE vendor_id = ?
    ''', (vendor_name, vendor_contact, vendor_email, vendor_type, vendor_id))
    conn.commit()
    conn.close()
def delete_vendor(vendor_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vendors WHERE vendor_id = ?', (vendor_id,))
    conn.commit()
    conn.close()





create_event("Birthday party", "2025-12-25", "15:00", "My House", "A fun day where I was born")
events = read_events()
print(events)