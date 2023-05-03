# Dependencies
import os, customtkinter, webbrowser, urllib.request
from tkinter import PhotoImage

# Get the current version of the software
def check_current_version(current_version):
	url = 'https://api.github.com/repos/LeonPupier/Mensible/releases/latest'

	try:
		data = urllib.request.urlopen(url)
		data = data.read().decode('utf-8')
		data = data.split('"tag_name":"')[1].split('",')[0]
		if data != current_version:
			return True
		else:
			return False
	except:
		return False


# Current folder
def env(relative_path):
	return os.getcwd() + "/" + relative_path


# Center window on the screen
def center_window(win, software, ico_name='app'):
	win.update()
	win.update_idletasks()
	width = win.winfo_width()
	frm_width = win.winfo_rootx() - win.winfo_x()
	win_width = width + 2 * frm_width
	height = win.winfo_height()
	titlebar_height = win.winfo_rooty() - win.winfo_y()
	win_height = height + titlebar_height + frm_width
	x = win.winfo_screenwidth() // 2 - win_width // 2
	y = win.winfo_screenheight() // 2 - win_height // 2

	win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
	if os.name != 'posix':
		win.iconbitmap(env(f"Content/Images/{ico_name}.ico"))
	else:
		win.iconphoto(True, PhotoImage(file=env(f"Content/Images/{ico_name}.png")))


# Display a space between widgets in a window
def space(window):
	empty_widget = customtkinter.CTkLabel(window, text="")
	empty_widget.pack()
	return empty_widget


# Open a link to the github project page in the default browser
def open_github_repository(bind=None):
	webbrowser.open("https://github.com/LeonPupier/Mensible/releases/latest")


# Open a link to the survey in the default browser
def open_survey(bind=None):
	webbrowser.open("https://forms.gle/hXpfJA1fNQPFG8KX7")


# Open a link to my ko-fi page in the default browser
def support_kofi(bind=None):
	webbrowser.open("https://ko-fi.com/leonpupier")
