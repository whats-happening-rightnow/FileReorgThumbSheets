import os
import FileSystem as fs
import Functions as fn

class FileInfo:

	def __init__(self, fullpath, workingfolder):

		filename_arr = fullpath.split(os.sep)
				 
		self.rootfolder = workingfolder
		self.fullfilename = fullpath
		self.filename = filename_arr[-1]
		self.extension = fs.FileExt(fullpath); 
		self.folder = os.sep.join(filename_arr[:-1])
		self.excludefilereorg = fn.ExcludeInFileReorg(self.fullfilename)

		self.isatroot = self.rootfolder == self.folder;
		if self.isatroot: 
			return
		
		parent_arr = fullpath.replace(workingfolder, "").split(os.sep)
		
		self.parentfoldername = [s for s in parent_arr if len(s) > 0][0]
		
		workingfolderArr = [s for s in workingfolder.split(os.sep) if len(s) > 0]
		workingfolderArr.append(self.parentfoldername)

		self.parentfolderpath = os.sep.join(workingfolderArr)
