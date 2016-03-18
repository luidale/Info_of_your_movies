from Tkinter import *
#from Tkinter import ttk
import pickle
import imdb
from PIL import Image, ImageTk
import os


def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)#movie name
    print 'You selected item %d: "%s"' % (index, value)
    global movie_info
    movie_info.delete("0.0","end")
    movie_info.insert("end", movie_data[var_type.get()][value]["imdb"].summary())
    global movie_img
#    print index, len(pildid)
#    if index < len(pildid):
#        print pildid[index]
#        global pilt
    global cover
    global folder
    #print value,movie_img[value]
    if value in movie_img:
        #print("S")
        image = Image.open(movie_img[value])
        photo2 = ImageTk.PhotoImage(image)

#        photo2 = ImageTk.PhotoImage(os.path.join(folder,image))

        cover.configure(image=photo2)
        cover.image=photo2
    else:
        cover.configure(image="")

def movie_type_menu(value):
    global var_type
    global menu_type
    print "AA"
    var_type = StringVar()
    var_type.set(movie_types[0])
    #genre_menu(movie_types[0])
    menu_type = OptionMenu(frame_genres,var_type,*movie_types,command = genre_menu)
    menu_type.grid(row=1, column=0,sticky=W)
#    menu_type.place(x=5,y=25)    


def genre_menu(value):   
    try:
        #to remove previous genre_menu button
        global menu_genre
        menu_genre.destroy()
    except:
        UnboundLocalError
    var = StringVar()
    var.set(sorted(genres[value].keys())[0])
    movie_list(sorted(genres[value].keys())[0])
    menu_genre = OptionMenu(frame_genres,var,*sorted(genres[value]),command = movie_list)
    menu_genre.grid(row=3, column=0,sticky = W)
#    menu_genre.place(x=5,y=80)

def movie_list(value):
    try:
        #to remove previous genre_menu button
        global movies
        movies.destroy()
    except:
        UnboundLocalError
    #global movies
   # if movies != "":
   #     for movie2 in movies:
   #     movie.destroy()
    #global yscrollbar
    #global frame_movies
    #movies = Listbox(frame_movies,yscrollcommand=yscrollbar.set)
    #yscrollbar.config(command=movies.yview)
    #yscrollbar.pack(side=RIGHT, fill=Y)
    #for item in sorted(genres[var_type.get()][value]):
    #    movies.insert(END, item)
    #movies.place(x=200,y=20)
    #
    #global movies
    global xscrollbar
    global yscrollbar
    movies = Listbox(frame_movies, yscrollcommand = yscrollbar.set,xscrollcommand = xscrollbar.set ,height = 35,width = 40)
    for item in sorted(genres[var_type.get()][value]):
        movies.insert(END, item)
    yscrollbar.config(command=movies.yview)
    xscrollbar.config(command=movies.xview)
    movies.bind('<<ListboxSelect>>', onselect)

    movies.grid(row=0, column=0, sticky=N+S+E+W)

    
    #movies = [StringVar()]*len(genres[var_type.get()][value])
    #for i , movie in enumerate(sorted(genres[var_type.get()][value])):
     #   movies[i] = Label(frame,text = movie)
      #  movies[i].place(x=200,y=20+(20*i))
        #movie.set(movie)

def collect_genre(movie_data,movie_types):
    genres = {}
    for movie_type in movie_types:
        genres[movie_type] = {}
        #print movie_data[movie_type]
        for movie in movie_data[movie_type]:
            #print movie
            #if "title" in movie_data[movie_type][movie]:
                #print movie_data[movie_type][movie]["title"]
                #print movie_data[movie_type][movie]["imdb"]
            if movie_data[movie_type][movie]["imdb"] != "ND":
                if "genres" in movie_data[movie_type][movie]["imdb"].keys():
                    #print movie_data[movie_type][movie]["imdb"]["genres"]
                    for genre in movie_data[movie_type][movie]["imdb"]["genres"]:
                        #print genre
                        if genre not in genres[movie_type]:
                            genres[movie_type][genre] = [movie]
                        else:
                            genres[movie_type][genre].append(movie)
        #for genre in genres[movie_type]:
            #print genre
            #print len(genres[movie_type][genre])
    return genres


def collect_movie_img(input_folder):
    movie_images = {}
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if os.path.isfile(filepath): #checks all files
            if filename[-3:]== "jpg":
                movie_images[filename[:-4]]=filepath
    return movie_images

######DATA#######
print "Collecting database"
folder = "C:/Users/agfasd/Dropbox/programmeerimine/movies/"
movie_data = pickle.load(open(os.path.join(folder,"data/movies.p"),"rb"))
movie_types =sorted(list(movie_data.keys()))
#movie_genre = {"episode": ["a","b"],"movie":["c","d"]}
#movie_data2 = {"a":["AA"],"b":["BB","CC"],"c":["CC"],"d":["DD"]}
genres = collect_genre(movie_data,movie_types)
movie_img = collect_movie_img(folder+"data/cover")

#movie_img = collect_movie_img(os.path.join(folder,"data/cover"))

#print movie_img

######GUI#######
root = Tk()
root.geometry("1000x600")
root.title("Movies")
###
frame_genres=Frame(root)
frame_genres.place(x=20,y=5)
#types
sign_type = Label(frame_genres, text = "Type")
sign_type.grid(row=0, column=0,sticky = W)
#genre
sign_genre = Label(frame_genres, text = "Genre")
sign_genre.grid(row=2, column=0,sticky = W)
###
frame_movies=Frame(root)
frame_movies.grid_rowconfigure(0, weight=1)
frame_movies.grid_columnconfigure(0, weight=1)
frame_movies.place(x=120,y=5)
yscrollbar = Scrollbar(frame_movies)
yscrollbar.grid(row=0, column=1, sticky=N+S)
xscrollbar = Scrollbar(frame_movies,orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)
###
frame_info=Frame(root)
#frame_info.grid_rowconfigure(0, weight=1)
frame_info.grid_columnconfigure(0, weight=1)
frame_info.place(x=420,y=5)
yscrollbar_info = Scrollbar(frame_info)
yscrollbar_info.grid(row=0, column=1, sticky=N+S)
###
frame_img=Frame(root)
frame_img.place(x=850,y=5)
###############
movie_type_menu(movie_types[0])
genre_menu(movie_types[0])
###
image = Image.open(os.path.join(folder,movie_img[sorted(genres[movie_types[0]][sorted(genres[movie_types[0]])[0]])[0]]))
photo = ImageTk.PhotoImage(image)
cover = Label(frame_img, image = photo)
cover.pack()
###
movie_info = Text(frame_info,width=50, height=35,yscrollcommand = yscrollbar_info.set)
yscrollbar_info.config(command=movie_info.yview)

#if movie_data[movie_types[0]][sorted(movie_data[movie_types[0]].keys())[0]]["imdb"] != "ND":
if movie_data[movie_types[0]][sorted(genres[movie_types[0]][sorted(genres[movie_types[0]])[0]])[0]]["imdb"] != "ND":
    movie_info.insert("end", movie_data[movie_types[0]][sorted(genres[movie_types[0]][sorted(genres[movie_types[0]])[0]])[0]]["imdb"].summary())

#    movie_info.insert("end",movie_data[movie_types[0]][sorted(movie_data[movie_types[0]].keys())[0]]["imdb"].summary())
#movie_info.pack()
movie_info.grid(row=0, column=0, sticky=N+S+E+W)
###



#movies
#movies =""
#movies = [StringVar()]*len(genres[movie_types[0]][sorted(genres[movie_types[0]].keys())[0]])
#sign_movies = Label(frame, text = "Movies")
#sign_movies.place(x=200,y = 5)
#movies[0] = Label(frame,textvariable=genres[movie_types[0]][sorted(genres[movie_types[0]].keys())[0]][0])
#movies2.place(x=200,y = 20)
#types
#movie_type_menu(movie_types[0])
#sign_type = Label(frame, text = "Type of video")
#sign_type.place(x=5,y=5)
#genre
#genre_menu(movie_types[0])
#sign_genre = Label(frame, text = "Genre")
#sign_genre.place(x=5,y=60)
#print sorted(genres[movie_types[0]].keys())[0]
#movie_list(sorted(genres[movie_types[0]].keys())[0])




mainloop()
