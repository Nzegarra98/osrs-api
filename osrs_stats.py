import requests

def get_player_stats(username):
    formatted_username = username.strip().replace(" ", "%20")  # Format username
    url = f"https://templeosrs.com/api/player_stats.php?player={formatted_username}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Debugging: Print raw response (remove this later)
        print("\nRaw API Response:", data)

        # Handle "User not found" errors
        if 'error' in data:
            print(f"Error: {data['error']['Message']}")
            return

        # Extract actual stats from 'data'
        player_data = data.get('data', {})

        # Display player stats
        print(f"\nStats for {username}:")
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

            # Ensure keys exist in API response
            if level_key in player_data and rank_key in player_data:
                level = player_data[level_key]
                xp = player_data.get(xp_key, "N/A")  # Some skills may not have EHP
                rank = player_data[rank_key]

                print(f"{skill}: Level {level} | XP: {xp} | Rank: {rank}")

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)

# Ask for username input
username = input("Enter OSRS username: ")
get_player_stats(username)
