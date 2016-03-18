import os
import re
#IMDbPY
#http://guessit.readthedocs.org/en/latest/

#input folders
input_folders =["/home/londo"]
movie_data = {} #(name,date,location)


#find files

def find_movies(input_folder,movie_data):
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if os.path.isdir(filepath):
            #avoiding folder "TV"
            if filepath.find("TV") != -1:
                continue
                
            #testing folder
            for new_filename in os.listdir(filepath):
                new_filepath = os.path.join(filepath, new_filename)
                if os.path.isdir(new_filepath):
                    movie_sub_folders =["CD1"]
                    #print(filename,new_filename)
                    if new_filename in movie_sub_folders:
                        movie_data[filename]=[list(find_movie_name(filename,filepath)),filepath]
                    else:
                        movie_data = find_movies(new_filepath,movie_data)
                elif os.path.isfile(new_filepath):
                    if is_movie_file(new_filepath):
                        movie_data[filename]=[list(find_movie_name(filename,filepath)),filepath]

        elif os.path.isfile(filepath):
            if is_movie_file(filepath):
                movie_data[filename]=[list(find_movie_name(filename,filepath)),filepath]
    return movie_data

def is_movie_file(input_file):
    movie_extensions=['avi', 'mp4', 'mkv', 'vob', 'divx','xvid','m4v']
    for movie_extension in movie_extensions:
        if input_file.endswith(movie_extension):
            return True
    return False


def find_movie_name(file_name,file_path):
    #1) year
    year = re.search(r"\d{4}",file_name)
    date =""
    if year:
        date = year.group()
        if file_name.find(year.group())> 1:
            file_name = file_name[:file_name.find(year.group())]
        else:
            file_name = file_name[file_name.find(year.group())+4:]
    #2) information tags in name

    ######## case insensitive
    information_tags =["CD1","CD2","CD3","DVD","DVDRip","HDTV","Blueray","BDRip","1080p","720p","BRRip","HDRip"]
    position = 99999
    for information_tag in information_tags:
        #print(file_name,file_name.lower().find(information_tag.lower()))
        if file_name.lower().find(information_tag.lower()) != -1:
            if file_name.lower().find(information_tag.lower()) < position:
                position = file_name.lower().find(information_tag.lower())
    if position < 9999:
        file_name = file_name[:position]
        #print("C",new_file_name,file_name)
    #3) remove parenthesis and points from end
    length = len(file_name)
    new_length = length-1
    #print("A",file_name)
    while length != new_length:
        #print("B",file_name)
        length = len(file_name)
        file_name = file_name.strip(")")
        file_name = file_name.strip("]")
        file_name = file_name.strip("(")
        file_name = file_name.strip("[")
        file_name = file_name.strip(".")
        file_name = file_name.strip("-")
        file_name = file_name.strip(" ")
        new_length = len(file_name)
    #4) remove points and "_" from the middle
    file_name = " ".join(file_name.split("."))
    file_name = " ".join(file_name.split("_"))
        
    return file_name, date
    

for input_folder in input_folders:
    movie_data = find_movies(input_folder,movie_data)


for movie in sorted(movie_data.keys()):
    print(movie_data[movie])
print(len(movie_data))
