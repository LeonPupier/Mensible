# Dependencies
import os, ctypes, Pmw, customtkinter, shutil, logging
from tkinter import Menu, Label, Frame, StringVar, messagebox, LEFT, END, X
from PIL import Image, ImageTk
from threading import Thread

# Internal dependencies
from software import SoftwareInformations
from settings import Settings
from changelog import Changelog
from credits import Credits
from downloader import Downloader
from utils import *

class Window(customtkinter.CTk):
	def __init__(self):
		# Initiate the customtkinter class
		super().__init__()

		# Initiate the software informations
		self.software = SoftwareInformations()

		# Initiate the Settings, Changelog and Credits windows
		self.settings = Settings(self)
		self.changelog = Changelog(self)
		self.credits = Credits(self)

		# Initiate the downloader
		self.dl = Downloader(self)

		# Resolution scaling (Windows only)
		if os.name != 'posix':
			ctypes.windll.shcore.SetProcessDpiAwareness(1)

		# Customtkinter design
		if self.software.theme == 0:
			customtkinter.set_appearance_mode("dark")
		else:
			customtkinter.set_appearance_mode("light")
		customtkinter.set_default_color_theme("blue")

		# Title of the window
		self.title(f'{self.software.title} {self.software.version}')

		# Icon of the window (Windows only)
		if os.name != 'posix':
			self.iconbitmap(env('Content/Images/app.ico'))

		# Window informations
		self.geometry("1000x680")
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.resizable(False, False)
		self.configure(cursor='')
		self.protocol("WM_DELETE_WINDOW", self.on_closing)
		center_window(self, self.software)

		# Balloon design (tooltip)
		self.balloon = Pmw.Balloon(self)
		self.lbl = self.balloon.component("label")
		self.lbl.config(background="white", foreground="black")

		# Menu
		self.menubar = Menu(self, font=self.software.bold_font, tearoff=0, relief='flat', borderwidth=0, activeborderwidth=0)
		self.menubar.config(background='#212121', foreground='white', activebackground='grey', activeforeground='white', border=0, relief='flat', borderwidth=0)

		self.menu1 = Menu(self.menubar, tearoff=0, relief='flat', font=self.software.bold_font, borderwidth=0, activeborderwidth=0)
		self.menu1.config(background='#212121', foreground='white', activebackground='grey', activeforeground='white', border=0, relief='flat', borderwidth=0)
		self.menu1.add_command(label=self.software.l.lang['settings'], command=self.settings.display)
		self.menu1.add_separator()
		self.menu1.add_command(label=self.software.l.lang['shutdown'], command=self.on_closing)
		self.menubar.add_cascade(label=self.software.l.lang['software'], menu=self.menu1)

		self.menu2 = Menu(self.menubar, tearoff=0, bd=0, relief='flat', font=self.software.bold_font, borderwidth=0, activeborderwidth=0)
		self.menu2.config(background='#212121', foreground='white', activebackground='grey', activeforeground='white', bd=0, relief='flat')
		self.menu2.add_command(label=self.software.l.lang['changelog'], command=self.changelog.display)
		self.menu2.add_command(label=self.software.l.lang['credits'], command=self.credits.display)
		self.menu2.add_command(label=self.software.l.lang['form'], command=open_survey)
		self.menubar.add_cascade(label=self.software.l.lang['help'], menu=self.menu2)

		self.config(menu=self.menubar)

		# Credit
		self.label_title = customtkinter.CTkLabel(self, text=self.software.l.lang['title_software'], font=self.software.title_font)
		self.label_disclaimer = customtkinter.CTkLabel(self,
			text=self.software.title + self.software.l.lang['disclaimer_software'] + self.software.author + " - " + self.software.date,
			font=self.software.main_font_italic
		)
		self.space_title = customtkinter.CTkLabel(self, text="")

		# Frame for the download bar
		self.c2 = customtkinter.CTkFrame(self)

		# YouTube / Spotify Choice
		self.image_btn_youtube = customtkinter.CTkImage(Image.open(env('Content/Images/youtube.png')), size=(30, 30))
		self.btn_youtube = customtkinter.CTkButton(self.c2, command=self.choice_youtube, text="", cursor='hand2', image=self.image_btn_youtube, width=40, height=40, fg_color='transparent')
		self.balloon.bind(self.btn_youtube, self.software.l.lang['download_youtube'])

		image_btn_spotify = customtkinter.CTkImage(Image.open(env('Content/Images/spotify.png')), size=(30, 30))
		self.btn_spotify = customtkinter.CTkButton(self.c2, command=self.choice_spotify, text="", cursor='hand2', image=image_btn_spotify, width=40, height=40, fg_color='transparent')
		self.balloon.bind(self.btn_spotify, self.software.l.lang['download_spotify'])

		# URL
		self.label_url = StringVar()
		self.label_url.set(self.software.l.lang['url'])
		self.label_url_widget = customtkinter.CTkLabel(self.c2, textvariable=self.label_url, font=self.software.bold_font)

		# Option choice (video / playlist)
		self.opt_choice = [
			self.software.l.lang['video'],
			self.software.l.lang['playlist']
		]
		self.opt_mode_choice = StringVar(self.c2)
		self.opt_mode_choice.set(self.opt_choice[0])

		self.opt_mode = customtkinter.CTkOptionMenu(self.c2, variable=self.opt_mode_choice, values=self.opt_choice)
		self.opt_mode.configure(font=self.software.bold_font, width=6, cursor='hand2')
		self.label_point = customtkinter.CTkLabel(self.c2, text=":", font=self.software.bold_font)

		# URL entry
		self.txt_url = customtkinter.CTkEntry(self.c2, width=450, justify='left', fg_color='grey', text_color='white')
		self.txt_url.insert(END, 'https://www.youtube.com/watch?v=')
		self.bind('<Return>', self.launch_search)

		# Audio download button
		self.image_btn_audio = customtkinter.CTkImage(Image.open(env('Content/Images/audio.png')), size=(30, 30))
		self.btn_audio = customtkinter.CTkButton(self.c2, command=self.audio_only, cursor='hand2', text="", image=self.image_btn_audio, width=40, height=40)
		self.balloon.bind(self.btn_audio, self.software.l.lang['download_audio'])

		# Video download button
		self.image_btn_video = customtkinter.CTkImage(Image.open(env('Content/Images/video.png')), size=(30, 30))
		self.image_btn_video_disabled = customtkinter.CTkImage(Image.open(env('Content/Images/video_disabled.png')), size=(30, 30))
		self.btn_video = customtkinter.CTkButton(self.c2, command=self.audio_video, cursor='hand2', text="", image=self.image_btn_video, width=40, height=40)
		self.balloon.bind(self.btn_video, self.software.l.lang['download_audio_video'])

		# Search video / audio button
		self.txt_btn = StringVar()
		self.txt_btn.set(self.software.l.lang['download'])
		self.btn_search = customtkinter.CTkButton(self.c2, textvariable=self.txt_btn, command=self.launch_search, cursor='hand2', font=self.software.bold_font, width=0, height=30)
		self.balloon.bind(self.btn_search, self.software.l.lang['download_file'])

		# Queue label
		self.queue_label = customtkinter.CTkLabel(self, text='')
		self.queue_label.configure(text=f"")

		# Queue frame for the download bar
		self.queue_frame = customtkinter.CTkFrame(self)

		# Image waiting download
		self.img_void = customtkinter.CTkImage(Image.open(env('Content/Images/void.png')), size=(275, 275))
		self.label_img_void = customtkinter.CTkLabel(self, image=self.img_void, text="")
		self.label_txt_void = customtkinter.CTkLabel(self, text=self.software.l.lang['no_download'], font=self.software.void_font)

		# Music folder label
		self.lbl_link = customtkinter.CTkLabel(self, text=f"{self.software.l.lang['file_in_folder']}: {self.software.path}", cursor='hand2')
		self.lbl_link.configure(text_color='#0078D7')
		self.lbl_link.bind("<Button-1>", self.open_music_folder)
		self.balloon.bind(self.lbl_link, self.software.l.lang['open_explorer'])

		# Status label
		self.status = StringVar()
		self.status_label = customtkinter.CTkLabel(self, textvariable=self.status, font=self.software.main_font_italic)

		# Support Ko-Fi button
		self.image_btn_kofi = customtkinter.CTkImage(Image.open(env('Content/Images/kofi.png')), size=(126, 32))
		self.html_support = customtkinter.CTkButton(self, text="", command=support_kofi, cursor='hand2', image=self.image_btn_kofi, fg_color="transparent", hover_color="#29ABE0", height=35)
		self.balloon.bind(self.html_support, self.software.l.lang['support_kofi'])

		# Adjust widgets about theme
		if self.software.theme == 0:
			self.dark_theme()
		else:
			self.light_theme()

		# Pre-selected options
		self.choice_youtube()
		self.audio_only()

		# Launch Credits, Settings and Changelog windows and hide them
		self.update()
		self.credits.launch()
		self.settings.launch()
		self.changelog.launch()

		logging.info("Widgets loaded")


	def load_loading(self):
		# Loading screen widgets
		self.loading_screen = Frame(self, width=self.winfo_width(), height=self.winfo_height(), bg="#1E1E1E")
		self.image_loading = ImageTk.PhotoImage(Image.open("Content/Images/loading.png").resize((50, 50)))
		self.label_image_loading = Label(self.loading_screen, image=self.image_loading, font=self.software.bold_font, bg="#1E1E1E", fg="white")
		self.label_loading = Label(self.loading_screen, text=self.software.l.lang['loading'], font=self.software.bold_font, bg="#1E1E1E", fg="white")
		self.loading_status = Label(self.loading_screen, text="", font=self.software.main_font_italic, bg="#1E1E1E", fg="white")
		logging.info("Loading screen loaded")


	def	loading(self):
		# Adjust widgets about theme for the loading screen
		if self.software.theme == 0:
			self.loading_screen.configure(bg="#1E1E1E")
			self.label_image_loading.configure(bg="#1E1E1E", fg="white")
			self.label_loading.configure(bg="#1E1E1E", fg="white")
			self.loading_status.configure(bg="#1E1E1E", fg="white")
		else:
			self.loading_screen.configure(bg="white")
			self.label_image_loading.configure(bg="white", fg="black")
			self.label_loading.configure(bg="white", fg="black")
			self.loading_status.configure(bg="white", fg="black")

		# Hide the main window and display the loading screen
		self.loading_screen.place(x=0, y=0)
		self.label_image_loading.place(x=(self.winfo_width() - self.label_image_loading.winfo_reqwidth()) / 2, y=(self.winfo_height() - self.label_image_loading.winfo_reqheight()) / 2)
		self.label_loading.place(x=(self.winfo_width() - self.label_loading.winfo_reqwidth()) / 2, y=(self.winfo_height() - self.label_loading.winfo_reqheight()) / 2 + 40)
		logging.info("Loading screen opened")


	def	loading_end(self):
		# Hide the loading screen and display the main window
		self.loading_screen.place_forget()
		logging.info("Loading screen closed")
	

	def update_loading_status(self, status):
		# Update the loading status
		self.update()
		self.loading_status.configure(text=status)
		self.loading_status.place(x=(self.winfo_width() - self.loading_status.winfo_reqwidth()) / 2, y=(self.winfo_height() - self.loading_status.winfo_reqheight()) / 2 + 60)
		self.update()


	def display(self):
		self.update_loading_status("Initialisation... (0/6)")

		# Hide the Changelog, Settings and Credits window
		self.changelog.hide()
		self.settings.hide()
		self.credits.hide()

		# Take the focus on the loading screen
		self.loading()
		self.loading_screen.tkraise()

		self.update_loading_status("focus on loading screen (1/6)")

		# Display the main window
		self.label_title.pack()
		self.label_disclaimer.pack()
		self.space_title.pack()

		self.update_loading_status("place title and disclaimer (2/6)")

		self.btn_youtube.pack(padx=5, pady=5, side=LEFT)
		self.btn_spotify.pack(padx=5, pady=5, side=LEFT)
		self.label_url_widget.pack(side=LEFT)
		self.opt_mode.pack(padx=5, pady=5, side=LEFT)
		self.label_point.pack(side=LEFT)
		self.txt_url.pack(padx=5, pady=5, side=LEFT)
		self.btn_audio.pack(padx=5, pady=5, side=LEFT)
		self.btn_video.pack(padx=5, pady=5, side=LEFT)
		self.btn_search.pack(padx=5, pady=5, side=LEFT)

		self.update_loading_status("place download bar (3/6)")

		self.c2.pack()

		self.update_loading_status("place container (4/6)")

		self.queue_label.pack()
		self.status_label.pack()

		if self.software.current_queue == 0:
			self.label_img_void.pack()
			self.label_txt_void.pack()
			self.lbl_link.pack()
		
		else:
			self.queue_frame.pack(fill=X, padx=10, pady=10)

		self.update_loading_status("place queue and status (5/6)")

		self.html_support.place(relx=0.004, rely=.935)

		self.update_loading_status("place theme button and ko-fi support (6/6)")
		
		# Display the main window and hide the loading screen
		self.update()
		self.loading_end()
		logging.info("Main window displayed")


	def hide(self):
		self.update()
		self.c2.pack_forget()

		self.btn_youtube.pack_forget()
		self.btn_spotify.pack_forget()
		
		self.label_url_widget.pack_forget()
		self.opt_mode.pack_forget()
		self.label_point.pack_forget()
		self.txt_url.pack_forget()
		self.btn_audio.pack_forget()
		self.btn_video.pack_forget()
		self.btn_search.pack_forget()

		self.queue_label.pack_forget()
		self.label_img_void.pack_forget()
		self.label_txt_void.pack_forget()
		self.lbl_link.pack_forget()
		self.status_label.pack_forget()
		self.queue_frame.pack_forget()
		
		self.update()
		logging.info("Main window hidden")
	

	def launch_search(self):
		# Launch the search to download the video/playlist
		Thread(target=self.dl.search_video).start()
	

	def open_music_folder(self, bind=None):
		# Open the music folder into the file explorer
		try:
			if os.name == 'posix':
				webbrowser.open("file://" + self.software.path)
			else:
				os.startfile(self.software.path)
		
		except Exception as e:
			logging.error("Error while opening the music folder: " + str(e))
		
		logging.info("Open music folder")
	

	def dark_theme(self):
		# Change theme method to dark
		customtkinter.set_appearance_mode("dark")
		self.menubar.config(background='#212121', foreground='#e3e3e3', activebackground='grey', activeforeground='white')
		self.menu1.config(background='#212121', foreground='#e3e3e3', activebackground='grey', activeforeground='white')
		self.menu2.config(background='#212121', foreground='#e3e3e3', activebackground='grey', activeforeground='white')
		self.lbl.config(background="#212121", foreground="#e3e3e3")
		self.update()
		logging.info("Dark theme applied")


	def light_theme(self):
		# Change theme method to light
		customtkinter.set_appearance_mode("light")
		self.menubar.config(background='#DBDBDB', foreground='#3e3e3e', activebackground='#c9c9c9', activeforeground='black')
		self.menu1.config(background='#DBDBDB', foreground='#3e3e3e', activebackground='#c9c9c9', activeforeground='black')
		self.menu2.config(background='#DBDBDB', foreground='#3e3e3e', activebackground='#c9c9c9', activeforeground='black')
		self.lbl.config(background="white", foreground="black")
		self.update()
		logging.info("Light theme applied")

	
	def choice_youtube(self):
		self.software.mode_plateform = 'youtube'

		self.btn_youtube.configure(cursor='arrow', fg_color='#2B719E', state='disabled')
		self.btn_spotify.configure(cursor='hand2', fg_color='transparent', state='normal')
		self.focus_set()

		self.single()

		self.btn_video.configure(state='normal', cursor='hand2', image=self.image_btn_video)
		self.balloon.bind(self.btn_video, self.software.l.lang['download_audio_video'])

		self.opt_mode_choice.set(self.opt_choice[0])
		self.opt_mode.configure(state='normal')
		self.opt_mode.configure(cursor='hand2')
		logging.info("Youtube selected as download platform")


	def choice_spotify(self):
		self.software.download_type = 'playlist'
		self.software.mode_plateform = 'spotify'

		self.btn_spotify.configure(cursor='arrow', fg_color='#2B719E', state='disabled')
		self.btn_youtube.configure(cursor='hand2', fg_color='transparent', state='normal')
		self.focus_set()

		self.txt_url.delete(0, END)
		self.txt_url.insert(0, 'https://open.spotify.com/playlist/')
		self.txt_btn.set(self.software.l.lang['download'])

		self.audio_only()

		self.btn_video.configure(image=self.image_btn_video_disabled, state='disabled', cursor='arrow', fg_color='transparent')
		self.balloon.bind(self.btn_video, self.software.l.lang['video_disabled'])
		self.opt_mode_choice.set(self.opt_choice[1])
		self.opt_mode.configure(state='disabled')
		self.opt_mode.configure(cursor='arrow')
		logging.info("Spotify selected as download platform")


	def audio_only(self):
		self.software.mode_download = 'audio'
		self.btn_audio.configure(cursor='arrow', fg_color='#2B719E', state='disabled')
		self.btn_video.configure(image=self.image_btn_video, cursor='hand2', fg_color='transparent', state='normal')
		self.focus_set()
		logging.info("Audio only selected as download mode")


	def audio_video(self):
		self.software.mode_download = 'video'
		self.btn_video.configure(cursor='arrow', fg_color='#2B719E', state='disabled')
		self.btn_audio.configure(image=self.image_btn_audio, cursor='hand2', fg_color='transparent', state='normal')
		self.focus_set()
		logging.info("Audio and video selected as download mode")


	def single(self):
		self.software.download_type = 'single'
		self.label_url.set(self.software.l.lang['url'])
		self.txt_url.delete(0, END)
		self.txt_url.insert(0, 'https://www.youtube.com/watch?v=')
		self.txt_btn.set(self.software.l.lang['download'])
		logging.info("Single download selected as download type")


	def playlist(self):
		self.software.download_type = 'playlist'
		self.label_url.set(self.software.l.lang['url'])
		self.txt_url.delete(0, END)
		self.txt_url.insert(0, 'https://www.youtube.com/playlist?list=')
		self.txt_btn.set(self.software.l.lang['download'])
		logging.info("Playlist download selected as download type")


	def loop_method(self):
		# Get type download
		opt_str = self.opt_mode_choice.get()

		# Check if type download is changed
		if opt_str != self.software.backup_download_type:

			# Delete all widgets in queue frame
			if opt_str == 'video':
				self.single()
			elif opt_str == 'playlist':
				if self.software.mode_plateform == 'youtube':
					self.playlist()

			# Save type download
			self.software.backup_download_type = opt_str

		# Update status
		self.after(10, self.loop_method)


	def launch(self):
		# Display window widgets
		self.display()

		# Refresh
		self.after(0, self.loop_method)
		self.update_idletasks()
		
		# Check if new version available
		if check_current_version(self.software.version):
			logging.info("New version available")
			if messagebox.askyesno(self.software.l.lang['update_available'], self.software.l.lang['update_message']):
				open_github_repository()
		else:
			logging.info("Current version is up to date")

		# Launch window
		self.mainloop()
	

	def on_closing(self):
		# Delete temp folder for thumbnail if exist (Windows and Linux)
		try:
			if os.name != 'posix':
				shutil.rmtree("C:/Windows/Temp/MensibleThumbnail")
			else:
				shutil.rmtree("/tmp/MensibleThumbnail")
		except FileNotFoundError:
			pass
		logging.info("Temp folder deleted")

		# Close window
		self.quit()
		logging.info("Window closed")
