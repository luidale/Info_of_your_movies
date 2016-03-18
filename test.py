import itertools
def tere(s,t):
    return s,t

#list(itertools.chain.from_iterable(list2d))
#s = list(itertools.chain.from_iterable([list(tere(1,2)),1]))
#s=[list(tere("1","2")),"1"]
#r = sum([list(tere("1","2")),"1"])
#r =[item for sublist in s for item in sublist]
#print(s,r)

from guessit import guess_file_info

s=guess_file_info('Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi')
print(s["title"])
print(s.nice_string())
