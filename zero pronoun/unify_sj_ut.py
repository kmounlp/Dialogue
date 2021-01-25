import re
import pickle
import os
import itertools


def triplewise(iterable: object) -> object:
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b,c = itertools.tee(iterable,3)
    next(b, None)
    next(c, None)
    assert isinstance(c, object)
    next(c, None)
    assert isinstance(b, object)
    assert isinstance(c, object)
    return zip(a, b, c)


def load_pickle(fname):
    with open(fname, 'rb') as f: return pickle.load(f)
# tag_morph = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", tag_word)


def print_xsv_xsa(sjf):
    for line in sjf.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        eojeol_list = line.split()
        eojeol_temp = []
        for eo in eojeol_list:
            morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", eo)
            morph_eojeol = []
            tag_eojeol = []
            for mo in morph_list:
                tag_eojeol.append(mo[mo.rfind('/')+1:])
                morph_eojeol.append(mo[:mo.rfind('/')])
            for ta in tag_eojeol:
                if ta == "XSA":
                    print(eo)


def modify_xsv(sjf,mjf,uprop):
    for line in sjf.readlines():
        line = line.strip()
        if len(line) == 0:
            print(file=mjf)
            continue
        eojeol_list = line.split()
        eojeol_temp = []
        for eo in eojeol_list:
            morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", eo)
            morph_eojeol = []
            tag_eojeol = []
            for mo in morph_list:
                tag_eojeol.append(mo[mo.rfind('/')+1:])
                morph_eojeol.append(mo[:mo.rfind('/')])
            for ta in tag_eojeol:
                if ta == "XSV":
                    print(eo)
            flag = False
            if len(tag_eojeol) > 2:

                for prev, cur, nxt in triplewise(tag_eojeol):
                    if prev == "NNG" and cur=="XSN" and nxt =="XSV":
                        flag = True
                    if prev == "XR" and cur=="XSN" and nxt =="XSV":
                        flag = True
            morph_temp = []
            tag_temp = []
            if flag:
                i = 0
                while i < len(tag_eojeol):
                    if not i< len(tag_eojeol)-2:
                        morph_temp.append(morph_eojeol[i])
                        tag_temp.append(tag_eojeol[i])
                        i += 1
                        continue
                    prev = tag_eojeol[i]
                    cur = tag_eojeol[i+1]
                    nxt = tag_eojeol[i+2]
                    if prev == "NNG" and cur == "XSN" and nxt == "XSV":
                        morph_temp.append( morph_eojeol[i]+morph_eojeol[i+1]+morph_eojeol[i+2])
                        tag_temp.append("VV")
                        i += 3
                        continue
                    if prev == "XR" and cur=="XSN" and nxt =="XSV":
                        morph_temp.append( morph_eojeol[i]+morph_eojeol[i+1]+morph_eojeol[i+2])
                        tag_temp.append("VV")
                        i += 3
                    morph_temp.append(morph_eojeol[i])
                    tag_temp.append(tag_eojeol[i])
                    i += 1
            if flag:
                eojeol_temp.append([i+"/"+j for i,j in zip(morph_temp,tag_temp)])
            else:
                eojeol_temp.append([i + "/" + j for i, j in zip(morph_eojeol, tag_eojeol)])

        st = ""
        for eoj in eojeol_temp:
            st += "+".join(eoj)
            st += " "
        print(st.strip(),file=mjf)


def modify_xsa(sjf,mjf,uprop):
    for line in sjf.readlines():
        line = line.strip()
        if len(line) == 0:
            print(file=mjf)
            continue
        eojeol_list = line.split()
        eojeol_temp = []
        for eo in eojeol_list:
            morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", eo)
            morph_eojeol = []
            tag_eojeol = []
            for mo in morph_list:
                tag_eojeol.append(mo[mo.rfind('/')+1:])
                morph_eojeol.append(mo[:mo.rfind('/')])
            for ta in tag_eojeol:
                if ta == "XSA":
                    print(eo)
            flag = False
            if len(tag_eojeol) > 2:

                for prev, cur, nxt in triplewise(tag_eojeol):
                    if prev == "NNG" and cur=="XSN" and nxt =="XSA":
                        flag = True
                    if prev == "XR" and cur=="XSN" and nxt =="XSA":
                        flag = True
            morph_temp = []
            tag_temp = []
            if flag:
                i = 0
                while i < len(tag_eojeol):
                    if not i< len(tag_eojeol)-2:
                        morph_temp.append(morph_eojeol[i])
                        tag_temp.append(tag_eojeol[i])
                        i += 1
                        continue
                    prev = tag_eojeol[i]
                    cur = tag_eojeol[i+1]
                    nxt = tag_eojeol[i+2]
                    if prev == "NNG" and cur == "XSN" and nxt == "XSA":
                        morph_temp.append( morph_eojeol[i]+morph_eojeol[i+1]+morph_eojeol[i+2])
                        tag_temp.append("VV")
                        i += 3
                        continue
                    if prev == "XR" and cur=="XSN" and nxt =="XSA":
                        morph_temp.append( morph_eojeol[i]+morph_eojeol[i+1]+morph_eojeol[i+2])
                        tag_temp.append("VV")
                        i += 3
                    morph_temp.append(morph_eojeol[i])
                    tag_temp.append(tag_eojeol[i])
                    i += 1
            if flag:
                eojeol_temp.append([i+"/"+j for i,j in zip(morph_temp,tag_temp)])
            else:
                eojeol_temp.append([i + "/" + j for i, j in zip(morph_eojeol, tag_eojeol)])

        st = ""
        for eoj in eojeol_temp:
            st += "+".join(eoj)
            st += " "
        print(st.strip(),file=mjf)


def morph_sep(morph_list):
    tag_eojeol = []
    morph_eojeol = []
    for mo in morph_list:
        tag_eojeol.append(mo[mo.rfind('/') + 1:])
        morph_eojeol.append(mo[:mo.rfind('/')])
    return morph_eojeol, tag_eojeol


def unify_task(sjf,utf, mtf, uprop):
    count = 0
    unify_mor = []
    unify_tag = []
    for line1, line2 in zip(sjf.readlines(),utf.readlines()):
        line1 = line1.strip()
        line2 = line2.strip()
        if len(line1) == 0:
            print(file=mtf)
            continue
        sejong_list = line1.split()
        utag_list = line2.split()
        unify_mor_sent = []
        unify_tag_sent = []
        for sj, ut in zip(sejong_list,utag_list):
            sj_morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", sj)
            ut_morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", ut)
            sj_mor, sj_tag = morph_sep(sj_morph_list)
            ut_mor, ut_tag = morph_sep(ut_morph_list)
            uni_mor = []
            uni_tag = []
            if sj_tag == ut_tag:
                for i in ut_mor:
                    uni_mor.append(i)
                for i in ut_tag:
                    uni_tag.append(i)
            else:
                xsv_idx = -1
                xsa_idx = -1
                for i in range(len(sj_tag)):
                    cur_tag = sj_tag[i]
                    if cur_tag == "XSV":
                        xsv_idx= i
                    if cur_tag == "XSA":
                        xsa_idx = i

                if xsv_idx != -1:
                    start_idx = -1
                    for i in range(xsv_idx+1,-1,-1):
                        if sj_tag[i] == "NNG":
                            start_idx = i
                            break
                        if sj_tag[i] == "XR":
                            start_idx = i
                            break
                        if sj_tag[i] == "MAG":
                            start_idx = i
                            break
                    if len(sj_mor[start_idx:xsv_idx+1]) != 0:
                        uni_mor.append("".join(sj_mor[start_idx:xsv_idx+1]))
                        uni_tag.append('VV')
                        for i in range(xsv_idx+1, len(sj_tag)):
                            uni_mor.append(sj_mor[i])
                            uni_tag.append(sj_tag[i])
                    else:
                        for i in sj_mor:
                            uni_mor.append(i)
                        for i in sj_tag:
                            uni_tag.append(i)
                    # continue

                if xsa_idx != -1:
                    start_idx = -1
                    for i in range(xsa_idx + 1, -1, -1):
                        if sj_tag[i] == "NNG":
                            start_idx = i
                            break
                        if sj_tag[i] == "XR":
                            start_idx = i
                            break
                        if sj_tag[i] == "MAG":
                            start_idx = i
                            break
                    if len(sj_mor[start_idx:xsa_idx+1]) != 0:
                        uni_mor.append("".join(sj_mor[start_idx:xsa_idx+1]))
                        uni_tag.append('VA')
                        for i in range(xsa_idx+1, len(sj_tag)):
                            uni_mor.append(sj_mor[i])
                            uni_tag.append(sj_tag[i])
                    else:
                        for i in sj_mor:
                            uni_mor.append(i)
                        for i in sj_tag:
                            uni_tag.append(i)
                if xsv_idx == -1 and xsa_idx == -1:
                    for i in sj_mor:
                        uni_mor.append(i)
                    for i in sj_tag:
                        uni_tag.append(i)

            for i in range(len(uni_mor)):
                uni_mo = uni_mor[i]
                uni_ta = uni_tag[i]
                if uni_mo.rfind("__") == -1:
                    for j in range(len(ut_mor)):
                        ut_mo = ut_mor[j]
                        ut_ta = ut_tag[j]
                        if ut_mo.rfind("__") != -1:
                            ut_m = ut_mo[:ut_mo.rfind("__")]
                            if uni_mo == ut_m and uni_ta==ut_ta:
                                uni_mor[i] = ut_mo
                                continue

            # uprop이용해서 어깨번호 붙이는 작업(아래)
            for i in range(len(uni_mor)):
                uni_mo = uni_mor[i]
                uni_ta = uni_tag[i]
                if uni_ta[0] == "V" and uni_ta!= "VX" and uni_ta!="VCP" and uni_ta!="VCN":
                    uprop_mor_list = []
                    uprop_num_list = []
                    uprop_mor_form = uni_mo + "다"
                    for key in uprop.keys():
                        word, num = key.split()
                        if uprop_mor_form == word:
                            uprop_mor_list.append(uni_mo)
                            uprop_num_list.append(num)
                    if len(uprop_mor_list) == 1:
                        uni_mor[i] = uprop_mor_list[0] + "__" + uprop_num_list[0]
                        continue
                    if len(uprop_mor_list) > 1:#형태소 분석이 다르며 어깨번호 용언이 많이 존재해서 어깨 번호를 사람이 매겨야 하는 것
                        count += 1
            unify_mor_sent.append(uni_mor)
            unify_tag_sent.append(uni_tag)
        sent = ""
        for idx in range(len(unify_mor_sent)):
            unify_morph_list = unify_mor_sent[idx]
            unify_tag_list = unify_tag_sent[idx]
            sent +="+".join([un_mo + "/" + ta_mo for un_mo,ta_mo in zip(unify_morph_list,unify_tag_list)])
            sent += " "
        sent.strip()
        print(sent,file=mtf)
        # unify_mor.append(unify_mor_sent)
        # unify_tag.append(unify_tag_sent)
    print(count)
    # return unify_mor, unify_tag






if __name__ == "__main__":
    pickle_path = './pickle'
    # is_pkldir(pickle_path)
    uprop_file = os.path.join(pickle_path, 'uprop_dict.pkl')
    utag = open('./corpus/sent_utag_result', 'r', encoding='utf-16')
    sejong = open('./corpus/sejong.tag', 'r', encoding="utf-16")
    unify = open('./corpus/unify.tag', 'w', encoding="utf-16")
    uprop_dict = load_pickle(uprop_file)
    unify_task(sejong,utag,unify,uprop_dict)
    # modify_xsv(sejong, xsv_sejong, uprop_dict)
    # modify_xsa(xsv_sejong, xsa_sejong,uprop_dict)
