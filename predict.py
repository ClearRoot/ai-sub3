import tensorflow as tf
import data
import os
import sys
import model as ml

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
    predic_output_dec, predic_output_dec_length = data.dec_output_processing([""], char2idx)
    predic_target_dec = data.dec_target_processing([""], char2idx)

    if DEFINES.serving == True:
        # 모델이 저장된 위치를 넣어 준다.  export_dir
        predictor_fn = tf.contrib.predictor.from_saved_model(
            export_dir="./data_out/model/1569975824"
        )
    else:
        # 에스티메이터 구성한다.
        classifier = tf.estimator.Estimator(
                model_fn=ml.Model, # 모델 등록한다.
                model_dir=DEFINES.check_point_path, # 체크포인트 위치 등록한다.
                params={ # 모델 쪽으로 파라메터 전달한다.
                    'model_hidden_size': DEFINES.model_hidden_size,  # 가중치 크기 설정한다.
                    'ffn_hidden_size': DEFINES.ffn_hidden_size,
                    'attention_head_size': DEFINES.attention_head_size,
                    'learning_rate': DEFINES.learning_rate,  # 학습율 설정한다.
                    'vocabulary_length': vocabulary_length,  # 딕셔너리 크기를 설정한다.
                    'embedding_size': DEFINES.embedding_size,  # 임베딩 크기를 설정한다.
                    'layer_size': DEFINES.layer_size,
                    'max_sequence_length': DEFINES.max_sequence_length,
                    'tokenize_as_morph': DEFINES.tokenize_as_morph,
                    'serving': DEFINES.serving # 모델 저장 및 serving 유무를 설정한다.
                })

    if DEFINES.serving == True:
        predictions = predictor_fn({'input':predic_input_enc, 'output':predic_output_dec, 'target':predic_target_dec})
        answer = data.model_pred(predictions, idx2char)
    else:
        # 예측을 하는 부분이다.
        predictions = classifier.predict(input_fn=lambda:data.eval_input_fn(predic_input_enc, predic_output_dec, predic_target_dec, 1))
        answer, finished = data.pred_next_string(predictions, idx2char)

    print("answer: ", answer)
