#The window of big cover is resized according to the big cover itself
#Big cover will be resized also if it is too big
#films are sorted according to the rating
#Cover is changed when new db is chosen or new genre is chosen
#To do:
#1)Finding files
#2)To make it more beatiful
#3)Movie list box into several columns
#4)Use database to store movie data

from Tkinter import *
import pickle
import imdb
import tkFileDialog
from PIL import Image, ImageTk
import os

def open_load_window(db_file):
    #is opening loading window
    global root_load
    global movia_data
    root_load = Toplevel()
    root_load.geometry(str(200+len(db_file.split("/")[-1])*10)+"x100")
    frame=Frame(root_load)
    frame.place(x=20,y=10)
    sign = Label(frame, text = "Loading database: "+db_file.split("/")[-1],
                 font=18)
    sign.grid(row=0, column=0,sticky = W)
    root_load.update_idletasks()
    root_load.update()

def close_load_window():
    #is closing load window
    root_load.destroy()

def show_big_cover(arg):
    #is opening big cover window
    global current_movie
    if current_movie+"_big" in big_movie_img:
        image2 = Image.open(big_movie_img[current_movie+"_big"])
        window_size = list(image2.size)
        ##resize window and image
        if window_size[0] > 800:
            window_size[1] = int(800/float(window_size[0])*window_size[1])
            window_size[0] = 800
        if window_size[1] > 800:
            window_size[0] = int(800/float(window_size[1])*window_size[0])
            window_size[1] = 800  
        global root_big_cover
        root_big_cover = Toplevel()
        root_big_cover.geometry(str(window_size[0])+"x"+str(window_size[1]))
        root_big_cover.title(current_movie)
        frame_big_cover=Frame(root_big_cover)
        frame_big_cover.grid(row=0, column=0,sticky = E)       
        image2 = Image.open(big_movie_img[current_movie+"_big"])
        image2 = image2.resize((window_size[0],window_size[1]),Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(image2)
        big_cover = Label(frame_big_cover,image = photo2)
        big_cover.image=photo2
        big_cover.bind("<Button 1>",close_big_cover) #adds hidden button to the image to close it on click
        big_cover.pack()
        root_big_cover.mainloop()

def close_big_cover(arg):
    #is closing big cover window
    root_big_cover.destroy()
    
def onselect(evt):
    #updating movie info upon selecting movie
    try:
        #testing isn't the movie list empty
        w = evt.widget
        index = int(w.curselection()[0])
    except:
        IndexError
    else:
        value = w.get(index).split("  -  ")[1]#movie name
        print 'You selected item %d: "%s"' % (index, value)
        ##changing global variable of current movie
        global current_movie
        current_movie = value
        ##changing movie info
        global movie_info
        movie_info.delete("0.0","end")
        movie_info.insert("end", movie_data[var_type.get()][value]["imdb"].summary())
        ##changing movie location
        global movie_location
        movie_location.delete("0.0","end")
        if var_type.get() == "episode":
            for location in movie_data[var_type.get()][value][sorted(movie_data[var_type.get()][value])[0]]["path"]: #as first is TV series then location of first season is given
                movie_location.insert("end", location.replace("/","\\")+"\n") 
        else:
            for location in movie_data[var_type.get()][value]["path"]:
                movie_location.insert("end", location.replace("/","\\")+"\n")
        ##changing subtitle location
        global movie_sub
        movie_sub.delete("0.0","end")
        movie_sub.insert("end",movie_data[var_type.get()][value]["subclub_eu"])
        ##changing movie picture
        global movie_img
        global cover
        if value in movie_img: #testing if image of the movie exists
            image = Image.open(movie_img[value])
            photo2 = ImageTk.PhotoImage(image)
            cover.configure(image=photo2)
            cover.image=photo2
        else:
            cover.configure(image="")

def movie_type_menu(value):
    # creates movie type menu
    try:
        #to remove previous type_menu button if exists
        global menu_type
        menu_type.destroy()
    except:
        UnboundLocalError
    global var_type
    var_type = StringVar()
    var_type.set(movie_types[0])
    menu_type = OptionMenu(frame_genres,var_type,*movie_types,command = genre_menu)
    menu_type.grid(row=1, column=0,sticky=W)

def genre_menu(value):
    #creates genre menu
    try:
        #to remove previous genre_menu button if exists
        global menu_genre
        menu_genre.destroy()
    except:
        UnboundLocalError
    var = StringVar()
    var.set(sorted(genres[value].keys())[0])
    movie_list(sorted(genres[value].keys())[0])
    menu_genre = OptionMenu(frame_genres,var,*sorted(genres[value]),command = movie_list)
    menu_genre.grid(row=3, column=0,sticky = W)

def sub_menu():
    yscrollbar_sub = Scrollbar(frame_sub)
    yscrollbar_sub.grid(row=4, column=1, sticky=N+S)
    ###Subtitles
    #global subtitles
    movie_sub_lable = Label(frame_sub, text = "Subtitles")
    movie_sub_lable.grid(row=1, column=0,sticky = N+S+E+W)
    global movie_sub
    subtitles = [""]
    var_sub = StringVar()
    var_sub.set("Subtitles")
    menu_sub = OptionMenu(frame_sub,var_sub,*subtitles,command =subtite)
    menu_sub.grid(row=2, column=0,sticky = W)
    movie_sub = Text(frame_sub,width=2, height=10,yscrollcommand = yscrollbar_sub.set)
    yscrollbar_sub.config(command=movie_sub.yview)
    movie_sub.grid(row=4, column=0, sticky=N+S+E+W)

def subtite(value):
    print "a"

def getKey(item):
    #function to sort movies by rating
    if "rating" in movie_data[var_type.get()][item]["imdb"].keys():
        return movie_data[var_type.get()][item]["imdb"]["rating"]
    else:
        return 0

def movie_list(value):
    #creates movie list
    try:
        #to remove previous genre_menu button is exists
        global movies
        movies.destroy()
    except:
        UnboundLocalError
    global xscrollbar
    global yscrollbar
    movies = Listbox(frame_movies, yscrollcommand = yscrollbar.set,xscrollcommand = xscrollbar.set ,height = 35,width = 55)
    for item in sorted(genres[var_type.get()][value], key = getKey, reverse = True):
        if "rating" in movie_data[var_type.get()][item]["imdb"].keys():
            movies.insert(END, str(movie_data[var_type.get()][item]["imdb"]["rating"])+"  -  "+item)
        else:
            movies.insert(END, "     -  "+item)
    yscrollbar.config(command=movies.yview)
    xscrollbar.config(command=movies.xview)
    movies.bind('<<ListboxSelect>>', onselect)
    movies.grid(row=0, column=0, sticky=N+S+E+W)
    ##changing the cover picture
    global cover
    global current_movie
    current_movie = sorted(genres[var_type.get()][value], key = getKey, reverse = True)[0]   
    if current_movie in movie_img: #testing if image of the movie exists
        image = Image.open(movie_img[current_movie])
        photo2 = ImageTk.PhotoImage(image)
        cover.configure(image=photo2)
        cover.image=photo2
    else:
        cover.configure(image="")
        cover.image=""
    ##changing movie info
    global movie_info
    movie_info.delete("0.0","end")
    movie_info.insert("end", movie_data[var_type.get()][current_movie]["imdb"].summary())
    ##changing movie location
    global movie_location
    movie_location.delete("0.0","end")
    if var_type.get() == "episode":
        for location in movie_data[var_type.get()][value][sorted(movie_data[var_type.get()][value])[0]]["path"]: #as first is TV series then location of first season is given
            movie_location.insert("end", location.replace("/","\\")+"\n") 
    else:
        for location in movie_data[var_type.get()][current_movie]["path"]:
            movie_location.insert("end", location.replace("/","\\")+"\n")
    ##changing movie subtitles
    global movie_sub
    movie_sub.delete("0.0","end")
    movie_sub.insert("end",movie_data[var_type.get()][current_movie]["subclub_eu"])



def collect_movie_img(input_folder):
    #collects links to all movie images
    movie_images = {}
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if os.path.isfile(filepath): #checks all files
            if filename[-3:]== "jpg":
                movie_images[filename[:-4]]=filepath
    return movie_images

def collect_sub_sites(movie_data):
    #collects subtitles sites in the database
    sub_sites = []
    for movie_type in movie_data:
        for movie in movie_data[movie_type]:
            for sub_site in movie_data[movie_type][movie]["subtitles"]:
                if sub_site not in subtitles:
                    sub_sites.add(sub_site)
    return sub_sites

def browse_db():
    #selects movie database and generates list of types, genres and movies
    db_file = tkFileDialog.askopenfilename(parent=root,title='Choose a file',filetypes=[('dbfiles', '.p'), ('all files', '.*')],initialdir="./data")
    if db_file.endswith(".p"):
        global movie_data
        global movie_types
        global genres
        global root_load
        global current_movie        
        ##window for loading
        open_load_window(db_file)
        movie_data = pickle.load(open(db_file,"rb"))
        ##collect types and genres
        movie_types =sorted(list(movie_data.keys()))
        genres = collect_genre(movie_data,movie_types)
        close_load_window()
        ##Create subtitle field
        sub_menu()
        ##Create movie type menu
        sign_type = Label(frame_genres, text = "Type")
        sign_type.grid(row=0, column=0,sticky = W)
        movie_type_menu(movie_types[0])
        ##Create lable with the name of database
        sign_database = Label(frame_database, text = "Database in use:",background = "white")
        sign_database.grid(row=2, column=0,sticky = W)
        sign_database = Label(frame_database, text = db_file.split("/")[-1],background = "white")
        sign_database.grid(row=3, column=0,sticky = W)

        
        ##Creates image section
        current_movie = sorted(genres[movie_types[0]][sorted(genres[movie_types[0]])[0]])[0]
        if current_movie in movie_img: #testing if image of the movie exists
            image = Image.open(movie_img[current_movie])
            photo2 = ImageTk.PhotoImage(image)
        else:
            photo2 = ""
        global cover
        cover = Label(frame_img, image = photo2)
        cover.image = photo2
        cover.bind("<Button 1>",show_big_cover)
        cover.grid(row=0, column=0, sticky=N+S+E+W)
        ##Create movie genre menu
        sign_genre = Label(frame_genres, text = "Genre")
        sign_genre.grid(row=2, column=0,sticky = W)
        genre_menu(movie_types[0])
        ##Adds info of first movie
        first_movie =  movie_data[movie_types[0]][sorted(genres[movie_types[0]][sorted(genres[movie_types[0]])[0]])[0]]
        if first_movie["imdb"] != "ND":
            movie_info.insert("end", first_movie["imdb"].summary())
        movie_info.grid(row=1, column=0, sticky=N+S+E+W)
        ##Adds location of first movie
        #First movies/episodes showed depends what type there exists
        movie_location.delete("0.0","end")
        if movie_types[0] == "movie": #no episode
            for location in first_movie["path"]:
                movie_location.insert("end", location.replace("/","\\")+"\n") #as first is TV series then location of first season is given    
        else:
            for location in first_movie[sorted(first_movie)[0]]["path"]:
                movie_location.insert("end", location.replace("/","\\")+"\n") #as first is TV series then location of first season is given

        
        
def collect_genre(movie_data,movie_types):
    #collects genre information from choosen database
    genres = {}
    for movie_type in movie_types:
        genres[movie_type] = {}
        for movie in movie_data[movie_type]:
            if movie_data[movie_type][movie]["imdb"] != "ND":
                if "genres" in movie_data[movie_type][movie]["imdb"].keys():
                    for genre in movie_data[movie_type][movie]["imdb"]["genres"]:
                        if genre not in genres[movie_type]:
                            genres[movie_type][genre] = [movie]
                        else:
                            genres[movie_type][genre].append(movie)
    return genres


######DATA#######
small_cover_folder = "./data/cover"
big_cover_folder = "./data/big_cover"
#################

movie_data=""
movie_types =[]
genres = []
current_movie = ""
cover = ""
movie_sub = ""
movie_img = collect_movie_img(small_cover_folder)
big_movie_img = collect_movie_img(big_cover_folder)


######GUI#######
###General
root = Tk()
root_big_cover = ""
root_load = ""
root.geometry("1150x610")
root.title("Info of your movies")

###First frame
frame_database=Frame(root)
frame_database.place(x=20,y=5)
###Find files
sign_database = Label(frame_database, text = "Find")
sign_database.grid(row=0, column=0,sticky = W)
select_db = Button(frame_database, text="Find movies", command=browse_db)
select_db.grid(row=1, column=0,sticky=W)
###Database
frame_database=Frame(root)
frame_database.place(x=20,y=200)
sign_database = Label(frame_database, text = "Database")
sign_database.grid(row=0, column=0,sticky = W)
select_db = Button(frame_database, text="Choose database", command=browse_db)
select_db.grid(row=1, column=0,sticky=W)
###Type, Genre
frame_genres=Frame(root)
frame_genres.place(x=20,y=300)

###Movie list frame
frame_movies=Frame(root)
frame_movies.grid_rowconfigure(0, weight=1)
frame_movies.grid_columnconfigure(0, weight=1)
frame_movies.place(x=140,y=25)
yscrollbar = Scrollbar(frame_movies)
yscrollbar.grid(row=0, column=1, sticky=N+S)
xscrollbar = Scrollbar(frame_movies,orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)
##List
movies = Listbox(frame_movies, yscrollcommand = yscrollbar.set,xscrollcommand = xscrollbar.set ,height = 35,width = 55)
yscrollbar.config(command=movies.yview)
xscrollbar.config(command=movies.xview)
movies.bind('<<ListboxSelect>>', onselect)
movies.grid(row=0, column=0, sticky=N+S+E+W)

###Info frame
frame_info=Frame(root)
frame_info.grid_columnconfigure(0, weight=1)
frame_info.place(x=520,y=5)
yscrollbar_info = Scrollbar(frame_info)
yscrollbar_info.grid(row=1, column=1, sticky=N+S)
yscrollbar_location = Scrollbar(frame_info)
yscrollbar_location.grid(row=3, column=1, sticky=N+S)
###Info
movie_info_lable = Label(frame_info, text = "Movie info")
movie_info_lable.grid(row=0, column=0,sticky = N+S+E+W)
movie_info = Text(frame_info,width=50, height=28,yscrollcommand = yscrollbar_info.set)
yscrollbar_info.config(command=movie_info.yview)
movie_info.grid(row=1, column=0, sticky=N+S+E+W)
###Location
movie_location_lable = Label(frame_info, text = "Location of the file")
movie_location_lable.grid(row=2, column=0,sticky = N+S+E+W)
movie_location = Text(frame_info,width=50, height=4,yscrollcommand = yscrollbar_location.set)
yscrollbar_location.config(command=movie_location.yview)
movie_location.grid(row=3, column=0, sticky=N+S+E+W)

###Image frame
frame_img=Frame(root)
frame_img.grid_columnconfigure(0, weight=1)
frame_img.place(x=950,y=25)

###Sub frame
frame_sub=Frame(root)
frame_sub.grid_columnconfigure(0, weight=1)
frame_sub.place(x=950,y=250)


mainloop()
