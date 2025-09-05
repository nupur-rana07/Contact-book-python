import csv
import os

FILENAME = "contacts.txt"
FIELDS = ["name", "phone", "email"]

def ensure_file():
    """Create the contacts file with a header if it doesn't exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

def load_contacts():
    """Return all contacts as a list of dicts."""
    ensure_file()
    with open(FILENAME, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_contact(contact):
    """Append a new contact (dict) to the file."""
    ensure_file()
    with open(FILENAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(contact)

def add_contact():
    print("\n=== Add Contact ===")
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email (optional): ").strip()

    if not name or not phone:
        print("Name and Phone are required.")
        return

    # very light validation
    if not phone.replace("+","").replace("-","").replace(" ","").isdigit():
        print("Phone should contain digits (with optional +, -, spaces).")
        return

    # prevent duplicate phone numbers
    contacts = load_contacts()
    for c in contacts:
        if c["phone"].strip() == phone:
            print("A contact with this phone already exists.")
            return

    contact = {"name": name, "phone": phone, "email": email}
    save_contact(contact)
    print("Contact saved.")

def view_contacts():
    print("\n=== All Contacts ===")
    contacts = load_contacts()
    if not contacts:
        print("(No contacts yet)")
        return
    for idx, c in enumerate(contacts, start=1):
        print(f"{idx}. {c['name']} | {c['phone']} | {c['email']}")

def search_contacts():
    print("\n=== Search Contacts ===")
    q = input("Search by name/phone/email: ").strip().lower()
    if not q:
        print("Empty query.")
        return

    contacts = load_contacts()
    matches = []
    for c in contacts:
        if (q in c["name"].lower()
            or q in c["phone"].lower()
            or q in c["email"].lower()):
            matches.append(c)

    if not matches:
        print("No matches found.")
        return

    print(f"Found {len(matches)} result(s):")
    for idx, c in enumerate(matches, start=1):
        print(f"{idx}. {c['name']} | {c['phone']} | {c['email']}")

def main():
    ensure_file()
    while True:
        print("\n==== Contact Book ====")
        print("1) Add contact")
        print("2) View all")
        print("3) Search")
        print("0) Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contacts()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
