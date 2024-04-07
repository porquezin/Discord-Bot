import requests
from settings import TOKEN


def get_discord_user_info(user_id: str, bot_token: str= TOKEN) -> dict:
    url = f"https://discord.com/api/v9/users/{user_id}"
    
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["username"]
    else:
        return {"error": f"Não foi possível obter informações do usuário. Status code: {response.status_code}"}