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
    print("MAIN MENU")
    print("********")
    print("1. Get Students Info")
    print("2. Students Menu")
    print("3. Course Menu")
    print("4. Remove Student")
    print("5. Exit")
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
            break
        elif choice == 2:
            students()
            break
        elif choice == 3:
            course()
            break
        elif choice == 5:
            quit ()
            break
        else:
            print("Invalid choice !!!")
def students():
    """
    Display Student manage options.
    """

    os.system('clear')
    print("STUDENT MANAGEMENT")
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
            print(" you choose remove")
            break
        elif choice == 0:
            main_menu()
            break
        else:
            print("Invalid choice !!!")

def add_new_student():
    print("Plaese enter Name,PersonalNumber(YYYYMMDDxxxx),Mobile No.(10 digits) and Email for the student")
    print("Example:John,197908167777,76895600000,john@xxxx.com")
    data_str = input("Enter your data here:")
    course_data=data_str.split(",") #the values should be a list
    student_course = SHEET.worksheet('student')
    student_course.append_row(course_data, table_range="A1:D1")
    print(f"Student info updated successfully")


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
    print("Plaese enter student name to register for course.")
    print("Plaese enter course name(classical/modern):")
    print("Example:John,classical")
    data_str = input("Enter your data here:")
    course_data=data_str.split(",") #the values should be a list
    student_course = SHEET.worksheet('course')
    student_course.append_row(course_data, table_range="A1:B1")
    print(f"Student registered successfully")
def unregister_course():
    print("Plaese enter student name to unregister from course.")
    '''print("Plaese enter course name(classical/modern):")'''
    print("Example:John,classical")
    data = input("Enter your data here:")
    student_course = SHEET.worksheet('course')
    cell = student_course.find(data)
    while cell == None:
       print(f"Please enter a valid student name")
       data = input("Enter your data here:")
       cell = student_course.find(data)
    row_num = cell.row
    student_course.delete_rows(row_num)
    print(f" {data} has been unregistered successfully")

def main():
    """
    Run all program functions
    """
    main_menu()


print("\n\nWelcome to Student Management for Indian Dance class in culture school.\n")
main()