def sep_file(result):
    f = ""
    for line in result.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        if "# f" in line:
            line_list = line.split("\\")
            fn_list = line_list[1]
            fn = "./anno_noun/anno_"+ fn_list
            f = open(fn,'w',encoding="utf-16")
            print(line,file=f)
            print(file=f)
            continue
        print(line,file=f)
        print(file=f)

if __name__ == "__main__":
    result = open("./corpus/result_speaker.txt",'r',encoding="utf-16")

    sep_file(result)