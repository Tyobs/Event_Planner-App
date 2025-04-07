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

#Creating the CRUD (Create,Read,Update, and Delete) operations for events, tasks, guests, budgets, and vendors tables

#this function will be used to create an event
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

#this function will be used to delete an event
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

#this is the function that will be used to read vendors vendor information into our database
def read_vendors(event_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vendors WHERE event_id = ?', (event_id,))
    vendors = cursor.fetchall()
    conn.close()
    return vendors

#this function will be used to read informationn of a single vendor
def read_vendor(vendor_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vendors WHERE vendor_id = ?', (vendor_id,))
    vendor = cursor.fetchone()
    conn.close()
    return vendor

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

#This function will be used in deleting a vendor
def delete_vendor(vendor_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vendors WHERE vendor_id = ?', (vendor_id,))
    conn.commit()
    conn.close()

# this functunction will be used to create a budget
def create_budget(event_id, category, amount, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO budgets (event_id, category, amount, description)
    VALUES (?, ?, ?, ?)
    ''', (event_id, category, amount, description))
    conn.commit()
    conn.close()

#this one will be used to update the budget
def update_budget(budget_id, category, amount, description):
    conn =  connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE budgets
    SET category = ?, amount = ?, description = ?
    WHERE budget_id = ?
    ''', (category, amount, description, budget_id))
    conn.commit()
    conn.close()

#this one will be used to read a particular nudget withing an event with given event_id key
def read_budget(budget_id):
    conn =  connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM budgets WHERE budget_id = ?', (budget_id,))
    budget = cursor.fetchone()
    conn.close()
    return budget

#this one will be used to read all budgets from an event
def read_budgets(event_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM budgets WHERE event_id = ?', (event_id,))
    budgets = cursor.fetchall()
    conn.close()
    return budgets

#this function will be used to delete a particular budget within an event
def delete_budget(budget_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM budgets WHERE budget_id = ?', (budget_id,))
    conn.commit()
    conn.close()

#this function will be used to create a task in a particular event
def create_task(event_id, task_name, task_description, task_due_date, task_status):
    conn =  connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tasks (event_id, task_name, task_description, task_due_date, task_status)
    VALUES (?, ?, ?, ?, ?)
    ''', (event_id, task_name, task_description, task_due_date, task_status))
    conn.commit()
    conn.close()

#this function will be reading a task from a particula event
def read_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

#this function will be readining all tasks within an event
def read_tasks(event_id):
    conn =  connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE event_id = ?', (event_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

#this function will be used to update a task in an event
def update_task(task_id, task_name, task_description, task_due_date, task_status):
    conn = connect_db()
    cursor =  conn.cursor()
    cursor.execute('''
    UPDATE tasks
    SET task_name = ?, task_description = ?, task_due_date = ?, task_status =?
    WHERE task_id = ?
    ''', (task_name, task_description, task_due_date, task_status, task_id))
    conn.commit()
    conn.close()

#this function will be used to delete a task in an event
def delete_task(task_id):
    conn=  connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
    conn.commit()
    conn.close()

#this function will be used to create a guest in an event
def  create_guest(event_id, guest_name, guest_email, guest_phone, rsvp_status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO guest (event_id, guest_name, guest_email, guest_phone, rsvp_status)
    VALUES (?, ?, ?, ?, ?)
    ''', (event_id, guest_name, guest_email, guest_phone, rsvp_status))
    conn.commit()
    conn.close()

#this function will be used to read all guests in an event
def read_guests(event_id):
    conn = connect_db()
    cursor = conn. cursor()
    cursor.execute('SELECT * FROM guest WHERE event_id = ?', (event_id,))
    guests = cursor.fetchall()
    conn.close()
    return guests

#thiss function will be used to read only one guest with a given key value as guest_id
def read_guest(guest_id):
    conn = connect_db()
    cursor =  conn.cursor()
    cursor.execute('SELECT * FROM guest WHERE guest_id = ?', (guest_id,))
    guest = cursor.fetchone()
    conn.close()
    return guest

#this function will be used in updating a guest
def update_guest(guest_id, guest_name, guest_email, guest_phone, rsvp_status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE guest
    SET guest_name = ?, guest_email = ?, guest_phone = ?, rsvp_status = ?
    WHERE guest_id = ?
    ''', (guest_name, guest_email, guest_phone, rsvp_status, guest_id))
    conn.commit()
    conn.close()

#this one will be wused to dete a guest from an event
def delete_guest(guest_id):
    conn =  connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM guest WHERE guest_id = ?', (guest_id,))
    conn.commit()
    conn.close()
