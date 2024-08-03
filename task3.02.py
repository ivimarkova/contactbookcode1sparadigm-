import calendar
import time
import os
import csv
#notification
#fields=['Name','Mobile phone','Groups','Company','Other phones','Emails','Melody','Other']
#fields = ['Name', 'Mobile phone', 'Company', {'Company': ['Name of a company', 'Occupation', 'Address', 'Web page']}, {'Other phones': ['Mobile phone 2', 'Mobile phone 3', 'Home phone', 'Office phone']}, {'Emails': ['Private email 1', 'Private email 2', 'Office email']}, 'Melody', {'Other': ['Address', 'Birth day', 'Notes', {'Spouse': ['Name', 'Birthday', 'Notes']}, {'Children': ['Name', 'Birthday', 'Notes']}]}]
fields = ['Name', 'Mobile phone', 'Company', {'Company': ['Name of a company', 'Occupation', 'Address', 'Web page']}, {'Other phones': ['Mobile phone 2', 'Mobile phone 3', 'Home phone', 'Office phone']}, {'Emails': ['Private email 1', 'Private email 2', 'Office email']}, 'Melody', {'Other': ['Address', 'Birth day', 'Notes', {'Spouse': ['Name', 'Birthday', 'Notes']}, {'Children': ['Name', 'Birthday', 'Notes']}]}]
today=time.localtime()
current_month = today.tm_mon
current_day = today.tm_mday
#sort the csv /text file
contacts=[]#initialize an empty list to store contacts
def input_operation():
    global contacts#use the global contacts list in the functions
    opr=int(input("1.Add new contact \n 2.Delete contact \n 3.Update contact \n 4.View birthday reminder\n 5.Create contact group \n 6. Delete contact group\n 7.Import contacts from csv file\n 8.Export contacts into csv file\n 9.Save contact/s into text file\n :"))
    try:
        if opr==1:
            add_contact(fields)
        elif opr==2:
            delete_contact()
        elif opr==3:
            update_contact()
        elif opr==4:
            birthday_reminder()
        elif opr==5:
            opr_group()
        elif opr==6:
            opr_group(delete_group=True)
        elif opr==7:
            filename=input("Write the name of your file:")
            contacts=import_csv(filename)
        elif opr==8:
            export_csv()
        elif opr==9:
            save_txt()
        else:
            print("Invalid input. Please enter a valid number.")
            pass
    except ValueError:
        print("Please enter a number from the list")
    except FileNotFoundError:
        print("File not found.Please check the file name.")
def add_contact(fields):
    global contacts
    contact={}
    for field in fields:
        if isinstance(field, str):
            if field == 'Melody':
                melodies = ['melody1', 'melody2', 'melody3']  # replace with your list of melodies
                print('Available melodies:')
                for i, melody in enumerate(melodies):
                    print(f'{i+1}. {melody}')
                while True:
                    try:
                        melody_index = int(input('Select a melody by its number: '))
                        if not melody_index:
                            contact[field] = melodies[0]  # set default melody to the first melody in the list
                        elif not 1 <= melody_index <= len(melodies):
                            print("ERROR: Invalid input. Please enter a valid melody index.")
                        else:
                            contact[field] = melodies[melody_index - 1]
                            break
                        melody_index = int(melody_index) - 1
                        contact[field] = melodies[melody_index]
                        break
                    except IndexError:
                        print("ERROR: Invalid input. Please enter a valid melody index.")
                    except ValueError:
                        print("ERROR: Invalid input. Please enter a valid melody index as a number.")
            elif field == 'Company':
                company_dict = {}
                for sub_field in field.values():
                    sub_value = input(f"Enter {sub_field}: ")
                    company_dict[sub_field] = sub_value
                    contact[field] = company_dict
            else:
                value=input(f"Enter {field}:")
                contact[field]=value
        else:
            sub_dict = {}
            sub_fields = list(field.values())[0]
            for sub_field in sub_fields:
                sub_value = input(f"Enter {sub_field}:")
                sub_dict[sub_field] = sub_value
            #contact_str = str(sub_dict)  # convert nested dictionary to string
            contact[list(field.keys())[0]] = sub_dict
    contacts.append(contact)
    print("Contact added successfully!")

def delete_contact():
    global contacts
    print("Your current contacts are:", contacts)
    name=input("Enter the name of the contact to delete:")
    for contact in contacts:
        if contact['Name']==name:
            contacts.remove(contact)
            print(f"{name} has been deleted.")
    return
    print(f"{name} not found.")
def update_contact():
    global contacts
    name=input("Enter the name of the contact to update:")
    for contact in contacts:
        if contact['Name']==name:
            print("Your current info:")
            for field in fields:
                if isinstance(field, str):
                    if field == 'Melody':
                        melodies = ['melody1', 'melody2', 'melody3']  # replace with list of melodies
                        print('Available melodies:')
                        for i, melody in enumerate(melodies):
                            print(f'{i+1}. {melody}')
                        while True:
                            try:
                                melody_index = int(input('Select a melody by its number: '))
                                if not melody_index:
                                    contact[field] = melodies[0]  # set default melody to the first melody in the list
                                    break
                                elif not 1 <= melody_index <= len(melodies):
                                    print("ERROR: Invalid input. Please enter a valid melody index.")
                                else:
                                    contact[field] = melodies[melody_index - 1]
                                    break
                                melody_index = int(melody_index) - 1
                                contact[field] = melodies[melody_index]
                                break
                            except IndexError:
                                print("ERROR: Invalid input. Please enter a valid melody index.")
                            except ValueError:
                                print("ERROR: Invalid input. Please enter a valid melody index as a number.")#
                    elif field == 'Company':
                        company_dict = {}
                        for sub_field in field.values():
                            sub_value = input(f"Enter {sub_field}: ")
                            company_dict[sub_field] = sub_value
                            contact[field] = company_dict
                    else:
                        value = input(f"Enter new {field}: ")
                        contact[field] = value
                else:
                    sub_dict = contact[list(field.keys())[0]]
                    for sub_field in sub_dict:
                        sub_value = input(f"Enter new {sub_field}: ")
                        sub_dict[sub_field] = sub_value
                    contact[list(field.keys())[0]] = sub_dict
    print("The contact was successfully updated.")
    return
def birthday_reminder():
    global contacts
    current_month=calendar.month_name[time.localtime().tm_mon]
    for contact in contacts:
        if 'Birthday' in contact.keys():
            bday=contact['Birthday'].split('/')
            if bday[1]==current_month:
                print(f"{contact['Name']} has birthday on {bday[1]} {bday[0]}.")
def opr_group(delete_group=False):
    global contacts
    group=[]
    print("Your current groups are:", group)
    group_name=input("Enter the name of the group:")
    for contact in contacts:
        if group_name in contact['Groups'].split(","):
            group.append(contact)
        if not group:
            print(f"No contacts found in group{group_name}.")
            return
    print(f"Contacts in group{group_name}:")
    for i, contact in enumеrate(group):#the process of extracting information from the Active Directory 
        print(f"{i+1}.{contact['Name']}")
        if delete_group:
            d_group=input(f"Select contacts to delete from group{group_name}(comma-separated list):")#comma separated numbers?
            d_contacts=[int(x-1) for x in d_group.split(',')]
            for i in d_contacts:
                group[i]['Groups']=group[i]['Groups'].replace(f",{group_name}","")
            print(f"{len(d_contacts)} contacts deleted from group{group_name}.")
        else:
            new_group=input("Enter a name for the group:")
            for contact in group:
                contact['Group']+=f",{new_group}"
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
