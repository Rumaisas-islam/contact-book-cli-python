import re
import shutil
from pathlib import Path
class ContactBook:
    def __init__(self, filename="contact.txt"):
        self.filename = filename

    def create_backup(self):
        if Path(self.filename).exists():
            shutil.copyfile(self.filename, "contact_backup.txt")
            print("🔄 Backup created as 'contact_backup.txt'")

    def add_contact(self):
        print("------- Welcome to the Contact Book -------")
        name = input("Enter name: ").strip()

        while True:
            phone_number = input("Enter phone number: ").strip()
            if phone_number.isdigit() and len(phone_number) == 11:
                break
            print("❌ Invalid phone number. Must be 11 digits.")

        while True:
            email = input("Enter email: ").strip()
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                break
            print("❌ Invalid email format. Try again (e.g., example@email.com)")

        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write("📇 Contact Record\n")
                f.write(f"Name:{name}\n")
                f.write(f"Phone_number:{phone_number}\n")
                f.write(f"Email:{email}\n")
                f.write("========================\n")
            print("✅ Contact saved successfully.")
        except Exception as e:
            print(f"Error saving contact: {e}")

    def search_contact(self, field):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("No file found")
            return

        value = input(f"Enter the {field.lower()} to search contact: ").strip()
        pattern = rf"^{field}:\s*{re.escape(value)}$"
        found = False
        block = []

        for line in lines:
            if line.strip() == "========================":
                if any(re.search(pattern, l.strip(), re.IGNORECASE) for l in block):
                    print("\n".join(block))
                    print("========================")
                    found = True
                block = []
            else:
                block.append(line.strip())

        if not found:
            print(f"No contact found with that {field.lower()}.")

    def delete_contact(self, field):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("No file found")
            return

        value = input(f"Enter the {field.lower()} to delete contact: ").strip()
        pattern = rf"^{field}:\s*{re.escape(value)}$"
        new_lines = []
        block = []
        found = False

        for line in lines:
            if line.strip() == "========================":
                if any(re.search(pattern, l.strip(), re.IGNORECASE) for l in block):
                    print("\n🔍 Matched Contact Record:")
                    print("\n".join(block))
                    confirm = input("Do you want to delete this contact? (yes/no): ").strip().lower()
                    if confirm == "yes":
                        self.create_backup()
                        found = True
                        # Skip writing this block
                    else:
                        new_lines.extend(block + ["========================\n"])
                else:
                    new_lines.extend(block + ["========================\n"])
                block = []
            else:
                block.append(line)

        if found:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print("✅ Selected contact(s) deleted successfully.")
        else:
            print(f"No contact found with that {field.lower()}.")

    def edit_contact(self, field):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("No file found")
            return

        value = input(f"Enter the {field.lower()} to edit: ").strip()
        pattern = rf"^{field}:\s*{re.escape(value)}$"
        new_lines = []
        block = []
        found = False

        for line in lines:
            if line.strip() == "========================":
                if any(re.search(pattern, l.strip(), re.IGNORECASE) for l in block):
                    print("\n🔍 Matched Contact Record:")
                    print("\n".join(block))
                    confirm = input("Do you want to edit this contact? (yes/no): ").strip().lower()
                    if confirm == "yes":
                        self.create_backup()
                        found = True

                        new_name = input("Enter name: ").strip()
                        while True:
                            new_phone_number = input("Enter phone number: ").strip()
                            if new_phone_number.isdigit() and len(new_phone_number) == 11:
                                break
                            print("❌ Invalid phone number. Must be 11 digits.")
                        while True:
                            new_email = input("Enter email: ").strip()
                            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', new_email):
                                break
                            print("❌ Invalid email format. Try again (e.g., example@email.com)")

                        new_lines.append("📇 Contact Record\n")
                        new_lines.append(f"Name:{new_name}\n")
                        new_lines.append(f"Phone_number:{new_phone_number}\n")
                        new_lines.append(f"Email:{new_email}\n")
                        new_lines.append("========================\n")
                    else:
                        new_lines.extend(block + ["========================\n"])
                else:
                    new_lines.extend(block + ["========================\n"])
                block = []
            else:
                block.append(line)

        if found:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print("✅ Contact updated successfully.")
        else:
            print(f"No contact found with that {field.lower()}.")

    def list_all_names(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                names = [line.strip().replace("Name:", "") for line in lines if line.startswith("Name:")]
                if names:
                    print("\n📋 All Saved Names")
                    for idx, name in enumerate(names, 1):
                        print(f"{idx}. {name}")
                else:
                    print("No names found.")
        except FileNotFoundError:
            print("No file found")

    def print_all_contact_info(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                parts = re.findall(r"📇 Contact Record\n(.*?)========================", content, re.DOTALL)
                if parts:
                    print("\n📑 All Saved Contact Info")
                    for idx, part in enumerate(parts, 1):
                        print(f"Contact {idx}:\n{part.strip()}\n========================")
                else:
                    print("No contacts found.")
        except FileNotFoundError:
            print("No file found")
if __name__ == "__main__":
    obj = ContactBook()

    while True:
        print("\n--- Contact Book Menu ---")
        print("1. Add contact")
        print("2. Search contact")
        print("3. Delete contact")
        print("4. Edit contact")
        print("5. List all names")
        print("6. Print all contact info")
        print("7. Exit")

        choice = input("Enter your choice (1–7): ").strip()

        if choice == "1":
            obj.add_contact()
        elif choice == "2":
            print("Make sure write (Name/Phone_number/Email) otherwise it does not work")
            print()
            field = input("Search by (Name/Phone_number/Email): ").strip().capitalize()
            obj.search_contact(field)
        elif choice == "3":
            print("Make sure write (Name/Phone_number/Email) otherwise it does not work")
            print()
            field = input("Delete by (Name/Phone_number/Email): ").strip().capitalize()
            obj.delete_contact(field)
        elif choice == "4":
            print("Make sure write (Name/Phone_number/Email) otherwise it does not work")
            print()
            field = input("Edit by (Name/Phone_number/Email): ").strip().capitalize()
            obj.edit_contact(field)
        elif choice == "5":
            obj.list_all_names()
        elif choice == "6":
            obj.print_all_contact_info()
        elif choice == "7":
            print("📤 Exiting Contact Book. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")
