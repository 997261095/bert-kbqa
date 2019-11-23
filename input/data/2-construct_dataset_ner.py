# coding:utf-8
import sys
import os
import pandas as pd


'''
通过 NLPCC2016KBQA 中的原始数据，构建用来训练NER的样本集合
构造NER训练集，实体序列标注，训练BERT+CRF
'''

data_dir = 'NLPCC2016KBQA'
file_name_list = ['train.txt','dev.txt','test.txt']

new_dir = 'ner_data'

question_str = "<question"
triple_str = "<triple"
answer_str = "<answer"
start_str = "============="

for file_name in file_name_list:

    q_t_a_list = []
    seq_q_list = []  # ["中","华","人","民"]
    seq_tag_list = []  # [0,0,1,1]

    file_path_name = os.path.join(data_dir,file_name)
    assert os.path.exists(file_path_name)
    with open(file_path_name,'r',encoding='utf-8') as f:
        q_str = ""
        t_str = ""
        a_str = ""

        for line in f:
            if question_str in line:
                q_str = line.strip()
            if triple_str in line:
                t_str = line.strip()
            if answer_str in line:
                a_str = line.strip()

            if start_str in line:  # new question answer triple
                entities = t_str.split("|||")[0].split(">")[1].strip()
                q_str = q_str.split(">")[1].replace(" ", "").strip()
                if entities in q_str:
                    q_list = list(q_str)
                    seq_q_list.extend(q_list)
                    seq_q_list.extend([" "])
                    tag_list = ["O" for i in range(len(q_list))]
                    tag_start_index = q_str.find(entities)
                    for i in range(tag_start_index, tag_start_index + len(entities)):
                        if tag_start_index == i:
                            tag_list[i] = "B-LOC"
                        else:
                            tag_list[i] = "I-LOC"
                    seq_tag_list.extend(tag_list)
                    seq_tag_list.extend([" "])
                else:
                    pass
                q_t_a_list.append([q_str, t_str, a_str])
    print(file_name)
    print('\t'.join(seq_tag_list[0:50]))
    print('\t'.join(seq_q_list[0:50]))
    seq_result = [str(q) + " " + tag for q, tag in zip(seq_q_list, seq_tag_list)]
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    with open(os.path.join(new_dir,file_name), "w", encoding='utf-8') as f:
        f.write("\n".join(seq_result))
    f.close()

    df = pd.DataFrame(q_t_a_list, columns=["q_str", "t_str", "a_str"])
    file_type = file_name.split('.')[0]
    csv_name = file_type+'.'+'csv'

    df.to_csv(os.path.join(new_dir,csv_name), encoding='utf-8', index=False)