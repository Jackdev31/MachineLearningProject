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

games_genre = {
    1: "Action", 2: "Shooter", 3: "RPG", 4: "Horror",
    5: "Racing", 6: "Puzzle", 7: "Adventure", 8: "Sport"
}

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
    game_genre = int(request.form['game_genre'])
    game_type = int(request.form['game_type'])

    select = [[game_genre, game_type]]
    game = model.predict(select)[0]
    
    recommended_games = data[(data['game_genre'] == game_genre) & 
    (data['game_type'] == game_type)][['game_name', 'game_image']].values.tolist()

    recommended_games = random.sample(recommended_games, 3)

    related_games = data[data['game_genre'] == game_genre][['game_name', 'game_image']].values.tolist()
    related_games = [game for game in related_games if game not in recommended_games]

    if len(related_games) >= 3:
        related_games = random.sample(related_games, 3)
    else:
        related_games = random.sample(related_games, 3)

    for game in recommended_games:
        game[1] = f"img/{game[1]}"
        
    for game in related_games:
        game[1] = f"img/{game[1]}"
    
    return render_template('index.html',
        recommended_games=recommended_games,
        related_games=related_games,
        selected_genre=games_genre[game_genre],
        selected_game_type=games_type[game_type],
        genres=games_genre,
        game_types=games_type)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
