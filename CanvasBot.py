from selenium import webdriver
import time
import datetime
import json,os

def Courses(x):
    for Course in data['Courses']:
        if x == data['Courses'][Course]:
            return Course
#================ Time Checking Function ================#

def time_between(start,end):
    start = datetime.time(start[0],start[1])
    end = datetime.time(end[0],end[1])
    check_time = datetime.datetime.now().time()
    return check_time >= start and check_time <= end

#================== Checks For Current Period =====================#
def Period_Checker():
    for Period in Periods:
        start = [Period[0][0],Period[0][1]]
        end = [Period[1][0],Period[1][1]]
        if time_between(start, end):
            current_Period = Period[2]
            current_session = Time_Table[dayorder][current_Period]
            return current_session

def get_key(val):
    for key, value in data['Courses'].items():
         if val == value:
             return key

#================ LOGIN SESSION ================#
def login():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://canvas.instructure.com/")
    email = driver.find_element_by_id('pseudonym_session_unique_id')
    email.send_keys(EMAIL)

    password = driver.find_element_by_id('pseudonym_session_password')
    password.send_keys(PASSWORD)

    stay_signed = driver.find_element_by_id('pseudonym_session_remember_me')
    stay_signed.click()

    password.submit()

#================== Canvas Automated Work =====================#
def canvas(course,manual=False):
    global past_session
    login()
    telebot.send_message("{} Class initiated".format(Courses(past_session)))
    driver.get(f"https://canvas.instructure.com/courses/{course}?view=feed")
    driver.find_element_by_xpath('//*[@id="___reactour"]/div[4]/div/div/div/span[1]/span/button').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="___reactour"]/div[4]/div/div/div/span[1]/span/button').click()
    flag = False
    for i in range(3):
        try:
            driver.find_element_by_xpath('//*[@id="course_home_content"]/div[2]/div[2]/div[2]/a').click()
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(30)
            print(driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/div/span/button[2]').click())
            telebot.send_message("{} is being attended".format(Courses(past_session)))
            flag = True
            break
        except:
            time.sleep(1)
            driver.refresh()
    if not flag:
        telebot.send_message("{} is doesnt having join option".format(Courses(past_session)))
        driver.close()
        return "Manual"
    if flag:
        while True:
            if manual:
                telebot.manual_termination()
                driver.close()
                break
            if not Period_Checker():
                telebot.send_message("All Classes has been Completed")
                break
            if past_session != Period_Checker():
                telebot.send_message("{} is been over".format(Courses(past_session)))
                driver.close()
                past_session = Period_Checker()
                canvas(Period_Checker())
            else:
                print(Courses(Period_Checker())+" is on live",end='\r')
        

        

#================== main =====================#
def main():
    global past_session
    while True:
        if Period_Checker() :
            print(Period_Checker())
            past_session = Period_Checker()
            print(f"{Courses(past_session)}")
            mode = canvas(past_session)
            if mode == 'Manual':
                val = telebot.manual_Initialization()
                if val in ['restart']:
                    telebot.send_message("Process is restarted. Switching to Automatic Mode")
                    break
                elif val == 'shutdown':
                    import os
                    os.system('shudown /s')
                    telebot.send_message("Shutting Down the System")
                    exit()
                else:
                    past_session = val
                    canvas(past_session,manual=True)
        else:
            telebot.send_message("No Class at this Time")
            val = telebot.manual_Initialization()
            if val in ['terminate']:
                telebot.send_message("Process is terminated. Will be initiated by tomorrow")
                exit()
            elif val == 'shutdown':
                    import os
                    os.system('shudown /s')
                    telebot.send_message("Shutting Down the System")
                    exit()
            else:
                past_session = globals()[val]
                canvas(past_session,manual=True)

#==================== User details ===========================#
if not os.path.exists('UserInfo.json'):
    print("This Information Extraction Happens Only Once !!!!\n")
    import info 
    info.Collector()
else:
    with open('UserInfo.json') as f:
        data = json.load(f)

import telebot
from num2words import num2words
EMAIL = data['Login']['Email']
PASSWORD = data['Login']['Password']

Periods=[]
for i in range(len(data['TimeAllotment'])):
    temp = num2words(i+1,'ordinal')
    exec("%s = %s" % (temp,data['TimeAllotment']['{}'.format(i+1)]))
    Periods.append(globals()[temp])





for num , i in enumerate(Periods):
    i.append(num)

Time_Table =[]
for i in data['DayOrder']:
    Time_Table.append(data['DayOrder'][i])

for x , i in enumerate(Time_Table):
    for y , j in enumerate(i):
        Time_Table[x][y] = data['Courses'][j]

print(Time_Table)
#==================== initialization  ===========================#


while True:
    if datetime.datetime.today().weekday() != 4:
        dayorder = telebot.dayorder()
        main()
        time.sleep(3)


