def seperate(rawf, sp, fn):
    for line in rawf.readlines():
        line = line.strip()
        if len(line) == 0:
            print(file=sp)
            continue
        if line[0] == "#":
            print(line,file=fn)
            continue
        print(line[:line.find(':')+2], file=sp)

if __name__ == "__main__":
    rawf = open('./corpus/sejong_raw(sent).txt', 'r', encoding='utf-16')
    sp = open('./corpus/speaker_info.txt', 'w', encoding="utf-16")
    fn = open('./corpus/filename_info.txt', 'w', encoding="utf-16")
    seperate(rawf, sp, fn)