import jieba
import re
import json
from enum import Enum

from models.db import db
from models.api.hot_word import get_by_group, update_tencent_hot_word, get_by_type, HotWordTypeEnum, to_yitu_hot_word
from models.api.func import get_enum_by_value, get_enum_by_name
from configs.serving import YITU_DEV_KEY, YITU_DEV_ID, TENCENT_SECRET_KEY, TENCENT_SECRTE_ID, ALIYUN_ASR_ACCESSKEYID, ALIYUN_ASR_ACCESSKEYSECRET, ALIYUN_ASR_APPKEY
from pkgs.yitu.yitu import YituASR
from pkgs.tencent.tencent_asr import TencentASR
from pkgs.tencent.hot_word import HotWord
from pkgs.ali.asr import AliASR
from pkgs.ali.slm import SLM
from utils.core import clog
from models.api.transcript import *

import dofast as df
from typing import List

# handlers = [
#     # YituASRHandler(ASRSourceEnum.yitu.name, 3, yitu_put_audio, yitu_get_res,
#     #                parse_yitu),
#     TencentASRHandler(ASRSourceEnum.tencent.name, 2, tencent_put_audio,
#                       tencent_get_res, parse_tencent),
#     AliyunASRHandler(ASRSourceEnum.aliyun.name, 1, ali_put_audio, ali_get_res,
#                      parse_aliyun),
#     PreprocessHandler('preprocess', 4),
#     # UploadHandler('upload_text', 5),
#     ToDatabaseHandler('to_database', 5)
# ]


# url = 'https://cos-1303988041.cos.ap-beijing.myqcloud.com/audio_half_minite.wav'
# # url = 'https://cos-1303988041.cos.ap-beijing.myqcloud.com/qzkj.wav'
# url = 'https://cos-1303988041.cos.ap-beijing.myqcloud.com/qimo.mp3'
# # asr = ASR(handlers)
# data = ASRInput(url, ASRClientEnum.default.name, hot_words=['Gong'])
# res = asr.handler(data)
class C:
    ks = df.jsonread('/usr/local/info/mgvai_aliyun.json')
    # ks = df.jsonread('/usr/local/info/aliyun_slipper.json')
    slm = SLM(ks['id'], ks['secret'], ks['appkey'])
    vocab_id = '83c6f59319e1469c896745fa76e0491b'
    asr = AliASR(ks['id'], ks['secret'], ks['appkey'])
    mgvai_vocab_id = '00dca9c672c546b0bff8e1e19004c56f'


def hotword_get_list():
    resp = C.slm.get_vocab_list()
    # for hw in resp['Page']['Content']:
    #     if hw['Description'] == '热词测试':
    #         C.slm.delete_vocab(hw['Id'])
    df.logger.info(resp)


def aliyun_create_hotword():
    word_weights = {'会话分析': 2, '语法分析': 1}
    resp = C.slm.create_vocab(Name='VocabTest',
                              WordWeights=json.dumps(word_weights),
                              Description="热词测试")
    df.pp(resp)


def update_vocab(word_list: List,
                 vocab_id: str = '83c6f59319e1469c896745fa76e0491b'):
    vocab = C.slm.get_vocab(vocab_id)
    word_weights = vocab['Vocab']['WordWeights']
    df.p(vocab, word_weights)
    for w in word_list:
        word_weights[w] = 3  # Set default weight to be 3
    word_weights['会话'] = 5
    resp = C.slm.update_vocab(vocab_id,
                              vocab['Vocab']['Name'],
                              WordWeights=json.dumps(word_weights))
    df.p(resp)


def test_slm():
    # resp = C.slm.create_model('slm_test', 'universal', 'slm测试模型')
    # df.p(resp)
    data_url = 'https://ali-oss-bucket-1.oss-cn-beijing.aliyuncs.com/train.txt'
    data_url = 'https://ali-oss-bucket-1.oss-cn-beijing.aliyuncs.com/train_huihua.txt'
    resp = C.slm.create_lm_data('data_test', data_url)
    model_id = '3cd1396ec8144bb1881cd88b42273324'
    data_id = '4a49c24ca918450ca154e15977da3049'
    # resp=C.slm.add_data_to_model(model_id, data_id)
    # resp = C.slm.retrain_with_data(model_id, data_id)

    # resp=C.slm.get_lm_data_list()
    # resp = C.slm.train_model(model_id)
    resp = C.slm.get_model_list()
    df.pp(resp)


def add_corpus_to_model(model_id:str, corpus:str):
    pass

if __name__ == '__main__':
    # hotword_get_list()
    # aliyun_create_hotword()
    hot_words = ["词向量", "开户费", '语法分析', '会话分析','提取会话']
    # hot_words += [w.strip() for w in open('/home/gaoang/Pictures/hotwords_computer_science.txt', 'r').readlines()]
    # df.p(hot_words)
    # update_vocab(hot_words, C.mgvai_vocab_id)
    # df.p(C.slm.get_vocab(C.mgvai_vocab_id))
    # df.pp(C.slm.get_model_list())
    # df.pp(C.slm.get_vocab_list())
    # df.pp(C.slm.get_data_status('4a49c24ca918450ca154e15977da3049'))

    df.info("Test")




