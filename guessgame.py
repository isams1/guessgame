__author__ = 'KhoaAlienware & BaileyDang'
import random
import urllib
from flask import Flask, url_for, render_template, request, session, redirect, flash
from form import LoginForm
from socket import *
from functools import wraps

app = Flask(__name__)
app.secret_key = 'testing'

def login_required(test):
  @wraps(test)
  def wrap(*args, **kwargs):
     if 'logged_in' in session:
        return test(*args, **kwargs)
     else:
        flash('You need to register first.', 'note')
        return redirect(url_for('user_register'))
  return wrap

@app.route('/', methods=['GET', 'POST'])
def user_register():
    name=None
    form = LoginForm(request.form)
    if request.method=='POST':
        if form.validate_on_submit():
            session['name'] = request.form['username']
            session['logged_in'] = True
            return redirect(url_for('newgame'))
    return render_template('login.html', form=form)

@app.route('/newgame')
@login_required
def newgame():
    session['number'] = random.randint(1, 30)
    session['live'] = 3
    name = session.get('name')
    game = url_for('guessgame', next=next)
    return render_template("newgame.html", game=game, name=name)


@app.route('/guessgame', methods=['GET', 'POST'])
@login_required
def guessgame():
    temp = session.get('number')
    number = int(temp)
    live = session.get('live')
    if request.method == 'POST':
        while True:
            try:
                submitNumb = int(request.form['submitNumb'])
                break
            except ValueError:
                flash('You must enter an number !', 'wrong')
                return render_template('guessgame.html', number=number, live=live)

        if (submitNumb == number):
            newgame = url_for('newgame')
            return render_template('correct.html', number=number, newgame=newgame)
        else:
            if live > 1:
                live -= 1
                session['live'] = live
                #flash('You have guessed it wrong.', 'wrong')
                if submitNumb <= 30 and submitNumb > 0:
                    if submitNumb < number:
                        flash('You have guessed it wrong. The number you have guess is less than our number =). Please try again!', 'wrong')
                    elif submitNumb > number:
                        flash('You have guessed it wrong. The number you have guess is more than our number =). Please try again!', 'wrong')
                else:
                    flash('Please enter a number in range 1 - 30. Thank you!', 'wrong');
                return redirect(url_for('guessgame'))
            else:
                number = session.get('number')
                newgame = url_for('newgame')
                return render_template('wrongnumber.html', number=number, newgame=newgame)
    return render_template('guessgame.html', number=number, live=live)
    #return "hello world"

@app.route("/logout")
def logout():
        session.pop('logged_in', None)
        flash('You were just logged out, we hope to see you again :)', 'goodbye')
        return redirect(url_for('user_register'))



if __name__ == '__main__':
    #this for changing Port
    hostname = 'localhost'
    #Create TCP connection
    ServerSocket = socket(AF_INET, SOCK_STREAM)
    #bind to socket
    try:
        ServerSocket.bind((hostname, 5000))
    except error: #socket.error if using import socket only
        ServerSocket.bind((hostname, 5555))
        print 'Port has been changed!'
    ServerSocket.listen(1)
    port = ServerSocket.getsockname()[1]
    print 'Server is running! It is now still connecting to', hostname,':', port
    print 'Please start up the web browser to enjoy!'
    ServerSocket.close()
    app.run(port=port, debug=True)



