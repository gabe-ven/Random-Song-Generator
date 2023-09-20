from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import random

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_random_tracks_from_genre(token, genre, total_tracks=150):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    all_tracks = []
    offset = 0
    limit = 50

    while len(all_tracks) < total_tracks:
        query = f"?q=genre:{genre}&type=track&limit={limit}&offset={offset}"
        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)

        if "tracks" in json_result:
            json_tracks = json_result["tracks"]["items"]
            all_tracks.extend(json_tracks)
        else:
            print(f"Error: 'tracks' key not found in JSON response")
            break

        offset += limit

    if not all_tracks:
        print(f"No tracks found for the genre: {genre}")
        return None

    random_track = random.choice(all_tracks)
    preview_url = random_track.get("preview_url")

    random_track["preview"] = preview_url
    return random_track
