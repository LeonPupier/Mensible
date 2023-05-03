# Dependencies
import os, configparser, logging, pytube.request
from PIL import Image

# Internal dependencies
from language import *
from utils import *
from spotify import SpotifyClass

class SoftwareInformations:
	def __init__(self):
		# Informations
		self.title = "Mensible"
		self.version = "1.5.0"
		self.author = "Léon Pupier"
		self.website = "https://leonpupier.fr"
		self.date = "2022 / 2023"
		self.author_email = "public_contact.l2qt6@slmail.me"
		self.path_changelog = "Content/changelog.txt"
		self.path_log = "Content/log.txt"
		
		# Mode download and informations (single or multiple)
		self.download_type = 'single'
		self.mode_download = None
		self.backup_download_type = 'single'
		self.current_queue = 0

		# Fonts
		self.title_font = customtkinter.CTkFont(family='Segoe', size=18, weight='bold')
		self.void_font = customtkinter.CTkFont(family='Segoe', size=12, weight='bold')
		self.main_font_italic = customtkinter.CTkFont(family='Segoe', size=12, slant='italic')
		self.main_font = customtkinter.CTkFont(family='Segoe', size=12)
		self.bold_font = customtkinter.CTkFont(family='Segoe', size=12, weight='bold')
		self.font_mini = customtkinter.CTkFont(family='Segoe', size=5)

		# Images data download
		self.image_pause = customtkinter.CTkImage(Image.open(env('Content/Images/pause.png')), size=(30, 30))
		self.image_resume = customtkinter.CTkImage(Image.open(env('Content/Images/play.png')), size=(30, 30))
		self.image_cancel = customtkinter.CTkImage(Image.open(env('Content/Images/cancel.png')), size=(30, 30))
		self.image_finish = customtkinter.CTkImage(Image.open(env('Content/Images/finish.png')), size=(30, 30))

		# Lists of objects for the download
		self.list_p_obj = []
		self.list_video_dl_p = []
		self.list_yt_obj = []

		# Configuration
		config = configparser.ConfigParser()
		config.read(env("Content/app.ini"))

		# Load the configuration file
		self.language = config['CONFIG']['language']
		self.path = config['CONFIG']['download.path']
		self.chunk_size = config['CONFIG']['download.chunk_size']
		self.theme = int(config['CONFIG']['theme'])
		self.spotify_client_id = config['CONFIG']['spotify.client']
		self.spotify_password = config['CONFIG']['spotify.password']

		# Chunk size support
		self.chunk_size_int = int(self.chunk_size.split(' ')[0]) * 1000000
		pytube.request.default_range_size = self.chunk_size_int

		# Load the language
		if self.language == 'Francais':
			self.l = Francais()
		elif self.language == 'Deutsch':
			self.l = Deutsch()
		elif self.language == 'Español':
			self.l = Spanish()
		elif self.language == 'Italiano':
			self.l = Italiano()
		elif self.language == '中国人':
			self.l = Chinese()
		else:
			self.l = English()

		# Default path to download music (Windows and Linux)
		if self.path == '':
			if os.name != 'posix':
				self.path = f"C:/Users/{os.getlogin()}/Music/"
			else:
				self.path = f"/home/{os.getlogin()}/Music/"
		
		# Default path to store thumbnails (Windows and Linux)
		try:
			if os.name != 'posix':
				os.mkdir("C:/Windows/Temp/MensibleThumbnail")
			else:
				os.mkdir("/tmp/MensibleThumbnail")
		except FileExistsError:
			pass
			
		# Delete the old log file if it exists
		try:
			os.remove(env(self.path_log))
		except FileNotFoundError:
			pass

		# Initiate the logging system
		logging.basicConfig(filename=env(self.path_log), level=logging.DEBUG)
		logging.info("Configuration file successfully loaded")
