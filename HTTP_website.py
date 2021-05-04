from socket import *
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler

SERVER = gethostbyname(gethostname())
PORT = 8000
SERVER_ADDRESS = (SERVER, PORT)

# Response
Addtask_form = open("Addtask_form.txt").read()
Display_form = open("Display_form.txt").read()
Removetask_form = open("Removetask_form.txt").read()

# Task
Tasklist = ['Task 1','Task 2','Task 3']

# Takes in request from the client
class Client_Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/'):
            # Standard Header response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(Display_form.encode())
                
        # Tasklist options
        if self.path.endswith('/Tasklist'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()            

            data_to_client = "<html><body>"
            data_to_client += "<h1>TaskList</h1>"
            # 'Add New Task' hyperlinks user to "/Tasklist/new"
            data_to_client += "<h3><a href='/Tasklist/new'>Add New Task</a></h3>"
            data_to_client += "<ol>"
            for task in Tasklist:
                data_to_client += "<li>"+task+" "
                # 'Remove' hyperlinks user to "/Tasklist/%s/remove"
                # %s points to deleted task
                data_to_client += "<a href='/Tasklist/%s/remove'>Remove</a>" %task
                data_to_client += "</li>"
                data_to_client += "</br>"
            data_to_client += "</ol>"
            data_to_client += "</body></html>"
            self.wfile.write(data_to_client.encode())
            
        # Page to add new tasks
        # Redirect to do_POST() once new task entered
        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            self.wfile.write(Addtask_form.encode())
            
        # Page to remove task
        # Redirect to do_POST() once task removed
        if self.path.endswith('/remove'):
            listIDpath = self.path.split('/')
            removed_task = listIDpath[2].replace('%20', ' ')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            data_to_client = "<html><body>"
            data_to_client += "<h2>Remove %s?</h2>" %removed_task
            data_to_client += "<form action='/Tasklist/%s/remove' method='POST' enctype='multipart/form-data'>" %removed_task
            data_to_client += "<input name='task' type= 'submit' value='Remove'></form>"
            # 'Cancel' hyperlinks user to "/Tasklist"
            data_to_client += "<a href='/Tasklist'>Cancel</a>" 
            data_to_client += "</body></html>"
            
            self.wfile.write(data_to_client.encode())
            
    # Handles clients submissions       
    def do_POST(self):
        # Handles new task
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            # String to bytes
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            content_length = int(self.headers['content-length'])
            pdict['CONTENT-LENGTH'] = content_length
            if ctype == 'multipart/form-data':
                # Read from pdict
                fields = cgi.parse_multipart(self.rfile, pdict)
                print(fields)
                # Add the task to Tasklist
                new_task = fields['task']
                Tasklist.append(new_task[0])
                #print(fields)
            
            # 301 'Moved Permanently' redirect URL to 'Location=/Tasklist'
            # /Tasklist page gets updated
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/Tasklist')
            self.end_headers()
            
        # Handles removed task
        if self.path.endswith('/remove'):
            listIDpath = self.path.split('/')
            removed_task = listIDpath[2].replace('%20', ' ')
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            if ctype == 'multipart/form-data':
                # Read from pdict
                # Gives us 'Remove' since its what we submitted
                # So we can't follow the process method from Add task
                Tasklist.remove(removed_task)
                
            # 301 'Moved Permanently' redirect URL to 'Location=/Tasklist'
            # /Tasklist page gets updated
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/Tasklist')
            self.end_headers()
                

#####################################################################################
#                                   Main Function                                   #
#####################################################################################
def main():
    HTTP_SERVER = HTTPServer(SERVER_ADDRESS, Client_Handler)
    HTTP_SERVER.serve_forever()
    

if __name__=='__main__':
    print(f'Access http://{SERVER}:{PORT}')
    main()
