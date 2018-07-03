# reorg config
paths = [r'C:\Users\jchoi\Desktop\wip\py\fs sf']
video_ext = [".mp4",".mkv",".avi", ".mov"]
contact_ext = ".png"
exclude_postfix = "-zz"
reorg = True

# thumbs config
width = 3000
thumbs_horizontal = 8
thumbs_vertical = 8
video_pad = 0.05
background_color = (244, 66, 232)
text_font = "courbd.ttf"
text_font_size = 25
thumb_spacing = 10
thumb_width = int(round((width * 1.0 - ((thumbs_horizontal * thumb_spacing) + thumb_spacing)) / thumbs_horizontal))
thumb_height = 0

# output
out_message = []