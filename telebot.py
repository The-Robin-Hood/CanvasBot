import requests
import json 
from datetime import datetime

#================ Bots info================#
def botinfo():
    with open('UserInfo.json') as f:
        teledata = json.load(f)
    return teledata
#================ Sends message to the Person ================#

def send_message(text, chat_id=botinfo()['Telegram']['ChatID']):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    requests.get(url)

#================ Resets and gets the updates of the messages ================#

def command(updateid=None):
    if updateid:
        url = URL+'getUpdates?offset='+str(updateid)
        requests.get(url)
    else:
        url = URL+'getUpdates'
        content = requests.get(url)
        js = json.loads(content.content.decode("utf8"))
        return js

#================ Last Chat from the telegram ================#
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    if num_updates > 0:
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        update_id = updates["result"][last_update]['update_id']
        update_id = int(update_id)+1
        command(update_id)
        return (text)

#================ Manual Mode Initialization and Termination ================#
def manual_Initialization():
    send_message(f"Manually Assign a session \nEnter the Class Name\n{CourseAlign()}\nrestart - To restart the process \nterminate - To Kill the process completely \nshutdown - To shutdown the system")
    while True:
        Last_Msg = get_last_chat_id_and_text(command())
        if Last_Msg in ['shutdown','restart','terminate']:
            break
        if Last_Msg in [i for i in botinfo()['Courses']]:
            print(botinfo()['Courses'][Last_Msg])
            return botinfo()['Courses'][Last_Msg]
        if Last_Msg in [str(x) for x in range(20)]:
            send_message("Enter the Course name not the number")
    return Last_Msg

def manual_termination():
    send_message("When Class gets over send command ('terminate') for end this current session")
    while True:
        Last_Msg = get_last_chat_id_and_text(command())
        if Last_Msg in ['terminate']:
            send_message("Manual Mode has been terminated and Automatic Mode has been initiated !!!")
            break
#================ Gets the day order ================#
def dayorder():
    send_message("Send the Day Order \nterminate - to exit")
    while True:
        dayorder = get_last_chat_id_and_text(command())
        if dayorder != None:
            if dayorder in [x for x in botinfo()['DayOrder']]:
                dayorder = int(dayorder)
                dayorder = dayorder-1
                break
            elif dayorder =='terminate':
                    send_message("Process Terminated")
                    exit()
            else:
                DO =[x for x in botinfo()['DayOrder']]
                send_message(f"Send the Dayorder {DO}")
    return dayorder

#================ Course Align For message ================#
def CourseAlign():
    Bot = ''
    for j,i in enumerate(botinfo()['Courses']):
        Bot += str(j+1)+ ". " + i +'\n'
    return Bot

URL = "https://api.telegram.org/bot"+botinfo()['Telegram']['BotID']+'/'