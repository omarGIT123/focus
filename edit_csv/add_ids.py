

with open("csv.txt", "r+", encoding="utf-8") as f:
    lines = f.read().splitlines()

with open("csv.txt", "w", encoding="utf-8") as f:
    i = 0
    for line in lines:
        if (line.find(",ID,") > -1):
            i = i+1
            print(line, file=f)
        elif (line.find(str(i)) > -1):
            i = i+1
            print(line, file=f)
        elif (line.find(str(i)) == -1):
            print(line + "," + str(i), file=f)
            i = i+1
