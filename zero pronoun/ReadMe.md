# 1. Introduction

- ### 개요

  - 필수논항 생략여부 검출

- ### 구현현황

  - O
    - 생략된 필수논항에 대한 기본적인 복원
    - ./corpus/zero_pronoun_corpus.conll
  - X  →  [utagger](<http://nlplab.ulsan.ac.kr/doku.php?id=start>) 이용
    - 관형절에 대한 복원
    - 조사가 생략된 경우에 대한 처리

- ### 사용환경

  - python >= 3.5
  - pandas

- ### 최종 수정 날짜

  - 2020-06-26

# 2. Project structure

- ### zero_pronoun_resolution/

  - #### corpus/

    - sejong(sent).txt
    - sejong_raw(sent).txt
    - sejong_sh.txt  -------------  용언 어깨번호가 부착된 세종 대화체 말뭉치
    - utagger(sent).txt
    - zero_pronoun_corpus.conll  -------------  필수논항 생략여부가 표시된 말뭉치

  - #### documents/

    - 사전에 없는 용언.txt
    - 용언 필수격 정리.hwp
    - 조사 및 어미 종류.hwp
    - 조사오류 수정목록.hwp
    - 진행상황 정리(outline).hwp

  - #### pickle/

    - case_frame_dict.pkl
    - case_frame_list.pkl
    - josa_list.pkl
    - josa_set.pkl
    - uprop_dict.pkl

  - #### sj_pos_corpus/

    - (작업에 사용한 말뭉치)

  - #### sj_현대구어/

    - 말뭉치목록_현대구어.xls
    - 말뭉치통계_현대구어.xls
    - 현대구어말뭉치_구축지침.hwp

  - #### upropbank/

    - 의미역 부착 격틀 사전.xls

  - case_frame_dictionary.py  -------------  필수논항 생략여부 판단근거(조사 및 어미 종류.hwp 참조)

  - zero_pronoun_resolution.py