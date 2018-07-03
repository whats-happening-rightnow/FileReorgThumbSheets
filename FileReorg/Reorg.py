import os
import sys

import Config as conf
import Functions as fn

# handle if folder path is passed in
if (len(sys.argv) > 1) and os.path.isdir(sys.argv[1]):
	conf.paths = [sys.argv[1].strip()]
	print "Folder: " + sys.argv[1]
	resp = raw_input("Reorganize folder? (y/n): ")
	print ""
	conf.reorg = resp.strip().lower() == "y"

# delete unwanted files
for dir in conf.paths:
	
	fn.DeleteUnwatedFiles(dir)

	if conf.reorg:
		fn.RenameMove(dir)
