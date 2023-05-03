# Dependencies
import customtkinter, webbrowser
from PIL import Image

# Internal dependencies
from utils import *

class Credits:
	def __init__(self, window):
		# Save properties
		self.window = window
		self.software = self.window.software

		# Image data
		self.img_logo_credits = customtkinter.CTkImage(Image.open(env('Content/Images/app.png')), size=(150, 150))
		self.img_hide_credits = customtkinter.CTkImage(Image.open(env('Content/Images/back_home.png')), size=(30, 30))


	def launch(self):
		# Logo credits
		self.label_img_logo_credits = customtkinter.CTkLabel(self.window, image=self.img_logo_credits, text="")

		# Credits data
		self.frame_credits = customtkinter.CTkFrame(self.window, bg_color='transparent', fg_color='transparent')

		self.title_software = customtkinter.CTkButton(self.frame_credits, font=self.software.bold_font, width=400, fg_color='#93b1f5',
								text=f"{self.software.l.lang['software']}: " + self.software.title, text_color='#193473')
		
		self.title_developper = customtkinter.CTkButton(self.frame_credits, font=self.software.bold_font, width=400, fg_color='#93b1f5',
						  		text=self.software.l.lang['developper'] + self.software.author, text_color='#193473')

		self.title_date = customtkinter.CTkButton(self.frame_credits, font=self.software.bold_font, width=400, fg_color='#93b1f5',
								text=self.software.l.lang['date'] + self.software.date, text_color='#193473')

		self.title_website = customtkinter.CTkButton(self.frame_credits, font=self.software.bold_font, width=400, fg_color='#5076cd',
								text=self.software.l.lang['website'] + self.software.website, command=self.website, cursor='hand2', text_color='#193473')
		self.window.balloon.bind(self.title_website, self.software.l.lang['open_website'])

		self.title_contact = customtkinter.CTkButton(self.frame_credits, font=self.software.bold_font, width=400, fg_color='#5076cd',
								text=self.software.l.lang['e-mail'] + self.software.author_email, command=self.write_mail, cursor='hand2', text_color='#193473')
		self.window.balloon.bind(self.title_contact, self.software.l.lang['write_mail'])

		self.title_message = customtkinter.CTkButton(self.frame_credits, font=self.software.bold_font, width=400, fg_color='#93b1f5',
								text=self.software.l.lang['message'] + self.software.l.lang['message_credits'], text_color='#193473')

		self.title_version = customtkinter.CTkButton(self.frame_credits, font=self.software.bold_font, width=400, fg_color='#93b1f5',
								text=f"{self.software.l.lang['version']}: " + self.software.version, text_color='#193473')

		# Hide credits window widgets
		self.space_btn_hide_credits = customtkinter.CTkLabel(self.window, text=" ")
		self.btn_hide_credits = customtkinter.CTkButton(self.window, text=self.software.l.lang['back_to_home'], anchor='left', font=self.software.bold_font,
								image=self.img_hide_credits, command=self.window.display, width=0, height=35)


	def display(self):
		self.window.update_loading_status("Initialisation... (0/3)")

		# Hide the changelog/setttings window and the main window
		self.window.changelog.hide()
		self.window.settings.hide()
		self.window.hide()

		self.window.update_loading_status("focus on loading screen (1/3)")

		# Take the focus on the loading screen
		self.window.loading()
		self.window.loading_screen.tkraise()

		self.window.update_loading_status("place all informations... (2/3)")
		
		# Display window credits widgets
		self.label_img_logo_credits.pack()
		self.title_software.grid(pady=(10, 0))
		self.title_developper.grid(pady=(10, 0))
		self.title_date.grid(pady=(10, 0))
		self.title_website.grid(pady=(10, 0))
		self.title_contact.grid(pady=(10, 0))
		self.title_message.grid(pady=(10, 0))
		self.title_version.grid(pady=(10, 0))
		self.frame_credits.pack()
		self.space_btn_hide_credits.pack()
		self.btn_hide_credits.pack()

		self.window.update_loading_status("display credits window (3/3)")

		# Display the credits window and hide the loading screen
		self.window.update()
		self.window.loading_end()


	def hide(self):
		# Hide window credits widgets
		self.label_img_logo_credits.pack_forget()
		self.frame_credits.pack_forget()
		self.title_software.grid_forget()
		self.title_developper.grid_forget()
		self.title_date.grid_forget()
		self.title_website.grid_forget()
		self.title_contact.grid_forget()
		self.title_message.grid_forget()
		self.title_version.grid_forget()
		self.space_btn_hide_credits.pack_forget()
		self.btn_hide_credits.pack_forget()
		self.window.update()


	def website(self):
		webbrowser.open(self.software.website)


	def write_mail(self):
		webbrowser.open("mailto:" + self.software.author_email)