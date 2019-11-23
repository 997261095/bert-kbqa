import os

dir_name = 'sim_data'
file_list = ['train.txt','dev.txt','test.txt']

for file in file_list:

    file_path_name = os.path.join(dir_name,file)

    max_len = 0
    print("****** {} *******".format(file))
    with open(file_path_name,'r',encoding='utf-8') as f:
        for line in f:

            line_list = line.split('\t')
            question = list(line_list[1])
            attribute = list(line_list[2])
            add_len = len(question) + len(attribute)
            if add_len > max_len:
                max_len = add_len
    print("max_len",max_len)
    f.close()

# ****** train.txt *******
# max_len 62
# ****** dev.txt *******
# max_len 61
# ****** test.txt *******
# max_len 62


# 因此，最大长度为 64 合理。

