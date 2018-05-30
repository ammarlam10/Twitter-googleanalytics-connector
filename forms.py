import json
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# Twitter 
import tweepy
import tweepy
import json
import time
import unicodedata
# from google_measurement_protocol import pageview, report

import re
# stre = "hello </789 gt6? 5&67_m buddy?007"
# my_new_string = re.sub('[^ a-zA-Z0-9]', '', stre)
# print(my_new_string)


import httplib, urllib


ACCESS_TOKEN = 'xxxx'
ACCESS_SECRET = 'xxxx'
CONSUMER_KEY = 'xxxx'
CONSUMER_SECRET = 'xxxx'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'xxxx'


class ReusableForm(Form):

    name = TextField('Name:', validators=[validators.required()])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
	form = ReusableForm(request.form)
	if request.method == 'GET':
		return render_template('form.html', form=form)

@app.route("/start", methods=['GET', 'POST'])
def start():
	form = ReusableForm(request.form)
	keyword = request.form['folder']

	

	ACCESS_TOKEN = 'xxxx'
	ACCESS_SECRET = 'xxxx'
	CONSUMER_KEY = 'xxxx'
	CONSUMER_SECRET = 'xxxx'

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

	api = tweepy.API(auth)

	# results = api.search(q="#lol")
	k = 0 
	while True:
		results = api.search(q=keyword)
		i = 0
		label = ''
		for tweet in results:
			k=k+1
			hashtag = 0
			i = i + 1
			user = ''
			# print tweet.text.split(' ')
			for v in tweet.text.split(' '):
				if '@' in v:
					label = v
					# print label
					
				if '#' in v:
					hashtag = hashtag + 1
			# print tweet.user.name
			print hashtag
			if '@' not in label:
				label = 'none'
			# print type(unicodedata.normalize('NFKD', tweet.user.name).encode('ascii','ignore'))
			# name = unicodedata.normalize('NFKD', tweet.user.name).encode('ascii','ignore')
			name = tweet.user.name.encode('ascii', 'ignore').decode('ascii')
			if len(name) == 0:
				name = 'none'.encode('ascii', 'ignore').decode('ascii')
			print name
			# print type(name)
			params = urllib.urlencode({
			    'v': 1,
			    'tid': 'UA-120052034-1',
			    'cid': k,
			    't': 'event',
			    'ec': 'tweet',
			    'ea': re.sub('[^ a-zA-Z0-9]', '', tweet.text),
			    'el': re.sub('[^ a-zA-Z0-9]', '', label),
			    'ev': hashtag,
			    'uid': re.sub('[^ a-zA-Z0-9]', '', tweet.user.name)
			})
			connection = httplib.HTTPConnection('www.google-analytics.com')
			connection.request('POST', '/collect', params)
			response = connection.getresponse()
			print response.status
		print i
		print 'will send a request again in 2 minutes'
		time.sleep(1)
	# tweet=[]
	# for v in results:
	# 	tweet.append(v.text)
	# return render_template('form2.html', form=form, type=tweet)


 
if __name__ == "__main__":
    app.run()
