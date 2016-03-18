from guessit import guessit
tere = guessit('CD1.avi')
if "year" not in tere:
    print("no year")
if "type" not in tere:
    print("no type")
print(tere["title"],tere["type"],tere["type"],tere)
