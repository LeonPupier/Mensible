# Dependencies
import os, customtkinter, shutil
from urllib import request
from PIL import Image
from tkinter import X, W, StringVar
from pytube import *

# Internal dependencies
from utils import *

class Board:
	def __init__(self, downloader):
		# Save properties
		self.downloader = downloader
		self.window = self.downloader.window
		self.software = self.downloader.software

		# Variables
		self.id = self.downloader.nb_video
		self.download_type = self.downloader.download_type
		self.mode_plateform = self.downloader.mode_plateform
		self.mode_download = self.downloader.mode_download

		# Check mode download selected
		if self.download_type == 'playlist':
			self.playlist_title = self.downloader.safe_title(self.downloader.title)
			self.nb_video_downloaded = 0
			self.nb_video_to_download = len(self.downloader.list_videos)

		# Informations of the video / playlist
		self.title = self.downloader.title
		self.views = self.downloader.views
		self.owner = self.downloader.owner
		self.author = self.downloader.author
		self.length = self.downloader.length
		self.publish_date = self.downloader.publish_date


	def instance(self):
		# Create the frame for the video in the queue
		self.window.queue_frame.pack(fill=X, padx=10, pady=10)

		# Open the thumbnail
		if self.download_type == 'single':
			if os.name != 'posix':
				self.path_thumbnail = f"C:/Windows/Temp/MensibleThumbnail/{self.title}.jpg"
			else:
				self.path_thumbnail = f"/tmp/MensibleThumbnail/{self.title}.jpg"

			# If the download mode is a single video
			self.photo_thumbnail = Image.open(self.path_thumbnail)
		else:
			# If the download mode is a playlist
			if self.mode_plateform == 'youtube':
				self.photo_thumbnail = Image.open(env('Content/Images/banner_youtube.jpg'))
			else:
				self.photo_thumbnail = Image.open(env('Content/Images/banner_spotify.jpg'))

		# Display the Frame for the thumbnail
		self.thumbnail_line = customtkinter.CTkFrame(self.window.queue_frame)
		self.thumbnail_line.grid(row=self.id, column=0, sticky=W, padx=5, pady=5)

		# Resize the thumbnail and display it
		self.photo_thumbnail.thumbnail((128, 72))
		self.img_thumbnail = customtkinter.CTkImage(self.photo_thumbnail, size=(128, 72))
		self.label_thumbnail = customtkinter.CTkLabel(self.thumbnail_line, text='', image=self.img_thumbnail, height=103)
		self.label_thumbnail.pack(padx=5, pady=5)

		# Display the Frame of the download
		self.queue_line = customtkinter.CTkFrame(self.window.queue_frame, width=823, height=113)
		self.queue_line.grid_propagate(False)
		self.queue_line.grid(row=self.id, column=1, sticky=W, padx=5, pady=5)

		# Display the title of the video/playlist
		self.category_title_label = customtkinter.CTkLabel(self.queue_line, text=self.software.l.lang['title'], font=self.software.bold_font)
		self.category_title_label.grid(row=0, column=0, sticky=W, padx=5)

		# Format the title and display it
		if len(self.title) > 65:
			self.video_title = self.title[:65] + "..."
		else:
			self.video_title = self.title
		self.title_label = customtkinter.CTkLabel(self.queue_line, text=self.video_title, font=self.software.main_font)
		self.title_label.grid(row=0, column=1, sticky=W)

		# Display informations of the video
		if self.download_type == 'single':
			# Views of the video (format and display)
			self.category_view = customtkinter.CTkLabel(self.queue_line, text=self.software.l.lang['views'], font=self.software.bold_font)
			self.category_view.grid(row=1, column=0, sticky=W, padx=5)
			if self.views != 'N/A':
				self.format_views = f"{int(self.views):,}"
			self.views_label = customtkinter.CTkLabel(self.queue_line, text=self.format_views, font=self.software.main_font)
			self.views_label.grid(row=1, column=1, sticky=W)

			# Publish date of the video
			self.category_publish_label = customtkinter.CTkLabel(self.queue_line, text=self.software.l.lang['publish_date'], font=self.software.bold_font)
			self.category_publish_label.grid(row=2, column=0, sticky=W, padx=5)
			self.publish_label = customtkinter.CTkLabel(self.queue_line, text=''.join(str(self.publish_date).split(' ')[0]), font=self.software.main_font)
			self.publish_label.grid(row=2, column=1, sticky=W)
		
			# Author
			self.category_author_label = customtkinter.CTkLabel(self.queue_line, text=self.software.l.lang['author'], font=self.software.bold_font)
			self.category_author_label.grid(row=3, column=0, sticky=W, padx=5)
			self.author_label = customtkinter.CTkLabel(self.queue_line, text=self.author[:65], font=self.software.main_font)
			self.author_label.grid(row=3, column=1, sticky=W)

		# Display informations of the playlist
		else:
			# Owner of the playlist
			self.category_owner_label = customtkinter.CTkLabel(self.queue_line, text=self.software.l.lang['owner'], font=self.software.bold_font)
			self.category_owner_label.grid(row=1, column=0, sticky=W, padx=5)
			self.owner_label = customtkinter.CTkLabel(self.queue_line, text=self.owner[:65], font=self.software.main_font)
			self.owner_label.grid(row=1, column=1, sticky=W)

			# Length of the playlist
			self.category_length_label = customtkinter.CTkLabel(self.queue_line, text=self.software.l.lang['length'], font=self.software.bold_font)
			self.category_length_label.grid(row=2, column=0, sticky=W, padx=5)
			self.length_label = customtkinter.CTkLabel(self.queue_line, text=f'{self.length} videos', font=self.software.main_font)
			self.length_label.grid(row=2, column=1, sticky=W)

		# Display the percentage of the download
		self.percent = StringVar()
		self.percent.set("0%")
		self.percent_label = customtkinter.CTkLabel(self.queue_line, textvariable=self.percent, font=self.software.bold_font)
		self.percent_label.place(x=560, y=15)

		# Display the progress bar of the download
		self.progress = customtkinter.CTkProgressBar(self.queue_line, orientation='horizontal', width=250, mode='determinate')
		self.progress.set(0)
		self.progress.place(x=560, y=45)

		# Display the Pause/Resume button
		self.is_pause = False
		self.btn_pause_resume = customtkinter.CTkButton(self.queue_line, text='', command=self.pause, cursor='hand2', image=self.software.image_pause, width=32, height=32)
		self.btn_pause_resume.place(x=715, y=60)
		self.window.balloon.bind(self.btn_pause_resume, self.software.l.lang['btn_pause'])

		# Display the Cancel button
		self.is_cancel = False
		self.btn_cancel = customtkinter.CTkButton(self.queue_line, text='', command=self.cancel, cursor='hand2', image=self.software.image_cancel, width=32, height=32)
		self.btn_cancel.place(x=765, y=60)
		self.window.balloon.bind(self.btn_cancel, self.software.l.lang['btn_cancel'])

		# Display the type of the download
		if self.mode_download == 'audio':
			txt_mode = 'type: audio (mp3)'
		else:
			txt_mode = 'type: video (mp4)'
		self.mode_download_label = customtkinter.CTkLabel(self.queue_line, text=txt_mode, font=self.software.bold_font)
		self.mode_download_label.place(x=560, y=55)
	
	
	def pause(self):
		# Pause the download
		if self.is_pause:
			self.btn_pause_resume.configure(image=self.software.image_pause)
			self.window.balloon.bind(self.btn_pause_resume, self.software.l.lang['btn_pause'])
			self.is_pause = False
		
		# Resume the download
		else:
			self.btn_pause_resume.configure(image=self.software.image_resume)
			self.window.balloon.bind(self.btn_pause_resume, self.software.l.lang['btn_resume'])
			self.window.update()
			self.is_pause = True


	def valid(self):
		# Valid the download
		self.thumbnail_line.grid_forget()
		self.queue_line.grid_forget()

		# Delete the queue line of the video/playlist
		self.software.current_queue -= 1
		self.window.queue_label.configure(text=f"{self.software.l.lang['download_queue']} {self.software.current_queue}/3")

		# Deletes the queue if there is no more video/playlist to download
		if self.software.current_queue == 0:
			self.window.label_img_void.pack()
			self.window.label_txt_void.pack()
			self.window.lbl_link.pack()
			self.window.queue_frame.pack_forget()
			self.window.status.set("")
			self.window.queue_label.configure(text="")

			# Lists of objects for the download
			self.software.list_yt_obj = []
			self.software.list_p_obj = []
		
		# Delete the video/playlist in the list of objects
		self.downloader.nb_video -= 1


	def cancel(self):
		# Cancel the download
		self.is_cancel = True
		self.percent.set(self.software.l.lang['download_cancel'])

		self.valid(self)

		# Remove the file in the download folder
		try:
			if self.download_type == 'video':
				os.remove(f'{self.software.path}/{self.file_name}')
			else:
				shutil.rmtree(f'{self.software.path}/{self.playlist_title}')

		except FileNotFoundError:
			pass


	def download_video(self, yt):
		# Choice the stream to download
		if self.mode_download == 'audio':
			stream = yt.streams.otf(False).get_audio_only()
		else:
			stream = yt.streams.otf(False).get_highest_resolution()

		# File size of the video
		filesize = stream.filesize

		# File name of the video
		if self.mode_download == 'audio':
			self.file_name = f'{yt.title}.mp3'
		else:
			self.file_name = f'{yt.title}.mp4'
		
		if self.download_type == 'playlist':
			self.file_name = f'{self.playlist_title}/{self.file_name}'
		
		# Create the playlist folder if it does not exist
		if self.download_type == 'playlist':
			if not os.path.exists(f'{self.software.path}/{self.playlist_title}'):
				os.makedirs(f'{self.software.path}/{self.playlist_title}')

		# Load and prepare the file
		with open(f"{self.software.path}/{self.file_name}", 'wb') as file:

			# Download the video
			stream = request.stream(stream.url)
			downloaded = 0

			while True:
				# The video / playlist is canceled
				if self.is_cancel:
					break

				# The video / playlist is paused
				if self.is_pause:
					self.window.update()
					continue

				# Get the next chunk of the video
				chunk = next(stream, None)
				if chunk:
					file.write(chunk)
					downloaded += len(chunk)

					# Update the percent of the download
					percent_value = downloaded * 100 / filesize

					# Display the new percent of the download
					if self.download_type == 'single':
						self.progress.set(percent_value / 100)
						self.percent.set(f"{int(percent_value)}%  {(downloaded / 1000000):.2f}Mb/{(filesize / 1000000):.2f}Mb")

					else:
						# One more music/video downloaded
						if percent_value == 100:
							self.nb_video_downloaded += 1
							percent_track_downloaded = self.nb_video_downloaded * 100 / self.nb_video_to_download
							self.progress.set(percent_track_downloaded / 100)
							self.percent.set(f"{int(percent_track_downloaded)}%  ({self.nb_video_downloaded}/{self.nb_video_to_download})  {(downloaded / 1000000):.2f}Mb/{(filesize / 1000000):.2f}Mb")

				# End of the download
				else:
					if self.download_type == 'single':
						self.btn_cancel.configure(image=self.software.image_finish, command=self.valid)
						self.btn_pause_resume.place_forget()
						self.window.balloon.bind(self.btn_cancel, self.software.l.lang['btn_valid'])

					else:
						if self.nb_video_downloaded == self.nb_video_to_download:
							self.btn_cancel.configure(image=self.software.image_finish, command=self.valid)
							self.btn_pause_resume.place_forget()
							self.window.balloon.bind(self.btn_cancel, self.software.l.lang['btn_valid'])
					break
