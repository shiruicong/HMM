list_char = []
list_en = []
with open("./data/raw_data.txt",'r', encoding='UTF-8') as fi:
    for line in fi.readlines():
        line = line.strip().split()
        try:
            for word in line:
                if word=="//w" :
                    char = "/"
                    en = "/w"
                else:
                    char, en = word.split("/")
                    list_char.append(char)
                    list_en.append(en)
        except : None
print(list_char)
print(list_en)




