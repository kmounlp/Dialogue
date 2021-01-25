def seperate(rawf, raw_sentf):
    for line in rawf.readlines():
        line = line.strip()
        if len(line) == 0:
            print(file=raw_sentf)
            continue
        if line[0] == "#":
            continue
        print(line[line.find(':')+2:],file=raw_sentf)

if __name__ == "__main__":
    rawf = open('./corpus/sejong_raw(sent).txt', 'r', encoding='utf-16')
    raw_sentf = open('./corpus/raw_sent_for_utag.txt', 'w', encoding="utf-16")
    seperate(rawf,raw_sentf)



