import csv
import calendar
import time
import os  # notification

fields = [
    'Name',
    'Mobile phone',
    {'Company': ['Name of a company', 'Occupation', 'Address', 'Web page']},
    {'Other phones': ['Mobile phone 2', 'Mobile phone 3', 'Home phone', 'Office phone']},
    {'Emails': ['Private email 1', 'Private email 2', 'Office email']},
    'Melody',
    {'Other': ['Address', 'Birth day', 'Notes']},
    {'Spouse': ['Name', 'Birthday', 'Notes']},
    {'Children': ['Name', 'Birthday', 'Notes']}]

contacts = []  # initialize an empty list to store contacts


def input_operation():
    global contacts  # use the global contacts list in the functions
    opr = int(input("1.Add new contact \n2.Delete contact \n3.Update contact \n4.View birthday reminder \n5.Create contact group \n6.Delete contact group\n7.Import contacts from csv file\n8.Export contacts into csv file\n9.Save contact/s into text file:\n"))
    if opr == 1:
        add_contact(fields)
    elif opr == 2:
        delete_contact()
    elif opr == 3:
        update_contact()
    elif opr == 4:
        birthday_reminder()
    elif opr == 5:
        opr_group()
    elif opr == 6:
        opr_group(delete_group=True)
    elif opr == 7:
        filename = input("Write the name of your file:")
        contacts = import_csv(filename)
    elif opr == 8:
        export_csv()
    elif opr == 9:
        save_txt()
    else:
        print("Invalid input. Please enter a valid number.")


def add_contact(fields):
    global contacts
    contact = {}
    for field in fields:
        if isinstance(field, str):
            value = input(f"Enter {field}: ")
            contact[field] = value
        elif isinstance(field, dict):
            for subfield in field:
                print(f"{subfield}:")
                subfield_values = {}
                for subsubfield in field[subfield]:
                    value = input(f"\t{subsubfield}: ")
                    subfield_values[subsubfield] = value
                subfield_tuple = tuple(subfield_values.items())
                contact[frozenset({subfield: subfield_tuple})] = subfield_values
    contacts.append(contact)


def delete_contact():
    global contacts
    name=input("Enter the name of the contact to delete:")
    for contact in contacts:
        if contact['Name']==name:
            contacts.remove(contact)
            print(f"{name} has been deleted.")
            return
    print(f"{name} not found.")

def update_contact():
    global contacts
    name = input("Enter the name of the contact to update: ")
    contact_index = None
    for i, contact in enumerate(contacts):
        if contact.get('Name') == name:
            contact_index = i
            break
    if contact_index is None:
        print(f"No contact found with name '{name}'.")
        return

    print(f"Current information for {name}:")
    for field, value in contacts[contact_index].items():
        if isinstance(field, str):
            print(f"{field}: {value}")
        elif isinstance(field, dict):
            for subfield in field:
                print(f"{subfield}:")
                for subsubfield, subvalue in value[subfield].items():
                    print(f"\t{subsubfield}: {subvalue}")

    while True:
        field_name = input("Enter the name of the field to update (or 'done' to finish): ")
        if field_name == 'done':
            break

        # find the field to update
        field_index = None
        for i, field in enumerate(fields):
            if isinstance(field, str) and field.lower() == field_name.lower():
                field_index = i
                break
            elif isinstance(field, dict):
                for subfield in field:
                    if subfield.lower() == field_name.lower():
                        field_index = i
                        break
                if field_index is not None:
                    break

        if field_index is None:
            print(f"Invalid field '{field_name}'.")
            continue

        # new value for the field
        new_value = input(f"Enter the new value for {field_name}: ")

        # update the field in the contact record
        if isinstance(fields[field_index], str):
            contacts[contact_index][fields[field_index]] = new_value
        elif isinstance(fields[field_index], dict):
            for subfield in fields[field_index]:
                subfield_values = {}
                for subsubfield in fields[field_index][subfield]:
                    subfield_values[subsubfield] = contacts[contact_index][frozenset({subfield: subfield_tuple})][subsubfield]
                subfield_values[subsubfield] = new_value
                subfield_tuple = tuple(subfield_values.items())
                contacts[contact_index][frozenset({subfield: subfield_tuple})] = subfield_values

        print(f"{field_name} updated.")

    print(f"{name} updated.")


    
    updated_fields = []
    while True:
        field = input("Enter the name of the field to update (or 'done' to finish): ")
        if field.lower() == 'done':
            break
        if field not in contacts[contact_index]:
            print(f"Invalid field '{field}'.")
            continue
        value = input(f"Enter the new value for {field}: ")
        updated_fields.append((field, value))

    
    for field, value in updated_fields:
        contacts[contact_index][field] = value

    print(f"{name} updated successfully.")


def birthday_reminder():
    current_month=calendar.month_name[time.localtime().tm_mon]
    for contact in contacts:
        if 'Birthday' in contact.keys():
            bday=contact['Birthday'].split('/')
            if bday[1]==current_month:
                print(f"{contact['Name']} has birthday on {bday[1]} {bday[0]}.")

def opr_group(delete_group=False):
    global contacts
    group_name=input("Enter the name of the group:")
    group=[]
    for contact in contacts:
        if group_name in contact['Groups'].split(','):
            group.append(contact)
    if not group:
        print(f"No contacts found in group {group_name}.")
        return
    print(f"Contacts in group {group_name}:")
    for i,contact in enumerate(group):
        print(f"{i+1}. {contact['Name']}")
    if delete_group:
        del_group=input(f"Select contacts to delete from group {group_name} (comma separated numbers):")
        del_contacts=[int(x)-1 for x in del_group.split(',')]
        for i in del_contacts:
            group[i]['Groups']=group[i]['Groups'].replace(f",{group_name}","")
        print(f"{len(del_contacts)} contacts deleted from group {group_name}.")
    else:
        new_group=input("Enter a name for the new group:")
        for contact in group:
            contact['Groups']+=f",{new_group}"
        print(f"{len(group)} contacts added to group {new_group}.")

def import_csv(filename:str):
    contacts=[]
    directory=input("Enter the directory path where your csv file is located (press enter to use current directory): ")
    try:
        with open(os.path.join(directory,filename+'.csv'),'r') as file:
        #with open(directory+'/'+filename,'r') as file:#opens file in reading regime
            reader=csv.DictReader(file)
            for row in reader:
                contact={field: row[field] for field in fields}
                contacts.append(contact)
        print("Contact added")
    except FileNotFoundError:
        print(f"File not found in {directory}. Please check the file name and directory path.")
    except Exception as e:
        print(f"An error occurred while importing the csv file: {e}")
    
    return contacts
def export_csv():#exports into csv by creating name the user saves it in a directory of choice
    global contacts
    filename = input("Enter the name of the file to export to (without .csv extension): ") + ".csv"
     # Път до директория
    directory = input("Enter the directory path to save the file (press enter to save in current directory): ")
    if directory:
        filename = os.path.join(directory, filename)
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact)
    print(f"Contacts have been exported to {filename}, csv.")
    
def save_txt():
    global contacts
    filename = input("Enter a name for the file: ")
    directory = input("Enter the directory to save the file: ")
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as file:
        for contact in contacts:
            for field in fields:
                file.write(f"{field}: {contact[field]}\n")
            file.write("\n")
    print(f"{len(contacts)} contacts saved in file {filepath}")
def save_contact(filename: str):
    global contacts
    name = input("Enter the name of the contact to save: ")
    for contact in contacts:
        if contact['Name'] == name:
            directory = input("Enter the directory to save the file: ")
            filename = input("Enter the name of the file: ")
            filepath = os.path.join(directory, f"{filename}.txt")
            with open(filepath, 'w') as file:
                for field in fields:
                    file.write(f"{field}: {contact[field]}\n")
                print(f"{name} saved to file {filepath}")
            return
    print(f"No contact with name {name} found.")
while True:
    input_operation()
