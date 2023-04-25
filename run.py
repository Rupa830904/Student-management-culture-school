# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
"""Import python modules"""
import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime, timedelta
import pandas as pd
import json
from pandas import json_normalize
from pandas import read_json
if os.path.exists("env.py"):
    import env
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Back, Style


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
    print("1. Get Students Info")
    print("2. Students Menu")
    print("3. Course Menu")
    print("4. Exit")
    print("*********")
    while True:
        try:
            choice = int(input("Enter Choice: \n"))
        except ValueError:
            print("You didn't enter a number !")
            continue

        if choice == 1:
            list_student = SHEET.worksheet('student')
            data = list_student.get_all_values()
            df = pd.DataFrame(data,columns=['','','',''])
            print(df)
            continue
        elif choice == 2:
            students()
            break
        elif choice == 3:
            course()
            break
        elif choice == 4:
            quit ()
            break
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
    print("2. List Students")
    print("3. Remove student")
    print("0. Main Menu")
    print("*********")

    while True:
        choice = input("Enter Choice: \n")
        if choice == "1":
            add_new_student()
            break
        elif choice == "2":
            list_student = SHEET.worksheet('student')
            data = list_student.col_values(1)
            print(data)
            break
        elif choice == "3":
            del_student()
            break
        elif choice == "0":
            main_menu()
            break
        else:
            print("Invalid choice !!!")

def add_new_student():
    print(Fore.WHITE + "Plaese enter Name,PersonalNumber(YYYYMMDDxxxx),Mobile No.(10 digits) and Email for the student")
    print("Example:John,197908167777,76895600000,john@xxxx.com")
    data_str = input("Enter your data here:")
    course_data=data_str.split(",") #the values should be a list
    list_student = SHEET.worksheet('student')
    list_student.append_row(course_data, table_range="A1:D1")
    print(f"Student info updated successfully")

def del_student():
    name_str = input("Plaese enter Name the name of the student:")
    list_student = SHEET.worksheet('student')
    cell = list_student.find(name_str)
    while cell == None:
       name_str = input("Please enter the valid student name to remove:")
       cell = list_student.find(name_str)
    row_num = cell.row
    list_student.delete_rows(row_num)
    print(f"Student {name_str} has been removed.")
    

def course():
    """
    Display course registration options.
    """

    os.system('clear')
    print("COURSE MENU")
    print("*********")
    print("1. Register Student")
    print("2. Unregister Student")
    print("0. Main Menu")
    print("*********")

    while True:
        choice = int (input("Enter Choice: \n"))
        if choice == 1:
            register_course()
            break
        elif choice == 2:
            unregister_course()
            break
        elif choice == 0:
            main_menu()
            break
        else:
            print("Invalid choice !!!")

def register_course():
    unstrip_name_str = input(Fore.GREEN + "Please enter the student name to register:")
    name_str = unstrip_name_str.strip() # Strip the user input
    classical_col = 1  # Column for classical course
    modern_col = 2  # Column for modern course
    unstrip_course_str = input("Please enter the course name to register(Classical/Modern/Both):")
    course_str = unstrip_course_str.strip() # Strip the user input
    if course_str == "Classical":
       student_course = SHEET.worksheet('course')
       last_row = len(student_course.get_all_values())
       student_course.update_cell(last_row + 1, classical_col, name_str)
       student_course.update_cell(last_row + 1, modern_col, '')
       print(f"Student registered successfully")
    elif course_str == "Modern":
       student_course = SHEET.worksheet('course')
       last_row = len(student_course.get_all_values())
       student_course.update_cell(last_row + 1, classical_col, '')
       student_course.update_cell(last_row + 1, modern_col, name_str)
       print(f"Student registered successfully")
    elif course_str == "Both":
       student_course = SHEET.worksheet('course')
       last_row = len(student_course.get_all_values())
       student_course.update_cell(last_row + 1, classical_col, name_str)
       student_course.update_cell(last_row + 1, modern_col, name_str)
       print(f"Student registered successfully")
    else :
        print(f"Sorry we don't have that course yet")

    
def unregister_course():
    unstrip_name_str = input(Fore.RED + "Please enter the student name to unregister:")
    name_str = unstrip_name_str.strip() # Strip the user input
    unstrip_course_str = input(Fore.RED + "Course to unregister(Classical/Modern/Both):")
    course_str = unstrip_course_str.strip() # Strip the user input
    student_course = SHEET.worksheet('course')
    cell = student_course.find(name_str)
    print (cell)
    while cell.value == None:
       print(f"Please enter a valid student name")
       name_str = input("Please enter the valid student name to unregister:")
       cell = student_course.find(name_str)
    '''row_num = cell.row'''
    
    if course_str == "Classical":
       classical_cell = student_course.find(query=name_str, in_column=1)
       modern_cell = student_course.find(query=name_str, in_column=2)
       if modern_cell == None:
        row_num_1 = classical_cell.row
        student_course.delete_rows(row_num_1)
        print(f" {name_str} has been unregistered successfully {course_str}")
       else:   
        row_num_1 = classical_cell.row
        student_course.update_cell(row_num_1,1,'')
        print(f" {name_str} has been unregistered successfully from {course_str}")
       '''print(cell)
       row_num = cell.row
       print(row_num)'''
    elif course_str == "Modern":
       classical_cell = student_course.find(query=name_str, in_column=1)
       modern_cell = student_course.find(query=name_str, in_column=2)
       if classical_cell == None:
        row_num_2 = modern_cell.row
        student_course.delete_rows(row_num_2)
        print(f" {name_str} has been unregistered successfully {course_str}")
       else:
        row_num_2 = modern_cell.row
        student_course.update_cell(row_num,2,'')
        print(f" {name_str} has been unregistered successfully from {course_str}")
    elif course_str == "Both":
     student_course.delete_rows(row_num)
     print(f" {name_str} has been unregistered successfully")

def main():
    """
    Run all program functions
    """
    main_menu()


print("\n\nWelcome to Student Management for Indian Dance class in culture school.\n")
main()