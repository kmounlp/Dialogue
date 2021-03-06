"""
격틀정보: 용언의 필수논항으로 검색되는 형태
대표형: 마킹할 때의 표시 형태
절에서 확인해야 할 조사: 생략 여부 판별을 위해 확인해야 할 대상들
"""
# [격틀정보]:[[대표형],[절에서 확인해야 할 조사]]
case_frame_dict = {
    0:[['이/JKS'],['ㅣ/JKS', '가/JKS', '께서/JKS', '도/JKS', '두/JKS', '서/JKS', '에서/JKS', '이/JKS']],
    1:[['을/JKO'],['ㄹ/JKO', '를/JKO', '을/JKO']],
    2:[['에/JKB'],['에/JKB', '에게/JKB']],
    3:[['에게/JKB'],['에/JKB', '에게/JKB', '한테/JKB']],
    4:[['에서/JKB'],['서/JKB', '에/JKB', '에서/JKB']],
    5:[['에게서/JKB'],['에/JKB', '에게/JKB', '에서/JKB', '에게서/JKB']],
    6:[['으로/JKB'],['로/JKB', '으로/JKB']],
    7:[['로부터/JKB'],['으로부터/JKB', '로부터/JKB']],
    8:[['과/JKB'],['과/JKB', '와/JKB']],
    9:[['보다/JKB'],['보다/JKB']],

}

#!: 절에서 확인해야 할 조사가 '-음에', '-기를' 등 두 형태소 이상으로 이루어진 어미
#   일단은 '에', '를' 등의 조사가 없어도 어미만 확인되면 생략되지 않은 것으로 판단할 것임.

case_frame_list = [['-가', '-이/가'], ['-를', '-을', '-을/를'], ['-에', '-에/게'], ['-에/에게', '-에게'], ['-에/에서', '-에서', '-에서/서'], ['-에/에게서', '-에게/에게서', '-에게서', '-에서/에게서'], ['-로', '-으로', '-으로/로'], ['-으로부터/로부터'], ['-와/과', '-과'], ['-보다'], ['-게'], ['-게/도록', '-도록/토록'], ['-려고'], ['-고'], ['-음에', '-음을', '-임을'], ['-기'], ['-기로', '-기를', '-기에'], ['-이기가/기가', '-이기에/기에'], ['-ㄴ지'], ['-ㄴ지가', '-ㄴ지를'], ['-ㄹ지'], ['-ㄹ지가', '-ㄹ지를'], ['-ㄹ까', '-을까/를까'], ['-ㄹ까를']]

# sub_josa = ['ㅣ/JKS', '가/JKS', '께서/JKS', '도/JKS', '두/JKS', '서/JKS', '에서/JKS', '이/JKS']  # '도/JX', '만/JX'
# obj_josa = ['ㄹ/JKO', '를/JKO', '을/JKO'] #
# 원천수혜_josa = ['에/JKB', '에게/JKB', '에서/JKB', '에게서/JKB']  # 검토
# 방향_josa = ['로/JKB', '으로/JKB']  # ?
# 동반_josa = ['과/JC', '랑/JC', '와/JC']  #
# 비교_josa = ['보다/JKB']  #
# 인용_josa = ['고/JKQ', '라고/JKQ', '라구/JKQ', '이라고/JKQ', '이라구/JKQ', '하고/JKQ']

import pickle

with open('./pickle/case_frame_dict.pkl', 'wb') as fdict:
    pickle.dump(case_frame_dict, fdict)
with open('./pickle/case_frame_list.pkl', 'wb') as flist:
    pickle.dump(case_frame_list, flist)

