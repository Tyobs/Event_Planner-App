import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
import os.path

#from pywin32_testutil import non_admin_error_codes
#from wx.lib.agw.ultimatelistctrl import wxEVT_COMMAND_LIST_COL_END_DRAG

DB_FILE = 'event_planner.db'
def connect_db():
    return sqlite3.connect(DB_FILE)

#checking if database file exists in my project folder
if not os.path.isfile(DB_FILE):
    #executing this block if the database in my folder does not exist by creating a new one
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
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO events (event_name, event_date, event_time, event_location,event_description)
        VALUES (?, ?, ?, ?, ?)
        ''', (event_name, event_date, event_time, event_location, event_description))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Sorry😒😒, failed to create an event {e}")
        if conn:
            conn.close()
        return None

#This is my function to read from events table
def read_events():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
        conn.close()
        return events
    except sqlite3.Error as e:
        print(f"Unknown Error occurred while reading data😒{e}")
        if conn:
            conn.close()
        return None

#this is a function similar to above function but is used to read a selected event
def read_event(event_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events WHERE event_id = ?', (event_id,))
        event = cursor.fetchone()
        conn.close()
        return event
    except sqlite3.Error as e:
        print(f"Error occurred while retrieving information of {event_id}😒😒 Sorry {e}")
        if conn:
            conn.close()
        return None

#this is the function to update data in the events table
def update_event(event_id, event_name, event_date, event_time, event_location, event_description):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE events
        SET event_name = ?, event_date = ?, event_time = ?, event_location = ?, event_description = ?
        WHERE event_id = ?
        ''', (event_name, event_date, event_time, event_location, event_description, event_id))
        conn.commit()
        conn.close()
    except sqlite3.error as e:
        print(f"Unknown Error has occurred while trying to update the data🤨 {e}")
        if conn:
            conn.close()
        return None
#this function will be used to delete an event
def delete_event(event_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM events WHERE event_id = ?', (event_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while deleting an event😒😒🤨 {e}")
        if conn:
            conn.close()
    return  None


#this is a function that will be used in creating a vendor
def create_vendor(vendor_name, vendor_contact, vendor_email, vendor_type, event_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO vendors (vendor_name, vendor_contact, vendor_email, vendor_type, event_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (vendor_name, vendor_contact, vendor_email, vendor_type, event_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"A vendor hasn't been created, try again later 🤨🤨🤨 {e}")
        if conn:
            conn.close()
    return None

#this is the function that will be used to read vendors vendor information into our database
def read_vendors(event_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendors WHERE event_id = ?', (event_id,))
        vendors = cursor.fetchall()
        conn.close()
        return vendors
    except sqlite3.Error as e:
        print(f"Unknown Error occurred while reading the vendors  from event😒 {e}")
        if conn:
            conn.close()
    return None

#this function will be used to read information of a single vendor
def read_vendor(vendor_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendors WHERE vendor_id = ?', (vendor_id,))
        vendor = cursor.fetchone()
        conn.close()
        return vendor
    except sqlite3.Error as e:
        print(f"Unable to review the vendor with vendor_id: {vendor_id}😒🤣 {e}")
        if conn:
            conn.close()
    return  None

#this function will be used to update a vendor's  information in our database
def update_vendors(vendor_id, vendor_name, vendor_contact, vendor_email, vendor_type):
    try:
        conn = connect_db()
        cursor =  conn.cursor()
        cursor.execute('''
        UPDATE vendors
        SET vendor_name = ?, vendor_contact = ?, vendor_email = ?, vendor_type = ?
        WHERE vendor_id = ?
        ''', (vendor_name, vendor_contact, vendor_email, vendor_type, vendor_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error occurred while trying to update the vendor.👽👽 {e}")
        if conn:
            conn.close()
    return None

#This function will be used in deleting a vendor
def delete_vendor(vendor_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM vendors WHERE vendor_id = ?', (vendor_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error occurred while trying to delete a vendor {e}")
        if conn:
            conn.close()
    return None
# this function will be used to create a budget
def create_budget(event_id, category, amount, description):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO budgets (event_id, category, amount, description)
        VALUES (?, ?, ?, ?)
        ''', (event_id, category, amount, description))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Unknown Error occurred while trying to create a budget😒 {e}")
        if conn:
            conn.close()
    return None

#this one will be used to update the budget
def update_budget(budget_id, category, amount, description):
    try:
        conn =  connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE budgets
        SET category = ?, amount = ?, description = ?
        WHERE budget_id = ?
        ''', (category, amount, description, budget_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An Error occurred while trying to update a budget😒 {e}")
        if conn:
            conn.close()
    return  None

#this one will be used to read a particular budget withing an event with given event_id key
def read_budget(budget_id):
    try:
        conn =  connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM budgets WHERE budget_id = ?', (budget_id,))
        budget = cursor.fetchone()
        conn.close()
        return budget
    except sqlite3.Error as e:
        print(f"An Error occurred while trying to read a budget😒 {e}")
        if conn:
            conn.close()
    return None
#this one will be used to read all budgets from an event
def read_budgets(event_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM budgets WHERE event_id = ?', (event_id,))
        budgets = cursor.fetchall()
        conn.close()
        return budgets
    except sqlite3.Error as e:
        print(f"An Error occurred while reading budgets from an event👽👽 {e}")
        if conn:
            conn.close()
    return None
#this function will be used to delete a particular budget within an event
def delete_budget(budget_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM budgets WHERE budget_id = ?', (budget_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error while trying to delete a budget from the budget table💀💀 {e}")
        if conn:
            conn.close()
    return None

#this function will be used to create a task in a particular event
def create_task(event_id, task_name, task_description, task_due_date, task_status):
    try:
        conn =  connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO tasks (event_id, task_name, task_description, task_due_date, task_status)
        VALUES (?, ?, ?, ?, ?)
        ''', (event_id, task_name, task_description, task_due_date, task_status))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An Error occurred while trying to create a task👽👽 {e}")
        if conn:
            conn.close()
    return None

#this function will be reading a task from a particula event
def read_task(task_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,))
        task = cursor.fetchone()
        conn.close()
        return task
    except sqlite3.Error as e:
        print(f"An Error occurred while trying to read a task from tasks🤣🤣 {e}")
        if conn:
            conn.close()
    return None

#this function will be reading all tasks within an event
def read_tasks(event_id):
    try:
        conn =  connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE event_id = ?', (event_id,))
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    except sqlite3.Error as e:
        print(f"An Error occurred while trying to read all tasks from the event😒😒 {e}")
        if conn:
            conn.close()
    return None

#this function will be used to update a task in an event
def update_task(task_id, task_name, task_description, task_due_date, task_status):
    try:
        conn = connect_db()
        cursor =  conn.cursor()
        cursor.execute('''
        UPDATE tasks
        SET task_name = ?, task_description = ?, task_due_date = ?, task_status =?
        WHERE task_id = ?
        ''', (task_name, task_description, task_due_date, task_status, task_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while trying to update the task🤣🤣 {e}")
        if conn:
            conn.close()
    return  None

#this function will be used to delete a task in an event
def delete_task(task_id):
    try:
        conn =  connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An Error occurred while trying to delete a particular task.❌🚫 {e}")
        if conn:
            conn.close()
    return None

#this function will be used to create a guest in an event
def  create_guest(event_id, guest_name, guest_email, guest_phone, rsvp_status):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO guest (event_id, guest_name, guest_email, guest_phone, rsvp_status)
        VALUES (?, ?, ?, ?, ?)
        ''', (event_id, guest_name, guest_email, guest_phone, rsvp_status))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error while trying to create a guest🚫🚫 {e}")
        if conn:
            conn.close()
    return None

#this function will be used to read all guests in an event
def read_guests(event_id):
    try:
        conn = connect_db()
        cursor = conn. cursor()
        cursor.execute('SELECT * FROM guest WHERE event_id = ?', (event_id,))
        guests = cursor.fetchall()
        conn.close()
        return guests
    except sqlite3.Error as e:
        print(f"Error while trying to read guests from the db🤣🤣🤣 {e}")
        if conn:
            conn.close()
    return None

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

#this one will be used to delete a guest from an event
def delete_guest(guest_id):
    conn =  connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM guest WHERE guest_id = ?', (guest_id,))
    conn.commit()
    conn.close()

#craeting a class that will be used for all GUI operations
class EventPlannerApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Event Planner")

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.create_widgets()
#This function will create special widgets for the whole functionality of the window
    def create_widgets(self):
        self.create_events_tab()
        self.create_tasks_tab()
        self.create_guest_tab()
        self.create_budget_tab()
        self.create_vendor_tab()

#creatin a function for events tab and the other tabs, task, guest, vendor, and budget
    def create_events_tab(self):
        self.events_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.events_frame, text='Events')

        self.events_list = tk.Listbox(self.events_frame, width=50)
        self.events_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # We can keep the listbox bind for potential future debugging or use
        # it as a visual reference.

        ttk.Label(self.events_frame, text="Select Event by ID:").pack(pady=5)
        self.select_event_id_entry = ttk.Entry(self.events_frame, width=10)
        self.select_event_id_entry.pack(pady=5)

        load_events_button = ttk.Button(self.events_frame, text="Load Events", command=self.load_events)
        load_events_button.pack(pady=5, fill=tk.X)

        update_event_button = ttk.Button(self.events_frame, text="Update Event", command=self.open_update_event_by_id)
        update_event_button.pack(pady=5, fill=tk.X)

        delete_event_button = ttk.Button(self.events_frame, text="Delete Event", command=self.delete_event_by_id)
        delete_event_button.pack(pady=5, fill=tk.X)

        create_event_button = ttk.Button(self.events_frame, text="Create New Event", command=self.open_create_event_window)
        create_event_button.pack(pady=5, fill=tk.X)

        self.selected_event_id = None  #To store the ID of the selected event

    def create_tasks_tab(self):
        self.tasks_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tasks_frame, text='Tasks')

        self.tasks_list = tk.Listbox(self.tasks_frame, width=50)
        self.tasks_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(self.tasks_frame, text="Select Task by ID:").pack(pady=5)
        self.select_task_id_entry = ttk.Entry(self.tasks_frame, width=10)
        self.select_task_id_entry.pack(pady=5)

        load_all_tasks_button = ttk.Button(self.tasks_frame, text="Load All Tasks", command=self.load_all_tasks)
        load_all_tasks_button.pack(pady=5, fill=tk.X)

        create_task_button = ttk.Button(self.tasks_frame, text="Add New Task", command=self.open_create_task_window)
        create_task_button.pack(pady=5, fill=tk.X)

        update_task_button = ttk.Button(self.tasks_frame, text="Update Task", command=self.open_update_task_window)
        update_task_button.pack(pady=5, fill=tk.X)

        delete_task_button = ttk.Button(self.tasks_frame, text="Delete Task", command=self.delete_selected_task)
        delete_task_button.pack(pady=5, fill=tk.X)

    def create_guest_tab(self):
        self.guest_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.guest_frame, text="Guests")

        self.guest_list = tk.Listbox(self.guest_frame, width=50)
        self.guest_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        load_guests_button = ttk.Button(self.guest_frame, text="Load Guests")
        load_guests_button.pack(pady=5)

        self.create_guest_button = ttk.Button(self.guest_frame, text="Add new task")
        self.create_guest_button.pack(pady=5)

        self.update_guest_button = ttk.Button(self.guest_frame, text="Update Task")
        self.update_guest_button.pack(pady=5)

        self.delete_guest_button = ttk.Button(self.guest_frame, text="Delete task")
        self.delete_guest_button.pack(pady=5)

    def create_budget_tab(self):
        self.budget_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.budget_frame, text="Budgets")

        self.budget_list = tk.Listbox(self.budget_frame, width=50)
        self.budget_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        load_budgets_button = ttk.Button(self.budget_frame, text="Load Tasks")
        load_budgets_button.pack(pady=5)

        self.create_budget_button = ttk.Button(self.budget_frame, text="Add new task")
        self.create_budget_button.pack(pady=5)

        self.update_budget_button = ttk.Button(self.budget_frame, text="Update Task")
        self.update_budget_button.pack(pady=5)

        self.delete_budget_button = ttk.Button(self.budget_frame, text="Delete task")
        self.delete_budget_button.pack(pady=5)

    def create_vendor_tab(self):
        self.vendor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.vendor_frame, text="Vendors")

        self.vendor_list = tk.Listbox(self.vendor_frame, width=50)
        self.vendor_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        load_vendors_button = ttk.Button(self.vendor_frame, text="Load Tasks")
        load_vendors_button.pack(pady=5)

        self.create_vendor_button = ttk.Button(self.vendor_frame, text="Add new task")
        self.create_vendor_button.pack(pady=5)

        self.update_vendor_button = ttk.Button(self.vendor_frame, text="Update Task")
        self.update_vendor_button.pack(pady=5)

        self.delete_vendor_button = ttk.Button(self.vendor_frame, text="Delete task")
        self.delete_vendor_button.pack(pady=5)

#this function will enable the selection of an existing event in events tab
    def on_event_select(self, event):
        print("on_event_select called")
        selected_index = self.events_list.curselection()
        print(f"Selected index: {selected_index}")
        if selected_index:
            selected_event_text = self.events_list.get(selected_index[0])
            print(f"Selected event text: {selected_event_text}")
            try:
                self.selected_event_id = int(selected_event_text.split('.')[0]) # Extract the event ID
                print(f"Selected event ID: {self.selected_event_id}")
                self.update_event_button.config(state=tk.NORMAL)
                self.delete_event_button.config(state=tk.NORMAL)
            except ValueError:
                self.selected_event_id = None
                self.update_event_button.config(state=tk.DISABLED)
                self.delete_event_button.config(state=tk.DISABLED)
                print("ValueError: Could not extract event ID.")
        else:
            self.selected_event_id = None
            self.update_event_button.config(state=tk.DISABLED)
            self.delete_event_button.config(state=tk.DISABLED)
            print("No event selected.")

#function for leading events to window in the notepad form
    def load_events(self):
        events = read_events()
        self.events_list.delete(0, tk.END)
        if events:
            for event in events:
                self.events_list.insert(tk.END, f"{event[0]}.   {event[1]}  {event[3]}   ({event[2]})    {event[4]}     {event[5]}")
        else:
            messagebox.showinfo("Infor", "No events found.🤣🤣")

#A function that will be triggered when the user hits "create event" button, this is  a window for creating and event
    def open_create_event_window(self):
        self.create_event_window = tk.Toplevel(self.window)
        self.create_event_window.title("Create event")

        tk.Label(self.create_event_window, text="Event Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.event_name_entry = tk.Entry(self.create_event_window, width=40)
        self.event_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.create_event_window, text="Event Date (DD/MM/YYYY):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.event_date_entry = tk.Entry(self.create_event_window, width=40)
        self.event_date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.create_event_window, text="Event Time (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.event_time_entry = Entry(self.create_event_window, width=40)
        self.event_time_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.create_event_window, text="Event Location:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.event_location_entry = Entry(self.create_event_window, width=40)
        self.event_location_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(self.create_event_window, text="Event Description:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.event_description_entry = Text(self.create_event_window, width=30, height=5)
        self.event_description_entry.grid(row=4, column=1, padx=5, pady=5)

        save_button = ttk.Button(self.create_event_window, text="Save Event", command=self.save_new_event)
        save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        cancel_button = ttk.Button(self.create_event_window, text="Cancel", command=self.create_event_window)
        cancel_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

#A function that will be triggered  when the user wants to update an event with the connection of "selected event" function
    def open_update_event_by_id(self):
        try:
            event_id = int(self.select_event_id_entry.get())
            if event_id > 0:
                self.selected_event_id = event_id #this line means we are setting the id
                event = read_event(self.selected_event_id)
                if event:
                    self.update_event_window = tk.Toplevel(self.window)
                    self.update_event_window.title(f"Update Event: {event[1]}")

                    #this will be same as the creating event window but with content prefilled
                    tk.Label(self.update_event_window, text="Event Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                    self.update_event_name_entry = tk.Entry(self.update_event_window, width=40)
                    self.update_event_name_entry.insert(0, event[1])
                    self.update_event_name_entry.grid(row=0, column=1, padx=5, pady=5)
                    tk.Label(self.update_event_window, text="Date (DD/MM/YYYY):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
                    self.update_event_date_entry = tk.Entry(self.update_event_window, width=40)
                    self.update_event_date_entry.insert(0, event[2])
                    self.update_event_date_entry.grid(row=1, column=1, padx=5, pady=5)

                    tk.Label(self.update_event_window, text="Time (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
                    self.update_event_time_entry = tk.Entry(self.update_event_window, width=40)
                    self.update_event_time_entry.insert(0, event[3])
                    self.update_event_time_entry.grid(row=2, column=1, padx=5, pady=5)

                    tk.Label(self.update_event_window, text="Location:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
                    self.update_event_location_entry = tk.Entry(self.update_event_window, width=40)
                    self.update_event_location_entry.insert(0, event[4])
                    self.update_event_location_entry.grid(row=3, column=1, padx=5, pady=5)

                    tk.Label(self.update_event_window, text="Description:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
                    self.update_event_description_entry = tk.Text(self.update_event_window, width=30, height=5)
                    self.update_event_description_entry.insert(tk.END, event[5])
                    self.update_event_description_entry.grid(row=4, column=1, padx=5, pady=5)

                    save_button = ttk.Button(self.update_event_window, text="Save Changes", command=self.save_updated_event)
                    save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

                    cancel_button = ttk.Button(self.update_event_window, text="Cancel", command=self.update_event_window.destroy)
                    cancel_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
                else:
                    messagebox.showerror("Error", f"Could not find event with ID: {event_id}")
            else:
                messagebox.showerror("Error", "Please enter a valid Event ID.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a numeric Event ID.")

#this function will be used to delete an event from the database
    def delete_event_by_id(self):
        try:
            event_id = int(self.select_event_id_entry.get())
            if event_id > 0:
                if messagebox.askyesno("Confirm", f"Are you sure you want to delete event ID {event_id}?"):
                    if delete_event(event_id):
                        messagebox.showinfo("Success", f"Event ID {event_id} deleted successfully!")
                        self.load_events()
                    else:
                        messagebox.showerror("Error", f"Failed to delete event ID {event_id}.")
            else:
                messagebox.showerror("Error", "Please enter a valid Event ID.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a numeric Event ID.")

#this function will be used after clicking the "save" button in event creation window
    def save_new_event(self):
        event_name = self.event_name_entry.get()
        event_date = self.event_date_entry.get()
        event_time = self.event_time_entry.get()
        event_location = self.event_location_entry.get()
        event_description = self.event_description_entry.get("1.0", tk.END).strip()

        if not event_name or not event_date or not event_time or not event_location:
            messagebox.showerror("Blank Input", "An Error⚠️ occurred due to blank fill. Please fill in the entry spaces provided😊.")
            return
        if  create_event(event_name, event_date, event_time, event_location, event_description):
            messagebox.showinfo("Success😊", f"You ave successfully created and event '{event_name}'!😊")
            self.load_events()
            self.create_event_window.destroy()
        else:
            messagebox.showerror("ERROR!", "Oooops! The system has failed to create the task. Please check the details.")

#this function will be used to save the updated event
    def save_updated_event(self):
        if self.selected_event_id:
            event_name = self.update_event_name_entry.get()
            event_date = self.update_event_date_entry.get()
            event_time = self.update_event_time_entry.get()
            event_location = self.update_event_location_entry.get()
            event_description = self.update_event_description_entry.get("1.0", tk.END).strip()

            if not event_name or not event_date or not event_time or not event_location:
                messagebox.showerror("Error", "Please fill in all the required fields.")
                return

            if update_event(self.selected_event_id, event_name, event_date, event_time, event_location, event_description):
                messagebox.showinfo("Success", f"Event '{event_name}' updated successfully!")
                self.load_events()  #this will reload the events list after a succeccful udate
                self.update_event_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to update the event. Please check the details.")
        else:
            messagebox.showinfo("Info", "No event selected to update.")




#this function will open a new window that will be used in creating a new task, this function is under construction
    def open_create_task_window(self):
        self.create_task_window = tk.Toplevel(self.window)
        self.create_task_window.title("Add New Task")

        tk.Label(self.create_task_window, text="Event ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.task_event_id_entry = tk.Entry(self.create_task_window, width=40)
        self.task_event_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.create_task_window, text="Task Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.task_name_entry = tk.Entry(self.create_task_window, width=40)
        self.task_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.create_task_window, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.task_description_entry = tk.Text(self.create_task_window, width=30, height=5)
        self.task_description_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.create_task_window, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.task_due_date_entry = tk.Entry(self.create_task_window, width=40)
        self.task_due_date_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.create_task_window, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.task_status_entry = tk.Entry(self.create_task_window, width=40)
        self.task_status_entry.grid(row=4, column=1, padx=5, pady=5)

        save_task_button = ttk.Button(self.create_task_window, text="Save Task", command=self.save_new_task)
        save_task_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        cancel_task_button = ttk.Button(self.create_task_window, text="Cancel", command=self.create_task_window.destroy)
        cancel_task_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

#this will be used when saving the task into our db
    def save_new_task(self):
        try:
            event_id = int(self.task_event_id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Event ID. Please enter a number.")
            return

        task_name = self.task_name_entry.get()
        task_description = self.task_description_entry.get("1.0", tk.END).strip()
        task_due_date = self.task_due_date_entry.get()
        task_status = self.task_status_entry.get()

        if not task_name or not task_due_date or not task_status:
            messagebox.showerror("Error", "Please fill in all the required fields (Name, Due Date, Status).")
            return

        if create_task(event_id, task_name, task_description, task_due_date, task_status):
            messagebox.showinfo("Success", f"Task '{task_name}' created successfully for Event ID {event_id}!")
            self.load_all_tasks() # Reload the task list
            self.create_task_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to create the task. Please check the details.")

#this function will be used in leading/viewing the tasks if they exist in the notepad
    def load_all_tasks(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT task_id, event_id, task_name FROM tasks')
        tasks = cursor.fetchall()
        conn.close()

        self.tasks_list.delete(0, tk.END)
        if tasks:
            for task in tasks:
                self.tasks_list.insert(tk.END, f"Task ID: {task[0]}, Event ID: {task[1]}, Name: {task[2]}")
        else:
            messagebox.showinfo("Info", "No tasks found.")


#function for deleting a task from our db (under construction)
    def delete_selected_task(self):
        try:
            task_id = int(self.select_task_id_entry.get())
            if task_id > 0:
                if messagebox.askyesno("Confirm", f"Are you sure you want to delete task ID {task_id}?"):
                    if delete_task(task_id):
                        messagebox.showinfo("Success", f"Task ID {task_id} deleted successfully!")
                        self.load_tasks()
                    else:
                        messagebox.showerror("Error", f"Failed to delete task ID {task_id}.")
            else:
                messagebox.showerror("Error", "Please enter a valid Task ID.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a numeric Task ID.")

#function for updating a task in our db (under construction)
    def open_update_task_window(self):
        try:
            task_id = int(self.select_task_id_entry.get())
            if task_id > 0:
                task = read_task(task_id)
                if task:
                    self.update_task_window = tk.Toplevel(self.window)
                    self.update_task_window.title(f"Update Task: {task[2]}")

                    tk.Label(self.update_task_window, text="Event ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                    self.update_task_event_id_entry = tk.Entry(self.update_task_window, width=40)
                    self.update_task_event_id_entry.insert(0, task[1])
                    self.update_task_event_id_entry.grid(row=0, column=1, padx=5, pady=5)

                    tk.Label(self.update_task_window, text="Task Name:").grid(row=1, column=0, padx=5, pady=5,
                                                                              sticky="w")
                    self.update_task_name_entry = tk.Entry(self.update_task_window, width=40)
                    self.update_task_name_entry.insert(0, task[2])
                    self.update_task_name_entry.grid(row=1, column=1, padx=5, pady=5)

                    tk.Label(self.update_task_window, text="Description:").grid(row=2, column=0, padx=5, pady=5,
                                                                                sticky="w")
                    self.update_task_description_entry = tk.Text(self.update_task_window, width=30, height=5)
                    self.update_task_description_entry.insert(tk.END, task[3])
                    self.update_task_description_entry.grid(row=2, column=1, padx=5, pady=5)

                    tk.Label(self.update_task_window, text="Due Date (DD/MM/YYYY):").grid(row=3, column=0, padx=5,
                                                                                          pady=5, sticky="w")
                    self.update_task_due_date_entry = tk.Entry(self.update_task_window, width=40)
                    self.update_task_due_date_entry.insert(0, task[4])
                    self.update_task_due_date_entry.grid(row=3, column=1, padx=5, pady=5)

                    tk.Label(self.update_task_window, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
                    self.update_task_status_entry = tk.Entry(self.update_task_window, width=40)
                    self.update_task_status_entry.insert(0, task[5])
                    self.update_task_status_entry.grid(row=4, column=1, padx=5, pady=5)

                    save_button = ttk.Button(self.update_task_window, text="Save Changes", command=self.save_updated_task)
                    save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

                    cancel_button = ttk.Button(self.update_task_window, text="Cancel",command=self.update_task_window.destroy)
                    cancel_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
                else:
                    messagebox.showerror("Error", f"Could not find task with ID: {task_id}")
            else:
                messagebox.showerror("Error", "Please enter a valid Task ID.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a numeric Task ID.")

    def save_updated_task(self):
        try:
            task_id = int(self.select_task_id_entry.get())
            if task_id > 0:
                event_id = int(self.update_task_event_id_entry.get())
                task_name = self.update_task_name_entry.get()
                task_description = self.update_task_description_entry.get("1.0", tk.END).strip()
                task_due_date = self.update_task_due_date_entry.get()
                task_status = self.update_task_status_entry.get()

                if not task_name or not task_due_date or not task_status:
                    messagebox.showerror("Error", "Please fill in all the required fields (Name, Due Date, Status).")
                    return

                if update_task(task_id, task_name, task_description, task_due_date, task_status):
                    messagebox.showinfo("Success", f"Task '{task_name}' updated successfully!")
                    self.load_all_tasks()
                    self.update_task_window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update the task. Please check the details.")
            else:
                messagebox.showerror("Error", "Please enter a valid Task ID to update.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a numeric Task ID and Event ID.")


if __name__ == "__main__":
    window = tk.Tk()
    app = EventPlannerApp(window)
    window.mainloop()