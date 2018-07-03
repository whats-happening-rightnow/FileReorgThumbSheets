import os
import sys
import cv2
import collections

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import Config as conf
import Classes as cl
import Image as img
from ClassFileInfo import *
import Capture as cap
import FileSystem as fs	
import Print as prn

def create_contact_sheet(filename):

	file_info = FileInfo(filename, '')

	prn.print_(file_info.fullfilename, "start")

	vid_attr = cl.vid_attr(file_info.fullfilename, conf.thumbs_horizontal, conf.thumbs_vertical, conf.video_pad)

	header_height, thumb_height, template_image = img.create_image_template(file_info.fullfilename)
	capture_success, thumbs = cap.capture_thumbnails(file_info.fullfilename)

	if not capture_success:
		conf.out_message.append("failed", file_info.fullfilename, True)
		return

	conf.thumb_height = thumb_height

	counter = 0
	thumbs_keys = list(thumbs.keys())
	thumbnail_scale = (conf.thumb_height * 1.0) / thumbs[thumbs_keys[0]].shape[0]
	x_offset = conf.thumb_spacing
	y_offset = header_height

	for y in range (1, conf.thumbs_vertical + 1):

		for x in range(1, conf.thumbs_horizontal + 1):

			thumbnail = thumbs[thumbs_keys[counter]]
			thumbnail_scaled = cv2.resize(thumbnail, (conf.thumb_width, conf.thumb_height), interpolation = cv2.INTER_AREA)
			template_image[y_offset: y_offset + thumbnail_scaled.shape[0], x_offset: x_offset + thumbnail_scaled.shape[1]] = thumbnail_scaled		

			x_offset += conf.thumb_spacing + conf.thumb_width
			counter += 1

		x_offset = conf.thumb_spacing
		y_offset += (conf.thumb_height + conf.thumb_spacing)

	cs_filename = file_info.fullfilename[:-len(file_info.extension)] + conf.contact_ext
	cv2.imwrite(cs_filename, template_image)
	prn.print_(cs_filename, "created", True)
	prn.print_("")

def create_image_template(filename):

	vid_attr = cl.vid_attr(filename, conf.thumbs_horizontal, conf.thumbs_vertical, conf.video_pad)

	thumb_height = int(round((vid_attr.height / (vid_attr.width * 1.0)) * conf.thumb_width))
	im_header = im_height = 0

	im_header += conf.thumb_spacing						# pad
	im_header += int(conf.text_font_size * 1.5)			# first line
	im_header += int(conf.text_font_size)				# second line
	im_header += int(conf.thumb_spacing / 2)			# pad
	im_height += ((thumb_height + conf.thumb_spacing) * conf.thumbs_vertical) + int(conf.thumb_spacing)	# all the thumbs

	im = Image.new('RGBA', (conf.width, im_header + im_height), conf.background_color)
	draw = ImageDraw.Draw(im)
	courier_font = ImageFont.truetype(os.path.join(conf.text_font), conf.text_font_size)

	draw_text = vid_attr.filename
	pos_x = pos_y = conf.thumb_spacing
	draw.text((pos_x, pos_y), draw_text, fill='black', font=courier_font)

	draw_text = "{0}, {1}x{2}, {3}fps, {4}".format(\
		vid_attr.size_string, \
		vid_attr.width, \
		vid_attr.height, \
		vid_attr.fps_string, \
		vid_attr.length_string)

	pos_y += int(conf.text_font_size * 1.5)
	draw.text((pos_x, pos_y), draw_text, fill='black', font=courier_font)

	return im_header, thumb_height, cv2.cvtColor(np.array(im), cv2.COLOR_BGRA2BGR)

def overlay_timecode_on_thumbnail(time_in_seconds, thumbnail):
	
	# get timecode image
	tc_img = timecode_image(time_in_seconds)

	# calculate timecode image size ratio to thumbnail
	resize_ratio = (thumbnail.shape[1] * 0.35) / tc_img.shape[1]

	# resize timecode image
	tc_img_sized = cv2.resize(tc_img, (0,0), fx=resize_ratio, fy=resize_ratio) 

	# flip both thumbnail and timecode image on x,y axis
	# no need to calculate timecode image offset to place on bottom right corner
	l_img = cv2.flip(thumbnail, -1)
	s_img = cv2.flip(tc_img_sized, -1)

	# overlay timecode image on thumbnail
	x_offset = y_offset = 0
	l_img[y_offset: s_img.shape[0], x_offset: s_img.shape[1]] = s_img

	# flip thumbnail again
	return cv2.flip(l_img, -1)


def timecode_image(seconds):

	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)

	timecode = "%02d:%02d:%02d" % (h, m, s)

	time_code_background_image = np.zeros((107, 500, 3), np.uint8)
	cv2.putText(time_code_background_image, timecode, (3, 90), cv2.FONT_HERSHEY_DUPLEX, 3.45, (255,255,255), 6, cv2.LINE_AA)
	return time_code_background_image 