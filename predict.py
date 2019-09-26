import tensorflow as tf
import data
import os
import sys
import model as ml

from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
from rouge import Rouge

from configs import DEFINES

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.ERROR)
    arg_length = len(sys.argv)

    if (arg_length < 2):
        raise Exception("Don't call us. We'll call you")

    char2idx, idx2char, vocabulary_length = data.load_voc()

    input = ""
    for i in sys.argv[1:]:
        input += i
        input += " "

    print(input)
    predic_input_enc, predic_input_enc_length = data.enc_processing([input], char2idx)

    predic_target_dec, predic_input_dec_length = data.dec_target_processing([""], char2idx)

    # 에스티메이터 구성한다.
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


    # 예측을 하는 부분이다.
    predictions = classifier.predict(input_fn=lambda:data.eval_input_fn(predic_input_enc, predic_target_dec, DEFINES.batch_size))
    answer, finished = data.pred_next_string(predictions, idx2char)

    print("answer: ", answer)
