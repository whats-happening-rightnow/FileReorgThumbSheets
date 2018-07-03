import os
import math

import numpy as np
import cv2

class vid_attr:

	def __init__(self, vid_name, horiz_ct, vert_ct, vid_pad):

		self.vid_cap = cv2.VideoCapture(vid_name)
		
		self.width = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		self.height = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		self.fps = self.vid_cap.get(cv2.CAP_PROP_FPS)
		self.fps_string = \
			str(math.floor(self.fps * 10 ** 1) / 10 ** 1) \
			if "." in str(self.fps) and ".0" not in str(self.fps) \
			else str(int(self.fps))

		self.frames = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
		self.length = int(self.frames / self.vid_cap.get(cv2.CAP_PROP_FPS))
		self.length_string = ""
		self.totalthumbs = horiz_ct * vert_ct
		self.frameinterval = int((self.frames * (1 - (vid_pad * 2))) / self.totalthumbs)
		self.startframe = int(self.frames * vid_pad)
		self.filename = vid_name.split(os.sep)[-1]
		self.size = os.path.getsize(vid_name)
		self.size_string = ""

		# self.length_strigngit
		m, s = divmod(self.length, 60)
		h, m = divmod(m, 60)

		if h > 0:
			self.length_string = "%02d:%02d:%02d" % (h, m, s)
		else:
			self.length_string = "%02d:%02d" % (m, s)

		# self.size_string
		# gt MB
		if self.size > 1073741824:
			self.size_string = "%.1fGB" % (self.size / 1073741824.0)
		# gt MB
		elif self.size > 1048576:
			self.size_string = "%dMB" % int(self.size / 1048576.0)
		else:
			self.size_string = "%dKB" % int(self.size / 1024.0)
