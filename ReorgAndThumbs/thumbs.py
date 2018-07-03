import os
import sys

from rtclasses import *

import rtfilesys as fs
import rtimaging as img
import rtconfig as cf
import rtfunctions as fn
import rtprint as pr

if cf.debug: pr.print_("Debug mode is on\n\n")

if (len(sys.argv) > 1):

	in_path = str(sys.argv[1]).strip().replace('"', '')

	if os.path.isdir(in_path):
		cf.thumb_paths = [in_path]
		pr.print_(in_path, "path")

for dir in cf.thumb_paths:

	files = list(fs.get_all_files(dir))

	for file in files:

		file_nfo = file_info(file, dir)

		if file_nfo.extension in cf.video_ext:

			if not fn.corresponding_contact_sheet_exists(file_nfo.fullfilename, files):

				try:
					img.create_contact_sheet(file_nfo)
				except:
					pr.print_("{0}{1}{2}{1}".format(file_nfo.fullfilename, str(sys.exc_info()[1]), "\n"), "error", True)

pr.print_("")

if len(cf.out_message) > 2:
	for msg in sorted(cf.out_message):
		pr.print_(msg)
