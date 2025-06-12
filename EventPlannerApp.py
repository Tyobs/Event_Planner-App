import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import hashlib
from tkcalendar import DateEntry
import sv_ttk

DB_FILE = 'event_planner.db'


# --- 1. ARCHITECTURE: THE DATABASE MANAGER ---
class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        if not os.path.isfile(self.db_file):
            print("Database not found. Creating a new one...")
            self.initialize_database()

    def connect(self):
        conn = sqlite3.connect(self.db_file)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def initialize_database(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)''')
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS events(event_id INTEGER PRIMARY KEY, event_name TEXT NOT NULL, event_date TEXT NOT NULL, event_time TEXT, event_location TEXT, event_description TEXT)''')
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS tasks (task_id INTEGER PRIMARY KEY, event_id INTEGER, task_name TEXT NOT NULL, task_description TEXT, task_due_date TEXT NOT NULL, task_status TEXT, FOREIGN KEY (event_id) REFERENCES events (event_id) ON DELETE CASCADE)''')
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS guest(guest_id INTEGER PRIMARY KEY, event_id INTEGER, guest_name TEXT NOT NULL, guest_email TEXT, guest_phone TEXT, rsvp_status TEXT, FOREIGN KEY (event_id) REFERENCES events (event_id) ON DELETE CASCADE)''')
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS budgets(budget_id INTEGER PRIMARY KEY, event_id INTEGER, category TEXT NOT NULL, amount REAL NOT NULL, description TEXT, FOREIGN KEY (event_id) REFERENCES events (event_id) ON DELETE CASCADE)''')
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS vendor(vendor_id INTEGER PRIMARY KEY, event_id INTEGER, vendor_name TEXT NOT NULL, vendor_contact TEXT, vendor_email TEXT, vendor_type TEXT, FOREIGN KEY (event_id) REFERENCES events (event_id) ON DELETE CASCADE)''')
            conn.commit()
            print("Database and tables created successfully!")

    def execute_query(self, query, params=(), fetch=None):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                if fetch == 'one': return cursor.fetchone()
                if fetch == 'all': return cursor.fetchall()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            return None

    def get_all(self, table, order_by=None):
        query = f"SELECT * FROM {table}"
        if order_by:
            query += f" ORDER BY {order_by}"
        return self.execute_query(query, fetch='all')

    def get_one(self, table, id_col, item_id):
        return self.execute_query(f"SELECT * FROM {table} WHERE {id_col} = ?", (item_id,), fetch='one')

    def delete_one(self, table, id_col, item_id):
        return self.execute_query(f"DELETE FROM {table} WHERE {id_col} = ?", (item_id,))

    # User Methods
    def add_user(self, u, h):
        return self.execute_query("INSERT INTO users (username, password_hash) VALUES (?, ?)", (u, h))

    def get_user_hash(self, u):
        res = self.execute_query("SELECT password_hash FROM users WHERE username = ?", (u,), fetch='one')
        return res[0] if res else None

    # Custom Add/Update Methods
    def add_event(self, n, d, t, l, de):
        return self.execute_query(
            "INSERT INTO events (event_name, event_date, event_time, event_location, event_description) VALUES (?, ?, ?, ?, ?)",
            (n, d, t, l, de))

    def update_event(self, eid, n, d, t, l, de):
        return self.execute_query(
            "UPDATE events SET event_name=?, event_date=?, event_time=?, event_location=?, event_description=? WHERE event_id=?",
            (n, d, t, l, de, eid))

    def add_task(self, eid, n, de, dd, s):
        return self.execute_query(
            "INSERT INTO tasks (event_id, task_name, task_description, task_due_date, task_status) VALUES (?, ?, ?, ?, ?)",
            (eid, n, de, dd, s))

    def update_task(self, tid, n, de, dd, s):
        return self.execute_query(
            "UPDATE tasks SET task_name=?, task_description=?, task_due_date=?, task_status=? WHERE task_id=?",
            (n, de, dd, s, tid))

    def add_guest(self, eid, n, e, p, r):
        return self.execute_query(
            "INSERT INTO guest (event_id, guest_name, guest_email, guest_phone, rsvp_status) VALUES (?, ?, ?, ?, ?)",
            (eid, n, e, p, r))

    def update_guest(self, gid, n, e, p, r):
        return self.execute_query(
            "UPDATE guest SET guest_name=?, guest_email=?, guest_phone=?, rsvp_status=? WHERE guest_id=?",
            (n, e, p, r, gid))

    def add_budget(self, eid, c, a, d):
        return self.execute_query("INSERT INTO budgets (event_id, category, amount, description) VALUES (?, ?, ?, ?)",
                                  (eid, c, a, d))

    def update_budget(self, bid, c, a, d):
        return self.execute_query("UPDATE budgets SET category=?, amount=?, description=? WHERE budget_id=?",
                                  (c, a, d, bid))

    def add_vendor(self, eid, n, c, e, t):
        return self.execute_query(
            "INSERT INTO vendor (event_id, vendor_name, vendor_contact, vendor_email, vendor_type) VALUES (?, ?, ?, ?, ?)",
            (eid, n, c, e, t))

    def update_vendor(self, vid, n, c, e, t):
        return self.execute_query(
            "UPDATE vendor SET vendor_name=?, vendor_contact=?, vendor_email=?, vendor_type=? WHERE vendor_id=?",
            (n, c, e, t, vid))

    # Dashboard Methods
    def get_dashboard_stats(self):
        upcoming = self.execute_query(
            "SELECT event_name, event_date FROM events WHERE date(event_date) >= date('now') ORDER BY date(event_date) ASC LIMIT 3",
            fetch='all')
        tasks = self.execute_query("SELECT task_status, COUNT(*) FROM tasks GROUP BY task_status", fetch='all')
        budget = self.execute_query("SELECT SUM(amount) FROM budgets", fetch='one')
        return upcoming, tasks, (budget[0] if budget and budget[0] else 0)


# --- 2. ARCHITECTURE: REUSABLE BASE DIALOG ---
class BaseDialog(tk.Toplevel):
    def __init__(self, parent, title, fields, initial_values=None):
        super().__init__(parent)
        self.title(title);
        self.transient(parent);
        self.result = None;
        self.entries = {}
        form_frame = ttk.Frame(self, padding="10");
        form_frame.pack(expand=True, fill="both")
        for i, (label, field_info) in enumerate(fields.items()):
            field_type = field_info[0] if isinstance(field_info, tuple) else field_info
            ttk.Label(form_frame, text=f"{label}:").grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if field_type == 'date':
                entry = DateEntry(form_frame, width=37, date_pattern='y-mm-dd')
            elif field_type == 'text':
                entry = ttk.Entry(form_frame, width=40)
            elif field_type == 'combo':
                entry = ttk.Combobox(form_frame, values=field_info[1], width=38, state="readonly")
            else:
                entry = tk.Text(form_frame, width=30, height=4, relief="solid", borderwidth=1)
            if initial_values and label in initial_values:
                if isinstance(entry, tk.Text):
                    entry.insert('1.0', initial_values[label])
                else:
                    entry.insert(0, initial_values[label]);
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.entries[label] = entry
        ttk.Button(form_frame, text="Save", command=self.on_save).grid(row=i + 1, column=1, sticky='e', padx=5, pady=10)
        self.grab_set();
        self.wait_window(self)

    def on_save(self):
        self.result = {}
        for label, entry in self.entries.items():
            self.result[label] = entry.get('1.0', 'end-1c') if isinstance(entry, tk.Text) else entry.get()
        self.destroy()


# --- 3. MAIN APPLICATION ---
class EventPlannerApp:
    def __init__(self, root):
        self.root = root;
        self.db = DatabaseManager(DB_FILE)
        sv_ttk.set_theme("dark")
        self.show_login_screen()

    def hash_password(self, password):
        salt = os.urandom(32);
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt.hex() + ':' + key.hex()

    def verify_password(self, stored_hash, provided_password):
        try:
            salt_hex, key_hex = stored_hash.split(':');
            salt = bytes.fromhex(salt_hex)
            new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
            return new_key.hex() == key_hex
        except:
            return False

    def clear_screen(self):
        [widget.destroy() for widget in self.root.winfo_children()]

    def show_login_screen(self):
        self.clear_screen();
        self.root.title("Event Planner Pro - Login");
        self.root.geometry("400x250");
        frame = ttk.Frame(self.root, padding="20");
        frame.pack(expand=True)
        ttk.Label(frame, text="Username:").grid(row=0, column=0, pady=5, sticky='w');
        self.username_entry = ttk.Entry(frame, width=30);
        self.username_entry.grid(row=0, column=1, pady=5)
        ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=5, sticky='w');
        self.password_entry = ttk.Entry(frame, width=30, show="*");
        self.password_entry.grid(row=1, column=1, pady=5)
        ttk.Button(frame, text="Login", command=self.handle_login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Register", command=self.handle_register_prompt).grid(row=3, column=0, columnspan=2)

    def handle_login(self):
        username = self.username_entry.get();
        password = self.password_entry.get()
        stored_hash = self.db.get_user_hash(username)
        if stored_hash and self.verify_password(stored_hash, password):
            self.show_main_app()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def handle_register_prompt(self):
        fields = {"Username": 'text', "Password": 'text', "Confirm Password": 'text'}
        dialog = BaseDialog(self.root, "Register New User", fields)
        if dialog.result:
            if not dialog.result['Username'] or not dialog.result['Password']: messagebox.showerror("Error",
                                                                                                    "Username and password cannot be empty."); return
            if dialog.result['Password'] != dialog.result['Confirm Password']: messagebox.showerror("Error",
                                                                                                    "Passwords do not match."); return
            if self.db.add_user(dialog.result['Username'], self.hash_password(dialog.result['Password'])):
                messagebox.showinfo("Success", "User registered successfully!")
            else:
                messagebox.showerror("Error", "Username may already exist.")

    def show_main_app(self):
        self.clear_screen();
        self.root.title("Event Planner Pro");
        self.root.geometry("1200x700")
        self.notebook = ttk.Notebook(self.root);
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        tabs = {"Dashboard": "dashboard", "Events": "events", "Tasks": "tasks", "Guests": "guests",
                "Budgets": "budgets", "Vendors": "vendors"}
        for text, name in tabs.items():
            frame = ttk.Frame(self.notebook, padding="10");
            self.notebook.add(frame, text=text)
            setattr(self, f"{name}_frame", frame)
            getattr(self, f"create_{name}_tab")()

    def create_dashboard_tab(self):
        frame = self.dashboard_frame;
        [widget.destroy() for widget in frame.winfo_children()]
        upcoming, tasks, budget = self.db.get_dashboard_stats()
        events_frame = ttk.LabelFrame(frame, text="Upcoming Events", padding="10");
        events_frame.pack(fill="x", pady=5)
        if upcoming:
            [ttk.Label(events_frame, text=f"• {name} on {date}").pack(anchor="w") for name, date in upcoming]
        else:
            ttk.Label(events_frame, text="No upcoming events.").pack()
        tasks_frame = ttk.LabelFrame(frame, text="Task Status", padding="10");
        tasks_frame.pack(fill="x", pady=5)
        if tasks:
            [ttk.Label(tasks_frame, text=f"• {status}: {count} task(s)").pack(anchor="w") for status, count in tasks]
        else:
            ttk.Label(tasks_frame, text="No tasks found.").pack()
        budget_frame = ttk.LabelFrame(frame, text="Budget Overview", padding="10");
        budget_frame.pack(fill="x", pady=5)
        ttk.Label(budget_frame, text=f"Total Budgeted Amount: ${budget:,.2f}").pack(anchor="w")
        ttk.Button(frame, text="Refresh Dashboard", command=self.create_dashboard_tab).pack(pady=20)

    def create_tab(self, name, cols, id_col_index=0):
        frame = getattr(self, f"{name}_frame");
        [widget.destroy() for widget in frame.winfo_children()]
        btn_frame = ttk.Frame(frame);
        btn_frame.pack(fill='x', pady=5)
        ttk.Button(btn_frame, text=f"Add New {name.capitalize()[:-1]}", command=lambda: self.add_item(name)).pack(
            side='left')
        update_btn = ttk.Button(btn_frame, text=f"Update Selected", command=lambda: self.update_item(name),
                                state='disabled');
        update_btn.pack(side='left', padx=10)
        delete_btn = ttk.Button(btn_frame, text=f"Delete Selected", command=lambda: self.delete_item(name),
                                state='disabled');
        delete_btn.pack(side='left')
        tree = ttk.Treeview(frame, columns=cols, show='headings')
        for col in cols: tree.heading(col, text=col); tree.column(col, width=150)
        tree.pack(expand=True, fill='both')
        tree.bind('<<TreeviewSelect>>',
                  lambda e: (update_btn.config(state='normal'), delete_btn.config(state='normal')))
        setattr(self, f"{name}_tree", tree);
        setattr(self, f"update_{name}_btn", update_btn);
        setattr(self, f"delete_{name}_btn", delete_btn)
        getattr(self, f"load_{name}")()

    def load_items(self, name, data):
        tree = getattr(self, f"{name}_tree");
        getattr(self, f"update_{name}_btn").config(state='disabled');
        getattr(self, f"delete_{name}_btn").config(state='disabled')
        [tree.delete(i) for i in tree.get_children()]
        for item in data: tree.insert("", "end", values=item, iid=item[0])

    def add_item(self, name):
        fields, _ = getattr(self, f"get_{name}_fields")()
        dialog = BaseDialog(self.root, f"Add {name.capitalize()[:-1]}", fields)
        if dialog.result:
            try:
                if name == 'events':
                    self.db.add_event(dialog.result['Name'], dialog.result['Date'], dialog.result['Time'],
                                      dialog.result['Location'], dialog.result['Description'])
                elif name == 'tasks':
                    self.db.add_task(int(dialog.result['Event ID'].split(' ')[0]), dialog.result['Name'],
                                     dialog.result['Description'], dialog.result['Due Date'], dialog.result['Status'])
                elif name == 'guests':
                    self.db.add_guest(int(dialog.result['Event ID'].split(' ')[0]), dialog.result['Name'],
                                      dialog.result['Email'], dialog.result['Phone'], dialog.result['RSVP Status'])
                elif name == 'budgets':
                    self.db.add_budget(int(dialog.result['Event ID'].split(' ')[0]), dialog.result['Category'],
                                       float(dialog.result['Amount']), dialog.result['Description'])
                elif name == 'vendors':
                    self.db.add_vendor(int(dialog.result['Event ID'].split(' ')[0]), dialog.result['Name'],
                                       dialog.result['Contact'], dialog.result['Email'], dialog.result['Type'])
                getattr(self, f"load_{name}")();
                messagebox.showinfo("Success", f"{name.capitalize()[:-1]} added successfully!")
            except Exception as e:
                messagebox.showerror("Input Error", f"Could not add item. Please check all fields.\nDetails: {e}")

    def update_item(self, name):
        tree = getattr(self, f"{name}_tree");
        selected_item_id = tree.focus()
        if not selected_item_id: return
        item_data = self.db.get_one(name, f"{name[:-1]}_id", selected_item_id)
        if not item_data: messagebox.showerror("Error", "Could not retrieve item details."); return
        fields, initial_values = getattr(self, f"get_{name}_fields")(item_data)
        dialog = BaseDialog(self.root, f"Update {name.capitalize()[:-1]}", fields, initial_values)
        if dialog.result:
            try:
                if name == 'events':
                    self.db.update_event(selected_item_id, dialog.result['Name'], dialog.result['Date'],
                                         dialog.result['Time'], dialog.result['Location'], dialog.result['Description'])
                elif name == 'tasks':
                    self.db.update_task(selected_item_id, dialog.result['Name'], dialog.result['Description'],
                                        dialog.result['Due Date'], dialog.result['Status'])
                elif name == 'guests':
                    self.db.update_guest(selected_item_id, dialog.result['Name'], dialog.result['Email'],
                                         dialog.result['Phone'], dialog.result['RSVP Status'])
                elif name == 'budgets':
                    self.db.update_budget(selected_item_id, dialog.result['Category'], float(dialog.result['Amount']),
                                          dialog.result['Description'])
                elif name == 'vendors':
                    self.db.update_vendor(selected_item_id, dialog.result['Name'], dialog.result['Contact'],
                                          dialog.result['Email'], dialog.result['Type'])
                getattr(self, f"load_{name}")();
                messagebox.showinfo("Success", f"{name.capitalize()[:-1]} updated successfully!")
            except Exception as e:
                messagebox.showerror("Input Error", f"Could not update item. Please check all fields.\nDetails: {e}")

    def delete_item(self, name):
        tree = getattr(self, f"{name}_tree");
        selected_item_id = tree.focus()
        if not selected_item_id: return
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this {name[:-1]}?"):
            self.db.delete_one(name, f"{name[:-1]}_id", selected_item_id);
            getattr(self, f"load_{name}")()

    def get_events_for_dropdown(self):
        events = self.db.get_all('events', 'event_id')
        return [f"{e[0]} - {e[1]}" for e in events] if events else []

    def get_events_fields(self, data=None):
        fields = {'Name': 'text', 'Date': 'date', 'Time': 'text', 'Location': 'text', 'Description': 'textarea'}
        if not data: return fields, None
        return fields, {'Name': data[1], 'Date': data[2], 'Time': data[3], 'Location': data[4], 'Description': data[5]}

    def get_tasks_fields(self, data=None):
        fields = {'Event ID': ('combo', self.get_events_for_dropdown()), 'Name': 'text', 'Due Date': 'date',
                  'Status': ('combo', ['Pending', 'In Progress', 'Completed']), 'Description': 'textarea'}
        if not data: return fields, None
        event_str = f"{data[1]} - {self.db.get_one('events', 'event_id', data[1])[1]}"
        return fields, {'Event ID': event_str, 'Name': data[2], 'Description': data[3], 'Due Date': data[4],
                        'Status': data[5]}

    def get_guests_fields(self, data=None):
        fields = {'Event ID': ('combo', self.get_events_for_dropdown()), 'Name': 'text', 'Email': 'text',
                  'Phone': 'text', 'RSVP Status': ('combo', ['Attending', 'Maybe', 'Declined', 'Pending'])}
        if not data: return fields, None
        event_str = f"{data[1]} - {self.db.get_one('events', 'event_id', data[1])[1]}"
        return fields, {'Event ID': event_str, 'Name': data[2], 'Email': data[3], 'Phone': data[4],
                        'RSVP Status': data[5]}

    def get_budgets_fields(self, data=None):
        fields = {'Event ID': ('combo', self.get_events_for_dropdown()), 'Category': 'text', 'Amount': 'text',
                  'Description': 'textarea'}
        if not data: return fields, None
        event_str = f"{data[1]} - {self.db.get_one('events', 'event_id', data[1])[1]}"
        return fields, {'Event ID': event_str, 'Category': data[2], 'Amount': data[3], 'Description': data[4]}

    def get_vendors_fields(self, data=None):
        fields = {'Event ID': ('combo', self.get_events_for_dropdown()), 'Name': 'text', 'Contact': 'text',
                  'Email': 'text', 'Type': 'text'}
        if not data: return fields, None
        event_str = f"{data[5]} - {self.db.get_one('events', 'event_id', data[5])[1]}"
        return fields, {'Event ID': event_str, 'Name': data[1], 'Contact': data[2], 'Email': data[3], 'Type': data[4]}

    def create_events_tab(self):
        self.create_tab('events', ('ID', 'Name', 'Date', 'Location'))

    def load_events(self):
        self.load_items('events', self.db.get_all('events', 'event_date'))

    def create_tasks_tab(self):
        self.create_tab('tasks', ('ID', 'Event ID', 'Name', 'Due Date', 'Status'))

    def load_tasks(self):
        self.load_items('tasks', self.db.get_all('tasks', 'task_due_date'))

    def create_guests_tab(self):
        self.create_tab('guests', ('ID', 'Event ID', 'Name', 'Email', 'RSVP'))

    def load_guests(self):
        self.load_items('guests', self.db.get_all('guest', 'guest_name'))

    def create_budgets_tab(self):
        self.create_tab('budgets', ('ID', 'Event ID', 'Category', 'Amount'))

    def load_budgets(self):
        self.load_items('budgets', self.db.get_all('budgets', 'category'))

    def create_vendors_tab(self):
        self.create_tab('vendors', ('ID', 'Event ID', 'Name', 'Contact', 'Type'))

    def load_vendors(self):
        self.load_items('vendors', self.db.get_all('vendor', 'vendor_name'))


if __name__ == "__main__":
    root = tk.Tk()
    app = EventPlannerApp(root)
    root.mainloop()