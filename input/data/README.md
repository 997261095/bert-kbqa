# 数据处理

1. [SplitData.py](./SplitData.py)
1. [ConstructDataSetNER.py](./ConstructDataSetNER.py)
1. [ConstructDatasetAttribute.py](./ConstructDatasetAttribute.py)

记录下数据中最长的序列长度:

```none
train.csv:      max_len: 62
dev.csv:        max_len: 60
test.csv:       max_len: 62
```

因此, 将最大长度设定为 64 较为合理.

1. [ConstructTriple.py](./ConstructTriple.py)
1. [LoadDbData.py](./LoadDbData.py)
