from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import random

app = Flask(__name__)

data = pd.read_csv('dataimg.csv')
data = data.dropna()

X = data.drop(columns=["game_name", "game_image"])
y = data["game_name"]

model = DecisionTreeClassifier()
model.fit(X.values, y)

#genres dictionary
games_genre = {
    1: "Action", 2: "Shooter", 3: "RPG", 4: "Horror",
    5: "Racing", 6: "Puzzle", 7: "Adventure", 8: "Sport"
}
#games type dictionary
games_type = {
    1: "PC", 2: "Mobile", 3: "Console"
}

@app.route('/')
def index():
    return render_template('index.html',    
        genres=games_genre, 
        game_types=games_type)

@app.route('/suggested', methods=['POST'])
def predict():
    game_genre = int(request.form['game_genre']) # game_genre kuha sa name sang select option
    game_type = int(request.form['game_type']) # game_type kuha sa name sang select option

    pili = [[game_genre, game_type]] #pili [[game_genre, game_type]]  
    what_game = model.predict(pili)[0] #what_game holds the predicted game
    
    #recommended_games select row data game_genre and game_type
    recommended_games = data[(data['game_genre'] == game_genre) & 

    #values.tolist() from internet converts the DataFrame into a list of lists.
    (data['game_type'] == game_type)][['game_name', 'game_image']].values.tolist() 
    
    #may 5 ako ka game per genre so i used random atleast 3 of them kay tatlo gusto ko edisplay
    recommended_games = random.sample(recommended_games, 3)

    #recommended_games select row data game_genre
    related_games = data[data['game_genre'] == game_genre][['game_name', 'game_image']].values.tolist()
    #values.tolist() from internet converts the DataFrame into a list of lists.

    #related_games check if what_game already recommended kung recommended na ma display related_games nga not in recommended  
    related_games = [what_game for what_game in related_games if what_game not in recommended_games]

    if len(related_games) >= 3:
        related_games = random.sample(related_games, 3)
    else:
        pass

    #recommended_games holds game name index0 and game image index1
    for what_game in recommended_games:
        #return ta siya as formated string for img calling sa aton nga template
        #img/{what_game[1]} kay diba ang index 1 ga return sang game image if 0 butang ta da nonsense
        #kay ging buhat ni nga for loop para mag loop sang aton nga url img or directory.
        what_game[1] = f"img/{what_game[1]}"

    #related_games holds game name index0 and game image index1 same lang sang recommended_games   
    for what_game in related_games:

        #return ta siya as formated string for img calling sa aton nga template
        #img/{what_game[1]} kay diba ang index 1 ga return sang game image if 0 butang ta da nonsense
        #kay ging buhat ni nga for loop para mag loop sang aton nga url img or directory.
        what_game[1] = f"img/{what_game[1]}"
    
    return render_template('index.html',
        recommended_games=recommended_games,
        related_games=related_games,
        selected_genre=games_genre[game_genre],
        selected_game_type=games_type[game_type],
        genres=games_genre,
        game_types=games_type)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
