import os
import shutil
import sys

import Config as conf
import FileSystem as fs
import Functions as fn
from ClassFileInfo import *

def RenameMove(workingdir):

	# rename video file name and move to parent
	allfiles = list(fs.GetAllFiles(workingdir))

	# move video files to working folder root
	for file in allfiles:

		# object to parse out file path parts
		fileinfo = FileInfo(file, workingdir)

		# skip file is not video or marked for omit reorg
		if (fileinfo.extension not in conf.video_ext) \
			or fileinfo.isatroot \
			or fileinfo.excludefilereorg: continue

		# unique counter 
		iterator = 0
		newfilename = os.path.join(fileinfo.rootfolder, fileinfo.parentfoldername) \
			+ fileinfo.extension

		# make filename unique if exists in destination
		while os.path.isfile(newfilename):
			newfilename = os.path.join(fileinfo.rootfolder, fileinfo.parentfoldername) + "-" + \
				("%02d" % (iterator,)) + fileinfo.extension
			iterator += 1

		# move / rename file to parent root dir
		fs.Movefile(fileinfo.fullfilename, newfilename)
	
	# delete subdirs

	# get first level subdirs
	subdirs = next(os.walk(workingdir))[1]

	# delete dir is not omit reorg
	for dir in subdirs:
		if not ExcludeInFileReorg(dir):
			shutil.rmtree(os.path.join(workingdir, dir))


def DeleteUnwatedFiles(workingdir):

	allfiles = list(fs.GetAllFiles(workingdir))

	# delete unwanted files
	for file in allfiles:
	
		fileinfo = FileInfo(file, workingdir)

		# if contact sheet
		if (fileinfo.extension == conf.contact_ext):
		# make sure matching video file exists
			if not CorrespondingVideoFileExists(fs.FileNameOnly(file), conf.video_ext, allfiles):
				# if no matching video file, delete
				fs.DeleteFile(file)
		# if is not contact sheet or video file, delete
		elif (fileinfo.extension not in conf.video_ext) or ('sample' in fileinfo.filename.lower()):
			fs.DeleteFile(file)


def CorrespondingVideoFileExists(cs_fn, vid_exts, all_files):

	for ext in vid_exts:
		if (cs_fn + ext) in all_files:
			return True

	return False

def CorrespondingContactSheetExists(vid_fn, cs_ext, all_files):

	if (vid_fn + cs_ext) in all_files:
		return True

	return False

def ExcludeInFileReorg(vid_fn):	

	fullpath = vid_fn.split(os.sep)
	excludepattern = conf.exclude_postfix

	for item in fullpath:
		if item.endswith(excludepattern):
			return True

	return False

def getopts(argv):

	opts = {}  # Empty dictionary to store key-value pairs.

	try:
		while argv:  # While there are arguments left to parse...
			if argv[0][0] == '-':  # Found a "-name value" pair.
				opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
			argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
	except:
		help()

	if not bool(opts): 
		help()
		return (False, opts)

	return (bool(opts), opts)

def help():
	prompt = '\n'
	prompt += 'Required arguments:\n'
	prompt += '-r: omit = 0, reorg = 1\n'
	prompt += '  reorganize, moves files to root directory\n'
	prompt += '  renames file to parent directory name\n'
	prompt += '-p: [path]\n'
	prompt += '  path to directory to be reorganized\n\n'
	prompt += 'sample:'
	prompt += '  -a 1 -p \\\\nas\\files\\videos\n\n'
	print prompt

def TruncString(str, pad):
	return ''.join([str[:pad], '....', str[-pad:]])