import re
import pickle
import os
import itertools
from copy import deepcopy
import sys
import json
# from utagger_py import my_in, UTagger

case_frame_dict = {
    0: [['이/JKS'], ['ㅣ/JKS', '가/JKS', '께서/JKS', '도/JKS', '두/JKS', '서/JKS', '에서/JKS', '이/JKS']],
    1: [['을/JKO'], ['ㄹ/JKO', '를/JKO', '을/JKO']],
    2: [['에/JKB'], ['에/JKB']],
    3: [['에게/JKB'], ['에게/JKB', '한테/JKB']],
    4: [['에서/JKB'], ['서/JKB', '에서/JKB']],
    5: [['에게서/JKB'], ['에게서/JKB']],
    6: [['으로/JKB'], ['로/JKB', '으로/JKB']],
    7: [['로부터/JKB'], ['으로부터/JKB', '로부터/JKB']],
    8: [['과/JKB'], ['과/JKB', '와/JKB']],
    9: [['보다/JKB'], ['보다/JKB']],

}
case_frame_list = [['-가', '-이/가'], ['-를', '-을', '-을/를'], ['-에', '-에/게'], ['-에/에게', '-에게'],
                   ['-에/에서', '-에서', '-에서/서'], ['-에/에게서', '-에게/에게서', '-에게서', '-에서/에게서'],
                   ['-로', '-으로', '-으로/로'], ['-으로부터/로부터'], ['-와/과', '-과'], ['-보다']]
subtitute_list = ['<NOUN>/NNN+가/JKS', '<NOUN>/NNN+을/JKO','<NOUN>/NNN+에/JKB','<NOUN>/NNN+에게/JKB','<NOUN>/NNN+에서/JKB',
                  '<NOUN>/NNN+에게서/JKB','<NOUN>/NNN+으로/JKB','<NOUN>/NNN+과/JKB','<NOUN>/NNN+보다/JKB']
case_frame_code = {
    0 : ["i",'i_ga'],
    1 : ['eul'],
    2 : ['e'],
    3 : ['ege'],
    4 : ['eseo'],
    5 : ['eso_egeseo'],
    6 : ['ro'],
    7 : ['robuteo'],
    8 : ['wa'],
    9 :['boda'],



}


def morph_sep(morph_list):
    tag_eojeol = []
    morph_eojeol = []
    for mo in morph_list:
        tag_eojeol.append(mo[mo.rfind('/') + 1:])
        morph_eojeol.append(mo[:mo.rfind('/')])
    return morph_eojeol, tag_eojeol


def pairwise(iterable: object) -> object:
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b, = itertools.tee(iterable)
    next(b, None)

    assert isinstance(b, object)

    return zip(a, b)


def load_pickle(fname):
    with open(fname, 'rb') as f: return pickle.load(f)


def recovery_task(unif, recof, uprop_dict, josa_dict):#,Utaager):
    count = 0
    unify_mor = []
    unify_tag = []
    for line in unif.readlines():
        line = line.strip()
        if len(line) == 0:
            print(file=recof)
            continue
        eojeol_list = line.split()
        v_index = []
        v_mo = []
        etm_context = []
        for eo_idx in range(len(eojeol_list)):

            eojeol = eojeol_list[eo_idx]
            morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", eojeol)
            mor, tag = morph_sep(morph_list)
            for mo, ta in zip(mor, tag):
                if ta == "VV" or ta == "VA":
                    if mo.rfind("__") != -1:
                        # ㄹ 수 있 없 만 걸르자

                        v_index.append(eo_idx)
                        v_mo.append("다 ".join(mo.split("__")))
                        if tag[-1] == "ETM":
                            if eo_idx +1 != len(eojeol_list):
                                nxt_eojeol = eojeol_list[eo_idx +1]
                                morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", nxt_eojeol)
                                mor, tag = morph_sep(morph_list)
                                if tag[0][0] == "N":
                                    etm_context.append(mor[0]+"/"+tag[0])
                        else:
                            etm_context.append([])


        if len(v_index) == 0:
            print(file=recof)
            continue
        word_list = list(uprop_dict.keys())
        josa_list = josa_dict
        pred_dict = {k: v for k, v in zip(word_list, josa_list)}
        # morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", eojeol_list[v_index])
        v_index.insert(0,0)
        recovery_fact = []
        v_mo_index = -1
        for cur, nxt in pairwise(v_index):#chunk및 보조용언 처리 필요!!!!!!!!!!
            v_mo_index += 1
            if cur == 0 and nxt == 0:#제일앞 걸러내기
                print("아무것도 없")
                print(v_mo[v_mo_index])
                print(etm_context[v_mo_index])
                recovery_fra = []

                recovery_fact.append(recovery_fra)
                continue
            if cur == 0 and nxt == 1 and v_index[0] == 0 and v_index[1] == 0:#제일앞이 용언으로 시작하는 것
                print("아무것도 없")
                print(v_mo[v_mo_index])
                recovery_fra = []

                recovery_fact.append(recovery_fra)
                continue
            if cur == 0 and nxt == 1:#제일앞에 하나 있는 것
                print(eojeol_list[cur:nxt])
                recovery_fra = []
                print(v_mo[v_mo_index])
                recovery_fact.append(recovery_fra)
                continue
            if nxt - cur == 1:# 사이에 아무것도 없는것
                print("아무것도 없")
                print(v_mo[v_mo_index])
                recovery_fra = []

                recovery_fact.append(recovery_fra)
                continue
            recovery_fra = []
            if cur == 0:

                # eojeol_list[cur:nxt]
                recovery(v_mo[v_mo_index],pred_dict,eojeol_list[cur:nxt])#,Utaager)
                print(eojeol_list[cur:nxt])
                print(v_mo[v_mo_index])
            else:
                recovery(v_mo[v_mo_index], pred_dict, eojeol_list[cur+1:nxt])#,Utaager)
                # eojeol_list[cur+1:nxt]
                print(eojeol_list[cur+1:nxt])
                print(v_mo[v_mo_index])

            recovery_fact.append(recovery_fra)






        print(eojeol_list)
        print(v_index)
        print("________________________")


def recovery(yong_eun,pred_dict, eojeols, etm_form=None):# Utagger, etm_form=None):
    case_frame = pred_dict[yong_eun]
    case_frame_copy = deepcopy(case_frame)

    for frame_idx in range(len(case_frame_copy)):
        frames = case_frame_copy[frame_idx]
        case_frame_copy[frame_idx] = ["-가"] + frames


    candidate_case = []
    ju_kuk_flag = False
    for eojeol in eojeols:
        morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", eojeol)
        mor, tag = morph_sep(morph_list)
        for idx in range(len(tag)-1,-1,-1):
            if tag[idx][0] != "J":
                break
            if tag[idx] == "JX":
                continue
            if tag[idx] == "JKB":
                morph_temp = mor[idx] +"/" +tag[idx]
                for val in case_frame_dict.values():
                    if morph_temp in val[1]:
                        candidate_case.append(val[0][0][:val[0][0].rfind('/')])
                break
            if tag[idx] == "JKO":
                morph_temp = mor[idx] + "/" + tag[idx]
                for val in case_frame_dict.values():
                    if morph_temp in val[1]:
                        candidate_case.append(val[0][0][:val[0][0].rfind('/')])
                break
            if tag[idx] == "JKS":
                morph_temp = mor[idx] + "/" + tag[idx]
                for val in case_frame_dict.values():
                    if morph_temp in val[1]:
                        candidate_case.append(val[0][0][:val[0][0].rfind('/')])
                break
    # morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", etm_form)
    # mor, tag = morph_sep(morph_list)
    # sent = "NAV " + mor[0] +"/" +tag[0] + " " + yong_eun
    # nav = Utagger.uwm1(sent)
    # if nav == "eul":
    #     candidate_case.append("을")

    print(case_frame_copy)
    print(list(set(candidate_case)))
    case_frame_filter = []
    for frames in case_frame_copy:
        frame_temp = []
        for frame in frames:
            include_frame =False
            for cand in candidate_case:
                if cand in frame:
                    include_frame= True
                    break
            if not include_frame:
                frame_temp.append(frame)
        case_frame_filter.append(frame_temp)
    min_idx = 0
    for idx in range(len(case_frame_filter)):
        if len(case_frame_filter[min_idx]) > len(case_frame_filter[idx]):
            min_idx = idx
    case_frame_pix = case_frame_filter[min_idx]
    case_code = []
    for case in case_frame_pix:
        for case_idx in range(len(case_frame_list)):
            if case in case_frame_list[case_idx]:
                case_code.append(case_frame_code[case_idx])

    false_list = [False] * len(case_frame_pix)
    for eojeol in eojeols:
        sent = ""
        morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", eojeol)
        mor, tag = morph_sep(morph_list)
        for idx in range(len(mor) - 1, -1, -1):
            if tag[idx][0:2] == "JK":
                break
            if tag[idx][0] == "N":
                sent = "NAV " + mor[idx] + " " + yong_eun
                # nav = Utagger.uwm1(sent)
                # for code_idx in range(len(case_code)):
                #     if nav in case_code[code_idx]:
                #         false_list[code_idx] = True
                break
    result_list = []

    for fal_idx in range(len(false_list)):
        if not false_list[fal_idx]:
            result_list.append(case_frame_pix[fal_idx])
            continue
    recovery_list = []
    for resul in result_list:
        for case_idx in range(len(case_frame_list)):
            if resul in case_frame_list[case_idx]:
                recovery_list.append(subtitute_list[case_idx])
                break






if __name__ == "__main__":
    pickle_path = './pickle'

    # rt = UTagger.Load_global()
    # if rt != '':
    #     print(rt)
    #     sys.exit(1)
    #
    # ut = UTagger(0)  # 0은 객체 고유번호. 0~99 지정 가능. 같은 번호로 여러번 생성하면 안됨. 한 스레드당 하나씩 지정 필요.
    # rt = ut.new_ucma()  # 객체 생성. 객체가 있어야 유태거 이용 가능.
    # if rt != '':
    #     print(rt)
    #     sys.exit(1)

    uprop_file = os.path.join(pickle_path, 'uprop_dict.pkl')
    josa_list_file = os.path.join(pickle_path, 'josa_list.pkl')
    josa_set_file = os.path.join(pickle_path, 'josa_set.pkl')
    josa_list = load_pickle(josa_list_file)
    josa_set = load_pickle(josa_set_file)  # 필수논항 조사 파악(표.국.사. '일러두기'에 있음) <- 'documents/조사 및 어미 종류.hwp'
    unify = open('./corpus/unify2.tag', 'r', encoding="utf-16")
    recovery_f = open('./corpus/recovery.tag', 'w', encoding="utf-16")
    uprop_dict = load_pickle(uprop_file)
    recovery_task(unify, recovery_f, uprop_dict, josa_list)#,ut)