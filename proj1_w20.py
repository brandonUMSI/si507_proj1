#########################################
##### Brandon Sapp:                 #####
##### Uniqname:  bsapp              #####
#########################################
import json
import requests
import webbrowser





class Media:

    def __init__(self, title="No Title", author="No Author", release_year = "No Release Year", url = "No URL",json = None):
        if json is None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

        else:
            self.title = json["collectionName"]
            self.author = json["artistName"]
            self.release_year = json["releaseDate"].split("-")[0]
            self.url = json["collectionViewUrl"]

    
    def info (self):
        return f"{self.title} by {self.author} {self.release_year}"
   
    def length(self):
        return 0

    
class Song(Media):
    def __init__(self,title="No Title", author="No Author", release_year = "No Release Year", url = "No URL", album = "No Album", genre = "No Genre", track_length = 0,json = None):
        
        
        if json is None:
            super().__init__(title, author, release_year, url)
            self.album = album 
            self.genre = genre
            self.track_length = track_length
        else: 
            self.title = json["trackName"]
            self.author = json["artistName"]
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.url = json["trackViewUrl"]
            self.track_length = json["trackTimeMillis"]
            self.release_year = json["releaseDate"].split("-")[0]


    def info(self):
        return super().info() + (f"[{self.genre}]")


    def length(self):
        return round(0.001 * self.track_length)


class Movie(Media):
    def __init__(self,title="No Title", author="No Author", release_year = "No Release Year", url = "No URL",  rating = "No Rating", movie_length = 0,json = None):
        

        if json is None:
            super().__init__(title, author, release_year, url)
            self.rating = rating 
            self.movie_length = movie_length 

        else: 
            self.title = json["trackName"]
            self.author = json["artistName"]
            self.release_year = json["releaseDate"].split("-")[0]
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = json["trackTimeMillis"]
            self.url = json["trackViewUrl"]


    def info(self):
        return super().info()+ (f"[{self.rating})")


    def length(self):
        return self.movie_length


 
def write_query(term,base_url = "https://itunes.apple.com/search"):
    query_params  = {}
    query_params["term"] = term
    #print (f"query params{query_params}")
    fetched_data = requests.get(base_url, params = query_params).json()
    #print (f"fetched data {fetched_data}") 
    query_results = fetched_data["results"]
    #print (f"query results{query_results}")

    return query_results

def append_results(query_results):
    song_data =[]
    movie_data =[]
    other_data = []
    all_media = {}

    for obj in query_results:
        if obj["wrapperType"] == "track":

            if obj["kind"] == "song":
                song_data.append(Song(json=obj))

            elif obj["kind"] == "feature-movie":
                movie_data.append(Movie(json=obj))
        else:
            other_data.append(Media(json=obj))

    all_media["Songs"] = song_data
    all_media["Movies"] = movie_data
    all_media["Other"] = other_data
    #print (f"song data{song_data}")
    #print (f"movie data{movie_data}")
    #print (f"other data{other_data}")
    #print (f"all media{all_media}")

    return all_media

def output(term):
    count = 1
    run_search = write_query(term)
    get_results = append_results(run_search)
    song_data = get_results["Songs"]
    movie_data = get_results["Movies"]
    other_data = get_results["Other"]

    print("\nSongs\n")
    if len(song_data) >= 1:
        for lst in range(len(song_data)):
            print(f"{count} {song_data[lst].info()}")
            count +=1
    else:
        print("Sorry no song results found")

    print("\nMovies\n")
    if len(movie_data) >= 1:
        for lst in range(len(movie_data)):
            print(f"{count} {movie_data[lst].info()}")
            count +=1
    else:
        print("Sorry no movie results found")

    print("\nOther\n")
    if len(other_data) >= 1:
        for lst in range(len(other_data)):
            print(f"{count} {other_data[lst].info()}")
            count +=1
    else:
        print("Sorry no results for other media types")

    


# Other classes, functions, etc. should go here

if __name__ == "__main__":
    query_input = str(input("Search for media or type exit to quit:"))
    if query_input == "exit":
            print("goodbye")
            
    while query_input.lower != "exit":
        output(query_input)
        preview = (input("To Continue: select an item number to preview, enter another search, or press exit to quit"))
        if query_input == "exit":
            print("goodbye")
            break
        elif int(preview) and int(preview) != 0:
            preview_link = output(query_input)[int(preview)-1].url
            if preview_link == "No Url":
                print("sorry, no preview is available")
                query_input = str(input("Search for media or type exit to quit:"))
            else:
                webbrowser.open_new(preview_link)
        else:
            output(preview)
            query_input = preview
            



    

    # your control code for Part 4 (interactive search) should go here
    
