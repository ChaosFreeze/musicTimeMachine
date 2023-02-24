import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "d28bdfff7f794841ad6633e0e4aa1a03"
CLIENT_SECRET = "46318132938747acb12ac853364f4bf3"

if __name__ == '__main__':
    date_of_song = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")
    response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date_of_song}")
    website_html = response.text
    soup = BeautifulSoup(website_html, "html.parser")
    songs = soup.select(selector="li h3.c-title")
    song_list = [song.getText().strip() for song in songs]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8080",
    ))
    user_id = sp.current_user()["id"]
    songs_uri = []
    for song in song_list:
        search_response = sp.search(q=f"track: {song} year: {date_of_song}", type="track")
        try:
            song_uri = search_response["tracks"]["items"][0]["uri"]
            songs_uri.append(song_uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify: So, Skipped.")

    playlist = sp.user_playlist_create(user=f"{user_id}", name=f"{date_of_song} Billboard 100", public=False)
    sp.playlist_add_items(playlist["id"], songs_uri)

