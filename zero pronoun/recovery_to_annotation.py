import re


def morph_sep(morph_list):
    tag_eojeol = []
    morph_eojeol = []
    for mo in morph_list:
        tag = mo[mo.rfind('/') + 1:]
        m = mo[:mo.rfind('/')]
        if m == "(이)":
            # print(m)
            # print(mo)
            mo = "이/VCP"
        if tag == "VV" or tag == "VA":
            tag_eojeol.append(mo[mo.rfind('/')+1:])
            morph_eojeol.append(mo[:mo.rfind('/')])
            continue
        if tag[0] == "N" and tag != "NNN":
            if m.rfind("__") != -1:
                tag_eojeol.append(mo[mo.rfind('/') + 1:])
                morph_eojeol.append(mo[:mo.rfind('__')])
            else:
                tag_eojeol.append(mo[mo.rfind('/')+1 :])
                morph_eojeol.append(mo[:mo.rfind('/')])
            tag_eojeol.append(" ")
            morph_eojeol.append(" ")
            continue

        if m.rfind("__") != -1:
            tag_eojeol.append(mo[mo.rfind('/')+1 :])
            morph_eojeol.append(mo[:mo.rfind('__')])
            continue
        if tag == "NNN":
            tag_eojeol.append(mo[mo.rfind('/')+1 :])
            morph_eojeol.append(mo[:mo.rfind('/')])
            continue
        else:
            tag_eojeol.append(mo[mo.rfind('/')+1 :])
            morph_eojeol.append(mo[:mo.rfind('/')])
            continue
    return morph_eojeol, tag_eojeol


def minus_slash(speakf,recof, annof):
    for line1,line2 in zip(speakf,recof.readlines()):
        line1 = line1.strip()
        line2 = line2.strip()
        if len(line1) == 0:
            print(file=annof)
            continue
        line_list = line2.split()
        result = []
        for eojeol in line_list:
            morph_list = re.split("(?<=/[A-Z]{2})\+|(?<=/[A-Z]{3})\+", eojeol)
            mor, _ = morph_sep(morph_list)
            result.append("".join(mor))
        print(line1, end=" ",file=annof)
        print(" ".join(result),file=annof)


def insert_file_info(annotation_f,info_f,result):
    fn = info_f.read()
    fn_list = fn.split("\n")
    print(fn_list[0],file=result)
    fn_list = fn_list[1:]
    idx = 0
    for line in annotation_f.readlines():
        line = line.strip()
        if len(line) == 0:
            print(file=result)
            print(fn_list[idx],file=result)
            idx += 1
            continue
        print(line,file=result)


if __name__ == "__main__":
    speaker_f = open("./corpus/speaker_info.txt",'r',encoding="utf-16")
    recovery_f = open('./corpus/recovery_debug.tag', 'r', encoding="utf-16")
    annotation_f = open("./corpus/annotation.tag", 'r', encoding="utf-16")
    info_f = open("./corpus/filename_info.txt",'r',encoding="utf-16")
    result = open("./corpus/result_final.txt",'w',encoding="utf-16")
    # minus_slash(speaker_f,recovery_f, annotation_f)
    insert_file_info(annotation_f,info_f,result)