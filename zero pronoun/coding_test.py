def solution(records):
    window, box = [], []
    s_flag, c_flag = 0, 0
    for noti in records:
        name, state = noti.split()
        if state == "share":
            c_flag = 0
            content = f"{name} shared your post"
            if s_flag == 0:
                window.append(content)
                print(window)
            elif s_flag == 1:
                sent = window[-1].split()
                sent.insert(1, f"and {name}")
                print(sent)
            elif s_flag > 1:
                sent[1] = f"and {s_flag} others"
                print(sent)
            s_flag += 1

        elif state == "comment":
            s_flag = 0
            content = f"{name} commented your post"
            if c_flag == 0:
                window.append(content)
                print(window)
            elif c_flag == 1:
                sent = window[-1].split()
                sent.insert(1, f"and {name}")
                print(sent)
            elif c_flag > 1:
                sent[1] = f"and {s_flag} others"
                print(sent)
            c_flag += 1
        elif state == "notification":
            box.append(window.pop())

        sent = ' '.join(sent)
        window[-1] = sent
        print(window)

if  __name__ == "__main__":
    # test = ["john share", "mary share", 'jay share', 'four share', 'five comment']
    # solution(test)
    records = ["john share", "mary comment", "jay share", "check notification", "check notification", "sally comment",
               "james share", "check notification", "lee share", "laura share", "will share", "check notification",
               "alice comment", "check notification"]
    solution(records)
    # answer = ["jay shared your post", "mary commented on your post", "james shared your post",
    #           "lee and 2 others share your post", "sally and alice commented on your post"]