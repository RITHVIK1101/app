from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/get_player_info', methods=['POST'])
def get_player_info():
    try:
        website_url = "https://www.wolvesfootball.com/roster/varsity"
        response = requests.get(website_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        player_name = request.json['queryResult']['parameters']['player_name']  # Extract player name from Dialogflow request

        # Find the player's information on the website (assuming player names are unique)
        player_info = soup.find('div', {'data-name': player_name})

        if player_info:
            # Extract grade, position, height, and weight from the website
            grade = player_info.find_next('p').text.strip()
            position = player_info.find_next('p').find_next('p').text.strip()
            height = player_info.find_next('p').find_next('p').find_next('p').text.strip()
            weight = player_info.find_next('p').find_next('p').find_next('p').find_next('p').text.strip()

            # Construct a response
            response_text = f"{player_name} is in grade {grade}, plays as {position}, and has a height of {height} and weight of {weight}."
        else:
            response_text = "Player not found."

        return jsonify({
            "fulfillmentText": response_text
        })

    except Exception as e:
        return jsonify({
            "fulfillmentText": f"An error occurred: {str(e)}"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
