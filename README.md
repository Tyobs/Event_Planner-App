1. Documentation 
This .md gives you the lowdown on the Event Planner app – your new best friend for getting those parties and gatherings sorted!

1.1. Overview
This Event Planner app is like your digital command center for everything event-related. It's a desktop tool that makes it super easy to keep track of all the bits and nods, from the big day itself to the folks helping out and the money side of things. Plus, we've got a little security thingy so only you can get in!

1.2. Features 
We've split everything into handy tabs, so you can find what you need quick-smart:

•	**Events**: This is where the magic starts! You can add all the details for your events – name, date, time, where it's happening, and a little description.

![A picture for events tab, currently unable to preview](<loaded events screen.png>)
 
o	See how it lists all your upcoming (and maybe past) events?
o	You can also click a button to make a brand new event pop up!

![Creating an event](<create event window.png>)
 
	This is where you type in all the important stuff.
o	Need to tweak something? Just punch in the Event ID, and you can update or even bin an event.

•	**Tasks**: Got to get stuff done? This tab lets you list all the tasks for each event. Name it, describe it, set a due date, and mark if it's done or not.

![picture for tasks window](<loaded tasks window.png>)
 
o	Keep track of who's doing what and when!
o	Adding, changing, and deleting tasks is a breeze with the buttons here.

•	**Guests**: Who's coming to your awesome event? Keep your guest list here! Name, email, number, and if they've said they're in or out – all in one place.
 
 ![loaded guests window](<loaded guests window.png>)

Easy to see who you need to chase up for an RSVP!
o	Adding new names and updating details is super straightforward.

•	**Budgets**: Let's talk money! This tab helps you keep an eye on where your cash is going for each event. Break it down by category, put in the amount, and add a little note.
 

![loaded budget](<loaded budget window.png>)

o	See how it's all laid out?
o	Adding new things to the budget and changing amounts is all point-and-click.

•	**Vendors**: Who's helping you make this event happen? Caterers, DJs, florists – pop their info in here! Name, contact details, email, and what type of vendor they are.

![vendors loaded](<loaded vendors.png>)
 
o	Keep all your important contacts handy.
o	Adding new vendors and updating their info is nice and simple.

•	**User Authentication**: We've got a basic login thingy so your event plans are just for your eyes. You can sign up and then log in with your username and password.

![logging in window](<logIn win.png>)

o	**This is the first thing you'll see.**

![registration window](<registration win.png>)

o	Signing up is quick and easy.

1.3. **How it Works** 
**Under the hood, this app uses:**

•	**Python**: That's the language we used to build it.
•	**Tkinter**: This is what makes all the buttons and windows you see. The **"ttk"** part gives it a nicer look.
•	**SQLite**: Think of this as a little digital filing cabinet that keeps all your event info safe in a file on your computer.
•	**sqlite3**: This is Python's way of talking to that filing cabinet.
•	**hashlib**: For keeping your password super secure when you sign up. It scrambles it up so no one can just read it!

1.4. **What's Next? (Dreaming Big!)**

**We've got some ideas for making this app even better**:

•	Making it easier to sort and filter through your lists.
•	Maybe a special view just for each event.
•	Getting reports out – like a list of all your guests or a summary of your budget.
•	Being able to import or export your event info.
•	Maybe even more ways to manage users later on.

