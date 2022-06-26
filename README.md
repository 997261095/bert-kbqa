# bert-kbqa

基于bert的kbqa系统

预训练模型太大, 放在百度网盘了

- 链接: https://pan.baidu.com/s/1EK-TGghfmj-0HbWl_xe3zg 
- 提取码: jqeg 

下载下来放在 `./bert-kbqa/input/config` 目录

## 使用方法

### 安装依赖

- PyTorch
- Transformers

### 构造数据集

详见 [input/data/](./input/data/) 目录

1. [SplitData.py](./input/data/SplitData.py) 切分数据
2. [ConstructDatasetNer.py](./input/data/ConstructDatasetNer.py) 构造命名实体识别的数据集
3. [ConstructDatasetAttribute.py](./input/data/ConstructDatasetAttribute.py) 构造属性相似度的数据集
4. [ConstructTriple.py](./input/data/ConstructTriple.py) 构造干净的三元组
5. [LoadMySQL.py](./input/data/LoadMySQL.py) 创建数据库和上传数据

### 模型训练

[CRF_Model.py](./CRF_Model.py)  条件随机场模型

[BERT_CRF_MODEL.py](./BERT_CRF_Model.py)  bert+条件随机场

[NERTrain.py](./NERTrain.py)  训练命令实体识别的模型

```console
$ python3 NERTrain.py \
    --data_dir ./input/data/ner_data \
    --vob_file ./input/config/bert-base-chinese-vocab.txt \
    --model_config ./input/config/bert-base-chinese-config.json \
    --output ./output \
    --pre_train_model ./input/config/bert-base-chinese-model.bin \
    --max_seq_length 64 \
    --do_train \
    --train_batch_size 16 \
    --eval_batch_size 256 \
    --gradient_accumulation_steps 4 \
    --num_train_epochs 15
```

[SIMTrain.py](./SIMTrain.py)  训练属性相似度的模型

```console
$ python3 SIMTrain.py \
    --data_dir ./input/data/sim_data \
    --vob_file ./input/config/bert-base-chinese-vocab.txt \
    --model_config ./input/config/bert-base-chinese-config.json \
    --output ./output \
    --pre_train_model ./input/config/bert-base-chinese-model.bin \
    --max_seq_length 64 \
    --do_train \
    --train_batch_size 32 \
    --eval_batch_size 256 \
    --gradient_accumulation_steps 4 \
    --num_train_epochs 15
```

### 模型测试

[NERTest.py](./NERTest.py)  测试命令实体识别

[SIMTest.py](./SIMTest.py) 测试属性相似度

## 项目展示

[ProjectTest.py](./ProjectTest.py) 测试整个项目 / 命令行界面的项目展示

[chat.py](./chat.py) Qt/QML 编写的图形界面

