
def SortData():
    with open("Question.txt", "r") as rf, open("Q.txt", "w") as wf:
        preWord = ""
        for line in rf.readlines():
            word = line[line.find("$") + 1]
            if word != preWord:
                wf.write(line)
                preWord = word
            else:
                print(word)


if __name__ == "__main__":
    SortData()
