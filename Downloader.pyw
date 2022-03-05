import os, webbrowser, requests, shutil, re
from tkinter import *
from tkinter import filedialog, messagebox, Text
from tkinter.ttk import Progressbar, Scrollbar
from PIL import Image, ImageTk
import tkinter.font as tkFont
from threading import *
from pytube import *
import pytube.request
import ctypes

# Internal modules
from changelog import *

#Ddw9CVIn6Zg
#XqcuHB2fN7U
#OLAK5uy_lbcsh_E-SKtipIUmpO7VDDdN2Ww3DMzGQ
#PLWYO6rEv8QXSYCoWbjnlBmr04AWq8Uk2T

# Resolution scaling
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Environment
try:
	os.mkdir('Thumbnail')
except FileExistsError:
	pass

# Variables
list_btn_pause = []
list_btn_is_pause = []
list_btn_is_cancel = []

list_p_obj = []
list_video_dl_p = []

list_yt_obj = []
list_frame_queue = []
list_frame_info = []
list_thumbnail = []
list_percent = []
list_progress = []

list_paused = []
list_canceled = []

pytube.request.default_range_size = 1000000 # 1Mo

color_theme = '#F5F5F5'
color_blue = '#6B6AF4'
color_bg_widget = '#DCDCDC'
color_default = '#F0F0ED'
color_frame_download = '#B3C8FF'
color_title = 'black'
color_text = 'grey'

# Functions
def center_window(win, ico_name='app'):
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
	win.iconbitmap(f'Content/{ico_name}.ico')
	win.configure(bg=color_theme)
	win.deiconify()


def space():
	Label(window, bg=color_theme).pack()


def safe_title(yt_obj):
	safe_title = yt_obj.title

	for carac in '''/:*?"<>|''':
		if carac in yt_obj.title:
			safe_title = ''.join(safe_title.split(carac))
	
	return safe_title


def download_thumbnail(url_image, title_image):
	r = requests.get(url_image, stream=True)
	r.raw.decode_content = True

	# Write the thumbnail into the directory
	with open(f'Thumbnail/{title_image}.jpg', 'wb') as f:
		shutil.copyfileobj(r.raw, f)


def download_info(yt_obj):
	global list_yt_obj, list_p_obj, list_thumbnail, list_frame_queue, list_frame_info, list_percent, list_progress, list_btn_pause, list_btn_is_pause

	download_type_now = download_type

	if download_type_now == 'single':
		list_yt_obj.append(yt_obj)

	# Display correct line
	nb_video = len(list_yt_obj) + len(list_p_obj) - 1

	# Download a file queue
	color_queue_line = color_frame_download
	queue_line = Frame(queue, bg=color_queue_line)
	queue_line.grid(row=nb_video, column=0, sticky='sw')
	list_frame_queue.append(queue_line)

	# Thumbnail
	if download_type_now == 'single':
		photo_thumbnail = Image.open(f'Thumbnail/{yt_obj.title}.jpg')
	else:
		photo_thumbnail = Image.open(f'Content/logo.jpg')

	photo_thumbnail.thumbnail((120, 90), Image.BICUBIC)
	img_thumbnail = ImageTk.PhotoImage(photo_thumbnail)
	list_thumbnail.append(img_thumbnail)
	Label(queue_line, image=img_thumbnail, bg=color_queue_line).pack(side=LEFT)

	# Infos
	frame_infos = Frame(queue_line, bg=color_queue_line)
	frame_infos.pack(side=LEFT)
	list_frame_info.append(frame_infos)

	# Title
	Label(list_frame_info[nb_video], text="Title: ", bg=color_queue_line, font=bold_font).grid(row=0, column=0, sticky='w')
	Label(list_frame_info[nb_video], text=yt_obj.title[:35], bg=color_queue_line, fg='white', font=bold_font).grid(row=0, column=1, sticky='w')

	if download_type_now == 'single':
		# Views
		Label(list_frame_info[nb_video], text="Views: ", bg=color_queue_line, font=bold_font).grid(row=1, column=0, sticky='w')
		Label(list_frame_info[nb_video], text=yt_obj.views, bg=color_queue_line, fg='white', font=bold_font).grid(row=1, column=1, sticky='w')

	else:
		# Owner
		Label(list_frame_info[nb_video], text="Owner: ", bg=color_queue_line, font=bold_font).grid(row=1, column=0, sticky='w')
		Label(list_frame_info[nb_video], text=yt_obj.owner, bg=color_queue_line, fg='white', font=bold_font).grid(row=1, column=1, sticky='w')

	if download_type_now == 'single':
		# Publish date
		Label(list_frame_info[nb_video], text="Publish date: ", bg=color_queue_line, font=bold_font).grid(row=0, column=2, padx=45, sticky='w')
		Label(list_frame_info[nb_video], text=''.join(str(yt_obj.publish_date).split(' ')[0]), bg=color_queue_line, fg='white', font=bold_font).grid(row=1, column=2)
	
		# Description
		Label(list_frame_info[nb_video], text="Author: ", bg=color_queue_line, font=bold_font).grid(row=3, column=0, sticky='w')
		Label(list_frame_info[nb_video], text=yt_obj.author, bg=color_queue_line, fg='white', font=bold_font).grid(row=3, column=1, sticky='w')

	else:
		# Length of the playlist
		Label(list_frame_info[nb_video], text="Length: ", bg=color_queue_line, font=bold_font).grid(row=3, column=0, sticky='w')
		Label(list_frame_info[nb_video], text=f'{yt_obj.length} videos', bg=color_queue_line, fg='white', font=bold_font).grid(row=3, column=1, sticky='w')

	# Percent
	progress = Progressbar(list_frame_info[nb_video], orient=HORIZONTAL, length=250, mode='determinate')
	progress.grid(row=1, column=3, sticky='w')
	list_progress.append(progress)

	# Progress
	percent = StringVar()
	percent.set("0%")
	list_percent.append(percent)
	Label(list_frame_info[nb_video], textvariable=list_percent[nb_video], bg=color_queue_line, font=bold_font).grid(row=0, column=3, sticky='w')

	# Pause/Resume
	btn_pause_resume = Button(list_frame_info[nb_video], command=lambda:pause(nb_video), bg=color_bg_widget, activebackground=color_blue, cursor='hand2', image=image_pause)
	btn_pause_resume.grid(row=3, column=3, sticky='w', padx=1)
	list_btn_pause.append(btn_pause_resume)
	list_btn_is_pause.append(False)

	# Cancel
	btn_cancel = Button(list_frame_info[nb_video], command=lambda:cancel(nb_video), bg=color_bg_widget, activebackground=color_blue, cursor='hand2', image=image_cancel)
	btn_cancel.grid(row=3, column=3, sticky='w', padx=46)
	list_btn_is_cancel.append(False)

	# Download mode
	if mode_download == 'audio':
		txt_mode = 'type: audio'
	else:
		txt_mode = 'type: audio + video'
	Label(list_frame_info[nb_video], text=txt_mode, bg=color_queue_line, font=bold_font, fg=color_text).grid(row=3, column=3, sticky='w', padx=90)

	return nb_video


def download_video(url, download_type_dl, p_queue=None, p_length=None):
	global list_video_dl_p, list_btn_is_pause, list_btn_is_cancel

	# Connecting
	yt = YouTube(url)
	yt.title = safe_title(yt)

	# Backup
	dl_type_now = download_type

	if dl_type_now == 'single':
		nb_video_yt = download_info(yt)

	# Stream choice
	if mode_download == 'audio':
		stream = yt.streams.otf(False).get_audio_only()
	else:
		stream = yt.streams.otf(False).get_highest_resolution()

	filesize = stream.filesize

	# File name
	if mode_download == 'audio':
		file_name = f'{yt.title} [AUDIO].mp4'
	else:
		file_name = f'{yt.title} [AUDIO+VIDEO].mp4'

	# Load and prepare the file
	with open(f"C:/Users/{os.getlogin()}/Music/{file_name}", 'wb') as file:
		stream = request.stream(stream.url)
		downloaded = 0

		# Download
		while True:
			# Cancel download
			if dl_type_now == 'single':
				if list_btn_is_cancel[nb_video_yt]:
					break

			else:
				if list_btn_is_cancel[p_queue]:
					break

			# Pause
			if dl_type_now == 'single':
				if list_btn_is_pause[nb_video_yt]:
					continue

			else:
				if list_btn_is_pause[p_queue]:
					continue

			chunk = next(stream, None)

			if chunk:
				file.write(chunk)
				downloaded += len(chunk)

				# Progress bar
				percent_value = downloaded*100/filesize

				if download_type_dl == 'single':
					list_progress[nb_video_yt]['value'] = percent_value
					list_percent[nb_video_yt].set(f"{int(percent_value)}%")

				else:
					# One more music/video downloaded
					if percent_value == 100:
						list_video_dl_p[p_queue] += 1
						percent_track_downloaded = list_video_dl_p[p_queue]*100/p_length
						list_progress[p_queue]['value'] = percent_track_downloaded
						list_percent[p_queue].set(f"{int(percent_track_downloaded)}%")

			# End of the download
			else:
				break


def search_video(bind_action=None):
	global current_queue

	if current_queue == 4:
		return

	# Check mode download selected
	if mode_download == None:
		status.set("Please choose a download mode...")
		txt_btn.set("Download")
		btn_search.configure(state='normal', cursor='hand2')
		return

	status.set("")

	url = txt_url.get()

	if download_type == 'single':
		try:
			yt = YouTube(url)
			yt.title = safe_title(yt)

			# Thumbnail
			download_thumbnail(yt.thumbnail_url, yt.title)

			label_img_void.pack_forget()
			label_txt_void.pack_forget()
			lbl_link.pack_forget()

			# Regular
			list_video_dl_p.append(0)

			current_queue += 1
			queue.configure(text=f"Download queue {current_queue}/4")

			# Entry
			txt_url.delete(0, END)
			if download_type == 'single':
				txt_url.insert(0, 'https://www.youtube.com/watch?v=')
			else:
				txt_url.insert(0, 'https://www.youtube.com/playlist?list=')

			# Download
			thread_download = Thread(target=download_video, args=(url, download_type,))
			thread_download.start()

		except Exception as e:
			status.set("Please provide a valid URL...")

	elif download_type == 'playlist':
		try:
			p = Playlist(url)

			del_security = False
			try:
				# Verification test
				p.title

				# Download
				list_p_obj.append(p)
				list_video_dl_p.append(0)
				del_security = True

				p_queue = download_info(p)

			except Exception as e:
				if del_security:
					del list_p_obj[-1]
					del list_video_dl_p[-1]
				del_security = False

				status.set("Please provide a valid URL...")
				return

			label_img_void.pack_forget()
			label_txt_void.pack_forget()
			lbl_link.pack_forget()

			current_queue += 1
			queue.configure(text=f"Download queue {current_queue}/4")

			for video_url in p.video_urls:
				yt = YouTube(video_url)
				yt.title = safe_title(yt)

				p_length = p.length
				Thread(target=download_video, args=(video_url, download_type, p_queue, p_length,)).start()

		except Exception as e:
			status.set("Please provide a valid URL...")


def audio_only():
	global mode_download
	mode_download = 'audio'
	btn_audio.configure(bg=color_blue, cursor='arrow')
	btn_video.configure(bg=color_bg_widget, cursor='hand2')


def audio_video():
	global mode_download
	mode_download = 'video'
	btn_video.configure(bg=color_blue, cursor='arrow')
	btn_audio.configure(bg=color_bg_widget, cursor='hand2')


def single():
	global download_type
	download_type = 'single'
	label_url.set("URL of the desired single video:")
	txt_url.delete(0, END)
	txt_url.insert(0, 'https://www.youtube.com/watch?v=')
	txt_btn.set("Download")


def playlist():
	global download_type
	download_type = 'playlist'
	label_url.set("URL of the desired playlist video:")
	txt_url.delete(0, END)
	txt_url.insert(0, 'https://www.youtube.com/playlist?list=')
	txt_btn.set("Download")

def pause(idx_btn):
	if list_btn_is_pause[idx_btn]:
		list_btn_pause[idx_btn].configure(image=image_pause)
		list_btn_is_pause[idx_btn] = False
	else:
		list_btn_pause[idx_btn].configure(image=image_resume)
		list_btn_is_pause[idx_btn] = True

def cancel(idx_btn):
	global current_queue

	list_btn_is_cancel[idx_btn] = True
	list_btn_pause[idx_btn].configure(state='disabled')
	list_btn_pause[idx_btn].configure(state='disabled')
	list_percent[idx_btn].set('Download cancel.')
	list_frame_info[idx_btn].pack_forget()
	list_frame_queue[idx_btn].grid_forget()

	current_queue -= 1
	queue.configure(text=f"Download queue {current_queue}/4")


def hyperlink(arg):
	webbrowser.open(f'C:/Users/{os.getlogin()}/Music/')


def check_update():
	#messagebox.askquestion(title="Update", message="A new version of the software is available ! Do you want to update it now ?")
	messagebox.showinfo(title="Update", message="You already have the most recent version of the software.")


def on_closing():
	global list_btn_is_cancel

	try:
		shutil.rmtree('Thumbnail')
	except FileNotFoundError:
		pass

	for idx_btn in range(len(list_btn_is_cancel)):
		list_btn_is_cancel[idx_btn] = True

	window.quit()


def changelog():
	win_log = Toplevel()
	win_log.title('Changelog')
	win_log.geometry("600x500")
	win_log.resizable(False, False)
	center_window(win_log, 'changelog')

	text_log = Text(win_log)
	text_log.pack(side=LEFT)

	log = changelog_txt()

	text_log.insert(END, log)
	text_log.configure(state="disabled")


# Initialisation
window = Tk()
window.title('YouTube Downloader v1.3.0')
window.geometry("900x700")
window.resizable(False, False)
center_window(window)

title_font = tkFont.Font(family='Segoe', size='12', weight='bold')
void_font = tkFont.Font(family='Segoe', size='15', weight='bold')
main_font = tkFont.Font(family='Segoe', size='9', slant='italic')
bold_font = tkFont.Font(family='Segoe', size='9', weight='bold')

# Type mode
download_type = "single"
mode_download = None

# Menu
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Single", command=single)
menu1.add_command(label="Playlist", command=playlist)
menu1.add_separator()
menu1.add_command(label="Shutdown", command=on_closing)
menubar.add_cascade(label="Mode", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Check for updates...", command=check_update)
menu2.add_command(label="Changelog", command=changelog)
menubar.add_cascade(label="Help", menu=menu2)

window.config(menu=menubar)

# Credit
Label(window, text="● YouTube Downloader ●", font=title_font, bg=color_theme, fg=color_title).pack()
Label(window, text="Uploaded videos will not exceed 720p resolution due to a blocking by Google LLC.", bg=color_theme, fg=color_text, font=main_font).pack()
space()

c2 = Frame(window, bg=color_frame_download)
c2.pack()

label_url = StringVar()
label_url.set("URL of the desired single video:")
Label(c2, textvariable=label_url, font=bold_font, bg=color_frame_download, fg=color_title).pack(side=LEFT)
txt_url = Entry(c2, width=50, justify='left')
txt_url.insert(END, 'https://www.youtube.com/watch?v=')
txt_url.pack(padx=5, pady=5, side=LEFT)
window.bind('<Return>', search_video)

# Download mode choice
image_audio = ImageTk.PhotoImage(Image.open('Content/audio.png'))
btn_audio = Button(c2, command=audio_only, bg=color_bg_widget, activebackground=color_blue, cursor='hand2', image=image_audio)
btn_audio.pack(padx=5, pady=5, side=LEFT)

image_video = ImageTk.PhotoImage(Image.open('Content/video.png'))
btn_video = Button(c2, command=audio_video, bg=color_bg_widget, activebackground=color_blue, cursor='hand2', image=image_video)
btn_video.pack(padx=5, pady=5, side=LEFT)


txt_btn = StringVar()
txt_btn.set("Download")
btn_search = Button(c2, textvariable=txt_btn, bg=color_bg_widget, fg=color_title, font=bold_font, activebackground=color_blue, command=search_video, cursor='hand2')
btn_search.pack(padx=5, pady=5, side=LEFT)
space()

# No queue
img_void = ImageTk.PhotoImage(Image.open('Content/void.png'))
label_img_void = Label(window, image=img_void, bg=color_theme)
label_img_void.pack()
label_txt_void = Label(window, text="There are no downloads in progress...", bg=color_theme, font=void_font)
label_txt_void.pack()

# Music folder
lbl_link = Label(window, text=f"Your files are in the Music folder: {f'C:/Users/{os.getlogin()}/Music'}", bg=color_theme, cursor='hand2')
lbl_link.pack()
lbl_link.configure(fg=color_blue)
lbl_link.bind("<Button-1>", hyperlink)
space()

# Queue
queue = LabelFrame(window, text="Download queue 0/4", fg=color_text, bg=color_theme)
queue.pack(fill="both")

# Status
status = StringVar()
Label(window, textvariable=status, bg=color_theme, fg=color_text).pack()

space()
Label(window, text="Credit: Léon Pupier - 2022", bg=color_theme, fg=color_text, font=main_font).pack()
Label(window, text="This service does not respect the TOS and copyrights on YouTube, as a consumer you risk nothing.", bg=color_theme, fg=color_text, font=main_font).pack()

# Loop
liste_file = []
current_queue = 0

image_pause = ImageTk.PhotoImage(Image.open('Content/pause.png'))
image_resume = ImageTk.PhotoImage(Image.open('Content/play.png'))
image_cancel = ImageTk.PhotoImage(Image.open('Content/cancel.png'))

def loop_method():
	window.after(1000, loop_method)

# Refresh
window.after(0, loop_method)
window.update_idletasks()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()