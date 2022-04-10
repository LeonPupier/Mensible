# Dependencies
import os, re, sys, spotipy
from urllib import request as rq
from urllib.parse import quote
from pyfiglet import figlet_format
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_dl import YoutubeDL

class SpotifyClass:
	def __init__(self):
		self.__CLIENT_ID = os.environ.get("CLIENT_ID")
		self.__CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
		self.__USER_ID = os.environ.get("USER_ID")

		self.auth_manager = SpotifyClientCredentials(client_id=self.__CLIENT_ID, client_secret=self.__CLIENT_SECRET)
		self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

	def get_user_playlists(self):
		return [
			{"value": pl.get("uri"), "name": pl.get("name")}
			for pl in self.sp.user_playlists(self.__USER_ID).get("items")
		]

	def normalize_str(self, string):
		return string.translate(str.maketrans('\\/:*?"<>|', "__       "))

	def get_playlist_details(self, pl_url):
		offset = 0
		fields = "items.track.track_number,items.track.name,items.track.artists.name,items.track.album.name,items.track.album.release_date,total,items.track.album.images"
		pl_name = self.sp.playlist(pl_url)["name"]
		pl_items = self.sp.playlist_items(
			pl_url,
			offset=offset,
			fields=fields,
			additional_types=["track"],
		)["items"]

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

		return {"pl_name": pl_name, "pl_tracks": pl_tracks}

	def create_download_directory(self, dir_name):
		path = f"{os.environ.get('DOWNLOAD_PATH')}/{dir_name}"

		if os.path.exists(path):
			return path

		try:
			os.makedirs(path)
			return path
		except OSError:
			return

	def check_existing_tracks(self, playlist, path):
		existing_tracks = os.listdir(path)
		tracks = [track for track in playlist["pl_tracks"] if f"{track['file_name']}.mp3" not in existing_tracks]
		return tracks

	def download_tracks(self, pl_url):
		pl_details = self.get_playlist_details(pl_url)
		path = self.create_download_directory(pl_details["pl_name"])
		tracks = self.check_existing_tracks(pl_details, path)

		print(f"[info] Downloading {len(tracks)} tracks from {pl_details['pl_name']}")

		list_url = []
		for track in tracks:
			html = rq.urlopen(f"https://www.youtube.com/results?search_query={track['uri']}")
			video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

			if video_ids:
				url = "https://www.youtube.com/watch?v=" + video_ids[0]
				list_url.append(url)

		return list_url

#########
# TESTS #
#########

# ENVIRONMENT
import config

# PROGRAM
spotify = SpotifyClass()
spotify.download_tracks("https://open.spotify.com/playlist/121iThmBUZt2t5sLPP7L8m")