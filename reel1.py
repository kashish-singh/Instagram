import requests

def get_instagram_user_info(access_token):
    url = "https://graph.instagram.com/me"
    params = {
        'fields': 'username,followers_count',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
access_token = 'EAAOfo37U7V8BOwxgDFyYBu2pTdLU7gY8ZBLXplLkms79GYfqM8oPZCFOeftej7RhTWiQvp3pBjFSyvBwZByWQF1oHDKQBa0ES4zTZCfdAQfZCcpcBmDQQepJCqgz0nsv42v48FQ4T613U4jrnoogc3mohANuFONsrgzGB6m1ot8PCK7gHJMo1Yk6XNmDokakucB3LwOkbocue5BmvZCs4aB7nUQy1x3cLY1EwKoO2GlNyRp7GVnJMUAbfvckYi1wZDZD'

user_info = get_instagram_user_info(access_token)
if user_info:
    print(f"Username: {user_info['username']}")
    print(f"Followers: {user_info['followers_count']}")
else:
    print("User info not found.")
