"""
5. sejong(eojeol) 기준으로 용언 어깨번호 utagger_result_sh(eojeol)로부터 복사해오기
- sejong 결과대로 형태소 분석 안 되어 있으면 어깨번호 가져오지 않음
3)
input file: sejong(sent).txt, utagger(sent).txt
output file: sejong_sh.txt
"""
import re

CORP_PATH = "sj_pos_corpus/*"


def check_predicate(fr_sj, fr_ut, fw_sj):
    for i, (sj_line, ut_line) in enumerate(zip(fr_sj, fr_ut), 1):
        sj_line = sj_line.strip()
        ut_line = ut_line.strip()
        if re.search('V[V|A|X]', sj_line):  # 용언이 있는 문장만 확인
            col_idx = sj_line.find(':') + 2
            sj_sent, ut_sent = sj_line[col_idx:].split(), ut_line[col_idx:].split()
            new_sj_sent, new_ut_sent = [], []
            for sj_eojeol, ut_eojeol in zip(sj_sent, ut_sent):  # 문장을 어절별로 나눠서 용언 정보 옮겨옴
                predicate = re.findall('V[V|A|X]', sj_eojeol)  # 어절 당 용언 정보 저장(한 어절에 여러 용언 있을 수 있음)
                if predicate:  # 용언이 있는 어절
                    sj_eojeol = re.split(r'\+|\/', sj_eojeol)
                    ut_eojeol = re.split(r'\+|\/', ut_eojeol)
                    new_sj_eojeol = []
                    for pred in predicate:
                        if pred in ut_eojeol:  # 세종의 용언이 유태거 결과에도 있을 경우에만 어깨번호 가져옴
                            ut_idx = ut_eojeol.index(pred) - 1
                            try:
                                mor, sh = re.split('_{2}', ut_eojeol[ut_idx])
                                # mor, sh = ut_eojeol[ut_idx].split('__')
                                sj_idx = sj_eojeol.index(pred) - 1
                                sj_eojeol[sj_idx] += ('__' + sh)
                            except ValueError: pass
                    new_sj_eojeol = reunion(sj_eojeol, new_sj_eojeol)
                    new_sj_sent.append('+'.join(new_sj_eojeol))
                else: new_sj_sent.append(sj_eojeol)  # 용언이 없는 어절
            print(sj_line[:col_idx] + ' '.join(new_sj_sent), file=fw_sj)
        else: print(sj_line, file=fw_sj)


def reunion(sent, new_sent):
    for pair in mor_pos_pair(sent, 2):
        new_sent.append('/'.join(pair))
    return new_sent


def mor_pos_pair(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


if __name__ == "__main__":
    fr_ut = open("./corpus/utagger(sent).txt", 'r', encoding='utf-16')
    fr_sj = open('./corpus/sejong(sent).txt', 'r', encoding='utf-16')
    fw_sj = open('./corpus/sejong_sh.txt', 'w', encoding='utf-16')
    check_predicate(fr_sj, fr_ut, fw_sj)
