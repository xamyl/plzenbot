import os
import random
import schedule
import time
import requests
from atproto import Client

BLUESKY_USERNAME = os.getenv("BLUESKY_USERNAME")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
BASE_IMAGE_URL = "https://raw.githubusercontent.com/xamyl/plzenbot/main/images/"

def get_image_list():
    try:
        api_url = "https://api.github.com/repos/xamyl/plzenbot/contents/images"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return [item['name'] for item in data if item['type'] == 'file']
    except Exception as e:
        print(f"Error fetching image list: {e}") #a sports it's in the game
        return []

def post_random_image():
    try:
        client = Client()
        client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
        image_list = get_image_list()
        if not image_list:
            print("no images found very sad")
            return
        image_filename = random.choice(image_list)
        image_url = f"{BASE_IMAGE_URL}{image_filename}"
        client.post(text=None, embed=image_url)
        print(f"Posted image: {image_url}")
    except Exception as e:
        print(f"Error posting image: {e}")

schedule.every().week.do(post_random_image)

if __name__ == "__main__":
    print("starting...")
    while True:
        schedule.run_pending()
        time.sleep(1)
