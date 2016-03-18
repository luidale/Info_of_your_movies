from Tkinter import *
#from Tkinter import ttk
import pickle
import imdb

def movie_type_menu(value):
    global var_type
    var_type = StringVar()
    var_type.set(movie_types[0])
    #genre_menu(movie_types[0])
    menu_type = OptionMenu(frame,var_type,*movie_types,command = genre_menu)
    menu_type.place(x=5,y=25)    


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
    menu_genre = OptionMenu(frame,var,*sorted(genres[value]),command = movie_list)
    menu_genre.place(x=5,y=80)

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
    global scrollbar
    movies = Listbox(frame,yscrollcommand=scrollbar.set)
    scrollbar.config(command=movies.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    for item in sorted(genres[var_type.get()][value]):
        movies.insert(END, item)
    movies.place(x=200,y=20)
    #movies = [StringVar()]*len(genres[var_type.get()][value])
    #for i , movie in enumerate(sorted(genres[var_type.get()][value])):
     #   movies[i] = Label(frame,text = movie)
      #  movies[i].place(x=200,y=20+(20*i))
        #movie.set(movie)


movie_data = pickle.load(open("data/movies.p","rb"))
movie_types =sorted(list(movie_data.keys()))
#movie_genre = {"episode": ["a","b"],"movie":["c","d"]}
#movie_data2 = {"a":["AA"],"b":["BB","CC"],"c":["CC"],"d":["DD"]}

######Collect genre info#################
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
#movie_data2 = genres

frame = Tk()
frame.title("Movies")
frame.geometry("1000x400")
scrollbar = Scrollbar(frame, orient=VERTICAL)
#movies
#movies =""
#movies = [StringVar()]*len(genres[movie_types[0]][sorted(genres[movie_types[0]].keys())[0]])
sign_movies = Label(frame, text = "Movies")
sign_movies.place(x=200,y = 5)
#movies[0] = Label(frame,textvariable=genres[movie_types[0]][sorted(genres[movie_types[0]].keys())[0]][0])
#movies2.place(x=200,y = 20)
#types
movie_type_menu(movie_types[0])
sign_type = Label(frame, text = "Type of video")
sign_type.place(x=5,y=5)
#genre
genre_menu(movie_types[0])
sign_genre = Label(frame, text = "Genre")
sign_genre.place(x=5,y=60)
print sorted(genres[movie_types[0]].keys())[0]
movie_list(sorted(genres[movie_types[0]].keys())[0])




frame.mainloop()
