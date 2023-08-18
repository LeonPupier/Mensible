# Dependencies
import customtkinter, configparser, pytube.request
from tkinter import TOP, W, X, END, IntVar, StringVar, filedialog
from PIL import Image

# Internal dependencies
from utils import *

class Settings:
	def __init__(self, window):
		# Save properties
		self.window = window
		self.software = self.window.software

		# Variables
		self.space = 500
		self.password_status = 0

		# Image data
		self.img_back_home = customtkinter.CTkImage(Image.open(env('Content/Images/back_home.png')), size=(20, 20))
		self.img_show = customtkinter.CTkImage(Image.open(env('Content/Images/show.png')), size=(19, 22))
		self.img_hide = customtkinter.CTkImage(Image.open(env('Content/Images/hide.png')), size=(19, 22))
	
	
	def launch(self):
		# Title of the section
		self.title_label = customtkinter.CTkLabel(self.window, text=self.software.l.lang['general_settings'], font=self.software.title_font)

		# Frame for interface settings
		self.interface_label = customtkinter.CTkLabel(self.window, text="• " + self.software.l.lang['interface'], font=self.software.bold_font)
		self.win_interface = customtkinter.CTkFrame(self.window)

		# Language
		self.language_label = customtkinter.CTkLabel(self.win_interface, text=self.software.l.lang['language'], font=self.software.main_font, width=self.space, anchor=W)

		self.opt_language_str = ['English', 'Francais', 'Deutsch', 'Español', 'Italiano', 'Czech', '中国人']
		self.opt_language_choice = StringVar(self.window.c2)
		self.opt_language_choice.set(self.software.language)

		self.opt_language = customtkinter.CTkOptionMenu(self.win_interface, variable=self.opt_language_choice, values=self.opt_language_str, width=100)
		self.opt_language.configure(cursor='hand2')

		self.label_restart = customtkinter.CTkLabel(self.win_interface, text=f" ({self.software.l.lang['restart_valid_changes']})", text_color='grey', font=self.software.main_font_italic)

		# Choice the favorite theme color
		self.choice_theme_label = customtkinter.CTkLabel(self.win_interface, text=self.software.l.lang['choice_theme'], font=self.software.main_font, width=self.space, anchor=W)
		
		self.theme_var = IntVar()
		self.choice_theme_light = customtkinter.CTkRadioButton(self.win_interface, font=self.software.main_font, corner_radius=10, cursor='hand2', value=1)
		self.choice_theme_light.configure(text=self.software.l.lang['light'], variable=self.theme_var)
		self.window.balloon.bind(self.choice_theme_light, self.software.l.lang['light_theme'])
		self.choice_theme_dark = customtkinter.CTkRadioButton(self.win_interface, font=self.software.main_font, corner_radius=10, cursor='hand2', value=0)
		self.choice_theme_dark.configure(text=self.software.l.lang['dark'], variable=self.theme_var)
		self.window.balloon.bind(self.choice_theme_dark, self.software.l.lang['dark_theme'])

		# Frame for download settings
		self.download_label = customtkinter.CTkLabel(self.window, text="• " + self.software.l.lang['download'], font=self.software.bold_font)
		self.win_download = customtkinter.CTkFrame(self.window)

		# Download path
		self.info_download_label = customtkinter.CTkLabel(self.win_download, text=self.software.l.lang['download_path'], font=self.software.main_font, width=self.space, anchor=W)

		self.label_path = customtkinter.CTkLabel(self.win_download, text=self.software.path + "...")
		self.label_path.configure(text_color='#0078D7', font=self.software.main_font, cursor='hand2')
		self.window.balloon.bind(self.label_path, self.software.path)
		self.label_path.bind("<Button-1>", self.choose_path)

		# Download chunk size
		self.chunk_size_label = customtkinter.CTkLabel(self.win_download, text=self.software.l.lang['chunk_size'], font=self.software.main_font, width=self.space, anchor=W)

		self.opt_chunk_size_str = ['1 MB', '2 MB', '5 MB', '10 MB', '20 MB', '50 MB', '100 MB']
		self.opt_chunk_size_choice = StringVar(self.window.c2)
		self.opt_chunk_size_choice.set(self.software.chunk_size)

		self.opt_chunk_size = customtkinter.CTkOptionMenu(self.win_download, variable=self.opt_chunk_size_choice, values=self.opt_chunk_size_str, width=100, cursor='hand2')

		# Download quality
		self.quality_label = customtkinter.CTkLabel(self.win_download, text=self.software.l.lang['quality'], font=self.software.main_font, width=self.space, anchor=W)

		self.opt_quality_str = ['4320p', '2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p']
		self.opt_quality_choice = StringVar(self.window.c2)
		self.opt_quality_choice.set(self.software.quality)

		self.opt_quality = customtkinter.CTkOptionMenu(self.win_download, variable=self.opt_quality_choice, values=self.opt_quality_str, width=100, cursor='hand2')

		# Frame for Spotify settings
		self.spotify_label = customtkinter.CTkLabel(self.window, text="• Spotify (API)", font=self.software.bold_font)
		self.spotify_frame = customtkinter.CTkFrame(self.window)

		# Spotify settings
		self.spotify_client_label = customtkinter.CTkLabel(self.spotify_frame, text=self.software.l.lang['spotify_client_id'], font=self.software.main_font, width=self.space, anchor=W)
		self.spotify_client_entry = customtkinter.CTkEntry(self.spotify_frame, width=350)

		self.spotify_password_label = customtkinter.CTkLabel(self.spotify_frame, text=self.software.l.lang['spotify_password'], font=self.software.main_font, width=self.space, anchor=W)
		self.spotify_password_entry = customtkinter.CTkEntry(self.spotify_frame, width=350, show="•")

		# Show password button
		self.show_password_button = customtkinter.CTkButton(self.spotify_frame, text='', image=self.img_show, cursor='hand2', command=self.show_password, width=0)

		# Frame for informations
		self.infos_label = customtkinter.CTkLabel(self.window, text="• " + self.software.l.lang['information'], font=self.software.bold_font)
		self.win_infos = customtkinter.CTkFrame(self.window)
		
		self.infos_settings_label = customtkinter.CTkLabel(self.win_infos, text=self.software.l.lang['info_settings'], font=self.software.main_font)

		# Don't save changes
		self.cancel_button = customtkinter.CTkButton(self.window, text=self.software.l.lang['back_to_home'], image=self.img_back_home, cursor='hand2', command=self.window.display, width=0)

		# Saves changes
		self.save_button = customtkinter.CTkButton(self.window, text=self.software.l.lang['save_change'], cursor='hand2', command=self.validate_modif, width=0)

	
	def display(self):
		# Check there is no download in progress
		if self.software.current_queue:
			self.window.status.set(self.software.l.lang['block_settings'])
			return


		self.window.update_loading_status("Initialisation... (0/8)")

		# Hide the changelog/credits window and the main window
		self.window.changelog.hide()
		self.window.credits.hide()
		self.window.hide()

		self.window.update_loading_status("focus on loading screen (1/8)")

		# Take the focus on the loading screen
		self.window.loading()
		self.window.loading_screen.tkraise()

		self.window.update_loading_status("place title of the settings (2/8)")

		# Display the title of the section
		self.title_label.pack(side=TOP, anchor=W, padx=5)

		self.window.update_loading_status("place the interface section (3/8)")

		# Interface section
		self.interface_label.pack(side=TOP, anchor=W, padx=5)
		self.win_interface.pack(side=TOP, anchor=W, fill=X, padx=5)

		self.language_label.grid(row=0, column=0, sticky=W, padx=5, pady=2)
		self.opt_language.grid(row=0, column=1, sticky=W)
		self.label_restart.grid(row=0, column=2, sticky=W, padx=50)

		self.theme_var.set(self.software.theme)
		self.choice_theme_label.grid(row=1, column=0, sticky=W, padx=5)
		self.choice_theme_light.grid(row=1, column=1, sticky=W)
		self.choice_theme_dark.grid(row=1, column=2, sticky=W, padx=50)

		self.window.update_loading_status("place the download section (4/8)")

		# Download section
		self.download_label.pack(side=TOP, anchor=W, padx=5)
		self.win_download.pack(side=TOP, anchor=W, fill=X, padx=5)

		self.info_download_label.grid(row=1, column=0, sticky=W, padx=5)
		self.label_path.grid(row=1, column=1, sticky=W)

		self.window.update_loading_status("place the Spotify section (5/8)")

		self.chunk_size_label.grid(row=2, column=0, sticky=W, padx=5, pady=2)
		self.opt_chunk_size.grid(row=2, column=1, sticky=W)

		self.quality_label.grid(row=3, column=0, sticky=W, padx=5, pady=2)
		self.opt_quality.grid(row=3, column=1, sticky=W)

		# Spotify section
		self.spotify_label.pack(side=TOP, anchor=W, padx=5)
		self.spotify_frame.pack(side=TOP, anchor=W, fill=X, padx=5)

		self.spotify_client_label.grid(row=1, column=0, sticky=W, padx=5)
		self.spotify_client_entry.delete(0, END)
		if self.software.spotify_client_id is not None:
			self.spotify_client_entry.insert(END, self.software.spotify_client_id)
		else:
			self.spotify_client_entry.insert(END, '')
		self.spotify_client_entry.grid(row=1, column=1, sticky=W)

		self.spotify_password_label.grid(row=2, column=0, sticky=W, padx=5)
		self.spotify_password_entry.delete(0, END)
		if self.software.spotify_password is not None:
			self.spotify_password_entry.insert(END, self.software.spotify_password)
		else:
			self.spotify_password_entry.insert(END, '')
		self.spotify_password_entry.grid(row=2, column=1, sticky=W)
		self.show_password_button.grid(row=2, column=2, padx=5)

		self.window.update_loading_status("place the informations section (6/8)")

		# Informations section
		self.infos_label.pack(side=TOP, anchor=W, padx=5)
		self.win_infos.pack(side=TOP, anchor=W, fill=X, padx=5)

		self.infos_settings_label.grid(row=0, column=0, sticky=W, padx=5)

		self.window.update_loading_status("place saves/cancel changes buttons (7/8)")

		# Saves / Cancel the settings button
		self.cancel_button.pack(side=TOP, anchor=W, padx=5, pady=10)
		self.save_button.pack(side=TOP, anchor=W, padx=5)

		self.window.update_loading_status("display settings window (8/8)")

		# Display the settings window and hide the loading screen
		self.window.update()
		self.window.loading_end()

	
	def hide(self):
		# Hide the settings window
		self.title_label.pack_forget()
		self.interface_label.pack_forget()
		self.win_interface.pack_forget()
		self.language_label.grid_forget()
		self.opt_language.grid_forget()
		self.label_restart.grid_forget()
		self.choice_theme_label.grid_forget()
		self.choice_theme_light.grid_forget()
		self.choice_theme_dark.grid_forget()
		self.download_label.pack_forget()
		self.win_download.pack_forget()
		self.info_download_label.grid_forget()
		self.label_path.grid_forget()
		self.chunk_size_label.grid_forget()
		self.opt_chunk_size.grid_forget()
		self.quality_label.grid_forget()
		self.opt_quality.grid_forget()
		self.spotify_label.pack_forget()
		self.spotify_frame.pack_forget()
		self.spotify_client_label.grid_forget()
		self.spotify_client_entry.grid_forget()
		self.spotify_password_label.grid_forget()
		self.spotify_password_entry.grid_forget()
		self.show_password_button.grid_forget()
		self.infos_label.pack_forget()
		self.win_infos.pack_forget()
		self.infos_settings_label.grid_forget()
		self.cancel_button.pack_forget()
		self.save_button.pack_forget()

		# Hide window and widgets
		self.window.update()
	

	def show_password(self):
		if self.password_status == 0:
			self.spotify_password_entry.configure(show='')
			self.show_password_button.configure(image=self.img_hide)
			self.password_status = 1
		else:
			self.spotify_password_entry.configure(show='•')
			self.show_password_button.configure(image=self.img_show)
			self.password_status = 0


	def choose_path(self, bind=None):
		new_path = filedialog.askdirectory(initialdir="/", title=self.software.l.lang['download_folder'])

		if type(new_path) == str:
			if new_path != '':
				self.software.path = new_path
				self.label_path.configure(text=self.software.path[:25]+'...')
				self.window.balloon.bind(self.label_path, self.software.path)
				self.window.lbl_link.configure(text=f"{self.software.l.lang['folder_files']}: {self.software.path}")


	def validate_modif(self):
		# Create a new config file
		config_modif = configparser.ConfigParser()

		# Change the language
		self.new_language = self.opt_language_choice.get()

		# Change the download path
		self.software.theme = self.theme_var.get()

		# Change spotify settings
		self.software.spotify_client = self.spotify_client_entry.get()
		self.software.spotify_password = self.spotify_password_entry.get()

		# Change the chunk size
		self.software.chunk_size = self.opt_chunk_size_choice.get()
		self.software.chunk_size_int = int(self.software.chunk_size.split(' ')[0]) * 1000000
		pytube.request.default_range_size = self.software.chunk_size_int

		# Change the quality
		self.software.quality = self.opt_quality_choice.get()
	
		# Save the new settings
		config_modif['CONFIG'] = {
			'language': self.new_language,
			'download.path': self.software.path,
			'download.chunk_size': self.software.chunk_size,
			'download.quality': self.software.quality,
			'theme': self.software.theme,
			'spotify.client': self.software.spotify_client,
			'spotify.password': self.software.spotify_password
		}

		with open(env('Content/app.ini'), 'w') as configfile:
			config_modif.write(configfile)

		# Change the theme
		if self.software.theme == 0:
			self.window.dark_theme()
		else:
			self.window.light_theme()

		# Redisplay the main window
		self.window.display()
