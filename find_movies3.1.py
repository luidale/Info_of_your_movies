####DESCRIPTION#######
#Program which is finding video files and downloads IMDB data.
#In addition, it will find does the movie/episode has subtitles in estonian at http://www.subclub.eu/.
#Steps:
#1) Finds video files in given folder(s)
#2) Is guessing the file name
#3) Is downloading IMDB info about the movie episode
#4) Is finds the subtitle link from http://www.subclub.eu/
#5) Saves data as dictionary in the output file.
######################
#v3.1
#1)saving as json

####REQUIREMENTS######
#Python 2.7 - because of IMDbPy
######################

import os
import re
import imdb
#http://guessit.readthedocs.org/en/latest/
from guessit import guessit #now version 2
import cPickle as pickle
import urllib
import json

#####PARAMETERS#######
input_folders = ["C:/Users/agfasd/Downloads","G:\Filmid"]#["C:/Users/agfasd/Downloads/vaadatud/veronn"]#[ #,"G:/Filmid"] Use / not \ in the adress
os.sep = "/"
#Use / not \ in the adress of input_folders
movie_extensions=['avi', 'mp4', 'mkv', 'vob', 'divx','xvid','m4v'] #additional file formats can be added.
output_file = "HV"
#####################

###TO DO#############
#1) 
#
#####################



#find files
def find_movies2(input_folder,movie_data):
    #folder crowler which finds files and tests are they movies/episodes or not
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if os.path.isfile(filepath): #checks all files
            if is_movie_file(filename): #checks if it is moviefile
                ##############
                #when file name is sample or folder is sample then not consider or go up one folder
                ###########
                movie_data = get_info(filename,filepath,movie_data) #creates info about movie/episode
        elif os.path.isdir(filepath): #checks content of all folders
            find_movies2(filepath,movie_data)
    return movie_data

def is_movie_file(input_file):
    #will test does file is a video file
    if input_file.split(".")[-1] in movie_extensions: #testing the file extention
        return True
    return False

def get_info(filename,filepath,movie_data):
    #creats data about the video
    item = guessit(filename) #is guessig movie name
    print "\t", filename
    if item["type"] not in movie_data:
        movie_data[item["type"]] = {}
    if item["type"] == "movie":
        #data structure:
        #{"title--year":{"title":title,"year":year,"path":[path]}}
        title = get_info_property(item,filepath,"title")
        print "\t\t", title
        year = get_info_property(item,filepath,"year")
        if title+"--"+year not in movie_data[item["type"]]:
            movie_data[item["type"]][title+"--"+year]={}
            movie_data[item["type"]][title+"--"+year]["title"]=title
            movie_data[item["type"]][title+"--"+year]["year"]=year
            movie_data[item["type"]][title+"--"+year]["path"]=[filepath]
        else:
            movie_data[item["type"]][title+"--"+year]["path"].append(filepath)
        print "\t\t", movie_data[item["type"]][title+"--"+year]["path"]
    elif item["type"] == "episode":
        #data structure:
        #{"title":{"season--year":season--year,"episode":episode,"path":[path]}}
        title = get_info_property(item,filepath,"title")
        year = get_info_property(item,filepath,"year")
        season = get_info_property(item,filepath,"season")
        episode = get_info_property(item,filepath,"episode")
        mother_folder = os.path.split(os.path.split(filepath)[0])[-1]
       
        if title.lower().find(get_info_property(guessit(mother_folder),mother_folder,"title").lower()) != -1:#for "friday night dinner" where each episode have uniqe series name but share name with folder
            title = get_info_property(guessit(mother_folder),mother_folder,"title")
        if title.lower() not in [x.lower() for x in list(movie_data[item["type"]].keys())]:
            #checks titles in lower case to avoid multiple entries
            movie_data[item["type"]][title] = {}
        elif title not in movie_data[item["type"]]:
            #if title exists but not in existing case the title in existinge case is given
            title = sorted(list(movie_data[item["type"]].keys()))[sorted([x.lower() for x in list(movie_data[item["type"]].keys())]).index(title.lower())]

        if season+"--"+year not in movie_data[item["type"]][title]:
            movie_data[item["type"]][title][season+"--"+year] = {}
        if episode not in movie_data[item["type"]][title][season+"--"+year]:                   
            movie_data[item["type"]][title][season+"--"+year]["episode"]=episode
            movie_data[item["type"]][title][season+"--"+year]["path"]=[filepath]
        else:
            movie_data[item["type"]][title][season+"--"+year]["path"].append(filepath)

    return movie_data

def get_info_property(item,filepath,property_name):
    #gets specific data from guessit container
    if property_name in item:
        item_property = str(item[property_name])
    else: #check parameter from folder name
        item_new = guessit(os.path.split(os.path.split(filepath)[0])[-1])
        if property_name in item_new:
            item_property = str(item_new[property_name])
        else:
            item_property = "ND"
    return item_property


def sublub_eu(title):
    #looks for subtitles from http://www.subclub.eu
    #non-ASCII symbols will be replaced with "?"
    page = urllib.urlopen("http://www.subclub.eu/jutud.php?otsing="+"+".join("".join([x if ord(x) < 128 else '?' for x in title]).split(" ")))
    print "\t\tSubtitle search:","http://www.subclub.eu/jutud.php?otsing="+"+".join(title.split(" "))
    for line in page:
        #print line
        if line.find("Sinu otsingule vastavaid jutustusi ei leidu kahjuks meie baasis!") != -1:
            return "No subtitles"
        if line.find("catch(e){}") != -1:
            while True:
                line = page.readline()
                if line.startswith("<a class"):
                    return "http://www.subclub.eu"+get_link(line)
#        if line.find('"title="Vastuseid leiti') != -1:
    return "No subtitle"

def get_link(line):
    #gets link form specific HTML line
    start = line.find('href="')+len('href="')
    end = line[start:].find('"')+start
    return line[start:end].strip(".")                           



#Finding files    
print("#Finding files")
movie_data = {} #(name,date,location)
for input_folder in input_folders:
    print input_folder
    movie_data = find_movies2(input_folder,movie_data)

#Collecting data
print("#Collect data")
#create folders when missing
if not os.path.isdir("data"):
    os.mkdir("data")
if not os.path.isdir("data/cover"):
    os.mkdir("data/cover")
if not os.path.isdir("data/big_cover"):
    os.mkdir("data/big_cover")

i = imdb.IMDb()
for movie_type in sorted(movie_data.keys()):
    print "Type: ",movie_type
    for title in sorted(movie_data[movie_type].keys()):                    
        print "\t",title
        best_match = i.search_movie(title.split("--")[0])
        if len(best_match) == 0: #if no matches
            movie_data[movie_type][title]["imdb"] = "ND"
            continue
        best_match =i.search_movie(title.split("--")[0])[0] #first match is chosen
        i.update(best_match)
        #get the cover thumbnail
        #maybe the best is ["full-size cover url"]
        if "cover url" in list(best_match.keys()): #testing existence of url
            if not os.path.isfile("data/cover/"+title+".jpg"):#in image will be downloaded if it does not exist
                urllib.urlretrieve(best_match["cover url"],"data/cover/"+title+".jpg")
        if "full-size cover url" in list(best_match.keys()): #testing existence of url
            if not os.path.isfile("data/big_cover/"+title+"_big.jpg"): #in image will be downloaded if it does not exist
                urllib.urlretrieve(best_match["full-size cover url"],"data/big_cover/"+title+"_big.jpg")
        movie_data[movie_type][title]["imdb"]=best_match
        if "rating" in best_match.keys():
            print "\t\t",best_match["rating"],best_match["title"]
        #Request for subtitles
        movie_data[movie_type][title]["subclub_eu"]= sublub_eu(best_match["title"])
        print "\t\tSubtitles:",movie_data[movie_type][title]["subclub_eu"]
    print "Number of "+movie_type+": ",len(movie_data[movie_type])

print("Saving data")
def jdefault(o):
    return o.__dict__

#json.dump(movie_data, open("data/"+output_file+".json", "wb" ),default=jdefault)
pickle.dump(movie_data, open( "data/"+output_file+".p", "wb" ))

