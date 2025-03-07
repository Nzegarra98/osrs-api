from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_player_stats(username):
    formatted_username = username.strip().replace(" ", "%20")
    url = f"https://templeosrs.com/api/player_stats.php?player={formatted_username}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'error' in data:
            return {"error": data['error']['Message']}

        player_data = data.get('data', {})

        stats = {}
        skill_names = ["Overall", "Attack", "Defence", "Strength", "Hitpoints", 
                       "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting",
                       "Fletching", "Fishing", "Firemaking", "Crafting",
                       "Smithing", "Mining", "Herblore", "Agility",
                       "Thieving", "Slayer", "Farming", "Runecraft",
                       "Hunter", "Construction"]

        for skill in skill_names:
            level_key = f"{skill}_level"
            xp_key = f"{skill}_ehp"
            rank_key = f"{skill}_rank"

            if level_key in player_data and rank_key in player_data:
                stats[skill] = {
                    "level": player_data[level_key],
                    "xp": player_data.get(xp_key, "N/A"),
                    "rank": player_data[rank_key]
                }

        return stats

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/get_stats', methods=['GET'])
def get_stats():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400
    stats = get_player_stats(username)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
