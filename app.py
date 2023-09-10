import logging
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Define a function to scrape player information from "https://www.wolvesfootball.com/roster/varsity"
def scrape_player_info(player_name):
    try:
        website_url = "https://www.wolvesfootball.com/roster/varsity"
        response = requests.get(website_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        player_infos = soup.find_all('li', class_='list-item')

        player_data = []

        for player_info in player_infos:
            # Your scraping logic here

            return player_data

    except Exception as e:
        return str(e)

@app.route('/get_player_info', methods=['GET'])
def get_player_info():
    try:
        # Extract the player_name parameter from the user's query
        player_name = request.json['queryResult']['parameters']['player_name']

        # Call the scrape_player_info function to fetch player data
        player_data = scrape_player_info(player_name)

        if player_data:
            # Find player information based on the provided player_name
            found_players = [player for player in player_data if player_name in player['Player Name'].upper()]

            if found_players:
                # Take the first found player (you can modify this logic if needed)
                player_info = found_players[0]

                # Construct the URL for the Azure web app with the player_name parameter
                azure_url = f"https://ehsfb.azurewebsites.net/get_player_info?player_name={player_info['Player Name']}"

                # Construct a response
                response_text = (
                    f"{player_info['Player Name']} is in grade {player_info['Grade']}, "
                    f"plays as {player_info['Position']}, has a height of {player_info['Height']}, "
                    f"and a weight of {player_info['Weight']}. "
                    f"You can find more information [here]({azure_url})."
                )
            else:
                response_text = "Player not found."
        else:
            response_text = "No player data available."

    except Exception as e:
        response_text = f"An error occurred: {str(e)}"

    return jsonify({
        "fulfillmentText": response_text
    })

