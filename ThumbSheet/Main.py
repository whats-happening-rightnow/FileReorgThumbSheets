import os
import sys
import cv2
import collections

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.append("..{0}FileReorg".format(os.path.sep))

from ClassFileInfo import *

import Capture as cap
import Config as conf
import FileSystem as fs	
import Functions as fn
import Image as img
import Print as prn

if (len(sys.argv) > 1):

	in_path = str(sys.argv[1]).strip().replace('"', '')

	if os.path.isdir(in_path):
		conf.paths = [in_path]
		prn.print_(in_path, "path")

for dir in conf.paths:

	files = list(fs.GetAllFiles(dir))

	for file in files:

		file_info = FileInfo(file, dir)

		if file_info.extension in conf.video_ext:

			if not fn.CorrespondingContactSheetExists(os.path.join(file_info.folder, fs.FileNameOnly(file_info.filename)), conf.contact_ext, files):

				try:
					img.create_contact_sheet(file_info.fullfilename)
				except:
					prn.print_(str(sys.exc_info()[1]), "error", True)
					prn.print_("\n\n")

prn.print_("")
for msg in sorted(conf.out_message):
	prn.print_(msg)
