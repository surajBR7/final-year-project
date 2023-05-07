
#import pymysql
from flask import Flask, render_template, url_for, flash, redirect, request , session
from forms import RegistrationForm, LoginForm
from get_tweets import TweetName
from front_end_gui import File_Pass
import matplotlib.pyplot as plt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

#conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='xtipl')
#cur = conn.cursor()

import sqlite3
import os
conn = sqlite3.connect('stock_database')
cur = conn.cursor()
try:
    cur.execute('''CREATE TABLE user (
    id integer Primary key  AUTOINCREMENT,
    name varchar(20),
    email varchar(50),
    password varchar(20))''')
    conn.commit()
except:
    pass




filenumber = int(os.listdir('saved_conversations')[-1])
filenumber = filenumber+1
file= open('saved_conversations/'+str(filenumber),"w+")
file.write('bot : Hi There! I am a medical chatbot. You can begin conversation by typing in a message and pressing enter.\n')
file.close()

app = Flask(__name__)
english_bot = ChatBot('Bot',
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                         {
                            'import_path': 'chatterbot.logic.BestMatch'
                         },

                      ],
                      trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#login_manager = LoginManager(app)
#login_manager.login_view = 'login'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/contactus")
def contactus():
    return render_template('contactus.html', title='ContactUs')


@app.route("/register", methods=['GET', 'POST'])
def register():
    #if current_user.is_authenticated:
        #return redirect(url_for('account'))
    conn = sqlite3.connect('stock_database')
    cur = conn.cursor()
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method == "POST":
            details = request.form

        cur.execute("INSERT INTO user(name,email,password) VALUES ('%s', '%s', '%s')" % (
        form.username.data, form.email.data, form.password.data))
        conn.commit()
        cur.close()

        flash(f'Registration Successful for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
        #return redirect(url_for('account'))
    conn = sqlite3.connect('stock_database')
    cur = conn.cursor()
    form = LoginForm()



    if form.validate_on_submit():
        if request.method == "POST":
            count = cur.execute('SELECT * FROM user WHERE email = "%s" AND password = "%s"' % (form.email.data, form.password.data))
            conn.commit()
            #cur.close()
            if count:
                session['logged_in'] = True
                flash('{} You have been logged in!'.format(form.email.data), 'success')
                #login_user()
                return redirect(url_for('account'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/account")
#@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/onprediction", methods=['GET', 'POST'])
def onprediction():
    '''if request.method == 'GET':
        return render_template("onprediction.html")
    else:
        company = request.form['company']
        getweet = TweetName(company)
        print("deepak")
        getweet.get_tweets()'''
    return render_template('onprediction.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))

    appendfile=os.listdir('saved_conversations')[-1]
    appendfile= open('saved_conversations/'+str(filenumber),"a")
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    appendfile.close()

    return response

@app.route("/onsentiment", methods=['GET', 'POST'])
def onsentiment():

    return render_template('onsentiment.html',title='browse file')

@app.route("/onnifty50", methods=['GET', 'POST'])
def onnifty50():
    import csv

    with open('data.csv', newline='') as f:
        result = csv.reader(f)
        header = next(result)
        type(header)

        data = [row for row in result]

    return render_template('onnifty50.html', header=header, data=data)

@app.route("/prediction", methods=['GET', 'POST'])
def prediction():

        return render_template('prediction.html')

@app.route("/sentiment", methods=['GET', 'POST'])
def sentiment():
    if request.method == 'POST':
        company = request.form['company']
        getweet = TweetName(company)
        getweet.get_tweets()
    return render_template('sentiment.html')

@app.route('/analyse', methods=['POST', 'GET'])
def analyse():
    if request.method == 'POST':
        f = request.files['file']
        name = f.filename
        obj = File_Pass(name)
        data_out = obj.Analysiz_Text()

        labels = 'positive_sentiment', 'negative_sentiment', 'neutral_sentiment',
        sizes = [data_out[0], data_out[1], data_out[2]]
        explode = (0.1, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        fig1.savefig('static\my_plot.png')
        #plt.show()

        dict = {'Positive Sentiment': data_out[0], 'Negative Sentiment': data_out[1], 'Neutral Sentiment': data_out[2] }

        return render_template('display.html', result = dict)


@app.route('/chatbot')
def chatbot():
   return render_template('index.html')

@app.route("/logout")
def logout():
   session['logged_in'] = False
   return home()


if __name__ == '__main__':
    app.run(debug=True)
