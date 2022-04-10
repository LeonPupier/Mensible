# Dependencies
import os, git, shutil, datetime

def clear_update(date):
	try:
		shutil.rmtree(f"Updates/{date}", ignore_errors=True)
	except:
		return

def get_update():
	date_format = datetime.datetime.now()
	date = f"{date_format.year}-{date_format.month}-{date_format.day}"

	try:
		os.mkdir(f"Updates/{date}")
	except FileExistsError:
		return

	git.Git(f"Updates/{date}").clone("https://github.com/LeonPupier/Mensible.git")
	clear_update(date)

get_update()