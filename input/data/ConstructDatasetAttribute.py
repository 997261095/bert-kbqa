#-*-coding:UTF-8 -*-


import os
import random
import pandas as pd
import re

'''
通过 ner_data 中的数据 构建出 用来匹配句子相似度的 样本集合
构造属性关联训练集，分类问题，训练BERT分类模型
'''


data_dir = 'ner_data'
file_name_list = ['train.csv','dev.csv','test.csv']

new_dir = 'sim_data'

# 正则表达式
pattern = re.compile('^-+') # 以-开头



for file_name in file_name_list:
    file_path_name = os.path.join(data_dir,file_name)
    assert os.path.exists(file_path_name)

    attribute_classify_sample = []
    df = pd.read_csv(file_path_name, encoding='utf-8')
    df['attribute'] = df['t_str'].apply(lambda x: x.split('|||')[1].strip())
    # 将 DataFrame 数据类型转化为 List
    attributes_list = df['attribute'].tolist()
    # 通过列表set() 对其中的数据进行去重
    attributes_list = list(set(attributes_list))
    # 去尾部，去空格
    attributes_list = [att.strip().replace(' ','') for att in attributes_list]
    # 去掉 以-开头
    attributes_list = [re.sub(pattern,'',att) for att in attributes_list]
    # 再次去重
    attributes_list = list(set(attributes_list))

    for row in df.index:
        question, pos_att = df.loc[row][['q_str', 'attribute']]

        question = question.strip().replace(' ','') # 去尾部，空格
        question = re.sub(pattern, '', question)    # 去掉 以-开头

        pos_att = pos_att.strip().replace(' ','')   # 去尾部，空格
        pos_att = re.sub(pattern, '', pos_att)      # 去掉 以-开头

        neg_att_list = []
        while True:
            neg_att_list = random.sample(attributes_list, 5)
            if pos_att not in neg_att_list:
                break
        attribute_classify_sample.append([question, pos_att, '1'])

        neg_att_sample = [[question, neg_att, '0'] for neg_att in neg_att_list]
        attribute_classify_sample.extend(neg_att_sample)
    seq_result = [str(lineno) + '\t' + '\t'.join(line) for (lineno, line) in enumerate(attribute_classify_sample)]

    #处理后将文件写在./input/sim_data 下
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    file_type = file_name.split('.')[0]
    new_file_name = file_type + '.'+'txt'
    with open(os.path.join(new_dir,new_file_name), "w", encoding='utf-8') as f:
        f.write("\n".join(seq_result))

