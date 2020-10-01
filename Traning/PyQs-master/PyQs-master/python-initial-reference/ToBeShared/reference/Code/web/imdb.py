from flask import Flask,request, jsonify
import json 

app = Flask(__name__)

output = """
{"Title":"Venom","Year":"2018","Rated":"N/A","Released":"05 Oct 2018","Runtime":"112 min","Genre":"Action, Sci-Fi","Director":"Ruben Fleischer","Writer":"Jeff Pinkner (screenplay by), Scott Rosenberg (screenplay by), Kelly Marcel (screenplay by), Jeff Pinkner (screen story by), Scott Rosenberg (screen story by), Todd McFarlane (Marvel's Venom Character created by), David Michelinie (Marvel's Venom Character created by)","Actors":"Tom Hardy, Michelle Williams, Riz Ahmed, Scott Haze","Plot":"When Eddie Brock acquires the powers of a symbiote, he will have to release his alter-ego 'Venom' to save his life.","Language":"English","Country":"USA, China","Awards":"N/A","Poster":"https://m.media-amazon.com/images/M/MV5BNzAwNzUzNjY4MV5BMl5BanBnXkFtZTgwMTQ5MzM0NjM@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.0/10"},{"Source":"Metacritic","Value":"35/100"}],"Metascore":"35","imdbRating":"7.0","imdbVotes":"114,862","imdbID":"tt1270797","Type":"movie","DVD":"18 Jun 2013","BoxOffice":"N/A","Production":"Vis","Website":"N/A","Response":"True"}
"""


@app.route("/", methods=["GET"])
def index():
    print(request.url, request.args)
    resp = jsonify(json.loads(output))
    resp.status_code = 200 
    return resp


  
    

if __name__ == '__main__':
    app.run()
    
    