import binascii
import hashlib
import hmac
import json
import pycurl
import time
import base64
from Crypto.Cipher import AES
import re
from io import BytesIO


AES_KEY = '...'
TOKEN = '...'
key = '2Wq7)qkX~cp7)H|n_tc&o+:G_USN3/-uIi~>M+c ;Oq]E{t9)RC_5|lhAA_Qq%_4'
PRIVATE_KEY = 2615678
time = str(int(time.time()))
number='+38093.......'

def decrypt(AES_KEY, encrypted):
    d = base64.b64decode(encrypted)
    cipher = AES.new(binascii.unhexlify(AES_KEY), AES.MODE_ECB)
    decrypted = cipher.decrypt(d).decode("utf-8")
    decrypted = re.sub(r"}]}}.*$", "}]}}}}",str(decrypted))
    decrypted = re.sub(r"^b'", "", decrypted)
    return decrypted


def encrypt (AES_KEY, clear):
    __pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
    cipher = AES.new(binascii.unhexlify(AES_KEY), AES.MODE_ECB)
    decrypted = cipher.encrypt(__pad(clear))
    #print(decrypted.decode('utf-8'))
    return decrypted


def Send_Post(post_url, post_data, signature):
    global time, TOKEN
    response = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, post_url)
    if post_data != "":
        crl.setopt(crl.POST, 1)
        crl.setopt(crl.POSTFIELDS, post_data)
    crl.setopt(crl.SSL_VERIFYPEER, False)
    crl.setopt(crl.HTTPHEADER, [
         "X-App-Version: 4.9.1",
         "X-Token: " + TOKEN,
         "X-Os: android 5.0",
         "X-Client-Device-Id: 14130e29cebe9c39",
         "Content-Type: application/json; charset=utf-8",
         "Accept-Encoding: deflate",
         "X-Req-Timestamp: " + time,
         "X-Req-Signature: " + signature,
         "X-Encrypted: 1"])
    crl.setopt(crl.TIMEOUT, 60)
    crl.setopt(crl.WRITEDATA, response)
    crl.perform()
    crl.close()
    data = response.getvalue()
    return data.decode('utf8')

def GetByPhone(phone):
    global time, TOKEN, key, AES_KEY
    req='{"countryCode":"RU","source":"search","token":"' + TOKEN + '","phoneNumber":"' + number + '"}'
    string = (str(time) + '-' + req)
    signature = base64.b64encode(hmac.new(key.encode(), string.encode(), hashlib.sha256).digest())
    crypt_data =base64.b64encode(encrypt(AES_KEY, req))
    zprs = Send_Post("https://pbssrv-centralevents.com/v2.5/search", '{"data":"'+ str(crypt_data.decode('utf-8')) +'"}', str(signature.decode('utf-8')))
    struct = json.loads(zprs)
    return struct["data"]


def GetByPhoneTags(phone):
    global time, TOKEN, key, AES_KEY
    req='{"countryCode":"RU","source":"details","token":"' + TOKEN + '","phoneNumber":"' + number + '"}'
    string = (str(time) + '-' + req)
    signature = base64.b64encode(hmac.new(key.encode(), string.encode(), hashlib.sha256).digest())
    crypt_data =base64.b64encode(encrypt(AES_KEY, req))
    zprs = Send_Post("https://pbssrv-centralevents.com/v2.5/number-detail", '{"data":"'+ str(crypt_data.decode('utf-8')) +'"}', str(signature.decode('utf-8')))
    struct = json.loads(zprs)
    return struct["data"]



a = json.loads(decrypt(AES_KEY, GetByPhone(number)))
b = json.loads(decrypt(AES_KEY, GetByPhoneTags(number)))
print("DisplayName: " + a['result']['profile']['displayName'])
print("Country: " + a['result']['profile']['countryCode'])
for i in b['result']['tags']:
    print(i.get('tag'))
