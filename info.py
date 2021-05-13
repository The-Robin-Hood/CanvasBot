#Collects The information About the user
import os ,json

def clrsc():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system('clear')

def login_ID():
    clrsc()
    Email = input("Enter your Email(Canvas-Instructure) : ")
    Pswd = input("Enter your Password : ")
    info = {}
    info['Email']=Email
    info['Password']=Pswd
    return info

def courses():
    clrsc()
    No_Course = int(input("Enter the Number Of Courses : "))
    Courses = {}
    for i in range(No_Course):
        CourseName = input(f"Enter the Course {i+1} name : ")
        if i==0:
            print("\n !!! You Need to find the Particular Course Code !!!  \n\n Enter into canvas site and get into your Course in any browser \n At the Url you could find a link like 'https://canvas.instructure.com/courses/1234567' \n '123456' is Course Code \n")
        CourseCode = input(f"Enter the {CourseName} Course Code : ")
        clrsc()
        Courses[CourseName]=CourseCode
    return Courses

def telegram_infos():
    clrsc()
    BotID = input("Enter Your Bots ID : ")
    ChatID = int(input("Enter Your Chat ID : "))
    info={}
    info['BotID']=BotID
    info['ChatID']=ChatID
    return info

def DayOrder():
    clrsc()
    No_DayOrder = int(input("Enter the Number of Day orders : "))
    No_Periods = int(input('Enter the number of periods : '))
    info = {}
    for i in range(No_DayOrder):
        list = []
        clrsc()
        print("Following are the given courses : ")
        for periods in data['Courses']:
            print(periods)
        for j in range(No_Periods):
            Period = input(f"Enter the Period {j+1} of DayOrder {i+1} : ")
            list.append(Period)
        info[i+1]=list
    return info

def time_duration():
    clrsc()
    Time = {}
    for i in range(len(data['DayOrder'][1])):
        clrsc()
        start_time = input(f"Enter Period {i+1} Start time in HH:MM (Ex: 14:30 - 24hrs format) => ") 
        start = [int(j) for j in start_time.split(":")]
        end_time = input(f"Enter Period {i+1} End time in HH:MM (24hrs format) => ") 
        end = [int(j) for j in end_time.split(":")]
        Time[i+1]=[start,end]
    return Time

def Collector():
    global data
    data={}
    data['Login']=login_ID()
    data['Courses']=courses()
    data['DayOrder']=DayOrder()
    data['TimeAllotment']=time_duration()
    data['Telegram']=telegram_infos()
    out_file = open("UserInfo.json", "w") 
    json.dump(data,out_file,indent = 3)

Collector()

