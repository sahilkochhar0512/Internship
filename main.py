import csv
import subprocess
import schedule
import datetime
from datetime import date
import shutil
from itertools import zip_longest
import NPi.GPIO as GPIO
pin1=11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
list1=[]
def createcsv(data):
    list1.append(data)
    d=[list1]
    exp_data=zip_longest(*d, fillvalue='')
    with open('first129.csv' , 'w', encoding='UTF8', newline='') as myfile:
        wr=csv.writer(myfile)
        wr.writerows(exp_data)
    myfile.close()
def sending():
    destination="/home/pi/files/"+str(date.today())+".csv"
    shutil.copy("/home/pi/first129.csv", destination, follow_symlinks=True)
    subprocess.run(["scp", "first129.csv", "pi@192.168.179.11:first129.csv"])
    with open('first129.csv' , 'w', encoding='UTF8', newline='') as myfile:
        myfile.truncate()
    myfile.close()
GPIO.add_event_detect(pin1, GPIO.RISING)
schedule.every().day.at("16:00").do(sending)
while True:
    schedule.run_pending()
    if GPIO.event_detected(pin1):
        data=str(datetime.datetime.now())
        createcsv(data)
