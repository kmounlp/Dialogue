##
import pandas as pd
import itertools
import pickle
import os
import re
import operator
from case_frame_dictionary import case_frame_dict, case_frame_list

PRED = re.compile('V[V|A]')


def make_dict(path):
    uprop = pd.read_excel(path)

    # '문형'열은 실제 예문에서 쓰이지 않은 필수격을 포함하고 있는 것으로 추정
    uprop_1 = uprop[['표제어', '의미역 격틀']].dropna()
    # 전체: 12,142 (5,189 + 6,953)
    # '의미역 격틀'이 없는 경우: 12,119 ☆
    # '문형'정보가 없는 경우: 6,492

    word_list = uprop['표제어'].tolist()
    case_list = uprop['의미역 격틀'].tolist()

    return dict(itertools.zip_longest(word_list, case_list))


##
def is_pkldir(pickle_path):
    if not os.path.isdir(pickle_path): os.mkdir(pickle_path)


def dump_pickle(dictionary, fname):
    with open(fname, 'wb') as f: pickle.dump(dictionary, f)


def load_pickle(fname):
    with open(fname, 'rb') as f: return pickle.load(f)


##
def zero_pronoun(uprop_dict, josa_dict, rfile_sh, rfile_raw, wfile):
    # expred_dict = dict()  # upropbank에 없는 용언
    for line_num, (line, line_raw) in enumerate(zip(rfile_sh, rfile_raw), 1):
        line, line_raw = line.strip(), line_raw.strip()
        if line:
            if line.startswith('#'): file_info = line.split()[2]
            else:
                print(f"# filename = {file_info}", file=wfile)
                print(f"# text = {line_raw}", file=wfile)
                sent = line.split()[1:]
                sent_raw = line_raw.split()[1:]
                if PRED.search(line): zero_pronoun_resolution(uprop_dict, josa_dict, sent, sent_raw, wfile, line_num)  #, expred_dict)
                else: to_conll(sent, sent_raw, wfile)
        else:
            print('\n', end='', file=wfile)  # double new-lines between files


def zero_pronoun_resolution(uprop_dict, josa_dict, sent, sent_raw, wfile, line_num): #, expred_dict):
    word_list = list(uprop_dict.keys())
    josa_list = josa_dict
    pred_dict = {k:v for k, v in zip(word_list, josa_list)}

    pred_id = []
    comb_sent, comb_sent_raw = [], []  # 생략성분 복원된 문장
    # 문장을 절로 분할(용언 기준)
    start_idx = 0
    for i, (eojeol, eojeol_raw) in enumerate(zip(sent, sent_raw)):
        if PRED.search(eojeol) or i == len(sent)-1:  # 두 번째 조건: 도치로 인해 문장 끝에 서술어가 오지 않는 경우를 위해
            # split into clause
            clause = sent[start_idx:i]
            clause_raw = sent_raw[start_idx:i]
            start_idx = i+1

            if PRED.search(eojeol):
                # convert predicate to dictionary format.
                pred = dictionary_form(eojeol)

                try:  # upropbank에 있는 용언
                    js_list = pred_dict[pred]
                    # 어느 js_set을 이용할 것인지 선택
                    js_set = select_js_set(js_list, clause)  # 해당 js_set을 이용해 복원
                    if js_set:  # 복원해야하면
                        clause, clause_raw = _zero_pronoun_resolution(clause, clause_raw, js_set)
                except KeyError: pass  # upropbank에 없는 용언(sejong_sh 나중에 다시 한번 검토)

            clause.append(eojeol)
            clause_raw.append(eojeol_raw)
            comb_sent.extend(clause)
            comb_sent_raw.extend(clause_raw)

    to_conll(comb_sent, comb_sent_raw, wfile)
    # 생략성분 복원된 문장을 conll 형식으로 변환


def dictionary_form(eojeol):
    pred = eojeol.split('/')[0]  # 용언이므로 항상 어절의 처음에 나온다고 상정
    pred = pred.split('__')
    if '__' not in pred: pred.append('000000')
    pred = pred[0] + '다 ' + pred[1]
    return pred


def select_js_set(js_list, clause):
    for js_set in js_list:
        js_set.insert(0, '-가')
        if not is_omission(js_set, clause):
            return False  # 모든 요소가 있는 경우: 복원 불필요
    return js_list[0]


def is_omission(js_set, clause):  # 한 set에서 생략 여부 판단: 생략 x면 return False
    for case_idx in case2idx(js_set):
        for eojeol in clause:
            for morph in eojeol.split('+'):
                if morph in case_frame_dict[case_idx][1]: return False
    return True


def case2idx(js_set):  # 격틀정보 중 어디에 속하는지 판단
    case_idx_list = []
    for idx, case in enumerate(case_frame_list):
        for js in js_set:  # js_set: 복원에 사용될 논항 set
            if js in case:
                case_idx_list.append(idx)
    return case_idx_list


def _zero_pronoun_resolution(clause, clause_raw, js_set):
    for case_idx in case2idx(js_set):
        josa_flag = 1
        for eojeol in clause:
            for morph in eojeol.split('+'):
                if morph in case_frame_dict[case_idx][1]: josa_flag = 0
        if josa_flag:  # 절 내에 필수논항에 해당하는 조사가 없는 경우
            case = ''.join(case_frame_dict[case_idx][0])
            clause.append('<NOUN>/NNN+'+case)
            clause_raw.append('<NOUN>'+case.split('/')[0])
    return clause, clause_raw


def to_conll(sent, sent_raw, wfile):  # sent: with shoulder number
    for idx, (token_eojeol, eojeol) in enumerate(zip(sent, sent_raw), 1):
        morph_list, pos_list = [], []
        token_morph_list = token_eojeol.split('+')
        for token_morph in token_morph_list:
            morph, pos = token_morph.split('/')
            morph_list.append(morph)
            pos_list.append(pos)
        morph = ' '.join(morph_list)
        pos = ' '.join(pos_list)
        print(f"{idx}\t{eojeol}\t{morph}\t{pos}", file=wfile)
    print('\n', end='', file=wfile)


def extract_josa(uprop_dict):
    word_list = list(uprop_dict.keys())
    case_list = list(uprop_dict.values())
    josa_list = []
    josa_set = set()
    for i, (case_by_word, jj) in enumerate(zip(case_list, word_list)):
        print("case_by_word(before)", case_by_word)
        if type(case_by_word) == float:
            josa_list.append(case_by_word)
        else:
            case_by_word = case_by_word.replace('} {', '}{')
            print("case_by_word", case_by_word)
            cases = case_by_word.split('}{')
            # cases = re.split(r'}.*{', case_by_word)
            josa_per_eojeol = []
            for case_info in cases:
                try:
                    case = re.findall('-[ㄱ-ㅎ]*[가-힣]*/*[가-힣]*', case_info)
                    print("case:", case)
                    josa_per_eojeol.append(case)
                except AttributeError: pass
            # print(word_list[i], i, josa_per_eojeol)
            josa_list.append(josa_per_eojeol)
            for josa in josa_per_eojeol:
                if josa: josa_set.add(josa[0])
    return josa_list, josa_set  # 32
    # dump_pickle(josa_set, './dictionary/josa_set.pkl')  # 32
    # dump_pickle(josa_list, './dictionary/josa_list.pkl')


if __name__ == "__main__":
## old uprop_dict
    # uprop_path_1 = './upropbank/200만-upropbank_mapping1_최종.xlsx'
    # uprop_path_2 = './upropbank/200만-upropbank_mapping2_최종.xlsx'
    # uprop_dict = make_dict(uprop_path_1, uprop_path_2)

## new uprop_dict
    # uprop_path = './upropbank/의미역 부착 격틀 사전.xlsx'
    # uprop_dict = make_dict(uprop_path)

## path info
    pickle_path = './pickle'
    # is_pkldir(pickle_path)
    uprop_file = os.path.join(pickle_path, 'uprop_dict.pkl')
    josa_list_file = os.path.join(pickle_path, 'josa_list.pkl')
    josa_set_file = os.path.join(pickle_path, 'josa_set.pkl')

## dict, list 정보 save and load
    # dump_pickle(uprop_dict, uprop_file)
    uprop_dict = load_pickle(uprop_file)
    # josa_list, josa_set = extract_josa(uprop_dict)
    # dump_pickle(josa_list, josa_list_file)
    # dump_pickle(josa_set, josa_set_file)
    josa_list = load_pickle(josa_list_file)
    josa_set = load_pickle(josa_set_file)  # 필수논항 조사 파악(표.국.사. '일러두기'에 있음) <- 'documents/조사 및 어미 종류.hwp'

## 대명사 marking
    fr_sj = open('./corpus/sejong_sh.txt', 'r', encoding='utf-16')
    fr_sj_raw = open('./corpus/sejong_raw(sent).txt', 'r', encoding='utf-16')
    fw_sj = open('./corpus/zero_pronoun_corpus(2).conll', 'w', encoding='utf-16')
    zero_pronoun(uprop_dict, josa_list, fr_sj, fr_sj_raw, fw_sj)
