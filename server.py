#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        request_data = self.data.decode().split()

        if (request_data[0] == 'GET'):
            if (request_data[1][0:3] == '/..'):
                self.request.sendall(bytearray("HTTP/1.1 404 - Page not found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n",'utf-8'))
            #checking if it is a directory
            # Reference #1 in README.md: Method 3 on this page: https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists-2/
            elif os.path.isdir("www" + request_data[1]):
                #checking if the path is correctly specified for the directory
                if (request_data[1][-1] != '/'):
                    # Reference #3 in README.md: for understanding http response format: https://docs.netscaler.com/en-us/citrix-adc/current-release/appexpert/http-callout/http-request-response-notes-format.html
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: {}\nContent-Type: text/html; charset=UTF-8\r\n\r\n".format(request_data[1] + "/"),'utf-8'))
                path = "www" + request_data[1] + "index.html"
                #opening the file in reading mode and read the content of the file
                with open(path, 'r') as f:
                    file_content = f.read()
                    # Reference #3 in README.md: for understanding http response format: https://docs.netscaler.com/en-us/citrix-adc/current-release/appexpert/http-callout/http-request-response-notes-format.html
                    self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"+file_content,'utf-8'))
            else:
                #checking if it's a file that exists 
                # Reference #2 in README.md: Method 2 on this page: https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists-2/
                if os.path.isfile("www" + request_data[1]):
                    path = "www" + request_data[1]
                    #if it's a html file
                    if 'html' in request_data[1]:
                        #opening the file in reading mode and read the content of the file
                        with open(path, 'r') as f:
                            file_content = f.read()
                            # Reference #3 in README.md: for understanding http response format: https://docs.netscaler.com/en-us/citrix-adc/current-release/appexpert/http-callout/http-request-response-notes-format.html
                            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"+file_content,'utf-8'))
                    #if it's a css file
                    elif 'css' in request_data[1]:
                        #opening the file in reading mode and read the content of the file
                        with open(path, 'r') as f:
                            file_content = f.read()
                            # Reference #3 in README.md: for understanding http response format: https://docs.netscaler.com/en-us/citrix-adc/current-release/appexpert/http-callout/http-request-response-notes-format.html
                            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=UTF-8\r\n\r\n"+file_content,'utf-8'))
                # this handles if that particular file or directory does not exist
                else:
                    # Reference #3 in README.md: for understanding http response format: https://docs.netscaler.com/en-us/citrix-adc/current-release/appexpert/http-callout/http-request-response-notes-format.html
                    self.request.sendall(bytearray("HTTP/1.1 404 - Page not found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n",'utf-8'))
        #this handles showing error response for requests other than GET requests
        else:
            # Reference #3 in README.md: for understanding http response format: https://docs.netscaler.com/en-us/citrix-adc/current-release/appexpert/http-callout/http-request-response-notes-format.html 
            self.request.sendall(bytearray("HTTP/1.1 405 Not Allowed\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
