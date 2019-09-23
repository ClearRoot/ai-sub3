from konlpy.tag import Kkma, Okt
import pandas as pd
import tensorflow as tf
import enum
import os
import re
import sys
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm

# Configs
tf.app.flags.DEFINE_integer('batch_size', 64, 'batch size') # 배치 크기
tf.app.flags.DEFINE_integer('train_steps', 20000, 'train steps') # 학습 에포크
tf.app.flags.DEFINE_float('dropout_width', 0.8, 'dropout width') # 드롭아웃 크기
tf.app.flags.DEFINE_integer('layer_size', 1, 'layer size') # 멀티 레이어 크기 (multi rnn)
tf.app.flags.DEFINE_integer('hidden_size', 128, 'weights size') # 가중치 크기
tf.app.flags.DEFINE_float('learning_rate', 1e-3, 'learning rate') # 학습률
tf.app.flags.DEFINE_float('teacher_forcing_rate', 0.7, 'teacher forcing rate') # 학습시 디코더 인풋 정답 지원율
tf.app.flags.DEFINE_string('vocabulary_path', './data_out_kkma/vocabularyData.voc', 'vocabulary path') # 사전 위치
tf.app.flags.DEFINE_string('check_point_path', './data_out_kkma/check_point', 'check point path') # 체크 포인트 위치
tf.app.flags.DEFINE_string('save_model_path', './data_out_kkma/model', 'save model') # 모델 저장 경로
tf.app.flags.DEFINE_integer('shuffle_seek', 1000, 'shuffle random seek') # 셔플 시드값
tf.app.flags.DEFINE_integer('max_sequence_length', 30, 'max sequence length') # 시퀀스 길이
tf.app.flags.DEFINE_integer('embedding_size', 128, 'embedding size') # 임베딩 크기
tf.app.flags.DEFINE_boolean('embedding', True, 'Use Embedding flag') # 임베딩 유무 설정
tf.app.flags.DEFINE_boolean('multilayer', True, 'Use Multi RNN Cell') # 멀티 RNN 유무
tf.app.flags.DEFINE_boolean('attention', True, 'Use Attention') #  어텐션 사용 유무
tf.app.flags.DEFINE_boolean('teacher_forcing', True, 'Use Teacher Forcing') # 학습시 디코더 인풋 정답 지원 유무
tf.app.flags.DEFINE_boolean('tokenize_as_morph', False, 'set morph tokenize') # 형태소에 따른 토크나이징 사용 유무
tf.app.flags.DEFINE_boolean('serving', True, 'Use Serving') #  서빙 기능 지원 여부
tf.app.flags.DEFINE_boolean('loss_mask', False, 'Use loss mask') # PAD에 대한 마스크를 통한 loss를 제한

# Define FLAGS
DEFINES = tf.app.flags.FLAGS

# Data
PAD_MASK = 0
NON_PAD_MASK = 1

FILTERS = "([~.,!?\"':;)(])"
PAD = "<PADDING>"
STD = "<START>"
END = "<END>"
UNK = "<UNKNOWN>"

PAD_INDEX = 0
STD_INDEX = 1
END_INDEX = 2
UNK_INDEX = 3

MARKER = [PAD, STD, END, UNK]
CHANGE_FILTER = re.compile(FILTERS)


def prepro_like_morphlized(data):
    morph_analyzer = Kkma()
    result_data = list()

    for seq in data:
        morphlized_seq = " ".join(morph_analyzer.morphs(seq.replace(' ', '')))
        result_data.append(morphlized_seq)

    return result_data


def enc_processing(value, dictionary):
    sequences_input_index = []
    sequences_length = []

    value = prepro_like_morphlized(value)

    for sequence in value:
        sequence = re.sub(CHANGE_FILTER, "", sequence)
        sequence_index = []

        for word in sequence.split():

            if dictionary.get(word) is not None:
                sequence_index.extend([dictionary[word]])
            else:
                sequence_index.extend([dictionary[UNK]])

        if len(sequence_index) > DEFINES.max_sequence_length:
            sequence_index = sequence_index[:DEFINES.max_sequence_length]

        sequences_length.append(len(sequence_index))
        sequence_index += (DEFINES.max_sequence_length - len(sequence_index)) * [dictionary[PAD]]
        sequences_input_index.append(sequence_index)

    return np.asarray(sequences_input_index), sequences_length


def dec_target_processing(value, dictionary):
    sequences_target_index = []
    sequences_length = []

    for sequence in value:
        sequence = re.sub(CHANGE_FILTER, "", sequence)
        sequence_index = [dictionary[word] for word in sequence.split()]

        if len(sequence_index) >= DEFINES.max_sequence_length:
            sequence_index = sequence_index[:DEFINES.max_sequence_length-1] + [dictionary[END]]
        else:
            sequence_index += [dictionary[END]]
                          
        sequences_length.append([PAD_MASK if num > len(sequence_index) else NON_PAD_MASK for num in range (DEFINES.max_sequence_length)])
        sequence_index += (DEFINES.max_sequence_length - len(sequence_index)) * [dictionary[PAD]]
        sequences_target_index.append(sequence_index)

    return np.asarray(sequences_target_index), np.asarray(sequences_length)


def pred2string(value, dictionary):

    sentence_string = []

    if DEFINES.serving == True:
        for v in value['output']: 
            sentence_string = [dictionary[index] for index in v]
    else:
        for v in value:
            sentence_string = [dictionary[index] for index in v['indexs']]
    
    # print(sentence_string)
    answer = ""

    for word in sentence_string:
        if word not in PAD and word not in END:
            answer += word
            answer += " "

    # print("answer : " + answer)
    return answer


def make_vocabulary(vocabulary_list):
    char2idx = {char: idx for idx, char in enumerate(vocabulary_list)}
    idx2char = {idx: char for idx, char in enumerate(vocabulary_list)}

    return char2idx, idx2char


def load_vocabulary():
    vocabulary_list = []

    assert os.path.exists(DEFINES.vocabulary_path)

    with open(DEFINES.vocabulary_path, 'r', encoding='utf-8') as vocabulary_file:
        for line in vocabulary_file:
            vocabulary_list.append(line.strip())

    char2idx, idx2char = make_vocabulary(vocabulary_list)

    return char2idx, idx2char, len(char2idx)


# Predict
def predict(query):
    tf.logging.set_verbosity(tf.logging.INFO)
    char2idx,  idx2char, vocabulary_length = load_vocabulary()
        
    # print(query)
    predic_input_enc, predic_input_enc_length = enc_processing([query], char2idx)
    predic_target_dec, _ = dec_target_processing([""], char2idx)

    if DEFINES.serving == True:
        predictor_fn = tf.contrib.predictor.from_saved_model(
            export_dir="./data_out_kkma/model/1569212618"
        )

    if DEFINES.serving == True:
        predictions = predictor_fn({'input':predic_input_enc, 'output':predic_target_dec})
        return pred2string(predictions, idx2char)


def main(self):
    query = str(input("문장을 입력하세요 : "))
    return "\n" + predict(query)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)