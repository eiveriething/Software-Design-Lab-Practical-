import random
from datetime import datetime


# =====
# User class
# =====

class User:
    def __init__(self, user_id, username, password, name):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.name = name

    def login(self, username, password):
        if self.username == username and self.password == password:
            return True
        return False


# =====
# Ticket class
# =====


class Ticket:
    def __init__(
        self,
        ticket_id,
        title,
        description,
        category=None,
        priority=None,
        status='Open',
        created_at=None,
        username=None,
        assigned_to=None,
        resolution=None
    ):
        self.ticket_id = ticket_id
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status
        self.created_at = created_at if created_at else datetime.now()
        self.username = username
        self.assigned_to = assigned_to
        self.resolution = resolution

    def update_status(self, new_status):
        self.status = new_status

    def __str__(self):
        return (
            f"Ticket ID: {self.ticket_id}, "
            f"Title: {self.title}, "
            f"Status: {self.status}, "
            f"Created At: {self.created_at}"
        )


# Store existing ticket IDs
existing_ticket_ids = set()


def generate_ticket_id():

    while True:
        number = random.randint(10000, 99999)
        ticket_id = f"TCK-{number}"

        # Make sure the ID not already used
        if ticket_id not in existing_ticket_ids:
            existing_ticket_ids.add(ticket_id)
            return ticket_id


def create_ticket():

    print("\n====== Create a New Ticket ======")

    title = input("Enter the title of the ticket: ")
    description = input("Describe the issue: ")
    username = input("Enter your username: ")

    # Generate a unique ticket ID
    ticket_id = generate_ticket_id()

    # Create Ticket object
    new_ticket = Ticket(
        ticket_id,
        title,
        description,
        username=username
    )

    print("\nTicket created successfully!")
    print(f"Ticket ID: {new_ticket.ticket_id}")

    return new_ticket


def print_ticket(ticket):

    print("\n====== Ticket Details ======")
    print(f"Ticket ID: {ticket.ticket_id}")
    print(f"Title: {ticket.title}")
    print(f"Description: {ticket.description}")
    print(f"Category: {ticket.category}")
    print(f"Priority: {ticket.priority}")
    print(f"Status: {ticket.status}")
    print(f"Assigned To: {ticket.assigned_to if ticket.assigned_to else 'Not assigned'}")
    print(f"Resolution: {ticket.resolution if ticket.resolution else 'Pending'}")
    print(f"Created At: {ticket.created_at}")
    print(f"Username: {ticket.username}")

# =====
# Notification class
# =====

class Notification:
    def __init__(self, notification_id, user_id, message):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.read = False

    def receive_notification(self):
        self.read = True
        return self.message


# =====
# Helpdesk System class
# =====

class HelpdeskSystem:
    def __init__(self):
        self.users = []
        self.tickets = []
        self.notifications = []

    # =====
    # User Registration
    # =====

    def register_user(self, username, password, name):
        if any(u.username == username for u in self.users):
            print("\nThat username is already taken.")
            return None

        user_id = 1 + len(self.users)
        user = User(user_id, username, password, name)
        self.users.append(user)
        print(f"\nAccount created. Welcome, {name}!")
        return user

    # =====
    # User Login
    # =====

    def user_login(self, username, password):
        for user in self.users:
            if user.login(username, password):
                print("\nLogin successful.")
                print(f"Welcome, {user.name}!")
                return user

        print("\nInvalid username or password.")
        return None

    # =====
    # Receive Ticket
    # =====

    def receive_ticket(self, user, title, description, category, priority):
        ticket_id = 1001 + len(self.tickets)
        ticket = Ticket(
            ticket_id,
            title,
            description,
            category=category,
            priority=priority,
            username=user.username
        )
        self.tickets.append(ticket)
        print("\nTicket Received")
        print("-----------------")
        print(ticket)
        self.receive_notification(user, ticket)
        self.confirmation(ticket)
        return ticket

    # =====
    # Receive Notification
    # =====

    def receive_notification(self, user, ticket):
        notification_id = 1 + len(self.notifications)
        message = (
            f"Your ticket #{ticket.ticket_id} "
            f"has been received successfully."
        )
        notification = Notification(notification_id, user.user_id, message)

        self.notifications.append(notification)
        print("\nNotification")
        print("-----------------")
        print(notification.receive_notification())

        return notification

    # =====
    # Confirmation
    # =====

    def confirmation(self, ticket):
        print("\nConfirmation")
        print("-----------------")
        print(f"Your helpdesk ticket #{ticket.ticket_id} "
              f"has been submitted successfully.")
        print("Please keep your ticket number for tracking.")

    # =====
    # View a user's tickets
    # =====

    def view_tickets(self, user):
        user_tickets = [t for t in self.tickets if t.username == user.username]

        if not user_tickets:
            print("\nYou have no tickets yet.")
            return

        print(f"\n====== Tickets for {user.username} ======")
        for ticket in user_tickets:
            print_ticket(ticket)


# =====
# Admin class
# =====


class Admin:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # ==========================
    # LOGIN
    # ==========================

    def login(self, username, password):

        if username == self.username and password == self.password:
            return True

        return False

    # ==========================
    # VIEW RECEIVED TICKETS
    # ==========================

    def view_tickets(self, tickets):

        print("\n====== RECEIVED TICKETS ======")

        if len(tickets) == 0:
            print("No tickets received.")
            return

        for ticket in tickets:

            print("\n------------------------------")
            print(f"Ticket ID: {ticket.ticket_id}")
            print(f"Title: {ticket.title}")
            print(f"Description: {ticket.description}")
            print(f"Username: {ticket.username}")
            print(f"Status: {ticket.status}")

            if ticket.assigned_to:
                print(f"Assigned To: {ticket.assigned_to}")
            else:
                print("Assigned To: Not assigned")

            print(f"Created At: {ticket.created_at}")

    # ==========================
    # CONFIRM TICKET
    # ==========================

    def confirm_ticket(self, ticket):

        print("\n====== TICKET CONFIRMATION ======")
        print(f"Ticket ID: {ticket.ticket_id}")
        print(f"Submitted by: {ticket.username}")
        print("Ticket received successfully!")

    # ==========================
    # SEARCH TICKET
    # ==========================

    def search_ticket(self, tickets, ticket_id):

        for ticket in tickets:

            if str(ticket.ticket_id) == str(ticket_id):
                return ticket

        return None

    # ==========================
    # ASSIGN TICKET
    # ==========================

    def assign_ticket(self, ticket, assigned_to):

        ticket.assigned_to = assigned_to

        print("\nTicket assigned successfully!")
        print(f"Ticket ID: {ticket.ticket_id}")
        print(f"Assigned To: {ticket.assigned_to}")

    # ==========================
    # UPDATE STATUS
    # ==========================

    def update_ticket_status(self, ticket, new_status):

        ticket.update_status(new_status)

        print("\nTicket status updated successfully!")
        print(f"Ticket ID: {ticket.ticket_id}")
        print(f"New Status: {ticket.status}")


# =====
# IT Staff class
# =====
# Inherits login/view_tickets/confirm_ticket/search_ticket/
# assign_ticket/update_ticket_status from Admin exactly as written.
# Only new behavior added is send_resolution().

class ITStaff(Admin):

    def send_resolution(self, ticket, resolution):

        ticket.resolution = resolution

        print("\nResolution sent successfully!")
        print(f"Ticket ID: {ticket.ticket_id}")
        print(f"Resolution: {ticket.resolution}")


# ==========================================
# ADMIN MENU
# Admin: view all tickets received, assign them to IT staff.
# (Confirm/Search stay here since they're admin intake duties;
# Update Status moved to the IT menu below.)
# ==========================================

def admin_menu(admin, tickets):

    while True:

        print("\n================================")
        print("        ADMIN DASHBOARD")
        print("================================")
        print("1. View Received Tickets")
        print("2. Search Ticket")
        print("3. Confirm Ticket")
        print("4. Assign Ticket")
        print("5. Logout")
        print("================================")

        choice = input("Enter choice: ")

        # VIEW
        if choice == "1":

            admin.view_tickets(tickets)

        # SEARCH
        elif choice == "2":

            ticket_id = input("Enter Ticket ID: ")

            ticket = admin.search_ticket(tickets, ticket_id)

            if ticket:

                print("\n====== TICKET FOUND ======")
                print(f"Ticket ID: {ticket.ticket_id}")
                print(f"Title: {ticket.title}")
                print(f"Description: {ticket.description}")
                print(f"Username: {ticket.username}")
                print(f"Status: {ticket.status}")

                if ticket.assigned_to:
                    print(f"Assigned To: {ticket.assigned_to}")
                else:
                    print("Assigned To: Not assigned")

                print(f"Created At: {ticket.created_at}")

            else:
                print("\nTicket not found.")

        # CONFIRM
        elif choice == "3":

            ticket_id = input("Enter Ticket ID: ")

            ticket = admin.search_ticket(tickets, ticket_id)

            if ticket:
                admin.confirm_ticket(ticket)
            else:
                print("\nTicket not found.")

        # ASSIGN
        elif choice == "4":

            ticket_id = input("Enter Ticket ID: ")

            ticket = admin.search_ticket(tickets, ticket_id)

            if ticket:

                print("\n====== ASSIGN TICKET ======")
                print("1. IT Staff 01")
                print("2. IT Staff 02")
                print("3. Network Support")
                print("4. Hardware Support")

                staff_choice = input("Choose personnel: ")

                if staff_choice == "1":
                    assigned_to = "IT Staff 01"

                elif staff_choice == "2":
                    assigned_to = "IT Staff 02"

                elif staff_choice == "3":
                    assigned_to = "Network Support"

                elif staff_choice == "4":
                    assigned_to = "Hardware Support"

                else:
                    print("\nInvalid choice.")
                    continue

                admin.assign_ticket(ticket, assigned_to)

            else:
                print("\nTicket not found.")

        # LOGOUT
        elif choice == "5":

            print("\nLogging out...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ==========================================
# IT STAFF MENU
# IT: only sees tickets assigned to them, updates status,
# and sends a resolution.
# ==========================================

def it_menu(it, system):

    while True:

        assigned_tickets = [
            t for t in system.tickets if t.assigned_to == it.username
        ]

        print("\n================================")
        print(f"     IT DASHBOARD ({it.username})")
        print("================================")
        print("1. View My Assigned Tickets")
        print("2. Search Ticket")
        print("3. Update Ticket Status")
        print("4. Send Resolution")
        print("5. Logout")
        print("================================")

        choice = input("Enter choice: ")

        # VIEW
        if choice == "1":

            it.view_tickets(assigned_tickets)

        # SEARCH
        elif choice == "2":

            ticket_id = input("Enter Ticket ID: ")
            ticket = it.search_ticket(assigned_tickets, ticket_id)

            if ticket:
                print_ticket(ticket)
            else:
                print("\nTicket not found among your assigned tickets.")

        # UPDATE STATUS
        elif choice == "3":

            ticket_id = input("Enter Ticket ID: ")
            ticket = it.search_ticket(assigned_tickets, ticket_id)

            if ticket:

                print("\n====== UPDATE TICKET STATUS ======")
                print("1. Open")
                print("2. Pending")
                print("3. In Progress")
                print("4. Resolved")
                print("5. Cancelled")

                status_choice = input("Choose status: ")

                if status_choice == "1":
                    status = "Open"

                elif status_choice == "2":
                    status = "Pending"

                elif status_choice == "3":
                    status = "In Progress"

                elif status_choice == "4":
                    status = "Resolved"

                elif status_choice == "5":
                    status = "Cancelled"

                else:
                    print("\nInvalid choice.")
                    continue

                it.update_ticket_status(ticket, status)

            else:
                print("\nTicket not found among your assigned tickets.")

        # SEND RESOLUTION
        elif choice == "4":

            ticket_id = input("Enter Ticket ID: ")
            ticket = it.search_ticket(assigned_tickets, ticket_id)

            if ticket:
                resolution = input("Enter resolution details: ")
                it.send_resolution(ticket, resolution)
            else:
                print("\nTicket not found among your assigned tickets.")

        # LOGOUT
        elif choice == "5":

            print("\nLogging out...")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ==========================================
# USER MENU
# User: create a ticket, view their own tickets (status/assignment/
# resolution all show up through print_ticket / view_tickets).
# ==========================================

def user_menu(system, user):

    while True:

        print("\n================================")
        print(f"       USER MENU ({user.username})")
        print("================================")
        print("1. Create Ticket")
        print("2. View My Tickets")
        print("3. Logout")
        print("4. Exit")
        print("================================")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            title = input("Enter the title of the ticket: ")
            description = input("Describe the issue: ")
            category = input("Enter a category: ")
            priority = input("Enter priority (Low/Medium/High): ")
            system.receive_ticket(user, title, description, category, priority)

        elif choice == "2":
            system.view_tickets(user)

        elif choice == "3":
            print("\nLogging out...")
            return "logout"

        elif choice == "4":
            print("\nGoodbye!")
            return "exit"

        else:
            print("\nInvalid choice. Please try again.")


# ==========================================
# LOGIN GATE
# Everyone starts here and picks which role they're logging in as.
# ==========================================

def login_gate(system, admin, it_staff):

    while True:

        print("\n================================")
        print("      HELPDESK SYSTEM LOGIN")
        print("================================")
        print("1. Login as Admin")
        print("2. Login as IT Staff")
        print("3. Login as User")
        print("4. Register (User)")
        print("5. Exit")
        print("================================")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")

            if admin.login(username, password):
                print("\nAdmin login successful.")
                return "admin", admin

            print("\nInvalid admin credentials.")

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")

            staff = it_staff.get(username)
            if staff and staff.login(username, password):
                print(f"\nWelcome, {username}.")
                return "it", staff

            print("\nInvalid IT staff credentials.")

        elif choice == "3":
            username = input("Username: ")
            password = input("Password: ")

            user = system.user_login(username, password)
            if user:
                return "user", user

        elif choice == "4":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            name = input("Enter your full name: ")
            system.register_user(username, password, name)

        elif choice == "5":
            print("\nGoodbye!")
            return None, None

        else:
            print("\nInvalid choice. Please try again.")


# =====
# Main
# =====

def main():

    system = HelpdeskSystem()

    admin = Admin("admin", "admin123")

    it_staff = {
        "IT Staff 01": ITStaff("IT Staff 01", "it01pass"),
        "IT Staff 02": ITStaff("IT Staff 02", "it02pass"),
        "Network Support": ITStaff("Network Support", "netpass"),
        "Hardware Support": ITStaff("Hardware Support", "hwpass"),
    }

    while True:

        role, actor = login_gate(system, admin, it_staff)

        if role is None:
            break

        if role == "admin":
            admin_menu(actor, system.tickets)

        elif role == "it":
            it_menu(actor, system)

        elif role == "user":
            result = user_menu(system, actor)
            if result == "exit":
                break
            # "logout" falls through and loops back to login_gate


if __name__ == "__main__":
    main()
