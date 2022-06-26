import os
from Configurations import DATA_DIR

"""
切分数据集；
原始的 nlpcc-iccpol-2016.kbqa.testing-data 有 9870 个样本
原始的 nlpcc-iccpol-2016.kbqa.training-data 有 14609 个样本；

nlpcc-iccpol-2016.kbqa.testing-data 中的数据对半分，一半变成验证集(dev.text)，一半变成测试集(test.txt)
nlpcc-iccpol-2016.kbqa.training-data 保持不变，复制成为训练集 train.txt
"""

file_name_list = ['nlpcc-iccpol-2016.kbqa.testing-data', 'nlpcc-iccpol-2016.kbqa.training-data']

# 文件处理
for file_name in file_name_list:
    file_path_name = os.path.join(DATA_DIR, file_name)
    file = []
    with open(file_path_name,'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            file.append(line)
    if 'training' in file_name:
        with open(os.path.join(DATA_DIR,'train.txt') , "w", encoding='utf-8') as f:
            f.write('\n'.join(file))
    elif 'testing' in file_name:
        assert len(file) % 4 == 0           # 断言处理，错误时触发异常
        testing_num = len(file) // 4        # 一个样本是由 4 行构成的
        line_no = testing_num // 2 * 4      # 将测试集分出一半用作评估

        # 测试数据
        with open(os.path.join(DATA_DIR, 'test.txt'), "w", encoding='utf-8') as f:
            for line in file[:line_no]:
                f.write(line + '\n')

        # 进行评估的数据
        with open(os.path.join(DATA_DIR, 'dev.txt'), "w", encoding='utf-8') as f:
            for line in file[line_no:]:
                f.write(line + '\n')

print("Done")

