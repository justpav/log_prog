#filenames
infile1 = "mytree.ged"
infile2 = "tree.pl"
#opening files
ged = open(infile1, 'r', encoding="UTF-8")
prolog = open(infile2, 'w', encoding="UTF-8")
gedcom = ged.readlines()
ged.close()
#data of persons
persons = []
id = ""
name = ""
surname = ""
sex = ""
for line in gedcom:
    word = line.split(' ')
    if (len(word) > 2 and word[2] == "INDI\n"):
        id = word[1]
    if word[1] == "GIVN":
        name = word[2][:-1].lower().replace("'", "")
    if word[1] == "SURN":
        surname = word[2][:-1].lower()
    if word[1] == "_MARNM":
        surname = word[2][:-1].lower()
    if word[1] == "SEX":
        sex = word[2][:-1]
    if (id != "" and name != "" and surname != "" and sex != ""):
        persons.append([id, name+" "+surname, sex])
        id = ""
        name = ""
        surname = ""
        sex = ""
#for getting name by id
def getnamebyid(id):
    for person in persons:
        if person[0] == id:
            return person[1]
#for predicate 'child'
fams = []
husb = ""
wife = ""
chil = []
for line in gedcom:
    word = line.split(' ')
    if word[1] == "HUSB":
        husb = word[2][:-1]
    if word[1] == "WIFE":
        wife = word[2][:-1]
    if word[1] == "CHIL":
        chil.append(word[2][:-1])
    if (len(word) > 2 and word[2] == "FAM\n" and (husb != '' or wife != '')):
        fams.append([husb, wife, chil])
        husb = ''
        wife = ''
        chil = []
#writing into pl-file
for person in persons:
    if person[2] == "M":
        prolog.write("male('" + person[1] + "').\n")
for person in persons:
    if person[2] == "F":
        prolog.write("female('" + person[1] + "').\n")
fam = []
for fam in fams:
    if fam[2] != []:
        for ch in fam[2]:
            if fam[0] != '':
                prolog.write("child('" + str(getnamebyid(ch)) + "', '" + str(getnamebyid(fam[0])) + "').\n")
            if fam[1] != '':
                prolog.write("child('" + str(getnamebyid(ch)) + "', '" + str(getnamebyid(fam[1])) + "').\n")
prolog.close()