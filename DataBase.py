import sqlite3
conn = sqlite3.connect('event_planner.db') #Connecting to database and creating it, if it is not created
cursor = conn.cursor()

#creating tables in our database
#creating an event table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS events(
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT,
        event_date TEXT,
        even_time TEXT,
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