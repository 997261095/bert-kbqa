from BERT_CRF_Model import BertCrf
from transformers import BertTokenizer
from NERTrain import NerProcessor,statistical_real_sentences,flatten,CrfInputFeatures
from torch.utils.data import DataLoader, RandomSampler,TensorDataset
from sklearn.metrics import classification_report
import torch
import numpy as np
from tqdm import tqdm, trange

"""
对命名实体识别模型进行简单的测试
"""

processor = NerProcessor()
tokenizer_inputs = ()
tokenizer_kwards = {'do_lower_case': False,
                    'max_len': 64,
                    'vocab_file': './input/config/bert-base-chinese-vocab.txt'}
tokenizer = BertTokenizer(*tokenizer_inputs,**tokenizer_kwards)

model = BertCrf(config_name= './input/config/bert-base-chinese-config.json',
                num_tags = len(processor.get_labels()),batch_first=True)
model.load_state_dict(torch.load('./output/best_ner.bin'))

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# features = torch.load(cached_features_file)
features = torch.load('./input/data/ner_data/cached_dev_64')

all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
all_attention_mask = torch.tensor([f.attention_mask for f in features], dtype=torch.long)
all_token_type_ids = torch.tensor([f.token_type_ids for f in features], dtype=torch.long)
all_label = torch.tensor([f.label for f in features], dtype=torch.long)
dataset = TensorDataset(all_input_ids, all_attention_mask, all_token_type_ids, all_label)

sampler = RandomSampler(dataset)
data_loader = DataLoader(dataset, sampler=sampler, batch_size=256)
loss = []
real_token_label = []
pred_token_label = []


for batch in tqdm(data_loader, desc="test"):
    model.eval()
    batch = tuple(t.to(device) for t in batch)
    with torch.no_grad():
        inputs = {'input_ids': batch[0],
                  'attention_mask': batch[1],
                  'token_type_ids': batch[2],
                  'tags': batch[3],
                  'decode': True,
                  'reduction': 'none'
                  }
        outputs = model(**inputs)
        # temp_eval_loss shape: (batch_size)
        # temp_pred : list[list[int]] 长度不齐
        temp_eval_loss, temp_pred = outputs[0], outputs[1]

        loss.extend(temp_eval_loss.tolist())
        pred_token_label.extend(temp_pred)
        real_token_label.extend(statistical_real_sentences(batch[3], batch[1], temp_pred))

loss = np.array(loss).mean()
real_token_label = np.array(flatten(real_token_label))
pred_token_label = np.array(flatten(pred_token_label))
assert real_token_label.shape == pred_token_label.shape
ret = classification_report(y_true=real_token_label, y_pred=pred_token_label, digits = 6,output_dict=False)

print(ret)


# CRF_LABELS = ["O", "B-LOC", "I-LOC"]


#               precision    recall  f1-score   support
#
#            0   0.998345  0.996229  0.997286     89638
#            1   0.993100  0.989685  0.991389      9016
#            2   0.992506  0.997225  0.994860     46483
#
#    micro avg   0.996142  0.996142  0.996142    145137
#    macro avg   0.994650  0.994380  0.994512    145137
# weighted avg   0.996149  0.996142  0.996143    145137
