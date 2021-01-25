"""
3. convert utagger result file and sejong corpus file to eojeol unit
1)
sejong_to_sent()
    input file:  sj_pos_corpus
    output file: sejong_raw(sent).txt
                 sejong(sent).txt
"""
import re
import glob

CORP_PATH = "sj_pos_corpus/*"


def utagger_result_to_eojeol(fread, fwrite):
    for line in fread:
        line = line.strip()
        if line:
            if line.startswith('#'):
                print(line, file=fwrite)
                continue
            # line = rm_shoulder(line)
            line = line.split()[1:]
            for eojeol in line:
                print(eojeol, file=fwrite)
        else: print('\n', end='', file=fwrite)


def rm_shoulder(line):
    return re.sub('[_{2}\d*]', '', line)


def read_file():
    file_list = glob.glob(CORP_PATH)
    for file in file_list:
        yield file


def sejong_to_eojeol(fread, fwrite):
    for line in fread:
        if re.match('[\d]', line):
            line = line.split('\t')
            if line[1].startswith('<'): pass
            else:
                print(line[2], end ='', file=fwrite)


def sejong_to_sent(fread, fwrite, raw=False):
    for line in fread:
        line = line.strip()
        if re.match('[\d]', line):
            line = line.split('\t')
            if line[1].startswith('<u who'):
                speaker = line[1].split('"')[1]
            elif line[1].startswith('<s n'): sent = []
            elif line[1].startswith('</s>'):
                if sent:
                    print(f"{speaker}:", end=' ', file=fwrite)
                    print(' '.join(sent), file=fwrite)
            elif line[1].startswith('<'): pass
            else:
                if raw:
                    raw_sent = line[1].replace("::", "")
                    raw_sent = re.sub("(\<.+\>)", "", raw_sent)  # <phon></phon>
                    sent.append(raw_sent)
                else: sent.append(line[2])


if __name__ == "__main__":
    # # utagger to eojeol
    # fr_ut = open("./corpus/utagger_result.txt", 'r', encoding='utf-16')
    # fw_ut = open('./corpus/utagger_result_sh(eojeol).txt', 'w', encoding='utf-16')
    # utagger_result_to_eojeol(fr_ut, fw_ut)
    # print('file save: utagger_result(eojeol).txt')

    # ignore_list = open('./corpus/rawCorpus_upper20utter(filename)_ignore.txt', 'r', encoding='utf-16').read()
    # sejong to eojeol
    wfile_path = './corpus/sejong_raw(sent).txt'
    fw_sj = open(wfile_path, 'w', encoding='utf-16')
    for file in read_file():
        # if file in ignore_list: continue
        print(f"# filename: {file}", file=fw_sj)
        fr_sj = open(file, 'r', encoding='utf-16')
        # sejong_to_eojeol(fr_sj, fw_sj)
        sejong_to_sent(fr_sj, fw_sj, True)
        print("\n", end='', file=fw_sj)
    print(f'file save: {wfile_path}')
    fw_sj.close()


