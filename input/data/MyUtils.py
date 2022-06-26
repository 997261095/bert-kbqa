from typing import Tuple
import re
import random

def line_parse(line: str) -> Tuple[str, str]:
    p1 = line.find('<')
    p2 = line.find('>')
    header = line[(p1+1):p2]
    content = line[p2+1:].strip()
    return header.split()[0], content


# 正则表达式
pattern = re.compile('^-+') # 以-开头

def my_strip(s: str) -> str:
    # 去首尾空白, 去除字符串之间空格
    s = s.strip().replace(' ', '')
    # 去掉字符串开始处的 '-'
    return re.sub(pattern, '', s)


shuffle_from_ = lambda l: random.choice(l)
