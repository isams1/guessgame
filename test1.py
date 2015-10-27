__author__ = 'KhoaAlienware'
from flask import Flask, render_template, request
import random, socket, threading
from socket import *

#tcp server
TCP_IP = '127.0.0.1'
TCP_PORT = 7005
BUFFER_SIZE  = 20

def launchServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    print('waiting for connection')
    conn, addr = s.accept()

    print ('Connection address:', addr)


#flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'button1':
            conn.send(b'button1')
            return "Random number between 1 and 10:  " + str(random.randint(1,10))
        elif request.form['submit'] == 'button2':
            conn.send(b'button1')
            return "Random number between 11 and 1000:  " + str(random.randint(11,1000))
        else:
            pass

    if request.method == 'GET':
        return '''
        <title>What would you like to do?</title>
        <form action="" method="post">
        <br><br>
        <input type="submit" name="submit" value="button1">
        <br><br>
        <input type="submit" name="submit" value="button2">
        </form>
        '''

if __name__ == "__main__":
    app.run(port=TCP_PORT, debug=True)
    t = threading.Thread(target=launchServer)
    t.daemon = True
    t.start()