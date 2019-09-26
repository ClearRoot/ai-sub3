import tensorflow as tf
import sqlite3
import os
import numpy as np

from flask import g
from flask import Flask, render_template, request
from slack import WebClient
from slackeventsapi import SlackEventAdapter

import data
import model as ml
from configs import DEFINES

app = Flask(__name__)

# slack 연동 정보 입력 부분
SLACK_TOKEN = "xoxb-728026288049-734244769025-K6y6Amjuqiga0LVVfJDKgiVP"
SLACK_SIGNING_SECRET = "5fc4b1c88e0683e61a748a4a0280cc48"

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


# Req. 2-2-1 대답 예측 함수 구현
def predict(query):
    char2idx,  idx2char, vocabulary_length = data.load_voc()
    predic_input_enc, _ = data.enc_processing([query], char2idx)
    predic_target_dec, _ = data.dec_target_processing([""], char2idx)

    classifier = tf.estimator.Estimator(
            model_fn=ml.Model, # 모델 등록한다.
            model_dir=DEFINES.check_point_path, # 체크포인트 위치 등록한다.
            params={ # 모델 쪽으로 파라메터 전달한다.
                'hidden_size': DEFINES.hidden_size,  # 가중치 크기 설정한다.
                'layer_size': DEFINES.layer_size,  # 멀티 레이어 층 개수를 설정한다.
                'learning_rate': DEFINES.learning_rate,  # 학습율 설정한다.
                'teacher_forcing_rate': DEFINES.teacher_forcing_rate, # 학습시 디코더 인풋 정답 지원율 설정
                'vocabulary_length': vocabulary_length,  # 딕셔너리 크기를 설정한다.
                'embedding_size': DEFINES.embedding_size,  # 임베딩 크기를 설정한다.
                'embedding': DEFINES.embedding,  # 임베딩 사용 유무를 설정한다.
                'multilayer': DEFINES.multilayer,  # 멀티 레이어 사용 유무를 설정한다.
                'attention': DEFINES.attention, #  어텐션 지원 유무를 설정한다.
                'teacher_forcing': DEFINES.teacher_forcing, # 학습시 디코더 인풋 정답 지원 유무 설정한다.
                'loss_mask': DEFINES.loss_mask, # PAD에 대한 마스크를 통한 loss를 제한 한다.
            })
    
    predictions = classifier.predict(input_fn=lambda:data.eval_input_fn(predic_input_enc, predic_target_dec, DEFINES.batch_size))

    answer, _ = data.pred_next_string(predictions, idx2char)

    return answer


# Req 2-2-2. app.db 를 연동하여 웹에서 주고받는 데이터를 DB로 저장
def insertDB(text):
    conn = sqlite3.connect('../DB/app.db')
    cur = conn.cursor()
    cur.execute("insert into search_history (query) values (:query)", {'query':text})
    conn.commit()
    conn.close()
    

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    text = " ".join(text.split()[1:])
    
    answer = predict(text)

    slack_web_client.chat_postMessage(
            channel=channel,
            text=answer,
        )

    return True


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/chat', methods = ['POST', 'GET'])
def chat():
    comments = []
    if request.method == 'POST':
        text = request.form['text']
        answer = predict(text)
        comments.append({
            "text": text,
            "answer": answer
        })
        return render_template('chat.html', comments=comments)
    
    elif request.method == 'GET':
        return render_template('chat.html', comment=comments)

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
    app.run()
