# coding:utf-8
import os
import csv
from Configurations import DATA_DIR, NER_DATA_DIR
from MyUtils import line_parse

'''
通过 NLPCC2016KBQA 中的原始数据, 构建用来训练NER的样本集合
构造 NER 训练集, 实体序列标注, 训练BERT+CRF
'''

file_name_list = ['train.txt', 'dev.txt', 'test.txt']

# 将处理后的文件写在 ./input/NER_data 下
if not os.path.exists(NER_DATA_DIR):
    os.mkdir(NER_DATA_DIR)

fields = ['question', 'triple', 'answer']

for file_name in file_name_list:
    
    # 写出序列标注
    tagged_q_str_file = open(os.path.join(NER_DATA_DIR, file_name), "w", encoding='utf-8')

    # 使用 csv.DictWriter 将 Q-T-A 对以 CSV 格式写出到对应的 CSV 文件里
    filename_tokens = file_name.split('.')
    filename_tokens[-1] = 'csv'
    qta_file = open(os.path.join(NER_DATA_DIR, '.'.join(filename_tokens)), mode='w', encoding='utf-8', newline='')
    qta_writer = csv.DictWriter(qta_file, fieldnames=fields)
    qta_writer.writeheader()

    file_path = os.path.join(DATA_DIR, file_name)
    assert os.path.exists(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        while True:
            try:
                # 一次读取三行
                l = [line_parse(f.__next__()) for i in range(3)]
                # 并映射到字典的形式
                s = {t[0]: t[1].strip() for t in l}
                # 跳过分割线行
                f.__next__()
                
                q_str = s['question'].replace(' ', '')
                s['question'] = q_str

                entity = s['triple'].split('|||')[0].strip()
                p = q_str.find(entity)
                # 若该实体名存在于问题中
                if p != -1:
                    tags = ['O'] * len(q_str)
                    # BIO 标注划分
                    # B-IOC: 一个地名的开始
                    # I-IOC：一个地名的中间部分
                    # 其余为 O
                    tags[p] = 'B-LOC'
                    for i in range(p + 1, p + len(entity)):
                        tags[i] = 'I-LOC'
                    # 存储序列标注等待写出
                    for q, t in zip(q_str, tags):
                        tagged_q_str_file.write(q + ' ' + t + '\n')
                    tagged_q_str_file.write('\n')
                else:
                    pass

                qta_writer.writerow(s)
            
            except StopIteration:
                qta_file.close()
                break
