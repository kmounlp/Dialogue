"""
1. convert sejong corpus to raw corpus (for uttager)
"""
import glob
import re
import sys
import os

CORP_PATH = "sj_pos_corpus/*"


def read_file():
    file_list = glob.glob(CORP_PATH)
    for file in file_list:
        yield file


def prunning(file, fwrite, file_count, utter_count, sent_count): #, fw_ignore):
    fread = open(file, 'r', encoding='utf-16')
    dialog = []
    for i, line in enumerate(fread, 2):
        if re.match('[\d]', line):
            line = line.split('\t')
            # 발화자 정보
            if line[1].startswith('<u who'):
                # speaker = re.findall('(P\d)', line[1])
                speaker = line[1].split('"')[1]
                utter = []
                utter.append(speaker)
            elif line[1].startswith('<s n'):

                sent = []
            elif line[1].startswith('</s>'):
                if sent: utter.append(' '.join(sent))
            elif line[1].startswith('</u>'):
                if len(utter) > 1:  # don't print nonverbal expressions(ex. <laugh></laugh>)
                    # print(sentences)
                    dialog.append(utter)
            # raw text화
            elif line[1].startswith('<'): pass
            else:
                line[1] = line[1].replace("::", "")
                line[1] = re.sub("(\<.+\>)", "", line[1])  # <phon></phon>
                sent.append(line[1])
            # pos_tagged_corpus

    file_count += 1
    print(f"# filename: {file}", file=fwrite)
    for utter in dialog:
        utter_count += 1
        print(utter, file=fwrite)
        for sent in utter[1:]:
            sent_count += 1
    print("\n", file=fwrite, end='')

    return file_count, utter_count, sent_count


if __name__ == "__main__":
    fwrite = open('./corpus/rawCorpus.txt', 'w', encoding='utf-16')
    # fw_ignore = open('rawCorpus_upper20utter(filename)_ignore.txt', 'w', encoding='utf-16')
    file_count, utter_count, sent_count = 0, 0, 0
    for file in read_file():
        # print(f"# filename: {file}", file=fwrite)
        file_count, utter_count, sent_count = prunning(file, fwrite, file_count, utter_count, sent_count) #, fw_ignore)
        # sys.exit()

    print(f"The number of files: {file_count}")  # 155 -> 98
    print(f"The number of utterances: {utter_count}")  # 73,723 -> 65,125
    print(f"The number of sentences: {sent_count}")  # 187,185 -> 124,886


