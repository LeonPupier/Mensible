import customtkinter
from PIL import Image
from tkinter import END

from utils import *

class Changelog:
	def __init__(self, window):
		# Save properties
		self.window = window
		self.software = self.window.software

		# Image data
		self.img_hide_credits = customtkinter.CTkImage(Image.open(env('Content/Images/back_home.png')), size=(30, 30))

	def launch(self):
		# Open the changelog file
		try:
			file_changelog = open(env(self.software.path_changelog), 'r', encoding='utf-8')
			self.log = file_changelog.read()
			file_changelog.close()
		except FileNotFoundError:
			return

		# Create the changelog text
		self.text_log = customtkinter.CTkTextbox(self.window, width=700, height=500)

		# Insert the changelog text
		self.text_log.insert(END, self.log)
		self.text_log.configure(state="disabled")

		# Hide credits window widgets
		self.space_btn_hide_credits = customtkinter.CTkLabel(self.window, text=" ")
		self.btn_hide_credits = customtkinter.CTkButton(self.window, text=self.software.l.lang['back_to_home'], anchor='left', font=self.software.bold_font,
						  		image=self.img_hide_credits, command=self.window.display, width=0, height=35)

	def display(self):
		self.window.update_loading_status("Initialisation... (0/2)")

		# Hide the credits/settings window and the a main window
		self.window.credits.hide()
		self.window.settings.hide()
		self.window.hide()

		# Take the focus on the loading screen
		self.window.loading()
		self.window.loading_screen.tkraise()

		self.window.update_loading_status("place changelog field (1/2)")

		# Display the changelog window
		self.text_log.pack()
		self.space_btn_hide_credits.pack()
		self.btn_hide_credits.pack()

		self.window.update_loading_status("Idisplay changelog window (2/2)")

		# Display the changelog window and hide the loading screen
		self.window.update()
		self.window.loading_end()
	
	def hide(self):
		# Hide the changelog window
		self.text_log.pack_forget()
		self.space_btn_hide_credits.pack_forget()
		self.btn_hide_credits.pack_forget()
		self.window.update()
