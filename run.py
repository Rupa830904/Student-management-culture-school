# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
"""Import python modules"""
import gspread
import pandas as pd
import json
import os
import time
from google.oauth2.service_account import Credentials
from colorama import just_fix_windows_console
from colorama import Fore, Back, Style
from email_validator import validate_email, EmailNotValidError
from datetime import date, datetime, timedelta
from pandas import json_normalize
from pandas import read_json
'''if os.path.exists("env.py"):
    import env'''

just_fix_windows_console()

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('dance_students')


def main_menu():
    """
    Displays the main menu icon in the terminal
    """

    os.system('clear')
    print(Fore.CYAN + "MAIN MENU")
    print("********")
    print("1. Students Menu")
    print("2. Course Menu")
    print("3. Exit")
    print("*********")
    while True:
        try:
            choice = int(input("Enter Choice: \n"))
        except ValueError:
            print("You didn't enter a number !")
            continue

        if choice == 1:
            students()
            break
        elif choice == 2:
            course()
            break
        elif choice == 3:
            quit()
        else:
            print("Invalid choice !!!")


def students():
    """
    Display Student manage options.
    """

    os.system('clear')
    print(Fore.GREEN + "STUDENT MANAGEMENT")
    print("*********")
    print("1. Add new student")
    print("2. Update Student Info")
    print("3. Find a student")
    print("4. Remove student")
    print("0. Main Menu")
    print("*********")

    while True:
        choice = input("Enter Choice: \n")
        if choice == "1":
            add_new_student()
            break
        elif choice == "2":
            update_student()
            break
        elif choice == "3":
            find_student()
            break
        elif choice == "4":
            del_student()
            break
        elif choice == "0":
            main_menu()
            break
        else:
            print("Invalid choice !!!")


def add_new_student():
    print(Fore.WHITE + "Enter Name,PersonalNumber(YYYYMMDDxxxx),Mobile, Email")
    print("Example:John,197908167777,76895600000,john@xxxx.com")
    data_str = input("Enter your data here:")
    list_student = SHEET.worksheet('student')
    student_data = data_str.split(",")  # the values should be a list
    student_cell = list_student.find(student_data[0])
    while student_cell is not None:
        print(f"Student already exists.Please try again!")
        quit()
    print(student_data[1])
    pn_str = student_data[1]
    pn_substr = pn_str[0:8]
    print(pn_substr)
    '''pn_str = student_data[1]'''

    while True:
        try:
            int(student_data[1])
            break
        except ValueError:
            print("Personal number can only be digits !")
            quit()
    while True:
        try:
            int(student_data[2])
            break
        except ValueError:
            print("Mobile number can only be digits !")
            quit()
    while True:
        try:
            # validate and get info
            validate_email(student_data[3])
            break
        except EmailNotValidError as e:
            print(str(e))
            quit()
    while True:
        try:
            datetime.strptime(pn_substr, '%Y%m%d')
            break
        except ValueError:
            print("Personal number must start with 'YYYYMMDD'!")
            quit()
    while True:
        try:
            check_len(pn_str)
            break
        except ValueError:
            print("Personal number must be of 12 digit!")
    list_student.append_row(student_data, table_range="A1:D1")
    print(f"Student info updated successfully")
    input("\nPress any key to continue...\n")
    students()


def check_len(str):
    if len(str) != 12:
        print("Personal number must be of 12 digits")
        quit()


def del_student():
    unstrip_name_str = input("Plaese enter Name the name of the student:")
    name_str = unstrip_name_str.strip()  # Strip the user input
    list_student = SHEET.worksheet('student')
    student_course = SHEET.worksheet('course')
    student_cell = list_student.find(name_str)
    course_cell = student_course.find(name_str)
    print(course_cell)
    while student_cell is None:
        name_str = input("Please enter the valid student name to remove:")
        student_cell = list_student.find(name_str)
    row_num = student_cell.row
    if course_cell is None:
        list_student.delete_rows(row_num)
        print(f"Student {name_str} has been removed.")
    else:
        print(f"Student {name_str} must be unregistred from course first.")
    input("\nPress any key to continue...\n")
    students()


def update_student():

    os.system('clear')

    while True:
        list_student = SHEET.worksheet('student')
        data = list_student.get_all_values()
        df = pd.DataFrame(data, columns=['', '', '', ''])
        print(df)
        name_str = input("Please choose the student to update info:")
        cell = list_student.find(name_str)
        while cell is None:
            name_str = input("Choose the valid student from table:")
            cell = list_student.find(name_str)
        row_num = cell.row
        print("1. Update Mobile No")
        print("2. Update Email")
        choice = input("Enter Choice: \n")
        if choice == "1":
            mobile_str = input("Please enter new mobile:")
            list_student.update_cell(row_num, 3, mobile_str)
            print(f"Mobile Number registered successfully")
            break
        elif choice == "2":
            mail_str = input("Please enter new email:")
            list_student.update_cell(row_num, 4, mail_str)
            print(f"Email registered successfully")
            break
    input("\nPress any key to continue...\n")
    students()


def find_student():

    os.system('clear')

    while True:
        list_student = SHEET.worksheet('student')
        name_str = input("Please type the student name to search:")
        cell = list_student.find(name_str)
        if cell is None:
            print(f"{name_str} is not a valid student in culture school")
            return
        else:
            student_info = list_student.get_all_values()
            df = pd.DataFrame(student_info, columns=['Name', 'PersonalNumber', 'Mobile', 'Email'])
            row = df.loc[df['Name'] == name_str]
            print(row)
            return


def json_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} is not serializable')


def course():
    """
    Display course registration options.
    """

    os.system('clear')
    print("COURSE MENU")
    print("*********")
    print("1. Register Student")
    print("2. Unregister Student")
    print("3. Search Registered course")
    print("0. Main Menu")
    print("*********")

    while True:
        choice = int(input("Enter Choice: \n"))
        if choice == 1:
            register_course()
            break
        elif choice == 2:
            unregister_course()
            break
        elif choice == 3:
            search_register_course()
            break
        elif choice == 0:
            main_menu()
            break
        else:
            print("Invalid choice !!!")


def register_course():
    unstrip_name_str = input(Fore.GREEN + "Enter student name to register:")
    name_str = unstrip_name_str.strip()  # Strip the user input
    classical_col = 1  # Column for classical course
    modern_col = 2  # Column for modern course
    '''date_col = 3'''
    '''today = datetime.now()'''
    '''date_str = json.dumps({today}, default=json_serializer)'''
    '''date_str = type(date_json_str)'''
    unstrip_course_str = input("Course to register(Classical/Modern/Both):")
    course_str = unstrip_course_str.strip()  # Strip the user input
    student_course = SHEET.worksheet('course')
    classical_cell = student_course.find(query=name_str, in_column=1)
    modern_cell = student_course.find(query=name_str, in_column=2)
    if course_str == "Classical":
        if classical_cell is None:
            if modern_cell is None:
                last_row = len(student_course.get_all_values())
                student_course.update_cell(last_row + 1, classical_col, name_str)
                student_course.update_cell(last_row + 1, modern_col, '')
                '''student_course.update_cell(last_row + 1, date_col, today)'''
                print(f"Student registered successfully")
            else:
                row_num = modern_cell.row
                student_course.update_cell(row_num, classical_col, name_str)
                '''student_course.update_cell(row_num, date_col, today)'''
                print(f"Student registered successfully")
        else:
            print(f"Student is already registered to {course_str}")
    elif course_str == "Modern":
        if modern_cell is None:
            if classical_cell is None:
                last_row = len(student_course.get_all_values())
                student_course.update_cell(last_row + 1, classical_col, '')
                student_course.update_cell(last_row + 1, modern_col, name_str)
                '''student_course.update_cell(last_row + 1, date_col, today)'''
                print(f"Student registered successfully")
            else:
                row_num = classical_cell.row
                student_course.update_cell(row_num,  modern_col, name_str)
                student_course.update_cell(row_num, date_col, today)
                '''print(f"Student registered successfully")'''
        else:
            print(f"Student is already registered to {course_str}")
    elif course_str == "Both":
        student_course = SHEET.worksheet('course')
        last_row = len(student_course.get_all_values())
        student_course.update_cell(last_row + 1, classical_col, name_str)
        student_course.update_cell(last_row + 1, modern_col, name_str)
        student_course.update_cell(last_row + 1, date_col, today.strftime('%Y-%m-%d %H:%M:%S.%f'))
        print(f"Student registered successfully")
    else:
        print(f"Sorry we don't have that course yet")
    return


def unregister_course():
    unstrip_name_str = input(Fore.RED + "Enter student name to unregister:")
    name_str = unstrip_name_str.strip()  # Strip the user input
    unstrip_course_str = input(Fore.RED + "Unregister(Classical/Modern/Both):")
    course_str = unstrip_course_str.strip()  # Strip the user input
    student_course = SHEET.worksheet('course')
    cell = student_course.find(name_str)
    print(cell)
    while cell is None:
        print(f"Please enter a valid student name")
        name_str = input("Please enter the valid student name to unregister:")
        cell = student_course.find(name_str)
    row_num = cell.row
    if course_str == "Classical":
        classical_cell = student_course.find(query=name_str, in_column=1)
        modern_cell = student_course.find(query=name_str, in_column=2)
        if classical_cell is None:
            print(f" {name_str} is not registered in {course_str}")
        elif modern_cell is None:
            row_num_1 = classical_cell.row
            student_course.delete_rows(row_num_1)
            print(f" {name_str} unregistered successfully from {course_str}")
        else:
            row_num_1 = classical_cell.row
            student_course.update_cell(row_num_1, 1, '')
            print(f" {name_str} unregistered successfully from {course_str}")
    elif course_str == "Modern":
        classical_cell = student_course.find(query=name_str, in_column=1)
        modern_cell = student_course.find(query=name_str, in_column=2)
        if modern_cell is None:
            print(f" {name_str} is not registered in {course_str}")
        elif classical_cell is None:
            row_num_2 = modern_cell.row
            student_course.delete_rows(row_num_2)
            print(f" {name_str} unregistered successfully from {course_str}")
        else:
            row_num_2 = modern_cell.row
            student_course.update_cell(row_num, 2, '')
            print(f" {name_str} unregistered successfully from {course_str}")
    elif course_str == "Both":
        student_course.delete_rows(row_num)
        print(f" {name_str} has been unregistered successfully")


def search_register_course():

    os.system('clear')

    while True:
        student_course = SHEET.worksheet('course')
        name_str = input("Please type the student name to search:")
        cell = student_course.find(name_str)
        classical_cell = student_course.find(query=name_str, in_column=1)
        modern_cell = student_course.find(query=name_str, in_column=2)
        course_info = student_course.get_all_values()
        df = pd.DataFrame(course_info, columns=['Classical', 'Modern'])
        if cell is None:
            print(f"{name_str} Invalid student or not registered to a course.")
        elif modern_cell is None:
            row = df.loc[df['Classical'] == name_str]
            print(row)
        elif classical_cell is None:
            row = df.loc[df['Modern'] == name_str]
            print(row)
        else:
            row = df.loc[df['Classical'] == name_str]
            print(row)
        return


def main():
    """
    Run all program functions
    """
    main_menu()


print("\n\nWelcome to Culture school Student Management.\n")
main()
