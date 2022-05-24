

import requests,json
import base64

# message = "Python is fun"
# message_bytes = message.encode('ascii')
# base64_bytes = base64.b64encode(message_bytes)

class SpotifyClient:
    def __init__(self,client_id,client_secret):
        print(client_id,client_secret)
        self.authorize(client_id)
        bearer_token = None
        if not bearer_token:
            bearer_token = self.getOauthToken(client_id,client_secret)
        self.api_key = bearer_token

    def authorize(self,client_id):
        #url = 'https://accounts.spotify.com/api/login'
        url ="https://accounts.spotify.com/authorize"
        response = ""

        # request_body = {
        #     "grant_type": "client_credentials",
        #     "client_id": client_id,
        #     "response_type": "code",
        #     "redirect_uri":"",
        #     "scope": "playlist-read-collaborative playlist-modify-public user-library-read user-read-email user-read-private playlist-modify-private user-read-private playlist-read-private" 
        # }
        scope="playlist-read-collaborative playlist-modify-public user-library-read user-read-email user-read-private playlist-modify-private user-read-private playlist-read-private" 
        redirect_uri = "http://localhost:8080/"

        url = 'https://accounts.spotify.com/authorize'
        url += '?response_type=token'
        url += '&client_id=' + client_id
        url += '&scope=' + scope
        url += '&redirect_uri=' + redirect_uri
        print(url)
        try:
            response = requests.get(
                url =url
            )
            print("login response status")
            print(response.status_code)

        except Exception as e:
            print("Error getting Oauth Token")
            print(e)
        print(response.text)
        #print(response.json()["access_token"]  )
        return
       
    def getOauthToken(self,client_id,client_secret):
        url = 'https://accounts.spotify.com/api/token'
        response = ""

        request_body = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        try:
            response = requests.post(
                url =url,
                data=request_body
            )
            print("Oauth response status")
            print(response.text)

        except Exception as e:
            print("Error getting Oauth Token")
            print(e)
        
        return response.json()["access_token"]        

    def getUserProfile(self):

        url = 'https://api.spotify.com/v1/me'
        try:
            response = requests.get(
                url,
                headers = {
                    "Content-Type": "application/json","Authorization": "Bearer "+"BQAxkstTWfMJ8XDzHgIzPm65cQ9HrJvMdeVaqWecvDYTyoVVM0ClsBe9oSgFLBUGXoEQBg7iryWSctW2lT80wFpfegvJKOtrE8ddDg0E_E47cnPFn5L6habk4fRUT5UC09X5X4PeesKk1JYUQFwTWglmBoKAWI2xb_nAASUINFOv_ZCYMReMq5e6DKkZvqZadVANpmM1X3Iw8RgPJUttUq9MEkuEdsoS5sHbQ6FRxkIWVw0FoZpkdJtV2hL8RvD3"
                }
            )
        except Exception as e:
            print("Error sending song request")
            print(e)

        return response.text


    def addItemToPlaylist(self,playlist_id,track_id):

        track_uri = f"spotify:track:{track_id}"
        print(f"Trying to add {track_uri} to {playlist_id}")
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        request_body = {
            "uris": [track_uri]
        }
        headers = {
            "Content-Type": "application/json","Authorization": "Bearer "+self.api_key
        }
        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=request_body
            )
        except Exception as e:
            print("Error sending song request")
            print(e)
        #print(response.text)
        return response.status_code

    def getPlaylistId(self,playlist):
        url = f'https://api.spotify.com/v1/me/playlists'
        try:
            response = requests.get(
                url,
                headers = {
                    "Content-Type": "application/json","Authorization": "Bearer "+self.api_key
                }
            )
        except Exception as e:
            print("Error sending song reuqest")
            print(e)
        print(response.status_code)
        print(response.text)
        for playlist_obj in response.json()["items"]:
            #print(playlist)
            if playlist_obj["name"] == playlist:
                return playlist_obj["id"]
            

    def getTrackId(self,track):
        url = f'https://api.spotify.com/v1/search'
        data ={"q":track,"type":"track","limit":1}
        try:
            response = requests.get(
                url,
                headers = {
                    "Content-Type": "application/json","Authorization": "Bearer "+self.api_key
                },
                params=data,
            )
            print(response.text)
        except Exception as e:
            print("Error sending song reuqest")
            print(e)


        return response.json()["tracks"]["items"][0]["id"]



    def getItemsInPlaylist(self,playlist_id):
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        try:
            response = requests.get(
                url,
                headers = {
                    "Content-Type": "application/json","Authorization": "Bearer "+self.api_key
                }
            )
        except Exception as e:
            print("Error sending song reuqest")
            print(e)

        return response.json()["tracks"]["items"]