import os
import re
import imdb
#http://guessit.readthedocs.org/en/latest/
from guessit import guessit #now version 2
import cPickle as pickle
import urllib

#input folders
input_folders =["C:/Users/agfasd/Downloads"] #,"G:/Filmid"]
movie_data = {} #(name,date,location)
os.sep = "/"

#find files
def find_movies2(input_folder,movie_data):
    #folder crowler which finds files and tests their properteis
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if os.path.isfile(filepath): #checks all files
            if is_movie_file(filename): #checks if it is moviefile
                ##############
                #when file name is sample or folder is sample then not consider or go up one folder
                ###########
                movie_data = get_info(filename,filepath,movie_data)
        elif os.path.isdir(filepath): #checks content of all folders
            find_movies2(filepath,movie_data)
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

def get_info(filename,filepath,movie_data):
    #creats data about the video
    item = guessit(filename)
    if item["type"] not in movie_data:
        movie_data[item["type"]] = {}
    if item["type"] == "movie":
        #data structure:
        #{"title--year":{"title":title,"year":year,"path":[path]}}
        title = get_info_property(item,filepath,"title")
        year = get_info_property(item,filepath,"year")
        if title+"--"+year not in movie_data[item["type"]]:
            movie_data[item["type"]][title+"--"+year]={}
            movie_data[item["type"]][title+"--"+year]["title"]=title
            movie_data[item["type"]][title+"--"+year]["year"]=year
            movie_data[item["type"]][title+"--"+year]["path"]=[filepath]
        else:
            movie_data[item["type"]][title+"--"+year]["path"].append(filepath)
    elif item["type"] == "episode":
        #data structure:
        #{"title":{"season--year":season--yeat,"episode":episode,"path":[path]}}
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

def is_movie_file(input_file):
    #will test does file is a video file
    movie_extensions=['avi', 'mp4', 'mkv', 'vob', 'divx','xvid','m4v']
    for movie_extension in movie_extensions:
        if input_file.endswith(movie_extension):
            return True
    return False
    
print("Finding files")
for input_folder in input_folders:
    print "\t",input_folder
    movie_data = find_movies2(input_folder,movie_data)
i = imdb.IMDb()

print("Collect data")
#create folders when missing
if not os.path.isdir("data"):
    os.mkdir("data")
if not os.path.isdir("data/cover"):
    os.mkdir("data/cover")
    
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
        if "cover url" in list(best_match.keys()):
            urllib.urlretrieve(best_match["cover url"],"data/cover/"+title+".jpg")
        movie_data[movie_type][title]["imdb"]=best_match
        if "rating" in best_match.keys():
            print best_match["rating"],best_match["title"]
    print "Number of "+movie_type+": ",len(movie_data[movie_type])

print("Saving data")

pickle.dump(movie_data, open( "data/movies.p", "wb" ) )
