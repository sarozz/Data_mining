from flask import Flask, render_template, request, url_for, flash, redirect, request,Response
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, SearchForm
# import request
import csv
import pandas as pd
from pprint import pprint
from apiclient.discovery import build
import warnings
from bs4 import BeautifulSoup
import urllib.request
import requests
app = Flask(__name__)
app.config['SECRET_KEY'] = '18871a99bd42fd0dfb4b7909d9c5c7f309'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key= True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#
#     def __repr__(self):
#         return f"User('{self.username}','{self.email}')"

#app.debug = True

@app.route('/search', methods = ['GET','POST'])
def search():
    # form = SearchForm()
    # # warnings.filterwarnings('ignore')
    # # api_key = "AIzaSyDuyO7-bZvAdsjQiWv8yw7350O8UX1mgzs"
    # # youtube = build('youtube', 'v3', developerKey = api_key)
    return render_template("youtube_search.html")

@app.route('/', methods = ['GET','POST'])
# @app.route('/search', methods = ['GET','POST'])
def home():
    form = SearchForm()
    if request.method == "POST":
        if form.validate_on_submit():
            url = form.video_url.data
            count = url.count('.')
            if count == 2:
                waste,site,tags = url.split('.')
                if site == "youtube":
                    api_key = "AIzaSyDuyO7-bZvAdsjQiWv8yw7350O8UX1mgzs"
                    youtube = build('youtube', 'v3', developerKey = api_key)
                    waste,video_id = url.split('=')
                    results = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults = 50
                      ).execute()
                    # print(type(results))
                    #pprint(results)

                    #print(len(results))
                    items=None
                    return render_template('youtube_search.html', name=site,items=results["items"])

                    # for items in results["items"]:
                    #     comment = items["snippet"]["topLevelComment"]
                    #     author = comment["snippet"]["authorDisplayName"]
                    #     text = comment["snippet"]["textDisplay"]
                    #     channelIds = comment["snippet"]["authorChannelId"]["value"]
                    #     raw_data = {'Author':[author], 'Comment': [text]}
                    #     num = len(raw_data)
                    return render_template('youtube_search.html',author=author,comment=text, name=site, num=num)
                    #trigger youtube scrapping function
                else:
                    #trigger facebook scrapping function
                    return render_template('facebook_search.html', name=name)
            elif count == 1:
                items =    []
                imp,was = url.split('.')
                wastte,sitee = imp.split('//')
                #trigger twitter scrapping function
                name = sitee
                url = form.video_url.data
                thepage = urllib.request.urlopen(url)
                soup = BeautifulSoup(thepage,"html.parser")
                owner = soup.title.text
                bio_raw = soup.find('p', class_ = "ProfileHeaderCard-bio u-dir")
                bio = bio_raw.text
                for all in soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
                    tweets = all.text
                    items.append(tweets)
                return render_template('twitter_search.html',owner=owner, name = sitee, bio = bio, url=url, items=items)



            else:
                flash("Enter valid url please, I am already messed up",'danger')
                name =''
            return render_template('search.html', name=name )
        else:
            flash('Unsuccessful. Please give the full URL', 'danger')
            return render_template("home.html",title = 'Home', form = form)
    else:
        return render_template('home.html', title = 'Home', form = form)

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'asd123':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html",title = 'Login', form = form)

@app.route('/register', methods = ['GET','POST'] )
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title = "Register", form = form)


if __name__ == '__main__':
    app.run(debug=True)
