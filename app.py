from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
import nltk
nltk.data.path.append('/mnt/d/html/nltk_data')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

js='data.json'
sid = SentimentIntensityAnalyzer()

app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html');

@app.route('/tweet', methods=['POST'])
def do_tweet():
    tweet = request.form['tweet']
    scores = sid.polarity_scores(tweet)
    com = sid.polarity_scores(tweet)['compound']
    neg = sid.polarity_scores(tweet)['neg']
    neu = sid.polarity_scores(tweet)['neu']
    pos = sid.polarity_scores(tweet)['pos']
    if float(com)>=0.50:
	res = "Super Hit"
    elif float(com)>0:
	res = "Hit"
    else:
	res = "Flop"
    return render_template('register.html',tweet=tweet,com=com,neg=neg,neu=neu,pos=pos,res=res);

@app.route('/login', methods=['POST'])
def do_admin_login():
    with open(js, 'r') as f:
        db = json.load(f)
    if request.form['password'] in db.values() and request.form['username'] in db.keys():
        session['logged_in'] = True
        session['username'] = request.form['username']
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route("/register")
def register():    
    return render_template('register.html');

@app.route('/register', methods=['POST'])
def do_register():
    with open(js, 'r') as f:
        db = json.load(f)
    if request.form['password'] in db.values() and request.form['username'] in db.keys():
        session['logged_in'] = True
        session['username'] = request.form['username']
    else:

        print ('Adding to database')
        db[request.form['username']]=request.form['password']
        with open(js, 'w') as f:
            json.dump(db, f)
        session['logged_in'] = True
        session['username'] = request.form['username']
    return home()

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=1952)
