from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

comments = []
@app.route('/', methods = ['POST', 'GET'])
def index():
	now = datetime.datetime.now()
	if request.method == 'POST':
		time= now.strftime('%H:%M:%S')
		temp = request.form
		for i in temp.values():
			comments.append(i)
		return render_template('index.html', comments=comments, time=time)
	elif request.method == 'GET':
		temp = request.args.get('comment')
		return render_template('index.html', comment=temp)

@app.route('/about')
def about():
	return render_template('about.html')