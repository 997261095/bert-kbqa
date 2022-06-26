# -*- coding: utf-8 -*-

import os
import csv
from Configurations import DATA_DIR, DB_DATA_DIR
from MyUtils import line_parse, my_strip

'''
构造 NER 训练集 (即三元组), 实体序列标注, 用于训练 BERT + BiLSTM + CRF
'''

# 将处理后的文件写在 ./input/DB_data 下
if not os.path.exists(DB_DATA_DIR):
    os.mkdir(DB_DATA_DIR)

filename_prefix = 'nlpcc-iccpol-2016.kbqa.'
filename_suffix = '-data'
file_name_list = [
    filename_prefix + var + filename_suffix for var in ['training', 'testing']
]

with open(os.path.join(DB_DATA_DIR, 'clean_triple.csv'), mode='w', encoding='utf-8', newline='') as out_csv_file:
    # 三元组: 实体, 属性, 答案
    writer = csv.DictWriter(out_csv_file, fieldnames=['entity', 'attribute', 'answer'])
    writer.writeheader()

    for filename in file_name_list:
        file_path = os.path.join(DATA_DIR, filename)
        assert os.path.exists(file_path)
        
        with open(file_path, mode='r', encoding='utf-8') as f:
            while True:
                try:
                    # 一次读取三行
                    l = [line_parse(f.__next__()) for i in range(3)]
                    # 并映射到字典的形式
                    s = {t[0]: t[1] for t in l}
                    # 跳过分割线行
                    f.__next__()
                    
                    triples = [t.strip() for t in s['triple'].split('|||')]
                    t = {
                        'entity': triples[0],
                        'attribute': triples[1],
                        'answer': triples[2],
                    }
                    if t['entity'] in s['question']:
                        writer.writerow(t)
                    else:
                        # print(s['question'])
                        # print(t['entity'])
                        # print('-' * 30)
                        pass
                except StopIteration:
                    break
