import logging
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Define a function to scrape player information from the website
def scrape_player_info():
    try:
        website_url = "https://www.wolvesfootball.com/roster/varsity"
        response = requests.get(website_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        player_infos = soup.find_all('li', class_='list-item')

        player_data = []

        for player_info in player_infos:
            player_name = player_info.find('h2', class_='list-item-content__title').text.strip()
            details = player_info.find('p', class_='').text.strip().split('|')
            grade = details[0].strip()
            position = details[1].strip()
            height = details[2].strip()
            weight = details[3].strip()

            player_data.append({
                "Player Name": player_name,
                "Grade": grade,
                "Position": position,
                "Height": height,
                "Weight": weight
            })

        return player_data

    except Exception as e:
        return str(e)

@app.route('/get_player_info', methods=['GET', 'POST'])
def get_player_info():
    try:
        player_name = request.args.get('player_name')
        if player_name is None:
            # Handle the case where 'player_name' is missing or None
            return jsonify({
                "fulfillmentText": "Please provide a player name."
            })

        player_name = player_name.upper()  # Normalize player name
        logging.info(f"Received request for player: {player_name}")

        # Dynamically construct the URL with the player_name parameter
        complete_url = f"https://ehsfb.azurewebsites.net/get_player_info?player_name={player_name}"

        # Make a request to the constructed URL
        response = requests.get(complete_url)
        response_data = response.json()

        # Extract the player information from the response
        if 'fulfillmentText' in response_data:
            response_text = response_data['fulfillmentText']
        else:
            response_text = "Player data not available."

        return jsonify({
            "fulfillmentText": response_text
        })

    except Exception as e:
        return jsonify({
            "fulfillmentText": f"An error occurred: {str(e)}"
        })

