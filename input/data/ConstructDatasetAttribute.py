#-*-coding:UTF-8 -*-

from Configurations import NER_DATA_DIR, SIM_DATD_DIR
from MyUtils import my_strip, shuffle_from_

import os
import csv

'''
通过 ner_data 中的数据 构建出 用来匹配句子相似度的 样本集合
构造属性关联训练集，分类问题，训练BERT分类模型
BERT:
    1. 预测 mask 概率;
    2. 预测 next sentence 概率.
'''

# 处理后将文件写在 ./input/SIM_data 下
if not os.path.exists(SIM_DATD_DIR):
    os.makedirs(SIM_DATD_DIR)

filenames = ['train.csv', 'dev.csv', 'test.csv']

sample_line_tmplt = '{}\t{}\t{}\t{}\n'

for filename in filenames:
    file_path = os.path.join(NER_DATA_DIR, filename)
    assert os.path.exists(file_path)   # 断言处理， 判断该文件是否存在
    rows = []                               # 记录文件内容
    attribute_set = set()                   # 存储 attribute 的集合
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # 读取文件
        for row in reader:
            # 处理 question 字符串
            question = my_strip(row['question'])
            # 提取并处理 attribute 字段
            attribute = my_strip(row['triple'].split('|||')[1])
            # 记录 attribute 字段
            row['attribute'] = attribute
            # 并存储在集合中
            rows.append(row)
            # 同时记录文件内容
            attribute_set.add(attribute)
    
    attribute_set = list(attribute_set)

    filename_tokens = filename.split('.')
    filename_tokens[-1] = 'txt'
    with open(os.path.join(SIM_DATD_DIR, '.'.join(filename_tokens)), mode='w', encoding='utf-8') as attribute_classify_sample:
        NEGATIVE_SAMPLE_COUNT = 5
        cnt = 0
        max_len = 0
        for row in rows:
            question, postive_attribute = row['question'], row['attribute']
            # 随机生成并记录负样本
            negative_attributes = []
            # 进行随机取样
            for i in range(NEGATIVE_SAMPLE_COUNT):
                sample = shuffle_from_(attribute_set)
                while sample == postive_attribute:
                    sample = shuffle_from_(attribute_set)
                negative_attributes.append(sample)
            # 写出生成的样本
            # 1 为正确答案， 0 为错误答案
            attribute_classify_sample.write(sample_line_tmplt.format(cnt, question, postive_attribute, 1))
            cnt += 1
            for var in negative_attributes:
                attribute_classify_sample.write(sample_line_tmplt.format(cnt, question, var, 0))
                cnt += 1
                # 记录最大字串序列长度
                max_len = max(max_len, len(question) + len(var))
            max_len = max(max_len, len(question) + len(postive_attribute))
        print('{}:\tmax_len: {}'.format(filename, max_len))
