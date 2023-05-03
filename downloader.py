# Dependencies
import os, requests, shutil, logging, pytube
from threading import Thread
from tkinter import END
from pytube import *

# Internal dependencies
from utils import *
from board import Board
from spotify import SpotifyClass

class Downloader:
	def __init__(self, window):
		# Save properties
		self.window = window
		self.software = self.window.software

		# Variables
		self.nb_video = 0


	def search_video(self):
		# Set the cursor to wait mode (Windows and Linux)
		if os.name != 'posix':
			self.window.configure(cursor='wait')
		else:
			self.window.configure(cursor='watch')
		
		# Saves informations of the selection mode
		self.mode_plateform = self.software.mode_plateform
		self.mode_download = self.software.mode_download
		self.download_type = self.software.download_type

		# Check if the folder to store downloads exists
		if not os.path.exists(f'{self.software.path}'):
			self.window.status.set(self.software.l.lang['folder_error'])
			self.window.configure(cursor='')
			return

		# Stop if there is too much video in the queue
		if self.software.current_queue == 3:
			self.window.configure(cursor='')
			return

		# Check mode download selected
		if self.mode_download is None:
			self.window.status.set(self.software.l.lang['download_mode'])
			self.window.txt_btn.set(self.software.l.lang['download'])
			self.window.btn_search.configure(state='normal', cursor='hand2')
			self.window.configure(cursor='')
			return

		# Waiting download informations
		self.window.queue_label.configure(text=f"{self.software.l.lang['download_queue']} {self.software.current_queue}/3")
		self.window.status.set(self.software.l.lang['loading_download'])
		self.window.update()

		# Get the url of the video
		self.url = self.window.txt_url.get()

		# Check if the download mode is single or playlist
		if self.download_type == 'single':
			# Check if the url is valid
			while (1):
				try:
					self.yt = YouTube(self.url)
					self.yt.title = self.safe_title(self.yt)
					break

				except (pytube.exceptions.RegexMatchError):
					# Quit if URL is invalid
					self.window.config(cursor='')
					self.window.status.set(self.software.l.lang['valid_url'])
					if self.software.current_queue != 0:
						self.window.queue_label.configure(text=f"{self.software.l.lang['download_queue']} {self.software.current_queue}/3")
					else:
						self.window.queue_label.configure(text="")
					return

				except Exception as e:
					logging.debug(f'Error Pytube: {e}')

			# Download the thumbnail
			self.download_thumbnail(self.yt.thumbnail_url, self.yt.title)

			# Prepare the queue space
			self.window.label_img_void.pack_forget()
			self.window.label_txt_void.pack_forget()
			self.window.lbl_link.pack_forget()

			# Display current queue number
			self.software.current_queue += 1
			self.window.queue_label.configure(text=f"{self.software.l.lang['download_queue']} {self.software.current_queue}/3")
			self.window.status.set("")

			# Set the URL entry to default
			self.window.txt_url.delete(0, END)
			if self.download_type == 'single':
				self.window.txt_url.insert(0, 'https://www.youtube.com/watch?v=')
			else:
				self.window.txt_url.insert(0, 'https://www.youtube.com/playlist?list=')

			# Reset cursor to default
			self.window.config(cursor='')

			# Download informations of the video
			self.download_info(self.yt)

			# Create the board for download
			self.board = Board(self)
			self.board.instance()
			self.nb_video += 1

			# Download the video
			thread_download = Thread(target=self.board.download_video, args=(self.yt,))
			thread_download.start()


		# Playlist mode
		elif self.download_type == 'playlist':

			# Platform
			if self.mode_plateform == 'youtube':
				self.playlist = Playlist(self.url)
			else:
				self.spotify = SpotifyClass(self.software)
				self.playlist = self.spotify.download_tracks(self.url, self.software.path)
				if self.playlist is None:
					self.window.config(cursor='')
					self.window.status.set(self.software.l.lang['valid_url'])
					return

			# Download informations of the playlist
			try:
				self.download_info(self.playlist)

			except Exception as e:
				# Display error and reset cursor
				self.window.config(cursor='')
				self.window.status.set(self.software.l.lang['valid_url'])
				logging.debug(f'Error download infos Playlist: {e}')
				return

			# End cursor animation
			self.window.config(cursor='')

			# Prepare the queue space
			self.window.label_img_void.pack_forget()
			self.window.label_txt_void.pack_forget()
			self.window.lbl_link.pack_forget()

			# Display current queue number
			self.software.current_queue += 1
			self.window.queue_label.configure(text=f"{self.software.l.lang['download_queue']} {self.software.current_queue}/3")

			# Propreties of the playlist
			if self.mode_plateform == 'youtube':
				self.list_videos = self.playlist.video_urls
				self.length_playlist = self.playlist.length
			else:
				self.list_videos = self.playlist[2]
				self.length_playlist = self.playlist[1]

			# Create the board for download
			self.board = Board(self)
			self.board.instance()

			# Create the list of video object for download
			for url in self.list_videos:
				while (1):
					try:
						yt = YouTube(url)
						yt.title = self.safe_title(yt)
						Thread(target=self.board.download_video, args=(yt,)).start()
						break
					except:
						logging.debug(f'Error Pytube in Playlist mode: {e}')
			
			# Increment the number of video
			self.nb_video += 1


	def safe_title(self, yt_obj):
		# Save the title
		safe_title = yt_obj.title

		# Remove the forbidden characters
		for carac in '''/:*?"<>|''':
			if carac in yt_obj.title:
				safe_title = ''.join(safe_title.split(carac))
		
		return safe_title


	def download_thumbnail(self, url_image, title_image):
		# Get the thumbnail
		r = requests.get(url_image, stream=True)
		r.raw.decode_content = True

		# Create the folder if it doesn't exist yet (Windows and Linux)
		if os.name != 'posix':
			path_thumbnail = f"C:/Windows/Temp/MensibleThumbnail/{title_image}.jpg"
		else:
			path_thumbnail = f"/tmp/MensibleThumbnail/{title_image}.jpg"

		# Write the thumbnail into the directory
		with open(path_thumbnail, 'wb') as f:
			shutil.copyfileobj(r.raw, f)
			logging.info(f"The thumbnail '{title_image}' was written in the folder")
	

	def download_info(self, yt_obj):
		# Initialize the properties
		self.title = 'N/A'
		self.views = 'N/A'
		self.owner = 'N/A'
		self.author = 'N/A'
		self.length = 'N/A'
		self.publish_date = 'N/A'

		# Properties of Spotify support
		if type(yt_obj) == tuple:
			self.title = yt_obj[0]
			self.length = yt_obj[1]

		# Properties of YouTube support
		else:
			self.title = yt_obj.title
			self.views = yt_obj.views

			# Get the publish date of the video
			try:
				self.publish_date = yt_obj.publish_date
			except AttributeError:
				pass

			# Get the owner of the video
			try:
				self.owner = yt_obj.owner
			except (IndexError, AttributeError):
				pass

			# Get the author of the video
			try:
				self.author = yt_obj.author
			except AttributeError:
				pass

			# Get the length of the video
			try:
				self.length = yt_obj.length
			except AttributeError:
				pass
