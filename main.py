import tensorflow as tf
import model as ml
import data
import numpy as np
import os
import sys

from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
from rouge import Rouge

from configs import DEFINES

DATA_OUT_PATH = './data_out/'

# Req. 1-5-1. bleu score 계산 함수
def bleu_compute(hyps, refs):
    chencherry = SmoothingFunction()
    scores = sentence_bleu([refs], hyps, smoothing_function=chencherry.method1)
    return scores

# Req. 1-5-2. rouge score 계산 함수
def rouge_compute(hyps, refs):
    rouge = Rouge()
    scores = rouge.get_scores(hyps, refs, avg=True)
    return scores

# Req. 1-5-3. main 함수 구성
def main(self):
    data_out_path = os.path.join(os.getcwd(), DATA_OUT_PATH)
    os.makedirs(data_out_path, exist_ok=True)

    char2idx, idx2char, vocabulary_length = data.load_voc()
    train_q, train_a, test_q, test_a = data.load_data()

    train_input_enc, train_input_enc_length = data.enc_processing(train_q, char2idx)
    train_target_dec, train_target_dec_length = data.dec_target_processing(train_a, char2idx)

    eval_input_enc, eval_input_enc_length = data.enc_processing(test_q, char2idx)
    eval_target_dec, eval_target_dec_length = data.dec_target_processing(test_a, char2idx)

    check_point_path = os.path.join(os.getcwd(), DEFINES.check_point_path)
    os.makedirs(check_point_path, exist_ok=True)

    # 에스티메이터 구성한다.
    classifier = tf.estimator.Estimator(
        model_fn=ml.Model,  # 모델 등록한다.
        model_dir=DEFINES.check_point_path,  # 체크포인트 위치 등록한다.
        params={  # 모델 쪽으로 파라메터 전달한다.
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

    # 학습 실행
    classifier.train(input_fn=lambda: data.train_input_fn(
        train_input_enc, train_target_dec_length, train_target_dec, DEFINES.batch_size), steps=DEFINES.train_steps)

    # 평가 실행
    eval_result = classifier.evaluate(input_fn=lambda: data.eval_input_fn(
        eval_input_enc,eval_target_dec, DEFINES.batch_size))
    print('\nEVAL set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    # 테스트
    predic_input_enc = data.enc_processing(["가끔 궁금해"], char2idx)
    predic_target_dec = data.dec_target_processing([""], char2idx)

    predictions = classifier.predict(input_fn=lambda:data.eval_input_fn(predic_input_enc, predic_target_dec, DEFINES.batch_size))

    answer, finished = data.pred_next_string(predictions, idx2char)

    # 예측한 값을 인지 할 수 있도록
    # 텍스트로 변경하는 부분이다.
    print("answer: ", answer)
    print("Bleu score: ", bleu_compute("그 사람도 그럴 거예요.", answer))
    print("Rouge score: ", rouge_compute("그 사람도 그럴 거예요.", answer))


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)

tf.logging.set_verbosity
