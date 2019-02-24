from flask import Flask, render_template, request, url_for, flash, redirect, request,Response
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, SearchForm
# import request
import csv
import pandas as pd
from pprint import pprint
from googleapiclient.discovery import build
import warnings
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
# import random
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
                    api_key = "AIzaSyDOw-hG4kvRwN5A4SHBipMhn7uBny16Ot4"
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
                    items=results["items"]
                    comments = []
                    name = str(video_id)
                    for item in items:
                        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                        comments .append(comment)
                    df = pd.DataFrame(comments)
                    # for i in comments:
                    #     value=i
                    #     value=re.sub(r'https?:\/\/.*[\r\n]*','',value)
                    #     # value=re.sub(r'pic?.*','',value)
                    #     value=re.sub(r"[a-zA-z.'#0-9@,:?'\u200b\u200c\u200d!/&~-]",'',value)
                    #     value=re.sub(r'[""“”()’:;]','',value)
                    #     value=' '.join(value.split())
                    #     data=[]
                    #     if value:
                    #         value=value.split("।")
                    #         for i in value:
                    #             if not i:
                    #                 pass
                    #             else:
                    #                 data.append(i)
                    # with open('./youtube_rabi.csv','r',encoding='utf-8'):
                    #     writer= csv.writer(writeFile)
                    #     for i in comments:
                    #         writer.writterow(i)
                    with open('youtube_data.csv', 'a',encoding="utf-8") as writeFile:
                        writer = csv.writer(writeFile)
                        for i in comments:
                            writer.writerow([i])
                    # df.to_csv(name +'_rabi.csv')
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
                response = None
                try:
                    response = requests.get(url)
                except Exception as e:
                    print(repr(e))
                # thepage = urllib.request.urlopen(url)
                # soup = BeautifulSoup(thepage,"html.parser")
                # owner = soup.title.text
                # bio_raw = soup.find('p', class_ = "ProfileHeaderCard-bio u-dir")
                # bio = bio_raw.text
                # for all in soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
                #     tweets = all.text
                #     items.append(tweets)
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.findAll('div',{'class':'js-tweet-text-container'})
                content = soup.findAll('p',{'class':'TweetTextSize js-tweet-text tweet-text'})
                data=[]
                for i in content:
                    value=i.text
                    value=re.sub(r'https?:\/\/.*[\r\n]*','',value)
                    value=re.sub(r'pic?.*','',value)
                    value=re.sub(r"[a-zA-z.'#0-9@,:?'\u200b\u200c\u200d!/&~-]",'',value)
                    value=re.sub(r'[""“”()’:;]','',value)
                    value=' '.join(value.split())
                    if value:
                        value=value.split("।")
                        for i in value:
                            if not i:
                                pass
                            else:
                                data.append(i)
                with open('twitter_data.csv', 'a',encoding="utf-8") as writeFile:
                    writer = csv.writer(writeFile)
                    for i in data:
                        writer.writerow([i])
                return render_template('twitter_search.html',name = sitee)



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
