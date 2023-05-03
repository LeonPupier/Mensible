# Dependencies
import os
import re
import spotipy
from urllib import request as rq
from urllib.parse import quote
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyClass:
	def __init__(self, software):
		# Save properties
		self.software = software

		# Spotify API credentials (user key)
		self.__CLIENT_ID = self.software.spotify_client_id
		os.environ["SPOTIPY_CLIENT_ID"] = self.__CLIENT_ID
		self.__CLIENT_SECRET = self.software.spotify_password
		os.environ["SPOTIPY_CLIENT_SECRET"] = self.__CLIENT_SECRET

		# Get environment variables
		self.__USER_ID = os.environ.get("USER_ID")

		# Check if environment variables are set and valid
		try:
			self.auth_manager = SpotifyClientCredentials(client_id=self.__CLIENT_ID, client_secret=self.__CLIENT_SECRET)
			self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
		except spotipy.exceptions.SpotifyException:
			# Bad client ID or password
			return None
	

	def download_tracks(self, pl_url, path):
		# Get playlist details
		pl_details = self.get_playlist_details(pl_url)
		if pl_details is None:
			return None

		tracks = self.check_existing_tracks(pl_details, path)

		# Get video URL for each track in the playlist (Spotify to YouTube URL)
		list_url = []
		for track in tracks:
			print(track['uri'])
			html = rq.urlopen(f"https://www.youtube.com/results?search_query={track['uri']}")
			video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

			if video_ids:
				url = "https://www.youtube.com/watch?v=" + video_ids[0]
				list_url.append(url)

		# Return playlist name, number of tracks and list of URLs
		return pl_details['pl_name'], len(tracks), list_url


	def get_playlist_details(self, pl_url):
		# Define playlist category
		fields = "items.track.track_number,items.track.name,items.track.artists.name,items.track.album.name,items.track.album.release_date,total,items.track.album.images"
		offset = 0

		# Get playlist details
		try:
			pl_name = self.sp.playlist(pl_url)["name"]
			pl_items = self.sp.playlist_items(
				pl_url,
				offset=offset,
				fields=fields,
				additional_types=["track"],
			)["items"]
		except:
			# Bad client ID or password
			return None

		# Get playlist tracks informations (name, artist, album, etc.)
		pl_tracks = []
		while len(pl_items) > 0:
			for item in pl_items:
				if item["track"]:
					track_name = self.normalize_str(item["track"]["name"])
					artist_name = self.normalize_str(
						item["track"]["artists"][0]["name"]
					)
					pl_tracks.append(
						{
							"uri": quote(
								f'{track_name.replace(" ", "+")}+{artist_name.replace(" ", "+")}'
							),
							"file_name": f"{artist_name} - {track_name}",
							"track_name": track_name,
							"artist_name": artist_name,
							"album_name": self.normalize_str(
								item["track"]["album"]["name"]
							),
							"album_date": item["track"]["album"]["release_date"],
							"track_number": item["track"]["track_number"],
							"album_art": item["track"]["album"]["images"][0]["url"],
						}
					)

			offset = offset + len(pl_items)
			pl_items = self.sp.playlist_items(
				pl_url,
				offset=offset,
				fields=fields,
				additional_types=["track"],
			)["items"]

		# Return playlist name and tracks
		return {"pl_name": pl_name, "pl_tracks": pl_tracks}


	def check_existing_tracks(self, playlist, path):
		# Get existing tracks in the folder
		existing_tracks = os.listdir(path)
		tracks = [track for track in playlist["pl_tracks"] if f"{track['file_name']}.mp3" not in existing_tracks]
		return tracks

	
	def get_user_playlists(self):
		# Get user playlists
		return [
			{"value": pl.get("uri"), "name": pl.get("name")}
			for pl in self.sp.user_playlists(self.__USER_ID).get("items")
		]


	def normalize_str(self, string):
		return string.translate(str.maketrans('\\/:*?"<>|', "__       "))
