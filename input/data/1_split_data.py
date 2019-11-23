#
# 切分数据集，
# 原始的 nlpcc-iccpol-2016.kbqa.testing-data 有 9870 个样本
# 原始的 nlpcc-iccpol-2016.kbqa.training-data 有 14609 个样本
#
# 将nlpcc-iccpol-2016.kbqa.testing-data 中的对半分，一半变成验证集(dev.text)，一半变成测试集(test.txt)
# nlpcc-iccpol-2016.kbqa.training-data 保持不变，复制成为训练集 train.txt
#


import pandas as pd
import os


data_dir = 'NLPCC2016KBQA'
file_name_list = ['nlpcc-iccpol-2016.kbqa.testing-data','nlpcc-iccpol-2016.kbqa.training-data']


for file_name in file_name_list:
    file_path_name = os.path.join(data_dir,file_name)
    file = []
    with open(file_path_name,'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            file.append(line)
        f.close()
    if 'training' in file_name:
        with open(os.path.join(data_dir,'train.txt') , "w", encoding='utf-8') as f:
            f.write('\n'.join(file))
        f.close()
    elif 'testing' in file_name:
        assert len(file) % 4 == 0           # 断言
        testing_num = len(file) / 4         # 一个样本是由 4 行构成的
        test_num = int(testing_num / 2)         # 真正的测试集分一半

        test_line_no = int(test_num * 4)


        with open(os.path.join(data_dir, 'test.txt'), "w", encoding='utf-8') as f:
            f.write('\n'.join(file[:test_line_no]))     # 乘以四得到行号，前一半给 test 数据集
        f.close()

        with open(os.path.join(data_dir, 'dev.txt'), "w", encoding='utf-8') as f:
            f.write('\n'.join(file[test_line_no:]))      # 乘以四得到行号，后一半给 dev 数据集
        f.close()

print("Done")

