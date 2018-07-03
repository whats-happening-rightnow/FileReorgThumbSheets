import os
from glob import glob

import Functions as fn

def GetAllFiles(rootPath):

	walk = os.walk(rootPath)

	for folder in walk:
		for file in folder[2]:
			yield os.path.join(folder[0], file)


def FileExt(filePath):
	filename, file_extension = os.path.splitext(filePath)
	return file_extension

def FileNameOnly(filePath):
	filename, file_extension = os.path.splitext(filePath)
	return filename

def DeleteFile(filePath):
	os.remove(filePath)
	print('del:\t' + filePath)

def Movefile(src, dest):
	os.rename(src, dest)
	#print('move:\t' + fn.TruncString(src, 20) + '\n\t' + fn.TruncString(dest, 15))
	print(''.join(['move:\t', src, ' -->\n\t', dest]))
