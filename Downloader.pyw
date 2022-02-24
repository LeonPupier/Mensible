import os, webbrowser
from tkinter import *
from tkinter import filedialog, messagebox, Text
from tkinter.ttk import Progressbar, Scrollbar
from PIL import Image, ImageTk
import tkinter.font as tkFont
from threading import *
from pytube import *
import pytube.request

# Internal modules
from changelog import *

#Ddw9CVIn6Zg
#OLAK5uy_lbcsh_E-SKtipIUmpO7VDDdN2Ww3DMzGQ

# Environment
pytube.request.default_range_size = 1000000 # 1Mo
os.environ['DOWNLOAD_IN_PROGRESS'] = 'False'

# Functions
def center_window(win):
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
	win.iconbitmap('app.ico')
	win.deiconify()


def progress_func(stream, chunk, bytes_remaining):
	global total_downloaded

	curr = stream.filesize - bytes_remaining
	percent_value = curr*100/stream.filesize

	if download_type == 'single':
		progress['value'] = percent_value
		percent.set(f"{int(percent_value)}%")

	else:
		# One more music/video downloaded
		if percent_value == 100:
			total_downloaded += 1
			percent_track_downloaded = total_downloaded*100/len(liste_file)
			progress['value'] = percent_track_downloaded
			percent.set(f"{int(percent_track_downloaded)}%")


def download_file(yt, mode):
	# File name
	if mode == 'audio':
		file_name = f'{yt.title} [AUDIO].mp4'
	else:
		file_name = f'{yt.title} [AUDIO+VIDEO].mp4'

	# Check if the file already exists
	try:
		with open(f'C:/Users/{os.getlogin()}/Music/{file_name}', 'r'):
			if download_type == 'single':
				status.set("The file already exists on your computer...")
				txt_btn.set("Download")
				btn_search.configure(state="normal")

				global list_file
				liste_file = []

			return

	except FileNotFoundError:
		pass

	# Stream
	if mode == 'audio':
		final_stream = yt.streams.otf(False).get_audio_only()
	else:
		final_stream = yt.streams.otf(False).get_highest_resolution()

	downloaded_file = final_stream.download(f'C:/Users/{os.getlogin()}/Music', filename=file_name)

	if os.environ['DOWNLOAD_IN_PROGRESS'] == 'True':
		print('Stop thread')
		sys.exit(0)


def cancel_download():
	pass


def search_video(bind_action=None):
	global liste_file, total_downloaded

	progress['value'] = 0
	percent.set("0%")

	status.set("")
	txt_1.set("")
	txt_2.set("")

	url = txt_url.get()

	if download_type == 'single':
		try:
			yt = YouTube(url, on_progress_callback=progress_func)
			
			liste_file = [yt.title]
			total_downloaded = 0

			txt_infos1.set(f"Title: {yt.title}")
			txt_infos2.set(f"Views: {yt.views} | Publish date: {yt.publish_date}")

			# Download
			try:
				txt_btn.set("Downloading in progress...")
				btn_search.configure(state="disabled")

				thread_download = Thread(target=download_file, args=(yt, mode_download,))
				thread_download.start()

			except:
				status.set("A problem occurred during the download...")
				txt_btn.set("Download")
				btn_search.configure(state="normal")

		except:
			status.set("Please provide a valid URL...")
			txt_infos1.set("")
			txt_infos2.set("")

	elif download_type == 'playlist':
		try:
			p = Playlist(url)
			txt_infos1.set(f"Title: {p.title}")
			txt_infos2.set(f"Length of the playlist: {p.length} | Views: {p.views}")
			
			# Download
			try:
				txt_btn.set("Downloading in progress...")
				btn_search.configure(state="disabled")
			
				liste_file = []
				total_downloaded = 0

				for video_url in p.video_urls:
					yt = YouTube(video_url, on_progress_callback=progress_func)
					liste_file.append(yt.title)
					Thread(target=download_file, args=(yt, mode_download,)).start()

			except:
				status.set("A problem occurred during the download...")
				txt_btn.set("Download")
				btn_search.configure(state="normal")
		except:
			status.set("Please provide a valid URL...")
			txt_infos1.set("")
			txt_infos2.set("")


def audio_only():
	global mode_download
	mode_download = 'audio'
	#btn_audio.configure(state="disabled", cursor='arrow')
	#btn_video.configure(state="normal", cursor='hand2')
	btn_audio.configure(bg="#4478E3", cursor='arrow')
	btn_video.configure(bg="#F0F0ED", cursor='hand2')


def audio_video():
	global mode_download
	mode_download = 'video'
	#btn_video.configure(state="disabled", cursor='arrow')
	#btn_audio.configure(state="normal", cursor='hand2')
	btn_video.configure(bg="#4478E3", cursor='arrow')
	btn_audio.configure(bg="#F0F0ED", cursor='hand2')


def single():
	global download_type
	download_type = 'single'
	label_url.set("URL of the desired single music/video:")
	txt_url.delete(0, END)
	txt_url.insert(0, 'https://www.youtube.com/watch?v=')
	txt_btn.set("Download")


def playlist():
	global download_type
	download_type = 'playlist'
	label_url.set("URL of the desired playlist music/video:")
	txt_url.delete(0, END)
	txt_url.insert(0, 'https://www.youtube.com/playlist?list=')
	txt_btn.set("Download (freeze for a few seconds)")


def hyperlink(arg):
	webbrowser.open(f'C:/Users/{os.getlogin()}/Music/')


def check_update():
	messagebox.askquestion(title="Update", message="A new version of the software is available ! Do you want to update it now ?")
	messagebox.showinfo(title="Update", message="You already have the most recent version of the software.")


def changelog():
	win_log = Toplevel()
	win_log.title('Changelog')
	win_log.geometry("600x500")
	win_log.resizable(False, False)
	center_window(win_log)

	text_log = Text(win_log)
	text_log.pack(side=LEFT)

	log = changelog_txt()

	text_log.insert(END, log)
	text_log.configure(state="disabled")


# Initialisation
window = Tk()
window.title('YouTube Downloader v1.2.1 [DEV]')
window.geometry("900x700")
window.resizable(False, False)
center_window(window)

title_font = tkFont.Font(family='lucida', size='12', weight='bold')
main_font = tkFont.Font(family='lucida', size='9', slant='italic')
bold_font = tkFont.Font(family='lucida', size='9', weight='bold')

# Type mode
download_type = "single"

# Menu
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Single", command=single)
menu1.add_command(label="Playlist", command=playlist)
menu1.add_separator()
menu1.add_command(label="Shutdown", command=window.quit)
menubar.add_cascade(label="Mode", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Check for updates...", command=check_update)
menu2.add_command(label="Changelog", command=changelog)
menubar.add_cascade(label="Help", menu=menu2)

window.config(menu=menubar)

# Credit
Label(window, text="● YouTube Downloader ●", font=title_font).pack()
Label(window, text="Made by Léon Pupier - 2022", font=main_font).pack()
Label(window, text="Uploaded videos will not exceed 720p resolution", fg="grey").pack()
Label(window, text="due to a blocking by Google LLC.", fg="grey").pack()
Label(window).pack()

c1 = Frame(window)
c1.pack()

label_url = StringVar()
label_url.set("URL of the desired single music/video: ")
Label(c1, textvariable=label_url, font=bold_font).pack(side=LEFT)
txt_url = Entry(c1, width=50, justify='left')
txt_url.insert(END, 'https://www.youtube.com/watch?v=')
txt_url.pack(side=LEFT)
window.bind('<Return>', search_video)

# Download mode choice
mode_download = 'video'
image_audio = ImageTk.PhotoImage(Image.open('Content/audio.png'))
btn_audio = Button(c1, state='normal', command=audio_only, cursor='hand2', image=image_audio)
image_video = ImageTk.PhotoImage(Image.open('Content/video.png'))
btn_video = Button(c1, state='normal', command=audio_video, cursor='arrow', image=image_video)
btn_audio.pack(padx=5, pady=5, side=LEFT)
btn_video.pack(padx=5, pady=5, side=LEFT)


txt_btn = StringVar()
txt_btn.set("Download")
btn_search = Button(c1, textvariable=txt_btn, state='normal', command=search_video, cursor='hand2')
btn_search.pack(padx=5, pady=5, side=LEFT)
Label(window).pack()

# Progress
cadre2 = Frame(window)
cadre2.pack()

percent = StringVar()
percent.set("0%")
Label(cadre2, textvariable=percent).pack(side=LEFT)

progress = Progressbar(cadre2, orient=HORIZONTAL, length=380, mode='determinate')
progress.pack(side=LEFT)

Button(cadre2, text="Cancel", state="disabled", command=cancel_download, cursor='arrow').pack(padx=5, side=RIGHT)

# Infos
txt_infos1 = StringVar()
txt_infos1.set("")
Label(window, textvariable=txt_infos1).pack()
txt_infos2 = StringVar()
txt_infos2.set("")
Label(window, textvariable=txt_infos2).pack()
Label(window).pack()

# Status
status = StringVar()
Label(window, textvariable=status).pack()
txt_1 = StringVar()
txt_1.set("")
Label(window, textvariable=txt_1).pack()
txt_2 = StringVar()
txt_2.set("")
lbl_link = Label(window, textvariable=txt_2, cursor='hand2')
lbl_link.pack()
lbl_link.configure(fg='blue')
lbl_link.bind("<Button-1>", hyperlink)

# Loop
liste_file = []
def loop_method():
	if progress['value'] == 100:
		status.set("Operation successfully completed.")

		if download_type == 'single':
			txt_1.set("Your file is in the Music folder")
		else:
			txt_1.set("Your files are in the Music folder")

		txt_2.set(f"located at the address: {f'C:/Users/{os.getlogin()}/Music'}")

		txt_btn.set("Download")
		btn_search.configure(state="normal")
		liste_file = []

	window.after(1000, loop_method)

# Refresh
window.after(1000, loop_method)
window.update_idletasks()
window.mainloop()