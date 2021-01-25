import re
CORP_PATH = "sj_pos_corpus/"

def insert_speaker_info(result,result_p):
    for line in result.readlines():
        line = line.strip()
        if len(line) == 0:
            print(file=result_p)
            continue
        if line[0] == "#":
            print(line,file=result_p)
            line_list = line.split()
            filename = line_list[2]
            fread = open(filename, 'r', encoding='utf-16')
            for i, line in enumerate(fread, 2):
                line = line.strip()
                if line.startswith('<person id'):
                    person_list = line.split()
                    print(person_list[1],file=result_p)
            print("del",file=result_p)
            continue
        print(line, file=result_p)



if __name__ == "__main__":
    result = open("./corpus/result_final.txt",'r',encoding="utf-16")
    result_p = open("./corpus/result_speaker.txt", 'w', encoding="utf-16")
    # minus_slash(speaker_f,recovery_f, annotation_f)
    insert_speaker_info(result,result_p)