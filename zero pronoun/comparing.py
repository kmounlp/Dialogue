"""
4. comparing two files(sejong(eojeol) and utagger_result(eojeol))
(생략 가)
"""
import sys

fr_ute = open('./corpus/utagger_result(eojeol).txt', 'r', encoding='utf-16')
fr_sje = open('./corpus/sejong(eojeol).txt', 'r', encoding='utf-16')

for i, (ut, sj) in enumerate(zip(fr_ute, fr_sje), 1):
    ut = ut.strip()
    sj = sj.strip()
    # if i == 77: sys.exit()
    if ut == sj: continue
    # if ut[0] == sj[0]: continue  # 27505
    elif 'VV' in ut or 'VV' in sj:
        print(i)
        print(ut)
        print(sj)
    elif 'VA' in ut or 'VV' in sj:
        print(i)
        print(ut)
        print(sj)
    elif 'VX' in ut or 'VV' in sj:
        print(i)
        print(ut)
        print(sj)
    elif 'VCP' in ut or 'VV' in sj:
        print(i)
        print(ut)
        print(sj)
    elif 'VCN' in ut or 'VV' in sj:
        print(i)
        print(ut)
        print(sj)


