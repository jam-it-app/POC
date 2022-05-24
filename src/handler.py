import os,json
from .common.spotify import *


def handle(event,context):
    print("Triggered by event " + json.dumps(event))

    print("initializing Spotify Client")

    spotify_client = SpotifyClient(client_id=os.getenv('SPOTIFY_CLIENT_ID'),client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))

    print("Getting current user details")
    print(spotify_client.getUserProfile())

    track = input("What song would you like to play? ")
    track_id = spotify_client.getTrackId(track=track)
    print("track_id" , track_id)
    playlist = input("What playlist would you like to add to? ")
    playlist_id = spotify_client.getPlaylistId(playlist=playlist)
    print("playlist_id" , playlist_id)

    
    print("Playlist content prior to update")
    print(spotify_client.getItemsInPlaylist(playlist_id=playlist_id))



    spotify_client.addItemToPlaylist(playlist_id=playlist_id,track_id=track_id)


    print("Playlist content after update")
    print(spotify_client.getItemsInPlaylist(playlist_id=playlist_id))



#tes"4U45aEWtQhrm8A5mxPaFZ7"


