# bert-kbqa
基于bert的kbqa系统

预训练模型太大了，无法上传。放在百度网盘了
链接：https://pan.baidu.com/s/1EK-TGghfmj-0HbWl_xe3zg 
提取码：jqeg 
下载下来放在./bert-kbqa/input/config目录


构造数据集
通过 1_split_data.py 切分数据

通过 2-construct_dataset_ner.py 构造命名实体识别的数据集

通过 3-construct_dataset_attribute.py 构造属性相似度的数据集

通过 4-print-seq-len.py 看看句子的长度

通过 5-triple_clean.py 构造干净的三元组

通过 6-load_dbdata.py 通过创建数据库 和 上传数据



CRF_Model.py  条件随机场模型

BERT_CRF.py  bert+条件随机场

NER_main.py  训练命令实体识别的模型

SIM_main.py  训练属性相似度的模型


test_NER.py  测试命令实体识别

test_SIM.py 测试属性相似度

test_pro.py  测试整个项目


主要依赖版本：

torch.__version__    1.2.0

transformers.__version__   2.0.0


带有命令运行的py文件的命令都在 该py文件的最上方



