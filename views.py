import instaloader
import pandas as pd
import re
import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_instagram_username_from_reel(reel_url, L):
    try:
        shortcode = re.findall(r'/reel/([^/]+)/', reel_url)[0]
        logging.info(f"Extracted shortcode: {shortcode}")
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        username = post.owner_username
        logging.info(f"Extracted username: {username}")
        return username
    except instaloader.exceptions.LoginRequiredException:
        logging.error("Checkpoint required. Please verify your account manually.")
        return None
    except instaloader.exceptions.ConnectionException as e:
        logging.error(f"Connection error: {e}")
        return None
    except Exception as e:
        logging.error(f"Error extracting username: {e}")
        return None

def get_number_of_followers(username, L):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        followers = profile.followers
        logging.info(f"Extracted followers: {followers}")
        return followers
    except instaloader.exceptions.LoginRequiredException:
        logging.error("Checkpoint required. Please verify your account manually.")
        return None
    except Exception as e:
        logging.error(f"Error extracting followers: {e}")
        return None

def get_views_count(reel_url, L):
    try:
        shortcode = re.findall(r'/reel/([^/]+)/', reel_url)[0]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        views = post._iphone_struct['play_count']
        logging.info(f"Extracted views: {views}")
        return views
    except instaloader.exceptions.LoginRequiredException:
        logging.error("Checkpoint required. Please verify your account manually.")
        return None
    except instaloader.exceptions.ConnectionException as e:
        logging.error(f"Connection error: {e}")
        return None
    except Exception as e:
        logging.error(f"Error extracting views: {e}")
        return None

async def fetch_data(row, L, session):
    reel_url = row['reel_url']
    username = get_instagram_username_from_reel(reel_url, L)
    if username:
        followers = get_number_of_followers(username, L)
        views = get_views_count(reel_url, L)
        if followers is not None and views is not None:
            return {'reel_url': reel_url, 'username': username, 'followers': followers, 'views': views}
        else:
            return {'reel_url': reel_url, 'username': username, 'followers': 'Failed to get followers', 'views': 'Failed to get views'}
    else:
        return {'reel_url': reel_url, 'username': 'Failed to extract username', 'followers': '', 'views': ''}

async def main():
    L = instaloader.Instaloader()
    session_file = 'session-avinashkumar8._'  # Replace with your actual username
    
    # Load session if it exists
    try:
        L.load_session_from_file('avinashkumar8._', session_file)  # Replace with your actual username
        logging.info("Session loaded successfully.")
    except FileNotFoundError:
        logging.info("Session file not found. Logging in...")
        username = input("Enter your Instagram username: ")
        password = input("Enter your Instagram password: ")
        try:
            L.login(username, password)
            L.save_session_to_file(session_file)
        except instaloader.exceptions.BadCredentialsException:
            logging.error("Login error: Wrong password. Please check your credentials and try again.")
            return

    df = pd.read_excel('instagram_data.xlsx', sheet_name='Sheet1')

    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, row in df.iterrows():
            tasks.append(fetch_data(row, L, session))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Convert results to DataFrame and save to Excel
    results_df = pd.DataFrame(results)
    with pd.ExcelWriter('instagram_data.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        results_df.to_excel(writer, sheet_name='Results', index=False)

if __name__ == "__main__":
    asyncio.run(main())
