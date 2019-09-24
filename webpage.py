from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

comments = []
@app.route('/chat', methods = ['POST', 'GET'])
def chat():
	now = datetime.datetime.now()
	if request.method == 'POST':
		time= now.strftime('%H:%M:%S')
		temp = request.form
		for i in temp.values():
			comments.append(i)
		return render_template('chat.html', comments=comments, time=time)
	elif request.method == 'GET':
		temp = request.args.get('comment')
		return render_template('chat.html', comment=temp)

@app.route('/about')
def about():
	return render_template('about.html')
