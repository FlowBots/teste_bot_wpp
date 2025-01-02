import requests
import logging
from app.config import APP_ID, APP_SECRET, ACCESS_TOKEN

def get_expiration_time():
    url = "https://graph.facebook.com/v14.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": ACCESS_TOKEN,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("expires_in")