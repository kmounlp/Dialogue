import re

josa_set = set()
with open('./corpus/sejong_sh.txt', 'r', encoding='utf-16') as f:
    for sent in f:
        sent = sent.strip().split()
        for eojeol in sent:
            try:
                eojeol = eojeol.split('+')
                for morph in eojeol:
                    if re.search('EC', morph):
                        josa_set.add(morph)
            except: pass
josa = sorted(josa_set)
print(josa)
print(len(josa))

# ['고/JC', '과/JC', '나/JC', '니/JC', '든/JC', '라던가/JC', '라던지/JC', '라든/JC', '라든가/JC', '라든지/JC', '랑/JC', '래든가/JC', '부터/JC', '에다/JC', '에다가/JC', '와/JC', '이고/JC', '이나/JC', '이니/JC', '이든/JC', '이든지/JC', '이라던가/JC', '이라든가/JC', '이라든지/JC', '이랑/JC', '이래든가/JC', '이래든지/JC', '이며/JC', '하고/JC', '하구/JC', '하며/JC']
# 31

# ['ㄴ/JKB', 'ㄹ로/JKB', 'ㄹ로써/JKB', 'ㄹ루/JKB', 'ㅕ서/JKB', '같이/JKB', '게/JKB', '과/JKB', '께/JKB', '께서/JKB', '나/JKB', '냐고/JKB', '다/JKB', '대로/JKB', '대루/JKB', '더러/JKB', '따/JKB', '따라/JKB', '랑/JKB', '로/JKB', '로부터/JKB', '로서/JKB', '로써/JKB', '루/JKB', '마따나/JKB', '만/JKB', '만큼/JKB', '보고/JKB', '보구/JKB', '보다/JKB', '보러/JKB', '부터/JKB', '서/JKB', '서부터/JKB', '에/JKB', '에게/JKB', '에게서/JKB', '에다/JKB', '에다가/JKB', '에따가/JKB', '에서/JKB', '에서부터/JKB', '와/JKB', '우루/JKB', '으로/JKB', '으로부터/JKB', '으로서/JKB', '으로써/JKB', '으루/JKB', '이/JKB', '이나/JKB', '이든/JKB', '이랑/JKB', '처럼/JKB', '하고/JKB', '하구/JKB', '한테/JKB', '한테서/JKB']
# 58

